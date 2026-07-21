"""Frozen result DTOs for authentication use-cases."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.auth.enums import AccountStatus, AuthFailureReason


@dataclass(frozen=True, slots=True)
class AuthSessionClaims:
    """Framework-free session claims after successful authentication."""

    user_id: str
    email: str
    remember_me: bool
    created_at: datetime
    last_activity_at: datetime
    email_verified: bool


@dataclass(frozen=True, slots=True)
class AuthResult:
    """Outcome of an authentication use-case."""

    success: bool
    reason: AuthFailureReason | None = None
    message: str = ""
    user_id: str | None = None
    email: str | None = None
    status: AccountStatus | None = None
    session: AuthSessionClaims | None = None
    # Present only in test / non-production wiring for email capture inspection.
    issued_token: str | None = None
