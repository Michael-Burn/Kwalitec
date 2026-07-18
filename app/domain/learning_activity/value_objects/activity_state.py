"""Activity lifecycle posture for a Learning Activity.

Canonical transitions::

    NOT_STARTED → ACTIVE → PAUSED ⇄ ACTIVE → COMPLETED
    NOT_STARTED | ACTIVE | PAUSED → SKIPPED

Terminal states: COMPLETED, SKIPPED.
"""

from __future__ import annotations

from enum import StrEnum


class ActivityState(StrEnum):
    """Lifecycle posture of a Learning Activity.

    Terminal states: COMPLETED, SKIPPED.
    """

    NOT_STARTED = "not_started"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class ActivityTransitionEvent(StrEnum):
    """Named events for ActivityState transitions."""

    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    COMPLETE = "complete"
    SKIP = "skip"


LAWFUL_ACTIVITY_TRANSITIONS: dict[
    tuple[ActivityState, ActivityTransitionEvent], ActivityState
] = {
    (ActivityState.NOT_STARTED, ActivityTransitionEvent.START): ActivityState.ACTIVE,
    (ActivityState.NOT_STARTED, ActivityTransitionEvent.SKIP): ActivityState.SKIPPED,
    (ActivityState.ACTIVE, ActivityTransitionEvent.PAUSE): ActivityState.PAUSED,
    (ActivityState.ACTIVE, ActivityTransitionEvent.COMPLETE): ActivityState.COMPLETED,
    (ActivityState.ACTIVE, ActivityTransitionEvent.SKIP): ActivityState.SKIPPED,
    (ActivityState.PAUSED, ActivityTransitionEvent.RESUME): ActivityState.ACTIVE,
    (ActivityState.PAUSED, ActivityTransitionEvent.COMPLETE): ActivityState.COMPLETED,
    (ActivityState.PAUSED, ActivityTransitionEvent.SKIP): ActivityState.SKIPPED,
}


def next_activity_state(
    current: ActivityState,
    event: ActivityTransitionEvent,
) -> ActivityState | None:
    """Return the lawful next state, or None if the transition is invalid."""
    return LAWFUL_ACTIVITY_TRANSITIONS.get((current, event))


def is_terminal_activity_state(state: ActivityState) -> bool:
    """True when the activity may not resume educational work."""
    return state in {ActivityState.COMPLETED, ActivityState.SKIPPED}


def is_open_activity_state(state: ActivityState) -> bool:
    """True when the activity may still accept work (including not started)."""
    return not is_terminal_activity_state(state)
