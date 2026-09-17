#!/usr/bin/env python3
"""Telegram Bot API polling control layer.

The bot is intentionally dependency-free and exposes only allowlisted actions.
It never accepts or executes arbitrary shell text from Telegram.
"""

import json
import os
import platform
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

from distros import status as distro_status  # noqa: E402
from installer import install, load  # noqa: E402
from scanner import scan  # noqa: E402

API_TIMEOUT = 40


def configuration() -> tuple[str, set[int]]:
    token = os.environ.get("BOT_TOKEN", "").strip()
    raw_admins = os.environ.get("ADMIN_USER_IDS", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN is required to start the Telegram bot")
    if not raw_admins:
        raise RuntimeError("ADMIN_USER_IDS is required; refusing to run without an admin allowlist")
    try:
        admins = {int(value.strip()) for value in raw_admins.split(",") if value.strip()}
    except ValueError as exc:
        raise RuntimeError("ADMIN_USER_IDS must be a comma-separated list of numeric Telegram user IDs") from exc
    if not admins:
        raise RuntimeError("ADMIN_USER_IDS must contain at least one user ID")
    return token, admins


def api(token: str, method: str, payload: Dict[str, Any] | None = None) -> Any:
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(payload or {}).encode()
    request = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=API_TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise RuntimeError(f"Telegram API request failed: {type(exc).__name__}") from exc
    if not body.get("ok"):
        raise RuntimeError("Telegram API returned an error")
    return body.get("result")


def keyboard() -> Dict[str, Any]:
    return {"inline_keyboard": [
        [{"text": "🖥 System", "callback_data": "system"}, {"text": "🧰 Tools", "callback_data": "tools"}],
        [{"text": "📦 Distros", "callback_data": "distros"}, {"text": "🔄 Refresh", "callback_data": "refresh"}],
    ]}


def render_system() -> str:
    return "🟢 SYSTEM ONLINE\n" f"Platform: {platform.system()}\nArchitecture: {platform.machine()}\nPython: {platform.python_version()}"


def render_tools() -> tuple[str, Dict[str, Any] | None]:
    result = scan()
    lines = ["🧰 TOOLS"]
    buttons = []
    for name, item in result.items():
        lines.append(f"{'🟢' if item['status'] in ('INSTALLED', 'PYTHON_INSTALLED') else '🟡' if item['status'] == 'EXTERNAL/LAB' else '🔴'} {name}: {item['status']}")
        if item["status"] == "NOT_INSTALLED":
            buttons.append([{"text": f"Install {name}", "callback_data": f"install:{name}"}])
    return "\n".join(lines), {"inline_keyboard": buttons} if buttons else None


def render_distros() -> str:
    data = distro_status()
    if not data["available"]:
        return "📦 Distros\nproot-distro is not available in this environment."
    installed = ", ".join(data["installed"]) if data["installed"] else "none reported"
    return "📦 Distros\nInstalled: " + installed + "\nNo distro is entered or removed automatically."


def authorized(update: Dict[str, Any], admins: set[int]) -> bool:
    user = update.get("message", {}).get("from") or update.get("callback_query", {}).get("from") or {}
    return user.get("id") in admins


def send(token: str, chat_id: int, text: str, markup: Dict[str, Any] | None = None) -> None:
    payload: Dict[str, Any] = {"chat_id": chat_id, "text": text}
    if markup:
        payload["reply_markup"] = json.dumps(markup)
    api(token, "sendMessage", payload)


def handle(token: str, admins: set[int], update: Dict[str, Any]) -> None:
    if not authorized(update, admins):
        return
    callback = update.get("callback_query")
    if callback:
        api(token, "answerCallbackQuery", {"callback_query_id": callback["id"]})
        data = callback.get("data", "")
        chat_id = callback["message"]["chat"]["id"]
        if data == "system" or data == "refresh":
            send(token, chat_id, render_system(), keyboard())
        elif data == "tools":
            text, markup = render_tools()
            send(token, chat_id, text, markup or keyboard())
        elif data == "distros":
            send(token, chat_id, render_distros(), keyboard())
        elif data.startswith("install:"):
            name = data.split(":", 1)[1]
            if name not in load():
                send(token, chat_id, "Unknown registry entry.", keyboard())
            else:
                send(token, chat_id, f"Install request received for {name}. Use the local CLI for explicit installation confirmation.", keyboard())
        return
    message = update.get("message", {})
    text = message.get("text", "")
    if text in ("/start", "/help"):
        send(token, message["chat"]["id"], "🤖 Pirate control layer\nChoose an allowlisted read-only operation.", keyboard())
    elif text == "/status":
        send(token, message["chat"]["id"], render_system(), keyboard())
    elif text == "/tools":
        rendered, markup = render_tools()
        send(token, message["chat"]["id"], rendered, markup or keyboard())
    elif text == "/distros":
        send(token, message["chat"]["id"], render_distros(), keyboard())


def main() -> int:
    try:
        token, admins = configuration()
    except RuntimeError as exc:
        print(f"Configuration error: {exc}")
        return 2
    offset = 0
    print("Pirate Telegram control layer started")
    while True:
        try:
            updates: Iterable[Dict[str, Any]] = api(token, "getUpdates", {"offset": offset, "timeout": 25}) or []
            for update in updates:
                offset = max(offset, int(update["update_id"]) + 1)
                try:
                    handle(token, admins, update)
                except (KeyError, RuntimeError, ValueError) as exc:
                    print(f"Update handling failed: {type(exc).__name__}")
        except KeyboardInterrupt:
            print("Telegram control layer stopped")
            return 0
        except RuntimeError as exc:
            print(f"Polling error: {exc}")
            time.sleep(5)


if __name__ == "__main__":
    raise SystemExit(main())
