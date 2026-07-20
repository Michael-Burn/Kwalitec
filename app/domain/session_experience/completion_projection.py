"""Completion / summary projection — close the session and return home.

Displays outcomes assembled from upstream ports. Never computes readiness,
recommendations, or journey progress independently.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReturnHomeAction:
    """Primary action after session completion — return to Student Home."""

    label: str = "Return Home"
    enabled: bool = True

    @classmethod
    def create(
        cls, *, label: str = "Return Home", enabled: bool = True
    ) -> ReturnHomeAction:
        return cls(
            label=(label or "Return Home").strip() or "Return Home",
            enabled=bool(enabled),
        )


@dataclass(frozen=True)
class CompletionProjection:
    """Domain projection for Session Summary and Complete surfaces.

    Home must already display updated readiness / recommendation /
    journey progress after completion — no refresh required on the
    experience side beyond returning to Home.
    """

    session_id: str
    student_id: str
    topics_completed: tuple[str, ...] = ()
    time_studied_minutes: int | None = None
    activities_completed: int = 0
    learning_insights: tuple[str, ...] = ()
    exam_readiness_change: float | None = None
    exam_readiness_change_label: str = ""
    next_recommendation: str = ""
    estimated_next_session_minutes: int | None = None
    return_home: ReturnHomeAction | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        session_id: str,
        student_id: str,
        *,
        topics_completed: list[str] | tuple[str, ...] | None = None,
        time_studied_minutes: int | None = None,
        activities_completed: int = 0,
        learning_insights: list[str] | tuple[str, ...] | None = None,
        exam_readiness_change: float | None = None,
        exam_readiness_change_label: str = "",
        next_recommendation: str = "",
        estimated_next_session_minutes: int | None = None,
        return_home: ReturnHomeAction | None = None,
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
    ) -> CompletionProjection:
        """Build a completion / summary projection from port facts."""
        if time_studied_minutes is not None and time_studied_minutes < 0:
            raise ValueError("time_studied_minutes must be non-negative")
        if activities_completed < 0:
            raise ValueError("activities_completed must be non-negative")
        if (
            estimated_next_session_minutes is not None
            and estimated_next_session_minutes < 0
        ):
            raise ValueError("estimated_next_session_minutes must be non-negative")
        if exam_readiness_change is not None and not (
            -1.0 <= exam_readiness_change <= 1.0
        ):
            raise ValueError("exam_readiness_change must be between -1 and 1")
        topics = tuple(
            t.strip()
            for t in (topics_completed or ())
            if isinstance(t, str) and t.strip()
        )
        insights = tuple(
            i.strip()
            for i in (learning_insights or ())
            if isinstance(i, str) and i.strip()
        )
        change_label = (exam_readiness_change_label or "").strip()
        if not change_label and exam_readiness_change is not None:
            change_label = readiness_change_label(exam_readiness_change)
        return cls(
            session_id=_require_non_empty(session_id, "session_id"),
            student_id=_require_non_empty(student_id, "student_id"),
            topics_completed=topics,
            time_studied_minutes=time_studied_minutes,
            activities_completed=int(activities_completed),
            learning_insights=insights,
            exam_readiness_change=exam_readiness_change,
            exam_readiness_change_label=change_label,
            next_recommendation=(next_recommendation or "").strip(),
            estimated_next_session_minutes=estimated_next_session_minutes,
            return_home=return_home or ReturnHomeAction.create(),
            metadata=tuple(metadata or ()),
        )

    @property
    def topic_count(self) -> int:
        """Number of topics completed in this session."""
        return len(self.topics_completed)

    @property
    def has_readiness_change(self) -> bool:
        """True when a readiness change fact is present."""
        return self.exam_readiness_change is not None

    @property
    def can_return_home(self) -> bool:
        """True when Return Home is actionable."""
        return bool(self.return_home and self.return_home.enabled)


def readiness_change_label(delta: float) -> str:
    """Map a readiness delta to a calm student-facing label."""
    if delta > 0.02:
        return "Exam readiness improved"
    if delta < -0.02:
        return "Exam readiness dipped slightly"
    return "Exam readiness steady"


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
