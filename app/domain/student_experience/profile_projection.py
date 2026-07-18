"""Profile projection — examination, preferences, stats, goals, settings."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StudyPreferences:
    """Student study preference presentation fields."""

    preferred_session_minutes: int | None = None
    preferred_study_days: tuple[str, ...] = field(default_factory=tuple)
    reminder_enabled: bool = False
    quiet_hours_label: str = ""

    @classmethod
    def create(
        cls,
        *,
        preferred_session_minutes: int | None = None,
        preferred_study_days: list[str] | tuple[str, ...] | None = None,
        reminder_enabled: bool = False,
        quiet_hours_label: str = "",
    ) -> StudyPreferences:
        minutes = preferred_session_minutes
        if minutes is not None and minutes < 0:
            raise ValueError("preferred_session_minutes must be non-negative")
        return cls(
            preferred_session_minutes=minutes,
            preferred_study_days=tuple(
                d.strip() for d in (preferred_study_days or ()) if str(d).strip()
            ),
            reminder_enabled=bool(reminder_enabled),
            quiet_hours_label=(quiet_hours_label or "").strip(),
        )


@dataclass(frozen=True)
class LearningStatistics:
    """Aggregated learning statistics for profile surfaces."""

    total_study_minutes: int = 0
    sessions_completed: int = 0
    topics_mastered: int = 0
    current_exam_readiness: float | None = None
    study_streak_days: int = 0

    @classmethod
    def create(
        cls,
        *,
        total_study_minutes: int = 0,
        sessions_completed: int = 0,
        topics_mastered: int = 0,
        current_exam_readiness: float | None = None,
        study_streak_days: int = 0,
    ) -> LearningStatistics:
        if total_study_minutes < 0:
            raise ValueError("total_study_minutes must be non-negative")
        if sessions_completed < 0:
            raise ValueError("sessions_completed must be non-negative")
        if topics_mastered < 0:
            raise ValueError("topics_mastered must be non-negative")
        if study_streak_days < 0:
            raise ValueError("study_streak_days must be non-negative")
        readiness = current_exam_readiness
        if readiness is not None and not 0.0 <= readiness <= 1.0:
            raise ValueError("current_exam_readiness must be between 0 and 1")
        return cls(
            total_study_minutes=int(total_study_minutes),
            sessions_completed=int(sessions_completed),
            topics_mastered=int(topics_mastered),
            current_exam_readiness=readiness,
            study_streak_days=int(study_streak_days),
        )


@dataclass(frozen=True)
class LearningGoal:
    """One student learning goal."""

    goal_id: str
    title: str
    target_label: str = ""
    progress_ratio: float = 0.0

    @classmethod
    def create(
        cls,
        goal_id: str,
        title: str,
        *,
        target_label: str = "",
        progress_ratio: float = 0.0,
    ) -> LearningGoal:
        ratio = float(progress_ratio)
        if not 0.0 <= ratio <= 1.0:
            raise ValueError("progress_ratio must be between 0 and 1")
        return cls(
            goal_id=_require_non_empty(goal_id, "goal_id"),
            title=_require_non_empty(title, "title"),
            target_label=(target_label or "").strip(),
            progress_ratio=ratio,
        )


@dataclass(frozen=True)
class AccountSettings:
    """Account settings flags for profile surfaces (presentation only)."""

    email: str = ""
    notifications_enabled: bool = True
    locale: str = ""
    timezone: str = ""

    @classmethod
    def create(
        cls,
        *,
        email: str = "",
        notifications_enabled: bool = True,
        locale: str = "",
        timezone: str = "",
    ) -> AccountSettings:
        return cls(
            email=(email or "").strip().lower(),
            notifications_enabled=bool(notifications_enabled),
            locale=(locale or "").strip(),
            timezone=(timezone or "").strip(),
        )


@dataclass(frozen=True)
class ProfileProjection:
    """Domain projection for the Profile experience."""

    student_id: str
    display_name: str = ""
    examination_label: str = ""
    preferences: StudyPreferences = field(default_factory=StudyPreferences)
    statistics: LearningStatistics = field(default_factory=LearningStatistics)
    goals: tuple[LearningGoal, ...] = field(default_factory=tuple)
    account: AccountSettings = field(default_factory=AccountSettings)

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        display_name: str = "",
        examination_label: str = "",
        preferences: StudyPreferences | None = None,
        statistics: LearningStatistics | None = None,
        goals: list[LearningGoal] | tuple[LearningGoal, ...] | None = None,
        account: AccountSettings | None = None,
    ) -> ProfileProjection:
        return cls(
            student_id=_require_non_empty(student_id, "student_id"),
            display_name=(display_name or "").strip(),
            examination_label=(examination_label or "").strip(),
            preferences=preferences or StudyPreferences.create(),
            statistics=statistics or LearningStatistics.create(),
            goals=tuple(goals or ()),
            account=account or AccountSettings.create(),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
