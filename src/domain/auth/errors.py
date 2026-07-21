"""Authentication domain error hierarchy.

These errors express identity and credential rule failures. They are not HTTP
status codes, ORM exceptions, or educational domain faults.
"""

from __future__ import annotations


class AuthDomainError(Exception):
    """Base error for authentication domain rule failures."""

    def __init__(self, message: str) -> None:
        cleaned = (message or "").strip() or "authentication domain error"
        super().__init__(cleaned)
        self.message = cleaned


class AuthInvariantViolation(AuthDomainError):  # noqa: N818
    """Raised when an authentication invariant is breached at construction time."""

    def __init__(self, message: str, *, invariant: str | None = None) -> None:
        super().__init__(message)
        self.invariant = (invariant or "").strip() or None
