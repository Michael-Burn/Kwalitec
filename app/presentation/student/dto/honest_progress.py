"""Honest Progress presentation DTOs (read-and-present only)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ProgressMilestoneRow:
    """One milestone already announced, for the Progress page list."""

    milestone_id: str
    label: str
    shown_at: date
    shown_at_label: str


@dataclass(frozen=True)
class HonestProgressPage:
    """Calm Progress summary: streak, coverage, mastery, milestones reached."""

    page_title: str
    current_streak_days: int
    longest_streak_days: int
    syllabus_coverage_percent: int | None
    syllabus_coverage_label: str
    topics_mastered_count: int
    milestones: tuple[ProgressMilestoneRow, ...]
    empty_milestones_message: str
    progress_href: str = ""
