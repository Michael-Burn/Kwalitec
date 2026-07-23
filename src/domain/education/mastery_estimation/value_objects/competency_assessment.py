"""Competency assessment — computed mastery for a single competency.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Competency Assessment
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.enums import KnowledgeGapKind
from domain.education.mastery_estimation.ids import CompetencyId, SubjectId
from domain.education.mastery_estimation.value_objects.assessment_reason import (
    AssessmentReason,
)
from domain.education.mastery_estimation.value_objects.evidence_contribution import (
    EvidenceContribution,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.mastery_estimation.value_objects.learning_stability import (
    LearningStability,
)
from domain.education.mastery_estimation.value_objects.mastery_confidence import (
    MasteryConfidence,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)


@dataclass(frozen=True, slots=True)
class CompetencyAssessment(EducationalValueObject):
    """Immutable mastery assessment for one competency.

    Represents educational reasoning about a single competency: its
    computed mastery, confidence, learning stability, the evidence that
    supported the estimate, and any knowledge gaps discovered either from
    the competency's own evidence or from weak structural prerequisites
    discovered through the knowledge graph.
    """

    competency_id: CompetencyId
    subject_id: SubjectId
    mastery: MasteryScore
    confidence: MasteryConfidence
    stability: LearningStability
    supporting_evidence: tuple[EvidenceContribution, ...] = ()
    gaps: tuple[KnowledgeGap, ...] = ()
    reasons: tuple[AssessmentReason, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.competency_id, CompetencyId):
            raise EducationalInvariantViolation(
                "competency_id must be a CompetencyId",
                invariant="CompetencyAssessment.competency_id.type",
            )
        if not isinstance(self.subject_id, SubjectId):
            raise EducationalInvariantViolation(
                "subject_id must be a SubjectId",
                invariant="CompetencyAssessment.subject_id.type",
            )
        if not isinstance(self.mastery, MasteryScore):
            raise EducationalInvariantViolation(
                "mastery must be a MasteryScore",
                invariant="CompetencyAssessment.mastery.type",
            )
        if not isinstance(self.confidence, MasteryConfidence):
            raise EducationalInvariantViolation(
                "confidence must be a MasteryConfidence",
                invariant="CompetencyAssessment.confidence.type",
            )
        if not isinstance(self.stability, LearningStability):
            raise EducationalInvariantViolation(
                "stability must be a LearningStability",
                invariant="CompetencyAssessment.stability.type",
            )
        object.__setattr__(
            self, "supporting_evidence", tuple(self.supporting_evidence)
        )
        for contribution in self.supporting_evidence:
            if not isinstance(contribution, EvidenceContribution):
                raise EducationalInvariantViolation(
                    "supporting_evidence must contain EvidenceContribution "
                    "value objects",
                    invariant="CompetencyAssessment.supporting_evidence.type",
                )
        object.__setattr__(self, "gaps", tuple(self.gaps))
        for gap in self.gaps:
            if not isinstance(gap, KnowledgeGap):
                raise EducationalInvariantViolation(
                    "gaps must contain KnowledgeGap value objects",
                    invariant="CompetencyAssessment.gaps.type",
                )
            if (
                gap.kind is KnowledgeGapKind.WEAK_EVIDENCE
                and gap.competency_id != self.competency_id
            ):
                raise EducationalInvariantViolation(
                    "a weak_evidence gap attached to this assessment must "
                    "reference this competency",
                    invariant="CompetencyAssessment.gaps.direct_scope",
                )
            if (
                gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE
                and gap.related_competency_id != self.competency_id
            ):
                raise EducationalInvariantViolation(
                    "a weak_prerequisite gap attached to this assessment "
                    "must reference this competency as the dependent "
                    "competency",
                    invariant="CompetencyAssessment.gaps.prerequisite_scope",
                )
        object.__setattr__(self, "reasons", tuple(self.reasons))
        for reason in self.reasons:
            if not isinstance(reason, AssessmentReason):
                raise EducationalInvariantViolation(
                    "reasons must contain AssessmentReason value objects",
                    invariant="CompetencyAssessment.reasons.type",
                )

    def weak_prerequisites(self) -> tuple[KnowledgeGap, ...]:
        return tuple(
            gap for gap in self.gaps if gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE
        )

    def direct_gaps(self) -> tuple[KnowledgeGap, ...]:
        return tuple(
            gap for gap in self.gaps if gap.kind is KnowledgeGapKind.WEAK_EVIDENCE
        )

    def has_gaps(self) -> bool:
        return len(self.gaps) > 0

    def evidence_count(self) -> int:
        return len(self.supporting_evidence)
