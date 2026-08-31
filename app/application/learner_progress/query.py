"""Qualifying study day query port (Honest Progress foundation).

Read-only, purpose-built interface parallel to LearnerTwinQueryPort (ADR-027).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class StreakStats:
    """Plain streak facts derived from qualifying study days."""

    current_streak_days: int
    longest_streak_days: int
    qualifying_dates: tuple[date, ...]


class QualifyingStudyDayQueryPort(Protocol):
    """Narrow read-only surface for qualifying study day history."""

    def qualifying_study_dates(
        self,
        *,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> tuple[date, ...]:
        """Distinct qualifying study dates in the inclusive range."""
        ...

    def streak_stats(
        self,
        *,
        user_id: int,
        as_of: date,
        lookback_days: int = 90,
    ) -> StreakStats:
        """Current and longest streak with qualifying dates in the lookback window."""
        ...
