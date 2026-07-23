"""Assessment snapshot — immutable, accurate mirror of a mastery assessment.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Assessment Snapshot
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.enums import KnowledgeGapKind
from domain.education.mastery_estimation.ids import AssessmentId
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
from domain.education.mastery_estimation.value_objects.subject_assessment import (
    SubjectAssessment,
)


@dataclass(frozen=True, slots=True)
class AssessmentSnapshot(EducationalValueObject):
    """Immutable, accurate capture of a MasteryAssessment aggregate.

    A snapshot is a read model. It does not re-estimate or recompute — it
    faithfully mirrors the assessment at the moment it was produced.
    """

    assessment_id: AssessmentId
    student_id: str
    overall_mastery: MasteryScore
    overall_confidence: MasteryConfidence
    overall_stability: LearningStability
    subject_assessments: tuple[SubjectAssessment, ...]
    knowledge_gaps: tuple[KnowledgeGap, ...]
    supporting_evidence: tuple[EvidenceContribution, ...]
    reasons: tuple[AssessmentReason, ...]
    assessed_at: datetime

    def _validate(self) -> None:
        if not isinstance(self.assessment_id, AssessmentId):
            raise EducationalInvariantViolation(
                "assessment_id must be an AssessmentId",
                invariant="AssessmentSnapshot.assessment_id.type",
            )
        if not isinstance(self.student_id, str) or not self.student_id.strip():
            raise EducationalInvariantViolation(
                "student_id must be a non-empty string",
                invariant="AssessmentSnapshot.student_id.required",
            )
        if not isinstance(self.overall_mastery, MasteryScore):
            raise EducationalInvariantViolation(
                "overall_mastery must be a MasteryScore",
                invariant="AssessmentSnapshot.overall_mastery.type",
            )
        if not isinstance(self.overall_confidence, MasteryConfidence):
            raise EducationalInvariantViolation(
                "overall_confidence must be a MasteryConfidence",
                invariant="AssessmentSnapshot.overall_confidence.type",
            )
        if not isinstance(self.overall_stability, LearningStability):
            raise EducationalInvariantViolation(
                "overall_stability must be a LearningStability",
                invariant="AssessmentSnapshot.overall_stability.type",
            )
        object.__setattr__(
            self, "subject_assessments", tuple(self.subject_assessments)
        )
        for assessment in self.subject_assessments:
            if not isinstance(assessment, SubjectAssessment):
                raise EducationalInvariantViolation(
                    "subject_assessments must contain SubjectAssessment "
                    "value objects",
                    invariant="AssessmentSnapshot.subject_assessments.type",
                )
        object.__setattr__(self, "knowledge_gaps", tuple(self.knowledge_gaps))
        for gap in self.knowledge_gaps:
            if not isinstance(gap, KnowledgeGap):
                raise EducationalInvariantViolation(
                    "knowledge_gaps must contain KnowledgeGap value objects",
                    invariant="AssessmentSnapshot.knowledge_gaps.type",
                )
        object.__setattr__(
            self, "supporting_evidence", tuple(self.supporting_evidence)
        )
        for contribution in self.supporting_evidence:
            if not isinstance(contribution, EvidenceContribution):
                raise EducationalInvariantViolation(
                    "supporting_evidence must contain EvidenceContribution "
                    "value objects",
                    invariant="AssessmentSnapshot.supporting_evidence.type",
                )
        object.__setattr__(self, "reasons", tuple(self.reasons))
        for reason in self.reasons:
            if not isinstance(reason, AssessmentReason):
                raise EducationalInvariantViolation(
                    "reasons must contain AssessmentReason value objects",
                    invariant="AssessmentSnapshot.reasons.type",
                )
        if not isinstance(self.assessed_at, datetime):
            raise EducationalInvariantViolation(
                "assessed_at must be a datetime",
                invariant="AssessmentSnapshot.assessed_at.type",
            )

    def subject_count(self) -> int:
        return len(self.subject_assessments)

    def knowledge_gap_count(self) -> int:
        return len(self.knowledge_gaps)

    def weak_prerequisites(self) -> tuple[KnowledgeGap, ...]:
        return tuple(
            gap
            for gap in self.knowledge_gaps
            if gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE
        )
