"""Immutable JourneyEvent contracts (P2-MS003–P2-MS005).

Experience Layer transitions only. Events never trigger educational
recalculation, persistence, or Programme I engine calls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.application.unified_journey.contracts import CONTRACT_VERSION
from app.application.unified_journey.stages import (
    JourneyStage,
    resolve_journey_stage,
)


class JourneyEventType(StrEnum):
    """Canonical Experience transition identifiers."""

    MISSION_STARTED = "mission_started"
    MISSION_COMPLETED = "mission_completed"
    REFLECTION_AVAILABLE = "reflection_available"
    WEEKLY_REVIEW_AVAILABLE = "weekly_review_available"
    # P2-MS004 guided study session (presentation only).
    SESSION_STARTED = "session_started"
    SESSION_RESUMED = "session_resumed"
    SESSION_COMPLETED = "session_completed"
    WRAP_UP_STARTED = "wrap_up_started"
    # P2-MS005 guided reflection (presentation only).
    REFLECTION_STARTED = "reflection_started"
    REFLECTION_COMPLETED = "reflection_completed"
    REFLECTION_SKIPPED = "reflection_skipped"


JOURNEY_EVENT_TYPES = frozenset(JourneyEventType)


@dataclass(frozen=True)
class JourneyEvent:
    """Immutable Experience transition record.

    Represents UI / journey-stage transitions only. Must never trigger
    educational recalculation or mutate Programme I outputs.
    """

    event_type: JourneyEventType
    stage: JourneyStage = JourneyStage.DAILY_MISSION
    message: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "event_type", _resolve_event_type(self.event_type)
        )
        object.__setattr__(self, "stage", resolve_journey_stage(self.stage))
        object.__setattr__(self, "message", (self.message or "").strip())


def mission_started(
    *,
    stage: JourneyStage | str = JourneyStage.DAILY_MISSION,
    message: str = "Mission started",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: student began today's mission."""
    return JourneyEvent(
        event_type=JourneyEventType.MISSION_STARTED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def mission_completed(
    *,
    stage: JourneyStage | str = JourneyStage.DAILY_MISSION,
    message: str = "Mission completed",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: student finished today's mission (UI only)."""
    return JourneyEvent(
        event_type=JourneyEventType.MISSION_COMPLETED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def reflection_available(
    *,
    stage: JourneyStage | str = JourneyStage.SESSION_REFLECTION,
    message: str = "Reflection is available",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: reflection surface is ready."""
    return JourneyEvent(
        event_type=JourneyEventType.REFLECTION_AVAILABLE,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def weekly_review_available(
    *,
    stage: JourneyStage | str = JourneyStage.WEEKLY_REVIEW,
    message: str = "Weekly review is available",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: weekly review surface is ready."""
    return JourneyEvent(
        event_type=JourneyEventType.WEEKLY_REVIEW_AVAILABLE,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def session_started(
    *,
    stage: JourneyStage | str = JourneyStage.STUDY_SESSION,
    message: str = "Study session started",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: guided session entered Studying (UI only)."""
    return JourneyEvent(
        event_type=JourneyEventType.SESSION_STARTED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def session_resumed(
    *,
    stage: JourneyStage | str = JourneyStage.STUDY_SESSION,
    message: str = "Study session resumed",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: guided session resumed Studying (UI only)."""
    return JourneyEvent(
        event_type=JourneyEventType.SESSION_RESUMED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def session_completed(
    *,
    stage: JourneyStage | str = JourneyStage.STUDY_SESSION,
    message: str = "Study session completed",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: guided session reached Complete (UI only)."""
    return JourneyEvent(
        event_type=JourneyEventType.SESSION_COMPLETED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def wrap_up_started(
    *,
    stage: JourneyStage | str = JourneyStage.STUDY_SESSION,
    message: str = "Wrapping up study session",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: guided session entered Wrapping Up (UI only)."""
    return JourneyEvent(
        event_type=JourneyEventType.WRAP_UP_STARTED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def reflection_started(
    *,
    stage: JourneyStage | str = JourneyStage.SESSION_REFLECTION,
    message: str = "Reflection started",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: Guided Reflection entered In Progress (UI only)."""
    return JourneyEvent(
        event_type=JourneyEventType.REFLECTION_STARTED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def reflection_completed(
    *,
    stage: JourneyStage | str = JourneyStage.SESSION_REFLECTION,
    message: str = "Reflection completed",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: Guided Reflection reached Completed (UI only)."""
    return JourneyEvent(
        event_type=JourneyEventType.REFLECTION_COMPLETED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def reflection_skipped(
    *,
    stage: JourneyStage | str = JourneyStage.SESSION_REFLECTION,
    message: str = "Reflection skipped",
    metadata: tuple[tuple[str, str], ...] = (),
) -> JourneyEvent:
    """Experience transition: Guided Reflection skipped (UI only)."""
    return JourneyEvent(
        event_type=JourneyEventType.REFLECTION_SKIPPED,
        stage=resolve_journey_stage(stage),
        message=message,
        metadata=metadata,
    )


def event_for_completion_status(
    completion_status: str,
    *,
    stage: JourneyStage | str = JourneyStage.DAILY_MISSION,
) -> JourneyEvent | None:
    """Map a presentation completion status to a JourneyEvent (no side effects).

    Returns None when the status does not imply a transition event.
    """
    status = (completion_status or "").strip().lower()
    if status == "in_progress":
        return mission_started(stage=stage)
    if status in {"complete", "completed"}:
        return mission_completed(stage=stage)
    return None


def event_for_session_phase(
    phase: str,
    *,
    previous_phase: str | None = None,
    stage: JourneyStage | str = JourneyStage.STUDY_SESSION,
) -> JourneyEvent | None:
    """Map a presentation phase change onto a JourneyEvent (pure, no side effects).

    Returns None when the phase alone does not imply a transition event.
    """
    current = (phase or "").strip().lower()
    previous = (previous_phase or "").strip().lower() if previous_phase else ""
    if current == "studying" and previous in {"", "ready"}:
        return session_started(stage=stage)
    if current == "studying" and previous in {"wrapping_up", "complete"}:
        return session_resumed(stage=stage)
    if current == "wrapping_up":
        return wrap_up_started(stage=stage)
    if current == "complete":
        return session_completed(stage=stage)
    return None


def event_for_reflection_state(
    state: str,
    *,
    previous_state: str | None = None,
    stage: JourneyStage | str = JourneyStage.SESSION_REFLECTION,
) -> JourneyEvent | None:
    """Map a presentation reflection-state change onto a JourneyEvent.

    Pure helper — no side effects. Returns None when no transition applies.
    """
    current = (state or "").strip().lower()
    previous = (previous_state or "").strip().lower() if previous_state else ""
    if current == "in_progress" and previous in {"", "available"}:
        return reflection_started(stage=stage)
    if current == "completed":
        return reflection_completed(stage=stage)
    if current == "skipped":
        return reflection_skipped(stage=stage)
    if current == "available" and previous in {"", "wrapping_up", "complete"}:
        return reflection_available(stage=stage)
    return None


def _resolve_event_type(value: JourneyEventType | str) -> JourneyEventType:
    if isinstance(value, JourneyEventType):
        return value
    normalized = (value or "").strip().lower()
    try:
        return JourneyEventType(normalized)
    except ValueError as exc:
        raise ValueError(f"unknown journey event type: {value!r}") from exc
