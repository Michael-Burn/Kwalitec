"""Errors for Exam Readiness Experience composition."""

from __future__ import annotations


class ReadinessExperienceError(Exception):
    """Base error for Exam Readiness Experience failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or "readiness_experience_error"


class ReadinessInvariantViolation(ReadinessExperienceError):  # noqa: N818
    """Raised when a readiness view model violates a shape invariant."""

    def __init__(self, message: str, *, invariant: str) -> None:
        super().__init__(message, code="readiness_invariant_violation")
        self.invariant = invariant
