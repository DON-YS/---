#!/usr/bin/env python3

import json
import shutil
import importlib.util
import os
from pathlib import Path

BASE = Path.home() / ".ys-ultra15"
REGISTRY = BASE / "config" / "registry.json"

def command_exists(name):
    return bool(name and shutil.which(name))

def expand(path):
    return Path(os.path.expandvars(os.path.expanduser(path)))

def check(spec):
    c = spec.get("check", {})
    kind = c.get("kind")

    if kind == "command":
        return "INSTALLED" if command_exists(c.get("name")) else "NOT_INSTALLED"

    if kind == "python_module":
        name = c.get("name")
        return "PYTHON_INSTALLED" if importlib.util.find_spec(name) else "NOT_INSTALLED"

    if kind == "python_file":
        path = expand(c.get("path", ""))
        return "INSTALLED" if path.is_file() else "NOT_INSTALLED"

    return "UNKNOWN"

def scan():
    data = json.loads(REGISTRY.read_text())
    result = {}

    for name, spec in data.get("tools", {}).items():

        tool_type = spec.get("type")

        if tool_type in ("web", "lab", "android", "external"):
            result[name] = {
                "status": "EXTERNAL/LAB",
                "install": spec.get("install", "")
            }
            continue

        result[name] = {
            "status": check(spec),
            "install": spec.get("install", "")
        }

    return result

def print_report():
    result = scan()

    counts = {}

    for item in result.values():
        status = item["status"]
        counts[status] = counts.get(status, 0) + 1

    print("⁖ 𝐃𝐎𝐍 ⁞ 𝐒𝐇𝐀𝐇𝐄𝐄𝐍-♔")
    print()
    print("🟢 INSTALLED:", counts.get("INSTALLED", 0))
    print("🟦 PYTHON:", counts.get("PYTHON_INSTALLED", 0))
    print("🔴 MISSING:", counts.get("NOT_INSTALLED", 0))
    print("🟡 EXTERNAL/LAB:", counts.get("EXTERNAL/LAB", 0))
    print()

    for name, item in result.items():
        s = item["status"]

        if s == "INSTALLED":
            print("✓", name)

        elif s == "PYTHON_INSTALLED":
            print("✓", name, "[PYTHON MODULE]")

        elif s == "NOT_INSTALLED":
            print("✗", name)

        else:
            print("•", name)

    return result

if __name__ == "__main__":
    print_report()
