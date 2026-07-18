"""Ingestion lifecycle states for curriculum document processing.

Lifecycle only — extraction / normalisation / validation gates.
No teaching, no activity or session generation.
"""

from __future__ import annotations

from enum import StrEnum


class IngestionState(StrEnum):
    """Lifecycle posture of an ingestion job.

    Forward pipeline ends at COMPLETED.
    Terminal failure state: FAILED.
    """

    RECEIVED = "received"
    CLASSIFIED = "classified"
    EXTRACTED = "extracted"
    NORMALIZED = "normalized"
    VALIDATED = "validated"
    PREVIEW_READY = "preview_ready"
    COMPLETED = "completed"
    FAILED = "failed"


class IngestionTransitionEvent(StrEnum):
    """Named events for IngestionState transitions."""

    MARK_CLASSIFIED = "mark_classified"
    MARK_EXTRACTED = "mark_extracted"
    MARK_NORMALIZED = "mark_normalized"
    MARK_VALIDATED = "mark_validated"
    MARK_PREVIEW_READY = "mark_preview_ready"
    MARK_COMPLETED = "mark_completed"
    MARK_FAILED = "mark_failed"
    RESET_TO_RECEIVED = "reset_to_received"


# (from_state, event) → to_state — authoritative lawful map.
LAWFUL_INGESTION_TRANSITIONS: dict[
    tuple[IngestionState, IngestionTransitionEvent], IngestionState
] = {
    (
        IngestionState.RECEIVED,
        IngestionTransitionEvent.MARK_CLASSIFIED,
    ): IngestionState.CLASSIFIED,
    (
        IngestionState.RECEIVED,
        IngestionTransitionEvent.MARK_FAILED,
    ): IngestionState.FAILED,
    (
        IngestionState.CLASSIFIED,
        IngestionTransitionEvent.MARK_EXTRACTED,
    ): IngestionState.EXTRACTED,
    (
        IngestionState.CLASSIFIED,
        IngestionTransitionEvent.MARK_FAILED,
    ): IngestionState.FAILED,
    (
        IngestionState.EXTRACTED,
        IngestionTransitionEvent.MARK_NORMALIZED,
    ): IngestionState.NORMALIZED,
    (
        IngestionState.EXTRACTED,
        IngestionTransitionEvent.MARK_FAILED,
    ): IngestionState.FAILED,
    (
        IngestionState.NORMALIZED,
        IngestionTransitionEvent.MARK_VALIDATED,
    ): IngestionState.VALIDATED,
    (
        IngestionState.NORMALIZED,
        IngestionTransitionEvent.MARK_FAILED,
    ): IngestionState.FAILED,
    (
        IngestionState.VALIDATED,
        IngestionTransitionEvent.MARK_PREVIEW_READY,
    ): IngestionState.PREVIEW_READY,
    (
        IngestionState.VALIDATED,
        IngestionTransitionEvent.MARK_FAILED,
    ): IngestionState.FAILED,
    (
        IngestionState.PREVIEW_READY,
        IngestionTransitionEvent.MARK_COMPLETED,
    ): IngestionState.COMPLETED,
    (
        IngestionState.PREVIEW_READY,
        IngestionTransitionEvent.MARK_FAILED,
    ): IngestionState.FAILED,
    (
        IngestionState.FAILED,
        IngestionTransitionEvent.RESET_TO_RECEIVED,
    ): IngestionState.RECEIVED,
}

PIPELINE_ORDER: tuple[IngestionState, ...] = (
    IngestionState.RECEIVED,
    IngestionState.CLASSIFIED,
    IngestionState.EXTRACTED,
    IngestionState.NORMALIZED,
    IngestionState.VALIDATED,
    IngestionState.PREVIEW_READY,
    IngestionState.COMPLETED,
)


def resolve_ingestion_state(value: IngestionState | str) -> IngestionState:
    """Resolve an IngestionState from enum or string token."""
    if isinstance(value, IngestionState):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return IngestionState(token)
    except ValueError as exc:
        raise ValueError(f"Unknown ingestion state: {value!r}") from exc


def next_ingestion_state(
    current: IngestionState | str,
    event: IngestionTransitionEvent | str,
) -> IngestionState:
    """Return the lawful next state for ``(current, event)``.

    Raises:
        ValueError: When the transition is not lawful.
    """
    state = resolve_ingestion_state(current)
    if isinstance(event, IngestionTransitionEvent):
        resolved_event = event
    else:
        token = (event or "").strip().lower().replace("-", "_").replace(" ", "_")
        try:
            resolved_event = IngestionTransitionEvent(token)
        except ValueError as exc:
            raise ValueError(f"Unknown ingestion event: {event!r}") from exc
    key = (state, resolved_event)
    if key not in LAWFUL_INGESTION_TRANSITIONS:
        raise ValueError(
            f"Illegal ingestion transition: {state.value} + {resolved_event.value}"
        )
    return LAWFUL_INGESTION_TRANSITIONS[key]


def pipeline_index(state: IngestionState | str) -> int:
    """Index of ``state`` in the forward pipeline, or -1 for FAILED."""
    resolved = resolve_ingestion_state(state)
    if resolved is IngestionState.FAILED:
        return -1
    try:
        return PIPELINE_ORDER.index(resolved)
    except ValueError:
        return -1


def has_reached(
    current: IngestionState | str,
    milestone: IngestionState | str,
) -> bool:
    """True when ``current`` is at or beyond ``milestone`` on the forward path."""
    cur = resolve_ingestion_state(current)
    goal = resolve_ingestion_state(milestone)
    if cur is IngestionState.FAILED or goal is IngestionState.FAILED:
        return False
    return pipeline_index(cur) >= pipeline_index(goal)


def is_terminal_ingestion_state(state: IngestionState | str) -> bool:
    """True for COMPLETED or FAILED."""
    resolved = resolve_ingestion_state(state)
    return resolved in {IngestionState.COMPLETED, IngestionState.FAILED}


def is_failure_state(state: IngestionState | str) -> bool:
    """True when the job is in FAILED."""
    return resolve_ingestion_state(state) is IngestionState.FAILED
