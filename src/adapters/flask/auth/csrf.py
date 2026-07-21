"""CSRF token helpers for authentication forms (stdlib + Flask session)."""

from __future__ import annotations

from flask import session

from adapters.flask.auth.dependency_provider import AUTH_CSRF_SESSION_KEY
from application.auth.security import constant_time_equals, generate_opaque_token


def ensure_csrf_token() -> str:
    """Return the session CSRF token, creating one when absent."""
    token = session.get(AUTH_CSRF_SESSION_KEY)
    if not isinstance(token, str) or not token.strip():
        token = generate_opaque_token(24)
        session[AUTH_CSRF_SESSION_KEY] = token
    return token


def validate_csrf_token(submitted: str | None) -> bool:
    """Return True when the submitted token matches the session token."""
    expected = session.get(AUTH_CSRF_SESSION_KEY)
    if not isinstance(expected, str) or not expected:
        return False
    return constant_time_equals(expected, (submitted or "").strip())
