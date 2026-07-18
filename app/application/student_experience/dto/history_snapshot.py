"""Immutable HistorySnapshot DTO for Student Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CompletedSessionSnapshot:
    """Read-only completed session card."""

    session_id: str
    topic_title: str
    completed_at: str = ""
    study_minutes: int = 0


@dataclass(frozen=True)
class ReadinessPointSnapshot:
    """Read-only readiness progression point."""

    recorded_at: str
    exam_readiness: float
    label: str = ""


@dataclass(frozen=True)
class AchievementSnapshot:
    """Read-only achievement card."""

    achievement_id: str
    title: str
    earned_at: str = ""
    description: str = ""


@dataclass(frozen=True)
class HistorySnapshot:
    """History experience projection DTO."""

    student_id: str
    completed_sessions: tuple[CompletedSessionSnapshot, ...] = field(
        default_factory=tuple
    )
    total_study_minutes: int = 0
    readiness_progression: tuple[ReadinessPointSnapshot, ...] = field(
        default_factory=tuple
    )
    mastered_topics: tuple[str, ...] = field(default_factory=tuple)
    revision_history: tuple[str, ...] = field(default_factory=tuple)
    recent_achievements: tuple[AchievementSnapshot, ...] = field(
        default_factory=tuple
    )
    session_count: int = 0
    mastered_count: int = 0
