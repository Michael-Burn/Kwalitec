"""UserAccount aggregate — trusted student identity credentials.

Authentication only. Does not create Student Twins, run onboarding, or
encode educational state.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from domain.auth.email_address import EmailAddress
from domain.auth.enums import AccountStatus
from domain.auth.errors import AuthDomainError, AuthInvariantViolation
from domain.auth.ids import UserId
from domain.auth.lockout_policy import LockoutPolicy


@dataclass(frozen=True, slots=True)
class UserAccount:
    """Immutable credential account for one authenticated identity."""

    user_id: UserId
    email: EmailAddress
    password_hash: str
    status: AccountStatus
    email_verified: bool
    failed_login_attempts: int
    locked_until: datetime | None
    created_at: datetime
    updated_at: datetime
    password_changed_at: datetime

    def __post_init__(self) -> None:
        if not (self.password_hash or "").strip():
            raise AuthInvariantViolation(
                "password hash is required",
                invariant="password_hash_non_empty",
            )
        if self.failed_login_attempts < 0:
            raise AuthInvariantViolation(
                "failed login attempts cannot be negative",
                invariant="failed_attempts_non_negative",
            )

    @classmethod
    def register(
        cls,
        *,
        user_id: UserId,
        email: EmailAddress,
        password_hash: str,
        now: datetime,
    ) -> UserAccount:
        """Create a new account pending email verification."""
        return cls(
            user_id=user_id,
            email=email,
            password_hash=password_hash,
            status=AccountStatus.PENDING_VERIFICATION,
            email_verified=False,
            failed_login_attempts=0,
            locked_until=None,
            created_at=now,
            updated_at=now,
            password_changed_at=now,
        )

    def assert_can_authenticate(
        self,
        *,
        now: datetime,
        lockout_policy: LockoutPolicy,
        require_verified_email: bool = True,
    ) -> None:
        """Raise when the account cannot accept a login attempt."""
        if self.status is AccountStatus.DISABLED:
            raise AuthDomainError("account is disabled")
        if lockout_policy.is_locked(locked_until=self.locked_until, now=now):
            raise AuthDomainError("account is locked")
        if self.status is AccountStatus.LOCKED:
            raise AuthDomainError("account is locked")
        if require_verified_email and not self.email_verified:
            raise AuthDomainError("email is not verified")

    def record_failed_login(
        self,
        *,
        now: datetime,
        lockout_policy: LockoutPolicy,
    ) -> UserAccount:
        """Return a copy with an incremented failure count and optional lock."""
        attempts = self.failed_login_attempts + 1
        locked_until = self.locked_until
        status = self.status
        if lockout_policy.should_lock(attempts):
            locked_until = lockout_policy.lock_until(now)
            status = AccountStatus.LOCKED
        return replace(
            self,
            failed_login_attempts=attempts,
            locked_until=locked_until,
            status=status,
            updated_at=now,
        )

    def record_successful_login(self, *, now: datetime) -> UserAccount:
        """Clear lockout state after a successful authentication."""
        status = (
            AccountStatus.ACTIVE
            if self.email_verified
            else AccountStatus.PENDING_VERIFICATION
        )
        return replace(
            self,
            failed_login_attempts=0,
            locked_until=None,
            status=status,
            updated_at=now,
        )

    def mark_email_verified(self, *, now: datetime) -> UserAccount:
        """Mark the account email as verified and activate the account."""
        return replace(
            self,
            email_verified=True,
            status=AccountStatus.ACTIVE,
            updated_at=now,
        )

    def change_password_hash(self, password_hash: str, *, now: datetime) -> UserAccount:
        """Replace the stored password hash and clear lockout counters."""
        cleaned = (password_hash or "").strip()
        if not cleaned:
            raise AuthInvariantViolation(
                "password hash is required",
                invariant="password_hash_non_empty",
            )
        return replace(
            self,
            password_hash=cleaned,
            password_changed_at=now,
            failed_login_attempts=0,
            locked_until=None,
            status=AccountStatus.ACTIVE if self.email_verified else self.status,
            updated_at=now,
        )
