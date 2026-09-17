#!/usr/bin/env python3
import base64
import hashlib
import os
import secrets
import sys

password = sys.argv[1] if len(sys.argv) == 2 else os.environ.get("PASSWORD")
if not password:
    raise SystemExit("usage: hash-password.py 'password' (prefer stdin in shell history-sensitive environments)")
salt = secrets.token_bytes(16)
derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310000)
print("pbkdf2_sha256$310000$%s$%s" % (base64.urlsafe_b64encode(salt).decode(), base64.urlsafe_b64encode(derived).decode()))
