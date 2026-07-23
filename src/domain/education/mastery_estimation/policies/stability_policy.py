"""Policy computing deterministic learning stability from evidence over time.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Stability Policy
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.education.mastery_estimation.value_objects.evidence_contribution import (
    EvidenceContribution,
)
from domain.education.mastery_estimation.value_objects.learning_stability import (
    LearningStability,
)

_MIN_EVIDENCE_FOR_STABILITY = 2


class StabilityPolicy:
    """Deterministically computes learning stability from a signal timeline.

    Stability is the inverse of the population variance of signed evidence
    contributions ordered by time. No randomness; the same contributions
    always produce the same stability.
    """

    @staticmethod
    def calculate(
        contributions: Sequence[EvidenceContribution],
    ) -> LearningStability:
        if len(contributions) < _MIN_EVIDENCE_FOR_STABILITY:
            return LearningStability.insufficient_data()
        ordered = sorted(contributions, key=lambda c: c.occurred_at.occurred_at)
        values = [c.contribution for c in ordered]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        # Contributions are bounded to [-1.0, 1.0], so variance around the
        # mean cannot exceed 1.0 (the bimodal extreme). Clamp defensively.
        variance = max(0.0, min(1.0, variance))
        magnitude = 1.0 - variance
        return LearningStability(
            magnitude=magnitude,
            evidence_count=len(contributions),
            variance=variance,
        )

    @staticmethod
    def aggregate_subject_stability(
        stabilities: Sequence[LearningStability],
    ) -> LearningStability:
        """Evidence-count-weighted average stability across competencies."""
        assessed = [
            stability
            for stability in stabilities
            if stability.evidence_count >= _MIN_EVIDENCE_FOR_STABILITY
        ]
        if not assessed:
            return LearningStability.insufficient_data()
        total_evidence = sum(stability.evidence_count for stability in assessed)
        weighted_magnitude = (
            sum(s.magnitude * s.evidence_count for s in assessed) / total_evidence
        )
        weighted_variance = (
            sum(s.variance * s.evidence_count for s in assessed) / total_evidence
        )
        return LearningStability(
            magnitude=weighted_magnitude,
            evidence_count=total_evidence,
            variance=weighted_variance,
        )
