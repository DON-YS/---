from pathlib import Path
import json
import py_compile


ROOT = Path(__file__).resolve().parents[1]


def test_version():
    assert (ROOT / "VERSION").exists()


def test_registry():
    path = ROOT / "config" / "registry.json"
    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert isinstance(data.get("tools", {}), dict)


def test_core_python():
    for path in (ROOT / "core").glob("*.py"):
        py_compile.compile(str(path), doraise=True)


def test_security_policy():
    path = ROOT / "security" / "policy.json"
    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["arbitrary_remote_shell"] is False
    assert data["credential_collection"] is False
