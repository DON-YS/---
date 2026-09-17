import json
import os
import py_compile
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

import distros
import scanner


class RepositoryTests(unittest.TestCase):
    def test_version(self):
        self.assertTrue((ROOT / "VERSION").exists())

    def test_registry(self):
        path = ROOT / "config" / "registry.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data.get("tools", {}), dict)

    def test_core_python(self):
        for path in (ROOT / "core").glob("*.py"):
            py_compile.compile(str(path), doraise=True)

    def test_security_policy(self):
        data = json.loads((ROOT / "security" / "policy.json").read_text(encoding="utf-8"))
        self.assertFalse(data["arbitrary_remote_shell"])
        self.assertFalse(data["credential_collection"])

    def test_scanner_uses_checkout_registry(self):
        result = scanner.scan()
        self.assertIn("nmap", result)

    @patch("distros.shutil.which", return_value=None)
    def test_distro_detection_degrades_without_proot(self, _which):
        self.assertFalse(distros.available())
        self.assertEqual(distros.installed_distros(), [])

    def test_bot_requires_explicit_configuration(self):
        env = os.environ.copy()
        env.pop("BOT_TOKEN", None)
        env.pop("ADMIN_USER_IDS", None)
        result = subprocess.run(
            [sys.executable, str(ROOT / "bot" / "bot.py")],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("your_telegram_bot_token", result.stdout)


if __name__ == "__main__":
    unittest.main()
