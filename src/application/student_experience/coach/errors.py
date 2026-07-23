"""Errors for AI Learning Coach composition."""

from __future__ import annotations


class CoachExperienceError(Exception):
    """Base error for AI Learning Coach failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or "coach_experience_error"


class CoachInvariantViolation(CoachExperienceError):  # noqa: N818
    """Raised when a coach view model violates a shape invariant."""

    def __init__(self, message: str, *, invariant: str) -> None:
        super().__init__(message, code="coach_invariant_violation")
        self.invariant = invariant
