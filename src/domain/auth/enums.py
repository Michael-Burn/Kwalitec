"""Authentication domain enumerations."""

from __future__ import annotations

from enum import StrEnum


class AccountStatus(StrEnum):
    """Lifecycle status of a user account."""

    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    LOCKED = "locked"
    DISABLED = "disabled"


class AuthTokenPurpose(StrEnum):
    """Purpose of a single-use authentication token."""

    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"


class AuthFailureReason(StrEnum):
    """Machine-readable authentication failure reasons (never leak secrets)."""

    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_DISABLED = "account_disabled"
    EMAIL_NOT_VERIFIED = "email_not_verified"
    WEAK_PASSWORD = "weak_password"
    EMAIL_TAKEN = "email_taken"
    INVALID_TOKEN = "invalid_token"
    TOKEN_EXPIRED = "token_expired"
    RATE_LIMITED = "rate_limited"
    SESSION_EXPIRED = "session_expired"
    VALIDATION_ERROR = "validation_error"
