"""Stateless confidence calculation policy."""

from __future__ import annotations

from app.domain.student_twin.confidence_band import confidence_band_from_score
from app.domain.student_twin.evidence_event import EvidenceEvent


class ConfidencePolicy:
    """Educational rules for confidence from evidence volume and consistency."""

    # Soft saturation: ~10 consistent events → high confidence.
    VOLUME_SATURATION = 10.0
    CONFLICT_PENALTY = 0.15

    @staticmethod
    def volume_score(event_count: int) -> float:
        """Map evidence count to [0, 1] with diminishing returns."""
        if event_count <= 0:
            return 0.0
        ratio = event_count / ConfidencePolicy.VOLUME_SATURATION
        if ratio >= 1.0:
            return 1.0
        return ratio

    @staticmethod
    def consistency_score(
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
    ) -> float:
        """Score outcome consistency in [0, 1]; 1.0 when no conflict."""
        from app.application.student_twin.policies.mastery_policy import MasteryPolicy

        polarities = [
            MasteryPolicy.polarity(event)
            for event in events
            if MasteryPolicy.polarity(event) != 0.0
        ]
        if len(polarities) < 2:
            return 1.0
        positive = sum(1 for p in polarities if p > 0)
        negative = sum(1 for p in polarities if p < 0)
        if positive == 0 or negative == 0:
            return 1.0
        conflict_ratio = min(positive, negative) / len(polarities)
        return max(0.0, 1.0 - conflict_ratio)

    @staticmethod
    def score_for(
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
    ) -> float:
        """Combine volume and consistency into a confidence score."""
        volume = ConfidencePolicy.volume_score(len(events))
        consistency = ConfidencePolicy.consistency_score(events)
        score = 0.6 * volume + 0.4 * consistency
        if consistency < 0.5:
            score = max(0.0, score - ConfidencePolicy.CONFLICT_PENALTY)
        if score > 1.0:
            return 1.0
        return score

    @staticmethod
    def band_for(
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
    ):
        """Return ConfidenceBand for a set of events."""
        return confidence_band_from_score(ConfidencePolicy.score_for(events))
