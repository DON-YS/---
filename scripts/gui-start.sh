#!/usr/bin/env bash
# Diagnostic/start helper for an already configured XFCE + Termux:X11 environment.
set -eu

if ! command -v startxfce4 >/dev/null 2>&1; then
  echo "XFCE is not installed in this environment."
  exit 2
fi

if [ -z "${DISPLAY:-}" ]; then
  echo "DISPLAY is not set; start Termux:X11 or a VNC server first."
  exit 2
fi

if command -v dbus-launch >/dev/null 2>&1; then
  exec dbus-launch --exit-with-session startxfce4
fi

exec startxfce4
