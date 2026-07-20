"""Educational foundation error hierarchy.

These errors express educational domain failures. They are not HTTP status
codes, ORM exceptions, or infrastructure faults.
"""

from __future__ import annotations


class EducationalDomainError(Exception):
    """Base error for educational domain rule failures.

    Raised when a domain operation cannot proceed because educational meaning
    would be violated or required information is educationally invalid.
    """

    def __init__(self, message: str) -> None:
        cleaned = (message or "").strip()
        if not cleaned:
            cleaned = "educational domain error"
        super().__init__(cleaned)
        self.message = cleaned


class EducationalInvariantViolation(EducationalDomainError):
    """Raised when an educational invariant is breached at construction time.

    Prefer this over silent coercion. Invalid educational objects must not
    enter the domain model.
    """

    def __init__(self, message: str, *, invariant: str | None = None) -> None:
        super().__init__(message)
        self.invariant = (invariant or "").strip() or None
