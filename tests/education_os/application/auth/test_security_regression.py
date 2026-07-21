"""Security regression tests for authentication (BR-001)."""

from __future__ import annotations

import pytest

from application.auth.security import constant_time_equals, hash_opaque_token
from domain.auth.errors import AuthInvariantViolation
from domain.auth.password_policy import PasswordPolicy


def test_argon2_hash_and_verify() -> None:
    pytest.importorskip("argon2")
    from infrastructure.security import Argon2PasswordHasher

    hasher = Argon2PasswordHasher()
    hashed = hasher.hash("CorrectHorse!1")
    assert hashed.startswith("$argon2")
    assert hasher.verify("CorrectHorse!1", hashed) is True
    assert hasher.verify("wrong", hashed) is False


def test_constant_time_equals() -> None:
    assert constant_time_equals("abc", "abc") is True
    assert constant_time_equals("abc", "abd") is False


def test_token_hash_is_digest() -> None:
    digest = hash_opaque_token("raw-token-value")
    assert digest != "raw-token-value"
    assert len(digest) == 64


def test_password_policy_rejects_weak() -> None:
    policy = PasswordPolicy()
    with pytest.raises(AuthInvariantViolation):
        policy.validate("short")
    with pytest.raises(AuthInvariantViolation):
        policy.validate("nouppercaseordigitorspecial")
    assert policy.validate("CorrectHorse!1") == "CorrectHorse!1"


def test_secure_cookie_config_flags() -> None:
    import importlib.util
    from pathlib import Path

    path = (
        Path(__file__).resolve().parents[4]
        / "src"
        / "adapters"
        / "flask"
        / "auth"
        / "secure_cookies.py"
    )
    spec = importlib.util.spec_from_file_location("secure_cookies_direct", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    config: dict = {}
    module.apply_secure_cookie_config(config, secure=True)
    assert config["SESSION_COOKIE_SECURE"] is True
    assert config["SESSION_COOKIE_HTTPONLY"] is True
    assert config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert config["REMEMBER_COOKIE_SECURE"] is True
