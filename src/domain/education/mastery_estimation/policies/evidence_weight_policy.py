"""Policy converting educational evidence into signed mastery contributions.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Weight Policy

This is the single, table-driven, deterministic bridge between
``educational_evidence.EducationalEvidence`` and this context's own
``EvidenceContribution``. No evidence type is interpreted anywhere else in
this bounded context.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.educational_evidence.enums import EvidenceType
from domain.education.mastery_estimation.value_objects.evidence_contribution import (
    EvidenceContribution,
)

if TYPE_CHECKING:
    from domain.education.educational_evidence.aggregates.educational_evidence import (
        EducationalEvidence,
    )

# Deterministic polarity per evidence type, in [-1.0, 1.0]. Positive values
# support mastery; negative values weigh against it; 0.0 denotes evidence
# that is considered (it still counts toward evidence_count) but carries no
# directional signal on its own — for example, general engagement. Evidence
# types absent from this table default to a neutral 0.0 polarity.
_POLARITY_BY_TYPE: dict[EvidenceType, float] = {
    EvidenceType.QUESTION_ANSWERED: 1.0,
    EvidenceType.QUESTION_INCORRECT: -1.0,
    EvidenceType.REVIEW_COMPLETED: 0.6,
    EvidenceType.COMPETENCY_PRACTISED: 0.3,
    EvidenceType.HINT_REQUESTED: -0.3,
    EvidenceType.CHECKPOINT_REACHED: 0.4,
    EvidenceType.MISSION_COMPLETED: 0.2,
    EvidenceType.MISSION_ABANDONED: -0.2,
    EvidenceType.GOAL_ACHIEVED: 0.2,
    EvidenceType.STUDY_SESSION_COMPLETED: 0.1,
}

# Self-reported confidence is weaker evidentiary status than an observed
# outcome, so its polarity is scaled down before combining with weight.
_CONFIDENCE_LEVEL_POLARITY: dict[str, float] = {
    "very_low": -1.0,
    "low": -0.5,
    "medium": 0.0,
    "high": 0.5,
    "very_high": 1.0,
    "unknown": 0.0,
}
_CONFIDENCE_REPORT_SCALE = 0.4


class EvidenceWeightPolicy:
    """Deterministically classifies and weighs evidence for mastery estimation.

    This policy performs no aggregation across multiple pieces of evidence
    — see ``MasteryPolicy`` for that — it only converts a single piece of
    evidence into a single signed ``EvidenceContribution``.
    """

    @staticmethod
    def polarity_for(evidence_type: EvidenceType) -> float:
        return _POLARITY_BY_TYPE.get(evidence_type, 0.0)

    @staticmethod
    def is_positive_signal(evidence_type: EvidenceType) -> bool:
        return EvidenceWeightPolicy.polarity_for(evidence_type) > 0.0

    @staticmethod
    def is_negative_signal(evidence_type: EvidenceType) -> bool:
        return EvidenceWeightPolicy.polarity_for(evidence_type) < 0.0

    @staticmethod
    def is_neutral_signal(evidence_type: EvidenceType) -> bool:
        return EvidenceWeightPolicy.polarity_for(evidence_type) == 0.0

    @staticmethod
    def contribution_for(evidence: EducationalEvidence) -> EvidenceContribution:
        """Convert a single piece of evidence into a signed contribution."""
        if evidence.evidence_type is EvidenceType.CONFIDENCE_REPORTED:
            level = str(evidence.metadata.get("confidence_level", "unknown"))
            polarity = (
                _CONFIDENCE_LEVEL_POLARITY.get(level, 0.0)
                * _CONFIDENCE_REPORT_SCALE
            )
        else:
            polarity = EvidenceWeightPolicy.polarity_for(evidence.evidence_type)
        contribution = max(-1.0, min(1.0, polarity)) * evidence.weight.magnitude
        return EvidenceContribution(
            evidence_id=evidence.evidence_id,
            evidence_type=evidence.evidence_type,
            contribution=contribution,
            weight=evidence.weight.magnitude,
            occurred_at=evidence.occurred_at,
        )
