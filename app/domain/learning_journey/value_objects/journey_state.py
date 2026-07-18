"""Journey lifecycle posture for a Learning Journey.

Canonical states align with ``knowledge/version2/STATE_MACHINE.md``.
``ARCHIVED`` is an implementation retention posture after a terminal outcome.
"""

from __future__ import annotations

from enum import StrEnum


class JourneyState(StrEnum):
    """Lifecycle posture of a Learning Journey.

    Terminal states: COMPLETED, ABANDONED, ARCHIVED.
    Pause and deferral are not completion.
    """

    NOT_STARTED = "not_started"
    ACTIVE = "active"
    PAUSED = "paused"
    RESUMED = "resumed"
    READY_FOR_COMPLETION = "ready_for_completion"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    ABANDONED = "abandoned"
    ARCHIVED = "archived"


# Events that drive lawful JourneyState transitions (STATE_MACHINE §2).
class JourneyTransitionEvent(StrEnum):
    """Named events for JourneyState transitions."""

    START_JOURNEY = "start_journey"
    PAUSE_JOURNEY = "pause_journey"
    RESUME_JOURNEY = "resume_journey"
    SETTLE_ACTIVE = "settle_active"
    COMPLETION_CRITERIA_MET = "completion_criteria_met"
    CONFIRM_TOPIC_COMPLETE = "confirm_topic_complete"
    CONTINUE_JOURNEY = "continue_journey"
    DEFER_JOURNEY = "defer_journey"
    ABANDON_JOURNEY = "abandon_journey"
    REACTIVATE_JOURNEY = "reactivate_journey"
    ARCHIVE_JOURNEY = "archive_journey"


# (from_state, event) → to_state — authoritative lawful map for domain validation.
LAWFUL_JOURNEY_TRANSITIONS: dict[
    tuple[JourneyState, JourneyTransitionEvent], JourneyState
] = {
    (
        JourneyState.NOT_STARTED,
        JourneyTransitionEvent.START_JOURNEY,
    ): JourneyState.ACTIVE,
    (
        JourneyState.NOT_STARTED,
        JourneyTransitionEvent.DEFER_JOURNEY,
    ): JourneyState.DEFERRED,
    (
        JourneyState.NOT_STARTED,
        JourneyTransitionEvent.ABANDON_JOURNEY,
    ): JourneyState.ABANDONED,
    (
        JourneyState.ACTIVE,
        JourneyTransitionEvent.PAUSE_JOURNEY,
    ): JourneyState.PAUSED,
    (
        JourneyState.ACTIVE,
        JourneyTransitionEvent.COMPLETION_CRITERIA_MET,
    ): JourneyState.READY_FOR_COMPLETION,
    (
        JourneyState.ACTIVE,
        JourneyTransitionEvent.DEFER_JOURNEY,
    ): JourneyState.DEFERRED,
    (
        JourneyState.ACTIVE,
        JourneyTransitionEvent.ABANDON_JOURNEY,
    ): JourneyState.ABANDONED,
    (
        JourneyState.PAUSED,
        JourneyTransitionEvent.RESUME_JOURNEY,
    ): JourneyState.RESUMED,
    (
        JourneyState.PAUSED,
        JourneyTransitionEvent.DEFER_JOURNEY,
    ): JourneyState.DEFERRED,
    (
        JourneyState.PAUSED,
        JourneyTransitionEvent.ABANDON_JOURNEY,
    ): JourneyState.ABANDONED,
    (
        JourneyState.RESUMED,
        JourneyTransitionEvent.SETTLE_ACTIVE,
    ): JourneyState.ACTIVE,
    (
        JourneyState.RESUMED,
        JourneyTransitionEvent.PAUSE_JOURNEY,
    ): JourneyState.PAUSED,
    (
        JourneyState.RESUMED,
        JourneyTransitionEvent.COMPLETION_CRITERIA_MET,
    ): JourneyState.READY_FOR_COMPLETION,
    (
        JourneyState.RESUMED,
        JourneyTransitionEvent.ABANDON_JOURNEY,
    ): JourneyState.ABANDONED,
    (
        JourneyState.READY_FOR_COMPLETION,
        JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE,
    ): JourneyState.COMPLETED,
    (
        JourneyState.READY_FOR_COMPLETION,
        JourneyTransitionEvent.CONTINUE_JOURNEY,
    ): JourneyState.ACTIVE,
    (
        JourneyState.READY_FOR_COMPLETION,
        JourneyTransitionEvent.PAUSE_JOURNEY,
    ): JourneyState.PAUSED,
    (
        JourneyState.READY_FOR_COMPLETION,
        JourneyTransitionEvent.ABANDON_JOURNEY,
    ): JourneyState.ABANDONED,
    (
        JourneyState.DEFERRED,
        JourneyTransitionEvent.REACTIVATE_JOURNEY,
    ): JourneyState.ACTIVE,
    (
        JourneyState.DEFERRED,
        JourneyTransitionEvent.ABANDON_JOURNEY,
    ): JourneyState.ABANDONED,
    (
        JourneyState.COMPLETED,
        JourneyTransitionEvent.ARCHIVE_JOURNEY,
    ): JourneyState.ARCHIVED,
    (
        JourneyState.ABANDONED,
        JourneyTransitionEvent.ARCHIVE_JOURNEY,
    ): JourneyState.ARCHIVED,
}


def next_journey_state(
    current: JourneyState,
    event: JourneyTransitionEvent,
) -> JourneyState | None:
    """Return the lawful next state, or None if the transition is invalid."""
    return LAWFUL_JOURNEY_TRANSITIONS.get((current, event))


def is_terminal_journey_state(state: JourneyState) -> bool:
    """True when the journey may not transition to further educational work."""
    return state in {
        JourneyState.COMPLETED,
        JourneyState.ABANDONED,
        JourneyState.ARCHIVED,
    }
