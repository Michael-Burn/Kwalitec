"""Policy aggregating evidence contributions into deterministic mastery scores.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Mastery Policy
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.education.mastery_estimation.enums import KnowledgeGapSeverity
from domain.education.mastery_estimation.policies.prerequisite_influence_policy import (  # noqa: E501
    PrerequisiteInfluencePolicy,
)
from domain.education.mastery_estimation.value_objects.evidence_contribution import (
    EvidenceContribution,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)

# A competency at or above this magnitude is not considered a gap, whether
# or not it has weak prerequisites of its own.
_GAP_SECURE_THRESHOLD = 0.60
_GAP_SEVERE_THRESHOLD = 0.25
_GAP_MODERATE_THRESHOLD = 0.45

# No-directional-signal default: when evidence exists but every
# contribution is neutral (for example only practice/engagement signals),
# there is genuinely no basis to skew the score up or down.
_NEUTRAL_EVIDENCE_MAGNITUDE = 0.5


class MasteryPolicy:
    """Deterministically aggregates evidence contributions into a MasteryScore.

    No randomness, no machine learning, and no wall-clock reads — the same
    contributions always aggregate to the same score.
    """

    @staticmethod
    def aggregate_contributions(
        contributions: Sequence[EvidenceContribution],
    ) -> MasteryScore:
        """Weighted-outcome aggregation of signed evidence contributions.

        The magnitude is the share of weighted evidentiary support that is
        positive out of all directionally-signed (non-neutral) evidence.
        Neutral evidence still counts toward ``evidence_count`` but does
        not skew the magnitude.
        """
        if not contributions:
            return MasteryScore.not_assessed()
        positive_weight = sum(
            c.weight for c in contributions if c.contribution > 0.0
        )
        negative_weight = sum(
            c.weight for c in contributions if c.contribution < 0.0
        )
        directional_weight = positive_weight + negative_weight
        if directional_weight <= 0.0:
            magnitude = _NEUTRAL_EVIDENCE_MAGNITUDE
        else:
            magnitude = positive_weight / directional_weight
        return MasteryScore(magnitude=magnitude, evidence_count=len(contributions))

    @staticmethod
    def apply_prerequisite_dampening(
        score: MasteryScore,
        weak_prerequisites: Sequence[KnowledgeGap],
    ) -> MasteryScore:
        """Reduce a mastery score's magnitude when prerequisites are weak.

        Structural prerequisites influence downstream mastery: a
        competency's demonstrated mastery is discounted when the
        foundation it structurally depends on is itself weak. Evidence
        count is preserved — dampening reinterprets the evidence's
        magnitude, it does not add or remove evidence.
        """
        if not weak_prerequisites or score.evidence_count == 0:
            return score
        factor = 1.0
        for gap in weak_prerequisites:
            factor *= PrerequisiteInfluencePolicy.dampening_factor(
                gap.dependency_strength, gap.mastery_score
            )
        dampened_magnitude = max(0.0, min(1.0, score.magnitude * factor))
        return MasteryScore(
            magnitude=dampened_magnitude, evidence_count=score.evidence_count
        )

    @staticmethod
    def aggregate_subject_scores(scores: Sequence[MasteryScore]) -> MasteryScore:
        """Evidence-count-weighted average of competency scores for a subject."""
        assessed = [score for score in scores if score.evidence_count > 0]
        if not assessed:
            return MasteryScore.not_assessed()
        total_evidence = sum(score.evidence_count for score in assessed)
        weighted_sum = sum(
            score.magnitude * score.evidence_count for score in assessed
        )
        magnitude = weighted_sum / total_evidence
        return MasteryScore(magnitude=magnitude, evidence_count=total_evidence)

    @staticmethod
    def classify_gap_severity(mastery: MasteryScore) -> KnowledgeGapSeverity | None:
        """Direct-evidence gap severity for one competency's own mastery.

        Returns ``None`` when the competency is not a gap: either it has
        no evidence at all (absence of evidence is not itself a gap) or its
        magnitude already meets the secure threshold.
        """
        if mastery.evidence_count == 0:
            return None
        if mastery.magnitude >= _GAP_SECURE_THRESHOLD:
            return None
        if mastery.magnitude < _GAP_SEVERE_THRESHOLD:
            return KnowledgeGapSeverity.SEVERE
        if mastery.magnitude < _GAP_MODERATE_THRESHOLD:
            return KnowledgeGapSeverity.MODERATE
        return KnowledgeGapSeverity.MINOR
