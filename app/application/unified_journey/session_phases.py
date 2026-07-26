"""Guided study session presentation phases and controls (P2-MS004).

Experience Layer states only. Transitions never trigger Runtime A,
Strategy, Adaptive, Evidence, Twin, or persistence.
"""

from __future__ import annotations

from enum import StrEnum

# Presentation phase vocabulary for the guided study session.
SESSION_PHASE_READY = "ready"
SESSION_PHASE_STUDYING = "studying"
SESSION_PHASE_WRAPPING_UP = "wrapping_up"
SESSION_PHASE_COMPLETE = "complete"
SESSION_PHASE_VALUES = frozenset(
    {
        SESSION_PHASE_READY,
        SESSION_PHASE_STUDYING,
        SESSION_PHASE_WRAPPING_UP,
        SESSION_PHASE_COMPLETE,
    }
)

# Presentation session-status labels (UI only).
SESSION_STATUS_LABELS: dict[str, str] = {
    SESSION_PHASE_READY: "Ready",
    SESSION_PHASE_STUDYING: "Studying",
    SESSION_PHASE_WRAPPING_UP: "Wrapping Up",
    SESSION_PHASE_COMPLETE: "Complete",
}

# Presentation elapsed-state vocabulary (no timers / clock math).
ELAPSED_NOT_STARTED = "not_started"
ELAPSED_IN_PROGRESS = "in_progress"
ELAPSED_ENDED = "ended"
ELAPSED_STATE_VALUES = frozenset(
    {
        ELAPSED_NOT_STARTED,
        ELAPSED_IN_PROGRESS,
        ELAPSED_ENDED,
        "",
    }
)


class SessionPhase(StrEnum):
    """Guided session Experience phases — presentation only."""

    READY = SESSION_PHASE_READY
    STUDYING = SESSION_PHASE_STUDYING
    WRAPPING_UP = SESSION_PHASE_WRAPPING_UP
    COMPLETE = SESSION_PHASE_COMPLETE


class SessionControl(StrEnum):
    """UI actions that update guided-session presentation state only."""

    START = "start"
    RESUME = "resume"
    FINISH = "finish"


SESSION_CONTROL_VALUES = frozenset(SessionControl)


def resolve_session_phase(value: SessionPhase | str) -> SessionPhase:
    """Resolve a session phase identifier; raises ``ValueError`` when unknown."""
    if isinstance(value, SessionPhase):
        return value
    key = (value or "").strip().lower()
    try:
        return SessionPhase(key)
    except ValueError as exc:
        raise ValueError(f"unknown session phase: {value!r}") from exc


def resolve_session_control(value: SessionControl | str) -> SessionControl:
    """Resolve a session control identifier; raises ``ValueError`` when unknown."""
    if isinstance(value, SessionControl):
        return value
    key = (value or "").strip().lower()
    try:
        return SessionControl(key)
    except ValueError as exc:
        raise ValueError(f"unknown session control: {value!r}") from exc


def session_status_label(phase: SessionPhase | str) -> str:
    """Student-facing status label for a presentation phase."""
    resolved = resolve_session_phase(phase)
    return SESSION_STATUS_LABELS[resolved.value]


def elapsed_state_for_phase(phase: SessionPhase | str) -> str:
    """Map presentation phase onto elapsed_state (no timing calculations)."""
    resolved = resolve_session_phase(phase)
    if resolved is SessionPhase.READY:
        return ELAPSED_NOT_STARTED
    if resolved is SessionPhase.STUDYING:
        return ELAPSED_IN_PROGRESS
    if resolved is SessionPhase.WRAPPING_UP:
        return ELAPSED_IN_PROGRESS
    return ELAPSED_ENDED
