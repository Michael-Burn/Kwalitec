"""Immutable JourneySnapshot DTO for Student Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class JourneyTopicSnapshot:
    """Read-only journey topic card."""

    topic_id: str
    title: str
    status_label: str = ""
    prerequisite_note: str = ""


@dataclass(frozen=True)
class JourneySnapshot:
    """Journey experience projection DTO."""

    student_id: str
    current_topic: JourneyTopicSnapshot | None = None
    completed_topics: tuple[JourneyTopicSnapshot, ...] = field(
        default_factory=tuple
    )
    upcoming_topics: tuple[JourneyTopicSnapshot, ...] = field(
        default_factory=tuple
    )
    overall_progress_ratio: float = 0.0
    progress_percent: int = 0
    estimated_completion_label: str = ""
    prerequisite_visibility: tuple[str, ...] = field(default_factory=tuple)
    examination_label: str = ""
    completed_count: int = 0
    upcoming_count: int = 0
