"""Runtime lifecycle phase for a Learning Session.

Application vocabulary used by the Learning Session Runtime. Maps onto
domain ``SessionState`` without forking educational meaning:

- PLANNED  → NOT_STARTED (created, not yet prepared)
- READY    → NOT_STARTED (prepared; lawful to start)
- ACTIVE   → ACTIVE
- PAUSED   → PAUSED
- COMPLETED → COMPLETED
- ARCHIVED → COMPLETED (runtime archival; no further educational work)

Domain terminals ABANDONED / SKIPPED remain domain-only; the runtime
surfaces them via session_state without inventing parallel phases.
"""

from __future__ import annotations

from enum import StrEnum

from app.domain.learning_journey.value_objects.session_state import SessionState


class RuntimePhase(StrEnum):
    """Lifecycle posture of a Learning Session at runtime."""

    PLANNED = "planned"
    READY = "ready"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class RuntimeTransitionEvent(StrEnum):
    """Named events for RuntimePhase transitions."""

    PREPARE = "prepare"
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    COMPLETE = "complete"
    ARCHIVE = "archive"


LAWFUL_RUNTIME_TRANSITIONS: dict[
    tuple[RuntimePhase, RuntimeTransitionEvent], RuntimePhase
] = {
    (RuntimePhase.PLANNED, RuntimeTransitionEvent.PREPARE): RuntimePhase.READY,
    (RuntimePhase.PLANNED, RuntimeTransitionEvent.START): RuntimePhase.ACTIVE,
    (RuntimePhase.READY, RuntimeTransitionEvent.START): RuntimePhase.ACTIVE,
    (RuntimePhase.ACTIVE, RuntimeTransitionEvent.PAUSE): RuntimePhase.PAUSED,
    (RuntimePhase.ACTIVE, RuntimeTransitionEvent.COMPLETE): RuntimePhase.COMPLETED,
    (RuntimePhase.PAUSED, RuntimeTransitionEvent.RESUME): RuntimePhase.ACTIVE,
    (RuntimePhase.PAUSED, RuntimeTransitionEvent.COMPLETE): RuntimePhase.COMPLETED,
    (RuntimePhase.COMPLETED, RuntimeTransitionEvent.ARCHIVE): RuntimePhase.ARCHIVED,
}


def next_runtime_phase(
    current: RuntimePhase,
    event: RuntimeTransitionEvent,
) -> RuntimePhase | None:
    """Return the lawful next phase, or None if the transition is invalid."""
    return LAWFUL_RUNTIME_TRANSITIONS.get((current, event))


def phase_from_session_state(
    state: SessionState,
    *,
    prepared: bool = False,
    archived: bool = False,
) -> RuntimePhase:
    """Derive a RuntimePhase from domain SessionState plus runtime flags."""
    if archived and state == SessionState.COMPLETED:
        return RuntimePhase.ARCHIVED
    if state == SessionState.ACTIVE:
        return RuntimePhase.ACTIVE
    if state == SessionState.PAUSED:
        return RuntimePhase.PAUSED
    if state == SessionState.COMPLETED:
        return RuntimePhase.COMPLETED
    if state == SessionState.NOT_STARTED:
        return RuntimePhase.READY if prepared else RuntimePhase.PLANNED
    # ABANDONED / SKIPPED: treat as archived educationally at runtime.
    return RuntimePhase.ARCHIVED


def is_terminal_runtime_phase(phase: RuntimePhase) -> bool:
    """True when the session may not resume educational work."""
    return phase in {RuntimePhase.COMPLETED, RuntimePhase.ARCHIVED}
