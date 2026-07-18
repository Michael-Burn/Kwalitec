"""Revision scheduler — deterministic revision window assignment."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.domain.adaptive_learning.revision_candidate import RevisionCandidate
from app.domain.adaptive_learning.revision_window import (
    RevisionUrgency,
    RevisionWindow,
    urgency_from_priority,
)


class RevisionScheduler:
    """Schedule revision windows from ranked candidates.

    Window start offsets are deterministic functions of urgency — no randomness.
    """

    URGENCY_OFFSET_HOURS: dict[RevisionUrgency, float] = {
        RevisionUrgency.IMMEDIATE: 0.0,
        RevisionUrgency.TODAY: 2.0,
        RevisionUrgency.THIS_WEEK: 24.0,
        RevisionUrgency.DEFERRED: 72.0,
    }

    @staticmethod
    def schedule(
        candidates: list[RevisionCandidate] | tuple[RevisionCandidate, ...],
        *,
        as_of: datetime,
        exam_proximity: float = 0.0,
        max_windows: int = 3,
    ) -> tuple[RevisionWindow, ...]:
        """Build ordered revision windows for the top candidates."""
        if not isinstance(as_of, datetime):
            raise ValueError("as_of must be a datetime")
        when = as_of if as_of.tzinfo else as_of.replace(tzinfo=UTC)
        ordered = sorted(candidates, key=lambda c: c.ranking_key)
        windows: list[RevisionWindow] = []
        for candidate in ordered[: max(0, max_windows)]:
            urgency = urgency_from_priority(
                candidate.priority.score,
                exam_proximity=exam_proximity,
            )
            offset_hours = RevisionScheduler.URGENCY_OFFSET_HOURS[urgency]
            start = when + timedelta(hours=offset_hours)
            minutes = candidate.roi.estimated_study_minutes
            windows.append(
                RevisionWindow.create(
                    candidate.topic_id,
                    urgency=urgency,
                    suggested_start=start,
                    allocated_minutes=minutes,
                    priority_score=candidate.priority.score,
                )
            )
        return tuple(windows)

    @staticmethod
    def urgency_for(
        priority_score: float,
        *,
        exam_proximity: float = 0.0,
    ) -> RevisionUrgency:
        """Expose urgency mapping for diagnostics / tests."""
        return urgency_from_priority(priority_score, exam_proximity=exam_proximity)
