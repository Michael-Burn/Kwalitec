"""CIP-001 Curriculum Intelligence Pipeline stages and lawful transitions.

Extends CS-DOC-001 document processing into the knowledge pipeline.
Embeddings / retrieval are Phase 2 (CIP-002) — this pipeline stops at
READY_FOR_EMBEDDINGS.
"""

from __future__ import annotations

from enum import StrEnum


class PipelineStage(StrEnum):
    """Authoritative CIP processing stages for an uploaded curriculum document."""

    UPLOADED = "uploaded"
    STORED = "stored"
    QUEUED = "queued"
    VERIFIED = "verified"
    EXTRACTED = "extracted"
    NORMALIZED = "normalized"
    PARSED = "parsed"
    MAPPED = "mapped"
    GRAPH_BUILT = "graph_built"
    READY_FOR_EMBEDDINGS = "ready_for_embeddings"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PipelineTransitionEvent(StrEnum):
    """Named events that advance or recover a CIP job."""

    MARK_VERIFIED = "mark_verified"
    MARK_EXTRACTED = "mark_extracted"
    MARK_NORMALIZED = "mark_normalized"
    MARK_PARSED = "mark_parsed"
    MARK_MAPPED = "mark_mapped"
    MARK_GRAPH_BUILT = "mark_graph_built"
    MARK_READY_FOR_EMBEDDINGS = "mark_ready_for_embeddings"
    MARK_FAILED = "mark_failed"
    MARK_CANCELLED = "mark_cancelled"
    RETRY = "retry"
    RESUME = "resume"


# Forward happy-path order (excludes FAILED / CANCELLED).
PIPELINE_ORDER: tuple[PipelineStage, ...] = (
    PipelineStage.UPLOADED,
    PipelineStage.STORED,
    PipelineStage.QUEUED,
    PipelineStage.VERIFIED,
    PipelineStage.EXTRACTED,
    PipelineStage.NORMALIZED,
    PipelineStage.PARSED,
    PipelineStage.MAPPED,
    PipelineStage.GRAPH_BUILT,
    PipelineStage.READY_FOR_EMBEDDINGS,
)

# Founder-facing milestone strip (subset used in UI).
FOUNDER_PIPELINE_MILESTONES: tuple[PipelineStage, ...] = (
    PipelineStage.QUEUED,
    PipelineStage.VERIFIED,
    PipelineStage.EXTRACTED,
    PipelineStage.PARSED,
    PipelineStage.MAPPED,
    PipelineStage.GRAPH_BUILT,
    PipelineStage.READY_FOR_EMBEDDINGS,
)

FOUNDER_STAGE_LABELS: dict[PipelineStage, str] = {
    PipelineStage.UPLOADED: "Uploaded",
    PipelineStage.STORED: "Stored",
    PipelineStage.QUEUED: "Processing",
    PipelineStage.VERIFIED: "Verified",
    PipelineStage.EXTRACTED: "Extracted",
    PipelineStage.NORMALIZED: "Normalized",
    PipelineStage.PARSED: "Parsed",
    PipelineStage.MAPPED: "Mapped",
    PipelineStage.GRAPH_BUILT: "Curriculum structure built",
    PipelineStage.READY_FOR_EMBEDDINGS: "Ready",
    PipelineStage.FAILED: "Failed",
    PipelineStage.CANCELLED: "Cancelled",
}

# (from_state, event) → to_state
LAWFUL_TRANSITIONS: dict[
    tuple[PipelineStage, PipelineTransitionEvent], PipelineStage
] = {
    (
        PipelineStage.QUEUED,
        PipelineTransitionEvent.MARK_VERIFIED,
    ): PipelineStage.VERIFIED,
    (PipelineStage.QUEUED, PipelineTransitionEvent.MARK_FAILED): PipelineStage.FAILED,
    (
        PipelineStage.QUEUED,
        PipelineTransitionEvent.MARK_CANCELLED,
    ): PipelineStage.CANCELLED,
    (
        PipelineStage.VERIFIED,
        PipelineTransitionEvent.MARK_EXTRACTED,
    ): PipelineStage.EXTRACTED,
    (PipelineStage.VERIFIED, PipelineTransitionEvent.MARK_FAILED): PipelineStage.FAILED,
    (
        PipelineStage.VERIFIED,
        PipelineTransitionEvent.MARK_CANCELLED,
    ): PipelineStage.CANCELLED,
    (
        PipelineStage.EXTRACTED,
        PipelineTransitionEvent.MARK_NORMALIZED,
    ): PipelineStage.NORMALIZED,
    (
        PipelineStage.EXTRACTED,
        PipelineTransitionEvent.MARK_FAILED,
    ): PipelineStage.FAILED,
    (
        PipelineStage.EXTRACTED,
        PipelineTransitionEvent.MARK_CANCELLED,
    ): PipelineStage.CANCELLED,
    (
        PipelineStage.NORMALIZED,
        PipelineTransitionEvent.MARK_PARSED,
    ): PipelineStage.PARSED,
    (
        PipelineStage.NORMALIZED,
        PipelineTransitionEvent.MARK_FAILED,
    ): PipelineStage.FAILED,
    (
        PipelineStage.NORMALIZED,
        PipelineTransitionEvent.MARK_CANCELLED,
    ): PipelineStage.CANCELLED,
    (PipelineStage.PARSED, PipelineTransitionEvent.MARK_MAPPED): PipelineStage.MAPPED,
    (PipelineStage.PARSED, PipelineTransitionEvent.MARK_FAILED): PipelineStage.FAILED,
    (
        PipelineStage.PARSED,
        PipelineTransitionEvent.MARK_CANCELLED,
    ): PipelineStage.CANCELLED,
    (
        PipelineStage.MAPPED,
        PipelineTransitionEvent.MARK_GRAPH_BUILT,
    ): PipelineStage.GRAPH_BUILT,
    (PipelineStage.MAPPED, PipelineTransitionEvent.MARK_FAILED): PipelineStage.FAILED,
    (
        PipelineStage.MAPPED,
        PipelineTransitionEvent.MARK_CANCELLED,
    ): PipelineStage.CANCELLED,
    (
        PipelineStage.GRAPH_BUILT,
        PipelineTransitionEvent.MARK_READY_FOR_EMBEDDINGS,
    ): PipelineStage.READY_FOR_EMBEDDINGS,
    (
        PipelineStage.GRAPH_BUILT,
        PipelineTransitionEvent.MARK_FAILED,
    ): PipelineStage.FAILED,
    (
        PipelineStage.GRAPH_BUILT,
        PipelineTransitionEvent.MARK_CANCELLED,
    ): PipelineStage.CANCELLED,
    # Recovery: FAILED → resume from last durable checkpoint (stored on job).
    (PipelineStage.FAILED, PipelineTransitionEvent.RETRY): PipelineStage.QUEUED,
    (PipelineStage.FAILED, PipelineTransitionEvent.RESUME): PipelineStage.QUEUED,
    (
        PipelineStage.CANCELLED,
        PipelineTransitionEvent.RETRY,
    ): PipelineStage.QUEUED,
}


def resolve_pipeline_stage(value: PipelineStage | str) -> PipelineStage:
    """Resolve a pipeline stage from enum or string token."""
    if isinstance(value, PipelineStage):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    # Legacy CS-DOC-001 aliases
    if token == "processing":
        return PipelineStage.QUEUED
    if token == "ready":
        return PipelineStage.READY_FOR_EMBEDDINGS
    try:
        return PipelineStage(token)
    except ValueError as exc:
        raise ValueError(f"Unknown CIP pipeline stage: {value!r}") from exc


def resolve_transition_event(
    value: PipelineTransitionEvent | str,
) -> PipelineTransitionEvent:
    """Resolve a transition event from enum or string."""
    if isinstance(value, PipelineTransitionEvent):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return PipelineTransitionEvent(token)
    except ValueError as exc:
        raise ValueError(f"Unknown CIP transition event: {value!r}") from exc


def next_pipeline_stage(
    current: PipelineStage | str,
    event: PipelineTransitionEvent | str,
) -> PipelineStage:
    """Return the lawful next stage for ``(current, event)``.

    Raises:
        ValueError: When the transition is not lawful.
    """
    state = resolve_pipeline_stage(current)
    resolved_event = resolve_transition_event(event)
    key = (state, resolved_event)
    if key not in LAWFUL_TRANSITIONS:
        raise ValueError(
            f"Illegal CIP transition: {state.value} + {resolved_event.value}"
        )
    return LAWFUL_TRANSITIONS[key]


def pipeline_index(stage: PipelineStage | str) -> int:
    """Index in forward pipeline, or -1 for FAILED/CANCELLED."""
    resolved = resolve_pipeline_stage(stage)
    if resolved in {PipelineStage.FAILED, PipelineStage.CANCELLED}:
        return -1
    try:
        return PIPELINE_ORDER.index(resolved)
    except ValueError:
        return -1


def has_reached(
    current: PipelineStage | str,
    milestone: PipelineStage | str,
) -> bool:
    """True when ``current`` is at or beyond ``milestone`` on the forward path."""
    cur = resolve_pipeline_stage(current)
    goal = resolve_pipeline_stage(milestone)
    if cur in {PipelineStage.FAILED, PipelineStage.CANCELLED}:
        return False
    if goal in {PipelineStage.FAILED, PipelineStage.CANCELLED}:
        return False
    return pipeline_index(cur) >= pipeline_index(goal)


def is_terminal(stage: PipelineStage | str) -> bool:
    """True for READY_FOR_EMBEDDINGS, FAILED, or CANCELLED."""
    resolved = resolve_pipeline_stage(stage)
    return resolved in {
        PipelineStage.READY_FOR_EMBEDDINGS,
        PipelineStage.FAILED,
        PipelineStage.CANCELLED,
    }


def is_failure(stage: PipelineStage | str) -> bool:
    """True when the job is FAILED."""
    return resolve_pipeline_stage(stage) is PipelineStage.FAILED


def founder_label(stage: PipelineStage | str) -> str:
    """Return Founder-facing label for a pipeline stage."""
    try:
        resolved = resolve_pipeline_stage(stage)
    except ValueError:
        return "Unknown"
    return FOUNDER_STAGE_LABELS.get(resolved, resolved.value.replace("_", " ").title())


def resume_stage_after_failure(checkpoint: PipelineStage | str | None) -> PipelineStage:
    """Stage to re-enter after FAILED, based on last successful checkpoint."""
    if checkpoint is None:
        return PipelineStage.QUEUED
    resolved = resolve_pipeline_stage(checkpoint)
    if resolved in {PipelineStage.FAILED, PipelineStage.CANCELLED}:
        return PipelineStage.QUEUED
    # Re-run the stage after the last success (or QUEUED if none past queue).
    idx = pipeline_index(resolved)
    if idx < 0:
        return PipelineStage.QUEUED
    # Resume by returning to the checkpoint itself so the coordinator re-runs
    # the *next* forward step from a known-good durable state.
    return resolved
