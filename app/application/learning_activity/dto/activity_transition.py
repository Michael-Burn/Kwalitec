"""Immutable record of an activity lifecycle transition."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    ActivityTransitionEvent,
)


@dataclass(frozen=True)
class ActivityTransition:
    """Lawful transition applied to a Learning Activity.

    Attributes:
        activity_id: Activity that transitioned.
        session_id: Parent session identity.
        event: Named transition event.
        from_state: State before the transition.
        to_state: State after the transition.
    """

    activity_id: str
    session_id: str
    event: ActivityTransitionEvent
    from_state: ActivityState
    to_state: ActivityState
