#!/usr/bin/env python3

import sys
from scanner import print_report
from installer import install

def main():

    if len(sys.argv) < 2:
        print("Usage:")
        print("core.py status")
        print("core.py install <tool>")
        return 1

    action = sys.argv[1]

    if action == "status":
        print_report()
        return 0

    if action == "install":

        if len(sys.argv) != 3:
            print("Usage: core.py install <tool>")
            return 1

        return install(sys.argv[2])

    print("Unknown action:", action)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
