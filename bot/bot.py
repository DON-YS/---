#!/usr/bin/env python3
"""Telegram Bot API control layer with allowlisted, confirmed actions."""

import json
import os
import platform
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

from distros import status as distro_status  # noqa: E402
from gui import format_diagnostics  # noqa: E402
from installer import install, load  # noqa: E402
from scanner import scan  # noqa: E402
from storage import capability  # noqa: E402
from system import format_snapshot  # noqa: E402

API_TIMEOUT = 40
PENDING = {}


def configuration():
    token = os.environ.get("BOT_TOKEN", "").strip()
    raw = os.environ.get("ADMIN_USER_IDS", "").strip()
    if not token or not raw:
        raise RuntimeError("BOT_TOKEN and ADMIN_USER_IDS are required")
    try:
        admins = {int(item.strip()) for item in raw.split(",") if item.strip()}
    except ValueError as exc:
        raise RuntimeError("ADMIN_USER_IDS must be comma-separated numeric IDs") from exc
    if not admins:
        raise RuntimeError("ADMIN_USER_IDS must not be empty")
    return token, admins


def api(token, method, payload=None):
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=urllib.parse.urlencode(payload or {}).encode(), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=API_TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise RuntimeError(f"Telegram API request failed: {type(exc).__name__}") from exc
    if not body.get("ok"):
        raise RuntimeError("Telegram API returned an error")
    return body.get("result")


def keyboard():
    rows = [
        [("🖥 System", "system"), ("🧰 Tools", "tools")],
        [("📦 Distros", "distros"), ("💾 Storage", "storage")],
        [("☁️ Cloud", "cloud"), ("🔐 Security", "security")],
        [("📤 Upload", "upload"), ("📥 Restore", "restore")],
        [("🔄 Update", "update"), ("🖥 Tmux", "tmux")],
        [("🌐 Web", "web"), ("📊 Processes", "processes")],
        [("🟢 BOT", "bot"), ("🎨 GUI", "gui")],
        [("📚 Commands", "commands")],
    ]
    return {"inline_keyboard": [[{"text": text, "callback_data": data} for text, data in row] for row in rows]}


def tool_view():
    result = scan()
    lines, buttons = ["🧰 TOOLS"], []
    for name, item in result.items():
        icon = "🟢" if item["status"] in ("INSTALLED", "PYTHON_INSTALLED") else "🟡" if item["status"] == "EXTERNAL/LAB" else "🔴"
        lines.append(f"{icon} {name}: {item['status']}")
        if item["status"] == "NOT_INSTALLED":
            buttons.append([{"text": f"Install {name}", "callback_data": f"install:{name}"}])
    return "\n".join(lines), {"inline_keyboard": buttons} if buttons else keyboard()


def send(token, chat_id, text, markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if markup:
        payload["reply_markup"] = json.dumps(markup)
    api(token, "sendMessage", payload)


def authorized(update, admins):
    source = update.get("message", {}).get("from") or update.get("callback_query", {}).get("from") or {}
    return source.get("id") in admins


def page(data):
    if data == "system": return format_snapshot(), keyboard()
    if data == "tools": return tool_view()
    if data == "distros":
        state = distro_status()
        return "📦 DISTROS\nproot-distro: " + ("available" if state["available"] else "not available") + "\nInstalled: " + (", ".join(state["installed"]) or "none reported"), keyboard()
    if data == "storage": return "💾 STORAGE\n" + json.dumps(capability(), indent=2), keyboard()
    if data == "cloud": return "☁️ CLOUD\nExternal infrastructure only; no provider is configured.", keyboard()
    if data == "security": return "🔐 SECURITY\nAuthorized targets and labs only. No arbitrary remote shell.", keyboard()
    if data in ("upload", "restore"): return "💾 Local manifest backup/restore is available through core/storage.py; Telegram file storage requires an explicit external channel configuration.", keyboard()
    if data == "update": return "🔄 UPDATE\nUse YS15_REPO with the local update command; no remote update is triggered from Telegram.", keyboard()
    if data == "tmux": return "🖥 TMUX\n" + ("tmux is installed." if __import__("shutil").which("tmux") else "tmux is not installed."), keyboard()
    if data == "web": return "🌐 WEB\nNo web server is started by Pirate.", keyboard()
    if data == "processes": return "📊 PROCESSES\n" + ("/proc is available." if Path("/proc").is_dir() else "Process information unavailable."), keyboard()
    if data == "bot": return "🟢 BOT\nPolling mode; admin allowlist enabled.", keyboard()
    if data == "gui": return format_diagnostics(), keyboard()
    if data == "commands": return "📚 COMMANDS\n/status  /tools  /distros  /help", keyboard()
    return "Unknown action.", keyboard()


def handle(token, admins, update):
    if not authorized(update, admins):
        return
    callback = update.get("callback_query")
    if callback:
        api(token, "answerCallbackQuery", {"callback_query_id": callback["id"]})
        data = callback.get("data", "")
        chat_id = callback["message"]["chat"]["id"]
        if data.startswith("install:"):
            name = data.split(":", 1)[1]
            if name not in load():
                send(token, chat_id, "Unknown registry entry.", keyboard())
            else:
                PENDING[callback["from"]["id"]] = name
                send(token, chat_id, f"Confirm installation of {name}? This runs its trusted registry installer.", {"inline_keyboard": [[{"text": "Confirm", "callback_data": "confirm_install"}, {"text": "Cancel", "callback_data": "cancel"}]]})
        elif data == "confirm_install":
            name = PENDING.pop(callback["from"]["id"], None)
            send(token, chat_id, "No pending installation." if not name else f"Installer exit code: {install(name)}", keyboard())
        elif data == "cancel":
            PENDING.pop(callback["from"]["id"], None)
            send(token, chat_id, "Cancelled.", keyboard())
        else:
            text, markup = page(data)
            send(token, chat_id, text, markup)
        return
    message = update.get("message", {})
    text = message.get("text", "")
    if text in ("/start", "/help"):
        send(token, message["chat"]["id"], "🤖 Pirate control menu", keyboard())
    elif text == "/status":
        send(token, message["chat"]["id"], format_snapshot(), keyboard())
    elif text == "/tools":
        text, markup = tool_view(); send(token, message["chat"]["id"], text, markup)
    elif text == "/distros":
        text, markup = page("distros"); send(token, message["chat"]["id"], text, markup)


def main():
    try:
        token, admins = configuration()
    except RuntimeError as exc:
        print(f"Configuration error: {exc}")
        return 2
    offset = 0
    print("Pirate Telegram bot started in polling mode")
    while True:
        try:
            for update in api(token, "getUpdates", {"offset": offset, "timeout": 25}) or []:
                offset = max(offset, int(update["update_id"]) + 1)
                try:
                    handle(token, admins, update)
                except (KeyError, RuntimeError, ValueError) as exc:
                    print(f"Update handling failed: {type(exc).__name__}")
        except KeyboardInterrupt:
            return 0
        except RuntimeError as exc:
            print(f"Polling error: {exc}")
            time.sleep(5)


if __name__ == "__main__":
    raise SystemExit(main())
