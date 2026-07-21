"""Authentication token value objects — email verification and password reset."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from domain.auth.enums import AuthTokenPurpose
from domain.auth.errors import AuthInvariantViolation
from domain.auth.ids import UserId


@dataclass(frozen=True, slots=True)
class AuthToken:
    """Opaque single-use authentication token bound to a user and purpose."""

    user_id: UserId
    purpose: AuthTokenPurpose
    token_hash: str
    expires_at: datetime
    created_at: datetime
    consumed_at: datetime | None = None

    def __post_init__(self) -> None:
        if not (self.token_hash or "").strip():
            raise AuthInvariantViolation(
                "token hash is required",
                invariant="token_hash_non_empty",
            )
        if self.expires_at <= self.created_at:
            raise AuthInvariantViolation(
                "token expiry must be after creation",
                invariant="token_expiry_after_creation",
            )

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at

    def is_consumed(self) -> bool:
        return self.consumed_at is not None

    def is_usable(self, now: datetime) -> bool:
        return not self.is_consumed() and not self.is_expired(now)

    @staticmethod
    def default_ttl(purpose: AuthTokenPurpose) -> timedelta:
        if purpose is AuthTokenPurpose.EMAIL_VERIFICATION:
            return timedelta(hours=24)
        return timedelta(hours=1)
