#!/usr/bin/env python3
"""Safe, read-only PRoot-Distro capability discovery."""

import shutil
import subprocess
from typing import List


def available() -> bool:
    return shutil.which("proot-distro") is not None


def installed_distros() -> List[str]:
    """Return distro names reported by proot-distro, never guessing availability."""
    if not available():
        return []
    try:
        result = subprocess.run(
            ["proot-distro", "list", "--quiet"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []
    return sorted({line.strip() for line in result.stdout.splitlines() if line.strip()})


def status() -> dict:
    names = installed_distros()
    return {
        "available": available(),
        "installed": names,
        "supported_targets": ["debian", "ubuntu", "kali-rolling", "alpine", "parrot", "nixos"],
    }


if __name__ == "__main__":
    data = status()
    if not data["available"]:
        print("proot-distro: NOT AVAILABLE")
    elif data["installed"]:
        print("Installed distributions:")
        for name in data["installed"]:
            print(f"✓ {name}")
    else:
        print("proot-distro is available, but no installed distributions were reported.")
