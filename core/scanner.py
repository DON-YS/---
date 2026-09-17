#!/usr/bin/env python3

import importlib.util
import json
import shutil
from pathlib import Path

try:
    from paths import registry_path
except ImportError:
    from .paths import registry_path


def command_exists(name):
    return bool(name and shutil.which(name))


def expand(path):
    return Path(path).expanduser()


def check(spec):
    check_spec = spec.get("check", {})
    kind = check_spec.get("kind")
    if kind == "command":
        return "INSTALLED" if command_exists(check_spec.get("name")) else "NOT_INSTALLED"
    if kind == "python_module":
        name = check_spec.get("name")
        try:
            found = bool(name and importlib.util.find_spec(name))
        except (ImportError, ModuleNotFoundError, ValueError):
            found = False
        return "PYTHON_INSTALLED" if found else "NOT_INSTALLED"
    if kind == "python_file":
        return "INSTALLED" if expand(check_spec.get("path", "")).is_file() else "NOT_INSTALLED"
    return "UNKNOWN"


def scan():
    registry = registry_path()
    data = json.loads(registry.read_text(encoding="utf-8"))
    result = {}
    for name, spec in data.get("tools", {}).items():
        tool_type = spec.get("type")
        if tool_type in ("web", "lab", "android", "external"):
            status = "EXTERNAL/LAB"
        else:
            status = check(spec)
        result[name] = {"status": status, "install": spec.get("install", "")}
    return result


def print_report():
    result = scan()
    counts = {}
    for item in result.values():
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    print("⁖ 𝐃𝐎𝐍 ⁞ 𝐒𝐇𝐀𝐇𝐄𝐄𝐍-♔\n")
    print("🟢 INSTALLED:", counts.get("INSTALLED", 0))
    print("🟦 PYTHON:", counts.get("PYTHON_INSTALLED", 0))
    print("🔴 MISSING:", counts.get("NOT_INSTALLED", 0))
    print("🟡 EXTERNAL/LAB:", counts.get("EXTERNAL/LAB", 0))
    for name, item in result.items():
        marker = "✓" if item["status"] in ("INSTALLED", "PYTHON_INSTALLED") else "•" if item["status"] == "EXTERNAL/LAB" else "✗"
        print(marker, name)
    return result


if __name__ == "__main__":
    print_report()
