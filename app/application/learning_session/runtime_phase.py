"""Runtime lifecycle phase for a Learning Session.

Application vocabulary used by the Learning Session Runtime. Maps onto
domain ``SessionState`` without forking educational meaning:

- PLANNED  → NOT_STARTED (created, not yet prepared)
- READY    → NOT_STARTED (prepared; lawful to start)
- ACTIVE   → ACTIVE
- PAUSED   → PAUSED
- READY_TO_FINISH → ACTIVE or PAUSED (finish review entered; not completed)
- COMPLETED → COMPLETED
- ARCHIVED → COMPLETED (runtime archival; no further educational work)

Domain terminals ABANDONED / SKIPPED remain domain-only; the runtime
surfaces them via session_state without inventing parallel phases.

Product lifecycle (LXP-003 / SR-001A P2)::

    Created → Started → In Progress → Paused → Resumed
    → Ready to Finish → Completed
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
    READY_TO_FINISH = "ready_to_finish"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class RuntimeTransitionEvent(StrEnum):
    """Named events for RuntimePhase transitions."""

    PREPARE = "prepare"
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    REQUEST_FINISH = "request_finish"
    COMPLETE = "complete"
    ARCHIVE = "archive"


LAWFUL_RUNTIME_TRANSITIONS: dict[
    tuple[RuntimePhase, RuntimeTransitionEvent], RuntimePhase
] = {
    (RuntimePhase.PLANNED, RuntimeTransitionEvent.PREPARE): RuntimePhase.READY,
    (RuntimePhase.PLANNED, RuntimeTransitionEvent.START): RuntimePhase.ACTIVE,
    (RuntimePhase.READY, RuntimeTransitionEvent.START): RuntimePhase.ACTIVE,
    (RuntimePhase.ACTIVE, RuntimeTransitionEvent.PAUSE): RuntimePhase.PAUSED,
    (RuntimePhase.ACTIVE, RuntimeTransitionEvent.REQUEST_FINISH): (
        RuntimePhase.READY_TO_FINISH
    ),
    (RuntimePhase.ACTIVE, RuntimeTransitionEvent.COMPLETE): RuntimePhase.COMPLETED,
    (RuntimePhase.PAUSED, RuntimeTransitionEvent.RESUME): RuntimePhase.ACTIVE,
    (RuntimePhase.PAUSED, RuntimeTransitionEvent.REQUEST_FINISH): (
        RuntimePhase.READY_TO_FINISH
    ),
    (RuntimePhase.PAUSED, RuntimeTransitionEvent.COMPLETE): RuntimePhase.COMPLETED,
    (RuntimePhase.READY_TO_FINISH, RuntimeTransitionEvent.RESUME): RuntimePhase.ACTIVE,
    (RuntimePhase.READY_TO_FINISH, RuntimeTransitionEvent.COMPLETE): (
        RuntimePhase.COMPLETED
    ),
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
    ready_to_finish: bool = False,
) -> RuntimePhase:
    """Derive a RuntimePhase from domain SessionState plus runtime flags."""
    if archived and state == SessionState.COMPLETED:
        return RuntimePhase.ARCHIVED
    if ready_to_finish and state in {SessionState.ACTIVE, SessionState.PAUSED}:
        return RuntimePhase.READY_TO_FINISH
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


def product_lifecycle_label(phase: RuntimePhase) -> str:
    """Student-product lifecycle label for ``phase`` (LXP-003)."""
    return {
        RuntimePhase.PLANNED: "Created",
        RuntimePhase.READY: "Created",
        RuntimePhase.ACTIVE: "In Progress",
        RuntimePhase.PAUSED: "Paused",
        RuntimePhase.READY_TO_FINISH: "Ready to Finish",
        RuntimePhase.COMPLETED: "Completed",
        RuntimePhase.ARCHIVED: "Completed",
    }.get(phase, phase.value)
