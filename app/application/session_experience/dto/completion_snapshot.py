"""Immutable completion / summary DTOs for Learning Session Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReturnHomeActionSnapshot:
    """Read-only Return Home action."""

    label: str = "Return Home"
    enabled: bool = True


@dataclass(frozen=True)
class CompletionSnapshot:
    """Session summary / completion projection DTO."""

    session_id: str
    student_id: str
    topics_completed: tuple[str, ...] = ()
    topic_count: int = 0
    time_studied_minutes: int | None = None
    activities_completed: int = 0
    learning_insights: tuple[str, ...] = ()
    exam_readiness_change: float | None = None
    exam_readiness_change_label: str = ""
    next_recommendation: str = ""
    estimated_next_session_minutes: int | None = None
    return_home: ReturnHomeActionSnapshot | None = None
    has_readiness_change: bool = False
    can_return_home: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
