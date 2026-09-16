#!/usr/bin/env python3

import shutil

TOOLS = {
    "python": "python",
    "git": "git",
    "go": "go",
    "node": "node",
    "npm": "npm"
}

for name, command in TOOLS.items():
    state = "✓" if shutil.which(command) else "✗"
    print(f"{state} {name}")
