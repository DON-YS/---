#!/usr/bin/env python3
"""Local backup/restore primitives with manifest and SHA-256 verification."""

import hashlib
import json
import shutil
from pathlib import Path


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_backup(source: str, destination: str) -> Path:
    source_path = Path(source).expanduser().resolve()
    destination_path = Path(destination).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination_path)
    manifest = destination_path.with_name(destination_path.name + ".manifest.json")
    manifest.write_text(json.dumps({
        "source": str(source_path),
        "backup": str(destination_path),
        "sha256": sha256(destination_path),
        "size": destination_path.stat().st_size,
    }, indent=2) + "\n", encoding="utf-8")
    return manifest


def verify_manifest(manifest: str) -> bool:
    data = json.loads(Path(manifest).expanduser().read_text(encoding="utf-8"))
    backup = Path(data["backup"]).expanduser()
    return backup.is_file() and backup.stat().st_size == data["size"] and sha256(backup) == data["sha256"]


def restore(manifest: str, destination: str) -> Path:
    if not verify_manifest(manifest):
        raise ValueError("Backup manifest verification failed")
    data = json.loads(Path(manifest).expanduser().read_text(encoding="utf-8"))
    target = Path(destination).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(data["backup"]).expanduser(), target)
    if sha256(target) != data["sha256"]:
        raise ValueError("Restored file hash does not match manifest")
    return target


def capability() -> dict:
    import shutil as _shutil
    return {"rclone": _shutil.which("rclone") is not None, "local_manifest": True, "telegram_storage": False}
