"""Frozen request DTOs for authentication use-cases."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterRequest:
    """Register a new student identity with email and password."""

    email: str
    password: str
    client_key: str = ""


@dataclass(frozen=True, slots=True)
class LoginRequest:
    """Authenticate with email and password."""

    email: str
    password: str
    remember_me: bool = False
    client_key: str = ""


@dataclass(frozen=True, slots=True)
class VerifyEmailRequest:
    """Confirm an email address using a verification token."""

    token: str
    client_key: str = ""


@dataclass(frozen=True, slots=True)
class RequestPasswordResetRequest:
    """Request a password-reset email for an account."""

    email: str
    client_key: str = ""


@dataclass(frozen=True, slots=True)
class ResetPasswordRequest:
    """Set a new password using a reset token."""

    token: str
    new_password: str
    client_key: str = ""


@dataclass(frozen=True, slots=True)
class ChangePasswordRequest:
    """Change password for an authenticated user."""

    user_id: str
    current_password: str
    new_password: str
    client_key: str = ""


@dataclass(frozen=True, slots=True)
class SessionValidationRequest:
    """Validate whether an authenticated session is still within policy."""

    user_id: str
    created_at_iso: str
    last_activity_at_iso: str
    remember_me: bool = False
