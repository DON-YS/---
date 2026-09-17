#!/usr/bin/env python3
"""Read-only host and runtime diagnostics for the CLI and bot."""

import os
import platform
import shutil
import subprocess
from pathlib import Path


def _read(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return "unknown"


def command_status(names):
    return {name: shutil.which(name) is not None for name in names}


def snapshot() -> dict:
    return {
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "termux": bool(os.environ.get("PREFIX", "").startswith("/data/data/com.termux")),
        "root": os.geteuid() == 0 if hasattr(os, "geteuid") else False,
        "memory": _read("/proc/meminfo").splitlines()[0] if Path("/proc/meminfo").exists() else "unavailable",
        "tools": command_status(("bash", "git", "python", "tmux", "rclone", "proot-distro", "sqlite3")),
    }


def format_snapshot(data=None) -> str:
    data = data or snapshot()
    tools = ", ".join(f"{name}={'yes' if value else 'no'}" for name, value in data["tools"].items())
    return ("🟢 SYSTEM ONLINE\n"
            f"Platform: {data['platform']}\n"
            f"Architecture: {data['architecture']}\n"
            f"Termux: {'yes' if data['termux'] else 'no'}\n"
            f"Root: {'yes' if data['root'] else 'no'}\n"
            f"Memory: {data['memory']}\n"
            f"Tools: {tools}")
