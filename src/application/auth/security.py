"""Constant-time comparison helpers (stdlib only)."""

from __future__ import annotations

import hashlib
import hmac
import secrets


def constant_time_equals(left: str, right: str) -> bool:
    """Compare two strings in constant time."""
    return hmac.compare_digest(
        (left or "").encode("utf-8"),
        (right or "").encode("utf-8"),
    )


def hash_opaque_token(raw_token: str) -> str:
    """Return a SHA-256 hex digest of an opaque token for storage."""
    return hashlib.sha256((raw_token or "").encode("utf-8")).hexdigest()


def generate_opaque_token(nbytes: int = 32) -> str:
    """Return a URL-safe opaque token."""
    return secrets.token_urlsafe(nbytes)
