"""Mission lifecycle vocabulary for Mission Engine 2.0.

Scheduling / delivery vocabulary only. Educational progression remains in
the Learning Journey Engine; session execution remains in the Learning
Session Runtime.
"""

from __future__ import annotations

from enum import StrEnum


class MissionState(StrEnum):
    """Lifecycle posture of a scheduled mission."""

    SCHEDULED = "scheduled"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    DEFERRED = "deferred"
    SKIPPED = "skipped"
    MISSED = "missed"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class MissionSlot(StrEnum):
    """Deterministic schedule slot for a mission."""

    TODAY = "today"
    TOMORROW = "tomorrow"
    DEFERRED = "deferred"
    MISSED = "missed"
    REVISION = "revision"


class DeliveryAction(StrEnum):
    """Dashboard / adapter delivery action tags (not UI)."""

    TODAY = "today_mission"
    RESUME = "resume_mission"
    CONTINUE = "continue_mission"
    REVIEW = "review_mission"
    REVISION = "revision_mission"
    NONE = "none"


class MissionTransitionEvent(StrEnum):
    """Named events for MissionState transitions."""

    ACTIVATE = "activate"
    START = "start"
    COMPLETE = "complete"
    DEFER = "defer"
    SKIP = "skip"
    MISS = "miss"
    RESCHEDULE = "reschedule"
    ARCHIVE = "archive"


LAWFUL_MISSION_TRANSITIONS: dict[
    tuple[MissionState, MissionTransitionEvent], MissionState
] = {
    (MissionState.SCHEDULED, MissionTransitionEvent.ACTIVATE): MissionState.ACTIVE,
    (MissionState.SCHEDULED, MissionTransitionEvent.DEFER): MissionState.DEFERRED,
    (MissionState.SCHEDULED, MissionTransitionEvent.SKIP): MissionState.SKIPPED,
    (MissionState.SCHEDULED, MissionTransitionEvent.MISS): MissionState.MISSED,
    (MissionState.SCHEDULED, MissionTransitionEvent.RESCHEDULE): MissionState.SCHEDULED,
    (MissionState.ACTIVE, MissionTransitionEvent.START): MissionState.IN_PROGRESS,
    (MissionState.ACTIVE, MissionTransitionEvent.DEFER): MissionState.DEFERRED,
    (MissionState.ACTIVE, MissionTransitionEvent.SKIP): MissionState.SKIPPED,
    (MissionState.ACTIVE, MissionTransitionEvent.MISS): MissionState.MISSED,
    (MissionState.ACTIVE, MissionTransitionEvent.COMPLETE): MissionState.COMPLETED,
    (MissionState.ACTIVE, MissionTransitionEvent.RESCHEDULE): MissionState.SCHEDULED,
    (MissionState.IN_PROGRESS, MissionTransitionEvent.COMPLETE): MissionState.COMPLETED,
    (MissionState.IN_PROGRESS, MissionTransitionEvent.DEFER): MissionState.DEFERRED,
    (MissionState.IN_PROGRESS, MissionTransitionEvent.SKIP): MissionState.SKIPPED,
    (MissionState.DEFERRED, MissionTransitionEvent.ACTIVATE): MissionState.ACTIVE,
    (MissionState.DEFERRED, MissionTransitionEvent.RESCHEDULE): MissionState.SCHEDULED,
    (MissionState.DEFERRED, MissionTransitionEvent.SKIP): MissionState.SKIPPED,
    (MissionState.MISSED, MissionTransitionEvent.RESCHEDULE): MissionState.SCHEDULED,
    (MissionState.MISSED, MissionTransitionEvent.ACTIVATE): MissionState.ACTIVE,
    (MissionState.MISSED, MissionTransitionEvent.SKIP): MissionState.SKIPPED,
    (MissionState.COMPLETED, MissionTransitionEvent.ARCHIVE): MissionState.ARCHIVED,
}


def next_mission_state(
    current: MissionState,
    event: MissionTransitionEvent,
) -> MissionState | None:
    """Return the lawful next state, or None if the transition is invalid."""
    return LAWFUL_MISSION_TRANSITIONS.get((current, event))


def is_terminal_mission_state(state: MissionState) -> bool:
    """True when the mission may not resume scheduling work."""
    return state in {
        MissionState.SKIPPED,
        MissionState.COMPLETED,
        MissionState.ARCHIVED,
    }


def is_open_mission_state(state: MissionState) -> bool:
    """True when the mission still occupies schedule capacity."""
    return state in {
        MissionState.SCHEDULED,
        MissionState.ACTIVE,
        MissionState.IN_PROGRESS,
        MissionState.DEFERRED,
        MissionState.MISSED,
    }
