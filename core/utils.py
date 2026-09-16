#!/usr/bin/env python3

from pathlib import Path

def banner():
    print("⁖ 𝐃𝐎𝐍 ⁞ 𝐒𝐇𝐀𝐇𝐄𝐄𝐍-♔")

def ensure(path):
    Path(path).mkdir(parents=True, exist_ok=True)
