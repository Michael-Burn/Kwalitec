"""Immutable ProfileSnapshot DTO for Student Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StudyPreferencesSnapshot:
    """Read-only study preferences."""

    preferred_session_minutes: int | None = None
    preferred_study_days: tuple[str, ...] = field(default_factory=tuple)
    reminder_enabled: bool = False
    quiet_hours_label: str = ""


@dataclass(frozen=True)
class LearningStatisticsSnapshot:
    """Read-only learning statistics."""

    total_study_minutes: int = 0
    sessions_completed: int = 0
    topics_mastered: int = 0
    current_exam_readiness: float | None = None
    study_streak_days: int = 0


@dataclass(frozen=True)
class LearningGoalSnapshot:
    """Read-only learning goal."""

    goal_id: str
    title: str
    target_label: str = ""
    progress_ratio: float = 0.0


@dataclass(frozen=True)
class AccountSettingsSnapshot:
    """Read-only account settings."""

    email: str = ""
    notifications_enabled: bool = True
    locale: str = ""
    timezone: str = ""


@dataclass(frozen=True)
class ProfileSnapshot:
    """Profile experience projection DTO."""

    student_id: str
    display_name: str = ""
    examination_label: str = ""
    preferences: StudyPreferencesSnapshot = field(
        default_factory=StudyPreferencesSnapshot
    )
    statistics: LearningStatisticsSnapshot = field(
        default_factory=LearningStatisticsSnapshot
    )
    goals: tuple[LearningGoalSnapshot, ...] = field(default_factory=tuple)
    account: AccountSettingsSnapshot = field(
        default_factory=AccountSettingsSnapshot
    )
