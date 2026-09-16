#!/usr/bin/env python3

import json
from pathlib import Path

REGISTRY = Path.home() / ".ys-ultra15" / "config" / "registry.json"

def load_registry():
    return json.loads(REGISTRY.read_text())

if __name__ == "__main__":
    data = load_registry()
    print("Tools:", len(data.get("tools", {})))
