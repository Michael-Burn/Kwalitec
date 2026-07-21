"""Argon2 password hashing for authentication infrastructure."""

from __future__ import annotations

from argon2 import PasswordHasher as Argon2Hasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from application.auth.ports import PasswordHasher
from application.auth.security import constant_time_equals


class Argon2PasswordHasher(PasswordHasher):
    """Production password hasher using Argon2id."""

    def __init__(self, hasher: Argon2Hasher | None = None) -> None:
        self._hasher = hasher or Argon2Hasher()

    def hash(self, password: str) -> str:
        return self._hasher.hash(password or "")

    def verify(self, password: str, password_hash: str) -> bool:
        if not password_hash:
            # Touch both sides so callers still exercise comparison work.
            return constant_time_equals(password or "", "")
        try:
            return bool(self._hasher.verify(password_hash, password or ""))
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False
