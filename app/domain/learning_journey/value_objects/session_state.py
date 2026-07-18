"""Session lifecycle posture for a Learning Session.

Canonical states align with ``knowledge/version2/STATE_MACHINE.md``.

Brief vocabulary mapping (examples only):
- PLANNED → NOT_STARTED
- IN_PROGRESS → ACTIVE
- SKIPPED → cancel of a planned session without completing work
"""

from __future__ import annotations

from enum import StrEnum


class SessionState(StrEnum):
    """Lifecycle posture of a Learning Session.

    Terminal states: COMPLETED, ABANDONED, SKIPPED.
    """

    NOT_STARTED = "not_started"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    SKIPPED = "skipped"


class SessionTransitionEvent(StrEnum):
    """Named events for SessionState transitions."""

    START_SESSION = "start_session"
    PAUSE_SESSION = "pause_session"
    RESUME_SESSION = "resume_session"
    FINISH_SESSION = "finish_session"
    ABANDON_SESSION = "abandon_session"
    SKIP_SESSION = "skip_session"
    CAPTURE_REFLECTION = "capture_reflection"


LAWFUL_SESSION_TRANSITIONS: dict[
    tuple[SessionState, SessionTransitionEvent], SessionState
] = {
    (
        SessionState.NOT_STARTED,
        SessionTransitionEvent.START_SESSION,
    ): SessionState.ACTIVE,
    (
        SessionState.NOT_STARTED,
        SessionTransitionEvent.ABANDON_SESSION,
    ): SessionState.ABANDONED,
    (
        SessionState.NOT_STARTED,
        SessionTransitionEvent.SKIP_SESSION,
    ): SessionState.SKIPPED,
    (
        SessionState.ACTIVE,
        SessionTransitionEvent.PAUSE_SESSION,
    ): SessionState.PAUSED,
    (
        SessionState.ACTIVE,
        SessionTransitionEvent.FINISH_SESSION,
    ): SessionState.COMPLETED,
    (
        SessionState.ACTIVE,
        SessionTransitionEvent.ABANDON_SESSION,
    ): SessionState.ABANDONED,
    (
        SessionState.PAUSED,
        SessionTransitionEvent.RESUME_SESSION,
    ): SessionState.ACTIVE,
    (
        SessionState.PAUSED,
        SessionTransitionEvent.FINISH_SESSION,
    ): SessionState.COMPLETED,
    (
        SessionState.PAUSED,
        SessionTransitionEvent.ABANDON_SESSION,
    ): SessionState.ABANDONED,
    # Reflection capture keeps COMPLETED; posture lives on JourneyReflection.
    (
        SessionState.COMPLETED,
        SessionTransitionEvent.CAPTURE_REFLECTION,
    ): SessionState.COMPLETED,
}


def next_session_state(
    current: SessionState,
    event: SessionTransitionEvent,
) -> SessionState | None:
    """Return the lawful next state, or None if the transition is invalid."""
    return LAWFUL_SESSION_TRANSITIONS.get((current, event))


def is_terminal_session_state(state: SessionState) -> bool:
    """True when the session may not resume educational work."""
    return state in {
        SessionState.COMPLETED,
        SessionState.ABANDONED,
        SessionState.SKIPPED,
    }
