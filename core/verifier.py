#!/usr/bin/env python3

import shutil
import sys

def verify(command):
    return shutil.which(command) is not None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: verifier.py <command>")
        raise SystemExit(1)

    print("✓ VERIFIED" if verify(sys.argv[1]) else "✗ NOT VERIFIED")
