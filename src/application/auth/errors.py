"""Application-layer authentication errors."""

from __future__ import annotations

from application.errors import ApplicationError
from domain.auth.enums import AuthFailureReason


class AuthenticationError(ApplicationError):
    """Raised when an authentication use-case cannot complete."""

    def __init__(
        self,
        message: str,
        *,
        reason: AuthFailureReason = AuthFailureReason.VALIDATION_ERROR,
    ) -> None:
        super().__init__(message)
        self.reason = reason
