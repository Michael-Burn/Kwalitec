"""Persistence DTOs for authentication aggregates (BR-004)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class UserAccountDTO:
    user_id: str
    email: str
    password_hash: str
    status: str
    email_verified: bool
    failed_login_attempts: int
    locked_until: datetime | None
    created_at: datetime
    updated_at: datetime
    password_changed_at: datetime
    row_version: int = 1


@dataclass(frozen=True, slots=True)
class AuthTokenDTO:
    user_id: str
    purpose: str
    token_hash: str
    expires_at: datetime
    created_at: datetime
    consumed_at: datetime | None = None
