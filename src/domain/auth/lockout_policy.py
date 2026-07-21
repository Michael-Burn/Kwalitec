"""Account lockout policy — pure threshold rules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True, slots=True)
class LockoutPolicy:
    """Determine when failed login attempts lock an account.

    Pure rules only. Persistence and attempt counting live in application ports.
    """

    max_failed_attempts: int = 5
    lockout_duration_seconds: int = 900
    attempt_window_seconds: int = 900

    def should_lock(self, failed_attempts: int) -> bool:
        """Return True when failed attempts reach the lockout threshold."""
        return failed_attempts >= self.max_failed_attempts

    def lock_until(self, now: datetime) -> datetime:
        """Return the UTC timestamp when a lockout expires."""
        return now + timedelta(seconds=self.lockout_duration_seconds)

    def is_locked(self, *, locked_until: datetime | None, now: datetime) -> bool:
        """Return True when the account is currently locked."""
        if locked_until is None:
            return False
        return locked_until > now

    def attempt_window_start(self, now: datetime) -> datetime:
        """Return the start of the sliding failed-attempt window."""
        return now - timedelta(seconds=self.attempt_window_seconds)
