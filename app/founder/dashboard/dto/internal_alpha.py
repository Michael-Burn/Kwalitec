"""Internal Alpha read-model DTOs for Founder Dashboard (FOS-004)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class InternalAlphaWeekSummary:
    """One Internal Alpha week summary for activity lists."""

    week: str
    feedback_count: int
    duplicate_count: int


@dataclass(frozen=True)
class InternalAlphaSnapshot:
    """Immutable Internal Alpha read-model for the dashboard."""

    current_week: str
    feedback_count: int
    duplicate_count: int
    category_counts: Mapping[str, int]
    latest_summary_file: str
    recent_weeks: tuple[InternalAlphaWeekSummary, ...] = ()


@dataclass(frozen=True)
class InternalAlphaSection:
    """Internal Alpha panel for the Founder Dashboard."""

    current_week: str
    feedback_count: int
    duplicate_count: int
    category_counts: Mapping[str, int]
    latest_summary_file: str
    recent_weeks: tuple[InternalAlphaWeekSummary, ...]
