#!/usr/bin/env python3
"""Non-destructive GUI capability checks for Termux/X11, XFCE and VNC."""

import os
import shutil


def diagnostics() -> dict:
    return {
        "termux_x11": bool(os.environ.get("TERMUX_VERSION")) and bool(os.environ.get("DISPLAY")),
        "display": os.environ.get("DISPLAY", "not set"),
        "pulse_server": os.environ.get("PULSE_SERVER", "not set"),
        "xfce4": shutil.which("startxfce4") is not None,
        "dbus": shutil.which("dbus-launch") is not None,
        "vnc": shutil.which("vncserver") is not None,
    }


def format_diagnostics(data=None) -> str:
    data = data or diagnostics()
    return ("🎨 GUI DIAGNOSTICS\n"
            f"Termux:X11: {'ready' if data['termux_x11'] else 'not detected'}\n"
            f"DISPLAY: {data['display']}\n"
            f"PULSE_SERVER: {data['pulse_server']}\n"
            f"XFCE: {'installed' if data['xfce4'] else 'missing'}\n"
            f"DBus: {'installed' if data['dbus'] else 'missing'}\n"
            f"VNC: {'installed' if data['vnc'] else 'missing'}")
