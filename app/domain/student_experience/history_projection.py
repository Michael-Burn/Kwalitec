"""History projection — accomplished learning without raw event logs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CompletedSessionCard:
    """One completed learning session for history surfaces."""

    session_id: str
    topic_title: str
    completed_at: str = ""
    study_minutes: int = 0

    @classmethod
    def create(
        cls,
        session_id: str,
        topic_title: str,
        *,
        completed_at: str = "",
        study_minutes: int = 0,
    ) -> CompletedSessionCard:
        if study_minutes < 0:
            raise ValueError("study_minutes must be non-negative")
        return cls(
            session_id=_require_non_empty(session_id, "session_id"),
            topic_title=_require_non_empty(topic_title, "topic_title"),
            completed_at=(completed_at or "").strip(),
            study_minutes=int(study_minutes),
        )


@dataclass(frozen=True)
class ReadinessPoint:
    """One readiness progression sample for history charts."""

    recorded_at: str
    exam_readiness: float
    label: str = ""

    @classmethod
    def create(
        cls,
        recorded_at: str,
        exam_readiness: float,
        *,
        label: str = "",
    ) -> ReadinessPoint:
        score = float(exam_readiness)
        if not 0.0 <= score <= 1.0:
            raise ValueError("exam_readiness must be between 0 and 1")
        return cls(
            recorded_at=_require_non_empty(recorded_at, "recorded_at"),
            exam_readiness=score,
            label=(label or "").strip(),
        )


@dataclass(frozen=True)
class AchievementCard:
    """Recent achievement for history surfaces."""

    achievement_id: str
    title: str
    earned_at: str = ""
    description: str = ""

    @classmethod
    def create(
        cls,
        achievement_id: str,
        title: str,
        *,
        earned_at: str = "",
        description: str = "",
    ) -> AchievementCard:
        return cls(
            achievement_id=_require_non_empty(achievement_id, "achievement_id"),
            title=_require_non_empty(title, "title"),
            earned_at=(earned_at or "").strip(),
            description=(description or "").strip(),
        )


@dataclass(frozen=True)
class HistoryProjection:
    """Domain projection for the History experience.

    Presents completed sessions, study time, readiness progression,
    mastered topics, revision history, and achievements — never raw logs.
    """

    student_id: str
    completed_sessions: tuple[CompletedSessionCard, ...] = field(
        default_factory=tuple
    )
    total_study_minutes: int = 0
    readiness_progression: tuple[ReadinessPoint, ...] = field(
        default_factory=tuple
    )
    mastered_topics: tuple[str, ...] = field(default_factory=tuple)
    revision_history: tuple[str, ...] = field(default_factory=tuple)
    recent_achievements: tuple[AchievementCard, ...] = field(
        default_factory=tuple
    )

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        completed_sessions: (
            list[CompletedSessionCard] | tuple[CompletedSessionCard, ...] | None
        ) = None,
        total_study_minutes: int | None = None,
        readiness_progression: (
            list[ReadinessPoint] | tuple[ReadinessPoint, ...] | None
        ) = None,
        mastered_topics: list[str] | tuple[str, ...] | None = None,
        revision_history: list[str] | tuple[str, ...] | None = None,
        recent_achievements: (
            list[AchievementCard] | tuple[AchievementCard, ...] | None
        ) = None,
    ) -> HistoryProjection:
        sessions = tuple(completed_sessions or ())
        if total_study_minutes is None:
            minutes = sum(s.study_minutes for s in sessions)
        else:
            minutes = int(total_study_minutes)
            if minutes < 0:
                raise ValueError("total_study_minutes must be non-negative")
        return cls(
            student_id=_require_non_empty(student_id, "student_id"),
            completed_sessions=sessions,
            total_study_minutes=minutes,
            readiness_progression=tuple(readiness_progression or ()),
            mastered_topics=tuple(
                t.strip() for t in (mastered_topics or ()) if str(t).strip()
            ),
            revision_history=tuple(
                r.strip() for r in (revision_history or ()) if str(r).strip()
            ),
            recent_achievements=tuple(recent_achievements or ()),
        )

    @property
    def session_count(self) -> int:
        return len(self.completed_sessions)

    @property
    def mastered_count(self) -> int:
        return len(self.mastered_topics)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
