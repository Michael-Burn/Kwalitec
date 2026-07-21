"""Application errors for Student Twin Initialization (BR-003)."""

from __future__ import annotations

from application.errors import ApplicationError


class StudentInitializationError(ApplicationError):
    """Base error for Student Twin Initialization coordination failures."""


class OnboardingValidationError(StudentInitializationError):
    """Raised when ``CompletedOnboarding`` cargo is incomplete or inconsistent."""
