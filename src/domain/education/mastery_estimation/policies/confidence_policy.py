"""Policy computing deterministic confidence in a mastery estimate.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Confidence Policy

Contradictory evidence — evidence that pulls in opposing directions for the
same competency — always reduces confidence deterministically. It never
raises an exception or produces undefined behaviour.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from domain.education.mastery_estimation.value_objects.confidence_score import (
    ConfidenceScore,
)
from domain.education.mastery_estimation.value_objects.evidence_contribution import (
    EvidenceContribution,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.mastery_estimation.value_objects.mastery_confidence import (
    MasteryConfidence,
)

_VOLUME_SATURATION_COUNT = 6
_WEIGHT_VOLUME = 0.40
_WEIGHT_CONSISTENCY = 0.35
_WEIGHT_RECENCY = 0.25
_RECENCY_WINDOW_DAYS = 30.0
_PREREQUISITE_PENALTY_FACTOR = 0.85


class ConfidencePolicy:
    """Deterministically computes confidence in a mastery estimate.

    Confidence is a fixed, weighted combination of evidence volume,
    evidence consistency (the inverse of contradiction), and recency,
    additionally penalised when weak structural prerequisites were
    discovered. No randomness; no wall-clock reads — ``as_of`` is always
    supplied by the caller.
    """

    @staticmethod
    def calculate(
        contributions: Sequence[EvidenceContribution],
        *,
        as_of: datetime,
        weak_prerequisites: Sequence[KnowledgeGap] = (),
    ) -> MasteryConfidence:
        if not contributions:
            return MasteryConfidence.zero()
        volume_factor = min(1.0, len(contributions) / _VOLUME_SATURATION_COUNT)
        contradiction_ratio = ConfidencePolicy.contradiction_ratio(contributions)
        consistency_factor = 1.0 - contradiction_ratio
        recency_factor = ConfidencePolicy.recency_factor(contributions, as_of=as_of)
        raw = (
            volume_factor * _WEIGHT_VOLUME
            + consistency_factor * _WEIGHT_CONSISTENCY
            + recency_factor * _WEIGHT_RECENCY
        )
        penalty_applied = len(weak_prerequisites) > 0
        if penalty_applied:
            raw *= _PREREQUISITE_PENALTY_FACTOR
        magnitude = max(0.0, min(1.0, raw))
        return MasteryConfidence(
            score=ConfidenceScore(magnitude=magnitude),
            evidence_count=len(contributions),
            contradiction_ratio=contradiction_ratio,
            recency_factor=recency_factor,
            prerequisite_penalty_applied=penalty_applied,
        )

    @staticmethod
    def contradiction_ratio(contributions: Sequence[EvidenceContribution]) -> float:
        """Symmetric measure of opposing evidence, in ``[0.0, 1.0]``.

        ``0.0`` denotes evidence that is entirely one-directional (or
        absent); ``1.0`` denotes a perfectly balanced conflict between
        positive and negative evidence.
        """
        positive_weight = sum(
            c.weight for c in contributions if c.contribution > 0.0
        )
        negative_weight = sum(
            c.weight for c in contributions if c.contribution < 0.0
        )
        total = positive_weight + negative_weight
        if total <= 0.0:
            return 0.0
        return min(positive_weight, negative_weight) / total * 2.0

    @staticmethod
    def recency_factor(
        contributions: Sequence[EvidenceContribution], *, as_of: datetime
    ) -> float:
        """Average recency weight of the contributions, in ``[0.0, 1.0]``.

        Evidence at or after ``as_of`` scores ``1.0``; evidence at or
        beyond ``_RECENCY_WINDOW_DAYS`` before ``as_of`` scores ``0.0``;
        evidence in between decays linearly.
        """
        if not contributions:
            return 0.0
        scores: list[float] = []
        for contribution in contributions:
            age_days = (
                as_of - contribution.occurred_at.occurred_at
            ).total_seconds() / 86400.0
            if age_days <= 0.0:
                scores.append(1.0)
            elif age_days >= _RECENCY_WINDOW_DAYS:
                scores.append(0.0)
            else:
                scores.append(1.0 - (age_days / _RECENCY_WINDOW_DAYS))
        return sum(scores) / len(scores)

    @staticmethod
    def aggregate_subject_confidence(
        confidences: Sequence[MasteryConfidence],
    ) -> MasteryConfidence:
        """Evidence-count-weighted average confidence across competencies."""
        assessed = [c for c in confidences if c.evidence_count > 0]
        if not assessed:
            return MasteryConfidence.zero()
        total_evidence = sum(c.evidence_count for c in assessed)
        weighted_magnitude = (
            sum(c.score.magnitude * c.evidence_count for c in assessed)
            / total_evidence
        )
        average_contradiction = sum(c.contradiction_ratio for c in assessed) / len(
            assessed
        )
        average_recency = sum(c.recency_factor for c in assessed) / len(assessed)
        penalty_applied = any(c.prerequisite_penalty_applied for c in assessed)
        return MasteryConfidence(
            score=ConfidenceScore(magnitude=weighted_magnitude),
            evidence_count=total_evidence,
            contradiction_ratio=average_contradiction,
            recency_factor=average_recency,
            prerequisite_penalty_applied=penalty_applied,
        )
