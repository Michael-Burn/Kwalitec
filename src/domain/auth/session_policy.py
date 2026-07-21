"""Session timeout policy — pure idle/absolute session rules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True, slots=True)
class SessionPolicy:
    """Session lifetime rules for authenticated sessions.

    Absolute timeout bounds total session age. Idle timeout bounds inactivity.
    """

    absolute_timeout_seconds: int = 43_200  # 12 hours
    idle_timeout_seconds: int = 1_800  # 30 minutes
    remember_me_seconds: int = 1_209_600  # 14 days

    def is_expired(
        self,
        *,
        created_at: datetime,
        last_activity_at: datetime,
        now: datetime,
        remember_me: bool = False,
    ) -> bool:
        """Return True when the session has timed out."""
        absolute = (
            self.remember_me_seconds if remember_me else self.absolute_timeout_seconds
        )
        if now - created_at >= timedelta(seconds=absolute):
            return True
        idle = self.remember_me_seconds if remember_me else self.idle_timeout_seconds
        return now - last_activity_at >= timedelta(seconds=idle)
