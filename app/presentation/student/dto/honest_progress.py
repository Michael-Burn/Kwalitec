"""Honest Progress / Stats presentation DTOs (read-and-present only)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ProgressMilestoneRow:
    """One milestone already announced, for the Stats page list."""

    milestone_id: str
    label: str
    shown_at: date
    shown_at_label: str


@dataclass(frozen=True)
class LearningStateCountRow:
    """One aggregate learning-state count for the Stats Learning section."""

    state: str
    state_label: str
    state_icon: str
    count: int


@dataclass(frozen=True)
class HonestProgressPage:
    """Calm Stats summary: consistency, learning, curriculum, milestones."""

    page_title: str
    current_streak_days: int
    longest_streak_days: int
    syllabus_coverage_percent: int | None
    syllabus_coverage_label: str
    covered_count: int
    topic_count: int
    learning_state_counts: tuple[LearningStateCountRow, ...]
    topics_mastered_count: int
    milestones: tuple[ProgressMilestoneRow, ...]
    empty_milestones_message: str
    progress_href: str = ""
