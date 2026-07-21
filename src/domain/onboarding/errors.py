"""Onboarding domain error hierarchy.

Structural and lifecycle failures only. Not HTTP statuses, ORM exceptions, or
educational judgement faults.
"""

from __future__ import annotations


class OnboardingDomainError(Exception):
    """Base error for onboarding domain rule failures."""

    def __init__(self, message: str) -> None:
        cleaned = (message or "").strip() or "onboarding domain error"
        super().__init__(cleaned)
        self.message = cleaned


class OnboardingInvariantViolation(OnboardingDomainError):  # noqa: N818
    """Raised when an onboarding invariant is breached at construction time."""

    def __init__(self, message: str, *, invariant: str | None = None) -> None:
        super().__init__(message)
        self.invariant = (invariant or "").strip() or None


class OnboardingValidationError(OnboardingDomainError):
    """Raised when step payload validation fails structurally."""

    def __init__(
        self,
        message: str,
        *,
        step: str | None = None,
        field: str | None = None,
    ) -> None:
        super().__init__(message)
        self.step = (step or "").strip() or None
        self.field = (field or "").strip() or None
