#!/usr/bin/env python3

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

BASE = Path.home() / ".ys-ultra15"
REGISTRY = BASE / "config" / "registry.json"

def load():
    return json.loads(REGISTRY.read_text())["tools"]

def run(cmd):
    print()
    print("COMMAND:")
    print(cmd)
    print()

    return subprocess.run(
        ["bash", "-lc", cmd],
        env=os.environ.copy()
    ).returncode

def install(name):

    tools = load()

    if name not in tools:
        print("❌ Unknown tool:", name)
        return 2

    spec = tools[name]
    tool_type = spec.get("type")

    if tool_type in ("web", "lab", "external", "android"):
        print("🟡 This entry is external/lab-only.")
        print(spec.get("install", ""))
        return 0

    cmd = spec.get("install")

    if not cmd:
        print("❌ No installer defined.")
        return 3

    if name == "sqlmap":
        target = Path.home() / ".ys-ultra15" / "opt" / "sqlmap"

        if target.exists():
            sqlmap = target / "sqlmap.py"

            if sqlmap.exists():
                print("✓ SQLMap repository already exists.")
                print("✓ Skipping clone.")
                return 0

            print("⚠ Existing SQLMap directory is incomplete.")
            print("Refusing to delete it automatically.")
            return 4

    return run(cmd)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: installer.py <tool>")
        raise SystemExit(1)

    raise SystemExit(install(sys.argv[1]))
