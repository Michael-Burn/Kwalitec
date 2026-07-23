"""Errors for Learning Journey Experience composition."""

from __future__ import annotations


class JourneyExperienceError(Exception):
    """Base error for Learning Journey Experience failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or "journey_experience_error"


class JourneyInvariantViolation(JourneyExperienceError):  # noqa: N818
    """Raised when a journey view model violates an immutability / shape invariant."""

    def __init__(self, message: str, *, invariant: str) -> None:
        super().__init__(message, code="journey_invariant_violation")
        self.invariant = invariant
