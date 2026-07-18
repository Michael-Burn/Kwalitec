"""Stateless mastery calculation policy."""

from __future__ import annotations

from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import (
    NEGATIVE_OUTCOMES,
    POSITIVE_OUTCOMES,
    EvidenceType,
)

# Deterministic mastery deltas by evidence type (base magnitude).
_TYPE_WEIGHTS: dict[EvidenceType, float] = {
    EvidenceType.ACTIVITY_COMPLETED: 0.04,
    EvidenceType.ASSESSMENT_OUTCOME: 0.12,
    EvidenceType.PRACTICE_RESULT: 0.08,
    EvidenceType.REFLECTION: 0.02,
    EvidenceType.SELF_ASSESSMENT: 0.03,
    EvidenceType.RECALL_PERFORMANCE: 0.10,
    EvidenceType.CONFIDENCE_RATING: 0.01,
    EvidenceType.TIME_ON_TASK: 0.01,
    EvidenceType.SESSION_COMPLETION: 0.03,
    EvidenceType.MISSION_COMPLETION: 0.05,
    EvidenceType.REVISION_OUTCOME: 0.09,
}


class MasteryPolicy:
    """Educational rules for mastery updates from evidence."""

    INITIAL_MASTERY = 0.0
    MIN_MASTERY = 0.0
    MAX_MASTERY = 1.0

    @staticmethod
    def weight_for(evidence_type: EvidenceType) -> float:
        """Return base magnitude for an evidence type."""
        return _TYPE_WEIGHTS.get(evidence_type, 0.02)

    @staticmethod
    def polarity(event: EvidenceEvent) -> float:
        """Return +1 / -1 / 0 polarity from outcome or score."""
        if event.score is not None:
            if event.score >= 0.6:
                return 1.0
            if event.score <= 0.4:
                return -1.0
            return 0.0
        if event.outcome is None:
            # Completions without outcome are weakly positive.
            if event.evidence_type in (
                EvidenceType.ACTIVITY_COMPLETED,
                EvidenceType.SESSION_COMPLETION,
                EvidenceType.MISSION_COMPLETION,
                EvidenceType.TIME_ON_TASK,
            ):
                return 0.5
            return 0.0
        if event.outcome in POSITIVE_OUTCOMES:
            return 1.0
        if event.outcome in NEGATIVE_OUTCOMES:
            return -1.0
        return 0.0

    @staticmethod
    def delta_for(event: EvidenceEvent) -> float:
        """Return deterministic mastery delta for one evidence event."""
        weight = MasteryPolicy.weight_for(event.evidence_type)
        polarity = MasteryPolicy.polarity(event)
        if event.confidence_rating is not None:
            weight *= 0.5 + 0.5 * event.confidence_rating
        return weight * polarity

    @staticmethod
    def apply_delta(current: float, delta: float) -> float:
        """Clamp mastery after applying a delta."""
        next_value = current + delta
        if next_value < MasteryPolicy.MIN_MASTERY:
            return MasteryPolicy.MIN_MASTERY
        if next_value > MasteryPolicy.MAX_MASTERY:
            return MasteryPolicy.MAX_MASTERY
        return next_value
