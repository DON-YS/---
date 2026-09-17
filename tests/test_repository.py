import hashlib
import json
import os
import py_compile
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

import distros
import gui
import scanner
import storage
import system


class RepositoryTests(unittest.TestCase):
    def test_version_and_registry(self):
        self.assertTrue((ROOT / "VERSION").exists())
        data = json.loads((ROOT / "config" / "registry.json").read_text())
        self.assertIsInstance(data.get("tools"), dict)

    def test_python_compile(self):
        for path in list((ROOT / "core").glob("*.py")) + [ROOT / "bot" / "bot.py"]:
            py_compile.compile(str(path), doraise=True)

    def test_security_policy(self):
        data = json.loads((ROOT / "security" / "policy.json").read_text())
        self.assertFalse(data["arbitrary_remote_shell"])
        self.assertFalse(data["credential_collection"])

    def test_scanner_and_distro_degradation(self):
        self.assertIn("nmap", scanner.scan())
        with patch("distros.shutil.which", return_value=None):
            self.assertFalse(distros.available())
            self.assertEqual(distros.installed_distros(), [])

    def test_storage_manifest_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"; source.write_text("Pirate")
            backup = root / "backup.txt"
            manifest = storage.create_backup(str(source), str(backup))
            self.assertTrue(storage.verify_manifest(str(manifest)))
            restored = root / "restored.txt"
            storage.restore(str(manifest), str(restored))
            self.assertEqual(restored.read_text(), "Pirate")

    def test_gui_diagnostics_are_non_destructive(self):
        result = gui.diagnostics()
        self.assertIn("display", result)
        self.assertIn("xfce4", result)

    def test_bot_requires_config_without_revealing_secret(self):
        env = os.environ.copy(); env.pop("BOT_TOKEN", None); env.pop("ADMIN_USER_IDS", None)
        result = subprocess.run([sys.executable, str(ROOT / "bot" / "bot.py")], env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("your_telegram_bot_token", result.stdout)


if __name__ == "__main__":
    unittest.main()
