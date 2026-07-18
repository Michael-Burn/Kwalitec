"""Immutable result of evaluating Learning Activity / sequence completion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityResult:
    """Whether an activity and/or its sequence is educationally complete.

    Never asserts Learning Session completion. Returns only a readiness signal
    for the Session Runtime to consume.

    Attributes:
        activity_id: Activity evaluated (None when evaluating sequence only).
        session_id: Parent session identity.
        activity_complete: True when the named activity is COMPLETED.
        sequence_complete: True when all activities are terminal
            (COMPLETED or SKIPPED).
        ready_for_session_completion: True when the sequence is closed enough
            for the Session Runtime to consider completing the session.
            Never completes the session itself.
        blockers: Deterministic blocker tags when not ready.
        reason: Human-readable educational explanation.
        completed_count: Number of COMPLETED activities.
        skipped_count: Number of SKIPPED activities.
        remaining_count: Number of non-terminal activities.
    """

    activity_id: str | None
    session_id: str
    activity_complete: bool
    sequence_complete: bool
    ready_for_session_completion: bool
    blockers: tuple[str, ...]
    reason: str
    completed_count: int
    skipped_count: int
    remaining_count: int
