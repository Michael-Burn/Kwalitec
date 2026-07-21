"""Application-layer onboarding errors."""

from __future__ import annotations

from application.errors import ApplicationError


class OnboardingApplicationError(ApplicationError):
    """Raised when an onboarding use-case cannot complete."""

    def __init__(self, message: str, *, code: str = "onboarding_error") -> None:
        super().__init__(message)
        self.code = (code or "").strip() or "onboarding_error"
