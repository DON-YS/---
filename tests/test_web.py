import base64
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from web import app, verify_password

class WebTests(unittest.TestCase):
    def test_password_hash(self):
        salt = base64.urlsafe_b64encode(b"0123456789abcdef").decode()
        digest = hashlib.pbkdf2_hmac("sha256", b"secret", b"0123456789abcdef", 310000)
        encoded = f"pbkdf2_sha256$310000${salt}${base64.urlsafe_b64encode(digest).decode()}"
        self.assertTrue(verify_password("secret", encoded))
        self.assertFalse(verify_password("wrong", encoded))

    def test_health(self):
        captured = {}
        def start(status, headers): captured.update(status=status, headers=headers)
        result = app({"REQUEST_METHOD":"GET", "PATH_INFO":"/health", "HTTP_COOKIE":"", "wsgi.input": tempfile.TemporaryFile()}, start)
        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(json.loads(result[0])["status"], "ok")

if __name__ == "__main__": unittest.main()
