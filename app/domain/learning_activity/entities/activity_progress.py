"""Progress posture across a Learning Activity sequence."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityProgress:
    """Immutable progress summary for an activity sequence.

    Attributes:
        session_id: Parent Learning Session identity.
        total_count: Number of activities in the sequence.
        completed_count: Activities in COMPLETED state.
        skipped_count: Activities in SKIPPED state.
        remaining_count: Activities not yet terminal.
        current_activity_id: Identity of the current focus activity, if any.
        current_index: Sequence index of the current activity, or -1.
        progress_percentage: 0–100 based on terminal activities / total.
    """

    session_id: str
    total_count: int
    completed_count: int
    skipped_count: int
    remaining_count: int
    current_activity_id: str | None
    current_index: int
    progress_percentage: float

    @classmethod
    def empty(cls, session_id: str) -> ActivityProgress:
        """Zero-progress posture for an empty or unstarted sequence."""
        return cls(
            session_id=session_id,
            total_count=0,
            completed_count=0,
            skipped_count=0,
            remaining_count=0,
            current_activity_id=None,
            current_index=-1,
            progress_percentage=0.0,
        )
