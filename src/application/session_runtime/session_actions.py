"""Lawful session actions and stage transition table.

Actions are lifecycle operations only. They never encode educational decisions
about what to study next — only how the runner advances through fixed stages.
"""

from __future__ import annotations

from enum import StrEnum

from application.session_runtime.session_state import SessionStage

# Linear guided-session stage order (excludes terminal COMPLETED for advance).
STAGE_ORDER: tuple[SessionStage, ...] = (
    SessionStage.NOT_STARTED,
    SessionStage.PREPARING,
    SessionStage.LEARNING,
    SessionStage.WORKED_EXAMPLE,
    SessionStage.NOTES,
    SessionStage.REFLECTION,
    SessionStage.COMPLETED,
)

ACTIVE_STAGES: frozenset[SessionStage] = frozenset(
    {
        SessionStage.PREPARING,
        SessionStage.LEARNING,
        SessionStage.WORKED_EXAMPLE,
        SessionStage.NOTES,
        SessionStage.REFLECTION,
    }
)


class SessionAction(StrEnum):
    """Public lifecycle operations on ``SessionRuntime``."""

    START = "start"
    ADVANCE = "advance"
    PAUSE = "pause"
    RESUME = "resume"
    COMPLETE = "complete"
    CANCEL = "cancel"


def next_stage(stage: SessionStage) -> SessionStage | None:
    """Return the next stage in ``STAGE_ORDER``, or None at the end."""
    try:
        index = STAGE_ORDER.index(stage)
    except ValueError:
        return None
    if index >= len(STAGE_ORDER) - 1:
        return None
    return STAGE_ORDER[index + 1]


def previous_stage(stage: SessionStage) -> SessionStage | None:
    """Return the previous stage in ``STAGE_ORDER``, or None at the start."""
    try:
        index = STAGE_ORDER.index(stage)
    except ValueError:
        return None
    if index <= 0:
        return None
    return STAGE_ORDER[index - 1]


def stage_index(stage: SessionStage) -> int:
    """Return the zero-based index of ``stage`` in ``STAGE_ORDER``."""
    return STAGE_ORDER.index(stage)
