"""Errors for Student Home Experience composition."""

from __future__ import annotations


class HomeExperienceError(Exception):
    """Base error for Student Home Experience failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or "home_experience_error"


class HomeInvariantViolation(HomeExperienceError):  # noqa: N818
    """Raised when a home view model violates an immutability / shape invariant."""

    def __init__(self, message: str, *, invariant: str) -> None:
        super().__init__(message, code="home_invariant_violation")
        self.invariant = invariant
