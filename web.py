#!/usr/bin/env python3
"""Small production-oriented WSGI web/API layer for Pirate.

The CLI and Termux components remain independent. This module exposes only
allowlisted read/status/install operations and uses the Python stdlib.
"""

import base64
import hashlib
import hmac
import http.cookies
import html
import json
import os
import secrets
import time
from pathlib import Path
from wsgiref.simple_server import make_server

ROOT = Path(__file__).resolve().parent
CORE = ROOT / "core"
import sys
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

from distros import status as distro_status
from installer import install, load
from scanner import scan
from system import snapshot

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
SESSION_TTL = 3600
SESSIONS = {}


def required_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def verify_password(password, encoded):
    try:
        algorithm, iterations, salt, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        derived = hashlib.pbkdf2_hmac("sha256", password.encode(), base64.urlsafe_b64decode(salt), int(iterations))
        return hmac.compare_digest(base64.urlsafe_b64encode(derived).decode(), expected)
    except (ValueError, TypeError):
        return False


def session_user(environ):
    cookie = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
    token = cookie.get("pirate_session")
    if not token:
        return None
    entry = SESSIONS.get(token.value)
    if not entry or entry["expires"] < time.time():
        SESSIONS.pop(token.value, None)
        return None
    return entry["user"]


def json_response(start, status, payload, headers=None):
    body = json.dumps(payload, ensure_ascii=False).encode()
    start(status, [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body))), *(headers or [])])
    return [body]


def page(title, body, user=None):
    nav = f'<form method="post" action="/logout"><button>Logout ({html.escape(user or "")})</button></form>' if user else ''
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)} · Pirate ☠️</title>"
            "<style>body{font-family:system-ui;background:#10131a;color:#eee;max-width:1000px;margin:2rem auto;padding:0 1rem}"
            "a,button{color:#fff;background:#263449;border:0;border-radius:6px;padding:.6rem 1rem;text-decoration:none}"
            ".card{background:#181e28;border:1px solid #344054;border-radius:10px;padding:1rem;margin:1rem 0}"
            "code,pre{white-space:pre-wrap;color:#b9f6ca}</style></head><body>"
            f"<header><h1>Pirate - ☠️</h1>{nav}</header>{body}</body></html>").encode()


def read_body(environ):
    length = int(environ.get("CONTENT_LENGTH") or 0)
    return environ["wsgi.input"].read(length).decode()


def app(environ, start):
    method, path = environ.get("REQUEST_METHOD", "GET"), environ.get("PATH_INFO", "/")
    user = session_user(environ)
    if path == "/health" and method == "GET":
        return json_response(start, "200 OK", {"status": "ok", "version": VERSION})
    if path == "/ready" and method == "GET":
        ready = bool(os.environ.get("ADMIN_USERNAME") and os.environ.get("ADMIN_PASSWORD_HASH") and os.environ.get("AUTH_SECRET"))
        return json_response(start, "200 OK" if ready else "503 Service Unavailable", {"status": "ready" if ready else "not_ready"})
    if path == "/version" and method == "GET":
        return json_response(start, "200 OK", {"name": "Pirate - ☠️", "version": VERSION})
    if path == "/login":
        if method == "POST":
            form = __import__("urllib.parse").parse_qs(read_body(environ))
            username = form.get("username", [""])[0]
            password = form.get("password", [""])[0]
            if hmac.compare_digest(username, os.environ.get("ADMIN_USERNAME", "")) and verify_password(password, os.environ.get("ADMIN_PASSWORD_HASH", "")):
                token = secrets.token_urlsafe(32)
                SESSIONS[token] = {"user": username, "expires": time.time() + SESSION_TTL}
                return json_response(start, "303 See Other", {}, [("Location", "/"), ("Set-Cookie", f"pirate_session={token}; HttpOnly; Secure; SameSite=Strict; Max-Age={SESSION_TTL}")])
            return page("Login", "<p>Invalid credentials.</p><form method='post'><input name='username' required><input name='password' type='password' required><button>Login</button></form>"), start("401 Unauthorized", [("Content-Type", "text/html; charset=utf-8")]) or []
        body = page("Login", "<form method='post'><input name='username' placeholder='Username' required><input name='password' type='password' placeholder='Password' required><button>Login</button></form>")
        start("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
        return [body]
    if path == "/logout" and method == "POST":
        cookie = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", "")); token = cookie.get("pirate_session")
        if token: SESSIONS.pop(token.value, None)
        return json_response(start, "303 See Other", {}, [("Location", "/login"), ("Set-Cookie", "pirate_session=; Max-Age=0; HttpOnly; Secure; SameSite=Strict")])
    if path.startswith("/api/") and not user:
        return json_response(start, "401 Unauthorized", {"error": "authentication required"})
    if path == "/api/status": return json_response(start, "200 OK", snapshot())
    if path == "/api/tools": return json_response(start, "200 OK", scan())
    if path == "/api/distros": return json_response(start, "200 OK", distro_status())
    if path == "/api/install" and method == "POST":
        data = json.loads(read_body(environ) or "{}")
        name = data.get("name")
        if not isinstance(name, str) or name not in load(): return json_response(start, "400 Bad Request", {"error": "unknown registry tool"})
        return json_response(start, "200 OK", {"tool": name, "exit_code": install(name)})
    if path == "/" and user:
        status = html.escape(json.dumps(snapshot(), indent=2))
        body = page("Dashboard", f"<div class='card'><h2>Dashboard</h2><pre>{status}</pre><p><a href='/api/tools'>Tools API</a> <a href='/api/distros'>Distros API</a></p></div>", user)
        start("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
        return [body]
    start("302 Found", [("Location", "/login")]); return [b""]


def main():
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    with make_server(host, port, app) as server:
        print(f"Pirate web server listening on {host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    main()
