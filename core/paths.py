#!/usr/bin/env python3
"""Shared repository path resolution for both source and installed layouts."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSTALL_ROOT = Path.home() / ".ys-ultra15"


def runtime_root() -> Path:
    """Return the installed root when it contains the registry, otherwise the checkout."""
    installed_registry = INSTALL_ROOT / "config" / "registry.json"
    if installed_registry.is_file():
        return INSTALL_ROOT
    return PROJECT_ROOT


def registry_path() -> Path:
    return runtime_root() / "config" / "registry.json"
