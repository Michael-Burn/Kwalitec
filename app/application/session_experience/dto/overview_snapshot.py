"""Immutable overview / session DTOs for Learning Session Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BeginSessionActionSnapshot:
    """Read-only Begin Session action."""

    label: str = "Begin Session"
    enabled: bool = True
    can_begin: bool = False
    session_id: str | None = None
    mission_id: str | None = None


@dataclass(frozen=True)
class OverviewSnapshot:
    """Session Overview projection DTO."""

    experience_session_id: str
    student_id: str
    session_id: str
    status: str = "ready"
    objective: str = ""
    learning_goal: str = ""
    estimated_minutes: int | None = None
    activity_count: int = 0
    topics: tuple[str, ...] = ()
    topic_count: int = 0
    expected_readiness_improvement: float | None = None
    why_studying: str = ""
    begin_action: BeginSessionActionSnapshot | None = None
    can_begin: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
