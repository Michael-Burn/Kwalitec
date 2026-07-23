"""Errors for Student Experience Integration (PX-002)."""

from __future__ import annotations


class IntegrationExperienceError(Exception):
    """Base error for Experience Integration failures."""

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or "integration_experience_error"


class IntegrationInvariantViolation(IntegrationExperienceError):  # noqa: N818
    """Raised when an integration artefact violates a shape invariant."""

    def __init__(self, message: str, *, invariant: str) -> None:
        super().__init__(message, code="integration_invariant_violation")
        self.invariant = invariant
