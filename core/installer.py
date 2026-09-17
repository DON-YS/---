#!/usr/bin/env python3
"""Registry-driven installer with safe path handling and bounded execution."""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict

try:
    from paths import registry_path
except ImportError:  # package-style imports
    from .paths import registry_path


INSTALL_TIMEOUT_SECONDS = 900


def load() -> Dict[str, dict]:
    path = registry_path()
    data = json.loads(path.read_text(encoding="utf-8"))
    tools = data.get("tools")
    if not isinstance(tools, dict):
        raise ValueError(f"Invalid registry: {path}")
    return tools


def run(cmd: str) -> int:
    """Run a trusted registry command; callers must never pass user shell text."""
    print("\nCOMMAND:\n" + cmd + "\n")
    try:
        completed = subprocess.run(
            ["bash", "-lc", cmd],
            env=os.environ.copy(),
            check=False,
            timeout=INSTALL_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"Installer timed out after {INSTALL_TIMEOUT_SECONDS} seconds.")
        return 124
    except OSError as exc:
        print(f"Unable to start installer: {exc}")
        return 127
    return completed.returncode


def install(name: str) -> int:
    if not name or name not in load():
        print("❌ Unknown tool:", name)
        return 2

    spec = load()[name]
    tool_type = spec.get("type")
    if tool_type in ("web", "lab", "external", "android"):
        print("🟡 This entry is external/lab-only.")
        print(spec.get("install", ""))
        return 0

    command = spec.get("install")
    if not isinstance(command, str) or not command.strip():
        print("❌ No installer defined.")
        return 3

    if name == "sqlmap":
        target = Path.home() / ".ys-ultra15" / "opt" / "sqlmap"
        if target.exists():
            if (target / "sqlmap.py").is_file():
                print("✓ SQLMap repository already exists; skipping clone.")
                return 0
            print("⚠ Existing SQLMap directory is incomplete; refusing to delete it.")
            return 4

    return run(command)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: installer.py <tool>")
        raise SystemExit(1)
    raise SystemExit(install(sys.argv[1]))
