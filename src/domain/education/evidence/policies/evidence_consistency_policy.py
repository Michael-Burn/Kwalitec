"""Policy governing educational consistency of evidence observations.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md (§2 Principles, §4 Quality Levels)
Concept
    Evidence Consistency Policy
"""

from __future__ import annotations

from domain.education.evidence.entities.evidence_item import EvidenceItem
from domain.education.evidence.entities.evidence_source import EvidenceSource
from domain.education.evidence.enums import (
    EvidenceItemKind,
    EvidenceSourceKind,
    EvidenceStrengthLevel,
)
from domain.education.evidence.value_objects.confidence_measure import ConfidenceMeasure
from domain.education.evidence.value_objects.evidence_strength import EvidenceStrength
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation

# Soft / metacognitive item kinds cannot alone warrant very strong strength.
_SOFT_ITEM_KINDS = frozenset(
    {
        EvidenceItemKind.REFLECTION,
        EvidenceItemKind.HINT_USAGE,
    }
)

# Source ↔ item affinity (educational meaning alignment, not product channels).
_SOURCE_ITEM_AFFINITY: dict[EvidenceSourceKind, frozenset[EvidenceItemKind]] = {
    EvidenceSourceKind.REFLECTION_CAPTURE: frozenset({EvidenceItemKind.REFLECTION}),
    EvidenceSourceKind.ASSESSMENT: frozenset(
        {
            EvidenceItemKind.QUESTION_RESPONSE,
            EvidenceItemKind.WORKED_EXAMPLE_OUTCOME,
            EvidenceItemKind.RETRIEVAL_ATTEMPT,
            EvidenceItemKind.TRANSFER_ATTEMPT,
        }
    ),
    EvidenceSourceKind.STUDENT_ACTION: frozenset(
        {
            EvidenceItemKind.QUESTION_RESPONSE,
            EvidenceItemKind.WORKED_EXAMPLE_OUTCOME,
            EvidenceItemKind.RETRIEVAL_ATTEMPT,
            EvidenceItemKind.TRANSFER_ATTEMPT,
            EvidenceItemKind.HINT_USAGE,
            EvidenceItemKind.REFLECTION,
        }
    ),
    EvidenceSourceKind.SYSTEM_OBSERVATION: frozenset(
        {
            EvidenceItemKind.HINT_USAGE,
            EvidenceItemKind.QUESTION_RESPONSE,
            EvidenceItemKind.RETRIEVAL_ATTEMPT,
            EvidenceItemKind.TRANSFER_ATTEMPT,
            EvidenceItemKind.WORKED_EXAMPLE_OUTCOME,
        }
    ),
    EvidenceSourceKind.LEARNING_EPISODE: frozenset(set(EvidenceItemKind)),
}

_STRENGTH_MAX_FOR_SOFT_ONLY = EvidenceStrengthLevel.MODERATE

_CONFIDENCE_FLOOR_FOR_STRENGTH: dict[EvidenceStrengthLevel, ConfidenceLevel] = {
    EvidenceStrengthLevel.WEAK: ConfidenceLevel.VERY_LOW,
    EvidenceStrengthLevel.MODERATE: ConfidenceLevel.LOW,
    EvidenceStrengthLevel.STRONG: ConfidenceLevel.MEDIUM,
    EvidenceStrengthLevel.VERY_STRONG: ConfidenceLevel.HIGH,
}


class EvidenceConsistencyPolicy:
    """Enforces internal educational consistency of evidence observations.

    Consistency is observational alignment (source ↔ items ↔ strength ↔
    confidence). It does not diagnose learners or recommend actions.
    """

    @staticmethod
    def assert_source_item_affinity(
        source: EvidenceSource,
        items: tuple[EvidenceItem, ...] | list[EvidenceItem],
    ) -> None:
        allowed = _SOURCE_ITEM_AFFINITY.get(source.kind)
        if allowed is None:
            raise EducationalInvariantViolation(
                f"unsupported evidence source kind: {source.kind}",
                invariant="EvidenceConsistencyPolicy.source.supported",
            )
        for item in items:
            if item.kind not in allowed:
                raise EducationalInvariantViolation(
                    f"item kind {item.kind.value} is inconsistent with "
                    f"source kind {source.kind.value}",
                    invariant="EvidenceConsistencyPolicy.source_item.affinity",
                )

    @staticmethod
    def assert_strength_consistent_with_items(
        strength: EvidenceStrength,
        items: tuple[EvidenceItem, ...] | list[EvidenceItem],
    ) -> None:
        """Soft-only evidence cannot claim strong or very strong warrant."""
        if not items:
            return
        only_soft = all(item.kind in _SOFT_ITEM_KINDS for item in items)
        if only_soft and strength.level in {
            EvidenceStrengthLevel.STRONG,
            EvidenceStrengthLevel.VERY_STRONG,
        }:
            raise EducationalInvariantViolation(
                "soft evidence items alone cannot warrant strong or very strong "
                "strength",
                invariant="EvidenceConsistencyPolicy.strength.soft_ceiling",
            )
        if only_soft and not strength.at_least(EvidenceStrength.weak()):
            # Always true for valid strengths; retained for explicit soft bound.
            _ = _STRENGTH_MAX_FOR_SOFT_ONLY

    @staticmethod
    def assert_confidence_consistent_with_strength(
        confidence: ConfidenceMeasure,
        strength: EvidenceStrength,
    ) -> None:
        """Higher strength requires at least a matching confidence floor."""
        floor = _CONFIDENCE_FLOOR_FOR_STRENGTH[strength.level]
        if not confidence.is_at_least(floor):
            raise EducationalInvariantViolation(
                f"confidence {confidence.level.value} is too low for strength "
                f"{strength.level.value}",
                invariant="EvidenceConsistencyPolicy.confidence.strength_floor",
            )

    @staticmethod
    def assert_merge_compatible(
        student_id: str,
        other_student_id: str,
        source: EvidenceSource,
        other_source: EvidenceSource,
    ) -> None:
        if student_id != other_student_id:
            raise EducationalInvariantViolation(
                "cannot merge evidence belonging to different students",
                invariant="EvidenceConsistencyPolicy.merge.same_student",
            )
        if source.kind != other_source.kind:
            raise EducationalInvariantViolation(
                "cannot merge evidence from incompatible source kinds",
                invariant="EvidenceConsistencyPolicy.merge.source_kind",
            )

    @staticmethod
    def assert_consistent(
        source: EvidenceSource,
        items: tuple[EvidenceItem, ...] | list[EvidenceItem],
        strength: EvidenceStrength,
        confidence: ConfidenceMeasure,
    ) -> None:
        EvidenceConsistencyPolicy.assert_source_item_affinity(source, items)
        EvidenceConsistencyPolicy.assert_strength_consistent_with_items(
            strength, items
        )
        EvidenceConsistencyPolicy.assert_confidence_consistent_with_strength(
            confidence, strength
        )
