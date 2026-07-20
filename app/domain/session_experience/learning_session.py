"""Learning Session — presentation handle for the focused study workflow.

References session / mission identities provided by upstream ports.
Never generates missions, stores evidence, or owns educational progression.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class LearningSessionStatus(StrEnum):
    """Presentation status of a Learning Session experience handle."""

    READY = "ready"
    OVERVIEW = "overview"
    IN_PROGRESS = "in_progress"
    REFLECTING = "reflecting"
    SUMMARIZING = "summarizing"
    COMPLETED = "completed"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class BeginSessionAction:
    """Student-facing call-to-action to begin the Learning Session."""

    label: str = "Begin Session"
    enabled: bool = True
    session_id: str | None = None
    mission_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        label: str = "Begin Session",
        enabled: bool = True,
        session_id: str | None = None,
        mission_id: str | None = None,
    ) -> BeginSessionAction:
        """Build a Begin Session action from port identities."""
        sid = None if session_id is None else str(session_id).strip() or None
        mid = None if mission_id is None else str(mission_id).strip() or None
        return cls(
            label=(label or "Begin Session").strip() or "Begin Session",
            enabled=bool(enabled),
            session_id=sid,
            mission_id=mid,
        )

    @property
    def can_begin(self) -> bool:
        """True when the action is enabled and has a session identity."""
        return self.enabled and bool(self.session_id)


@dataclass(frozen=True)
class LearningSession:
    """Presentation handle for one Learning Session study environment.

    Holds references and overview projection facts only.
    Educational execution belongs to Learning Session Runtime /
    Learning Activity Engine via application ports.
    """

    experience_session_id: str
    student_id: str
    session_id: str
    status: LearningSessionStatus = LearningSessionStatus.READY
    mission_id: str | None = None
    objective: str = ""
    learning_goal: str = ""
    estimated_minutes: int | None = None
    activity_count: int = 0
    topics: tuple[str, ...] = ()
    expected_readiness_improvement: float | None = None
    why_studying: str = ""
    begin_action: BeginSessionAction | None = None
    started_at: str = ""
    completed_at: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        experience_session_id: str,
        student_id: str,
        session_id: str,
        *,
        status: LearningSessionStatus | str = LearningSessionStatus.READY,
        mission_id: str | None = None,
        objective: str = "",
        learning_goal: str = "",
        estimated_minutes: int | None = None,
        activity_count: int = 0,
        topics: list[str] | tuple[str, ...] | None = None,
        expected_readiness_improvement: float | None = None,
        why_studying: str = "",
        begin_action: BeginSessionAction | None = None,
        started_at: str = "",
        completed_at: str = "",
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
    ) -> LearningSession:
        """Construct a Learning Session experience handle."""
        minutes = estimated_minutes
        if minutes is not None and minutes < 0:
            raise ValueError("estimated_minutes must be non-negative")
        if activity_count < 0:
            raise ValueError("activity_count must be non-negative")
        if (
            expected_readiness_improvement is not None
            and not -1.0 <= expected_readiness_improvement <= 1.0
        ):
            raise ValueError(
                "expected_readiness_improvement must be between -1 and 1"
            )
        sid = _require_non_empty(session_id, "session_id")
        action = begin_action or BeginSessionAction.create(
            enabled=True,
            session_id=sid,
            mission_id=mission_id,
        )
        cleaned_topics = tuple(
            t.strip() for t in (topics or ()) if isinstance(t, str) and t.strip()
        )
        return cls(
            experience_session_id=_require_non_empty(
                experience_session_id, "experience_session_id"
            ),
            student_id=_require_non_empty(student_id, "student_id"),
            session_id=sid,
            status=_resolve_status(status),
            mission_id=(
                None if mission_id is None else str(mission_id).strip() or None
            ),
            objective=(objective or "").strip(),
            learning_goal=(learning_goal or "").strip(),
            estimated_minutes=minutes,
            activity_count=int(activity_count),
            topics=cleaned_topics,
            expected_readiness_improvement=expected_readiness_improvement,
            why_studying=(why_studying or "").strip(),
            begin_action=action,
            started_at=(started_at or "").strip(),
            completed_at=(completed_at or "").strip(),
            metadata=tuple(metadata or ()),
        )

    @property
    def can_begin(self) -> bool:
        """True when Begin Session is actionable."""
        return bool(self.begin_action and self.begin_action.can_begin)

    @property
    def topic_count(self) -> int:
        """Number of topics listed for this session."""
        return len(self.topics)

    def with_status(self, status: LearningSessionStatus | str) -> LearningSession:
        """Return a copy with updated status."""
        return LearningSession(
            experience_session_id=self.experience_session_id,
            student_id=self.student_id,
            session_id=self.session_id,
            status=_resolve_status(status),
            mission_id=self.mission_id,
            objective=self.objective,
            learning_goal=self.learning_goal,
            estimated_minutes=self.estimated_minutes,
            activity_count=self.activity_count,
            topics=self.topics,
            expected_readiness_improvement=self.expected_readiness_improvement,
            why_studying=self.why_studying,
            begin_action=self.begin_action,
            started_at=self.started_at,
            completed_at=self.completed_at,
            metadata=self.metadata,
        )


def _resolve_status(
    value: LearningSessionStatus | str,
) -> LearningSessionStatus:
    if isinstance(value, LearningSessionStatus):
        return value
    return LearningSessionStatus(str(value).strip().lower())


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
