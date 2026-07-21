"""Secure cookie configuration for authenticated Flask sessions."""

from __future__ import annotations

from typing import Any


def apply_secure_cookie_config(
    config: dict[str, Any],
    *,
    secure: bool = True,
    httponly: bool = True,
    samesite: str = "Lax",
    session_lifetime_seconds: int = 43_200,
    remember_lifetime_seconds: int = 1_209_600,
) -> dict[str, Any]:
    """Mutate and return a Flask config mapping with hardened cookie flags.

    Args:
        config: Flask application config mapping.
        secure: Require HTTPS cookies (disable only for local HTTP tests).
        httponly: Block JavaScript access to session cookies.
        samesite: SameSite policy (``Lax`` or ``Strict``).
        session_lifetime_seconds: Absolute session cookie lifetime.
        remember_lifetime_seconds: Remember-me cookie lifetime.

    Returns:
        The same config mapping for chaining.
    """
    config["SESSION_COOKIE_SECURE"] = secure
    config["SESSION_COOKIE_HTTPONLY"] = httponly
    config["SESSION_COOKIE_SAMESITE"] = samesite
    config["REMEMBER_COOKIE_SECURE"] = secure
    config["REMEMBER_COOKIE_HTTPONLY"] = httponly
    config["REMEMBER_COOKIE_SAMESITE"] = samesite
    config["PERMANENT_SESSION_LIFETIME"] = session_lifetime_seconds
    config["REMEMBER_COOKIE_DURATION"] = remember_lifetime_seconds
    return config
