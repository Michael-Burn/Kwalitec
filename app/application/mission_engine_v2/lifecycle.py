"""Mission lifecycle vocabulary for Mission Engine 2.0.

Applies only to the mission wrapper. Educational progression remains in
the Learning Journey Engine; session execution remains in the Learning
Session Runtime.
"""

from __future__ import annotations

from enum import StrEnum


class MissionState(StrEnum):
    """Lifecycle posture of a mission wrapper."""

    PLANNED = "planned"
    READY = "ready"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class MissionSlot(StrEnum):
    """Deterministic schedule slot for a mission."""

    TODAY = "today"
    DEFERRED = "deferred"
    REVISION = "revision"
    MISSED = "missed"
    FUTURE = "future"


class DispatchAction(StrEnum):
    """Dashboard / API dispatch action tags (not UI)."""

    TODAY = "today_mission"
    RESUME = "resume_mission"
    CONTINUE = "continue_mission"
    REVIEW = "review_mission"
    REVISION = "revision_mission"
    DEFERRED = "deferred_mission"
    NONE = "none"


class MissionTransitionEvent(StrEnum):
    """Named events for MissionState transitions."""

    PREPARE = "prepare"
    ACTIVATE = "activate"
    PAUSE = "pause"
    RESUME = "resume"
    COMPLETE = "complete"
    ARCHIVE = "archive"


LAWFUL_MISSION_TRANSITIONS: dict[
    tuple[MissionState, MissionTransitionEvent], MissionState
] = {
    (MissionState.PLANNED, MissionTransitionEvent.PREPARE): MissionState.READY,
    (MissionState.PLANNED, MissionTransitionEvent.ACTIVATE): MissionState.ACTIVE,
    (MissionState.READY, MissionTransitionEvent.ACTIVATE): MissionState.ACTIVE,
    (MissionState.ACTIVE, MissionTransitionEvent.PAUSE): MissionState.PAUSED,
    (MissionState.ACTIVE, MissionTransitionEvent.COMPLETE): MissionState.COMPLETED,
    (MissionState.PAUSED, MissionTransitionEvent.RESUME): MissionState.ACTIVE,
    (MissionState.PAUSED, MissionTransitionEvent.COMPLETE): MissionState.COMPLETED,
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
    return state in {MissionState.COMPLETED, MissionState.ARCHIVED}


def is_open_mission_state(state: MissionState) -> bool:
    """True when the mission still occupies schedule capacity."""
    return state in {
        MissionState.PLANNED,
        MissionState.READY,
        MissionState.ACTIVE,
        MissionState.PAUSED,
    }


def is_active_mission_state(state: MissionState) -> bool:
    """True when the mission occupies the single active slot."""
    return state in {MissionState.ACTIVE, MissionState.PAUSED}
