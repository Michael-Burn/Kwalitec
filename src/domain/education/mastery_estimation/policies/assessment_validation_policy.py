"""Policy validating MasteryAssessment aggregate shapes.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Assessment Validation Policy

This policy performs shape validation only — unique identities, resolvable
references, and well-typed fields. The educational reasoning that produces
those fields lives in ``MasteryPolicy``, ``ConfidencePolicy``,
``StabilityPolicy``, ``PrerequisiteInfluencePolicy``, and
``EvidenceWeightPolicy``.
"""

from __future__ import annotations

from datetime import datetime

from domain.education.foundation.base import require_identity_value
from domain.education.foundation.errors import EducationalInvariantViolation
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


class AssessmentValidationPolicy:
    """Validates MasteryAssessment shapes — no educational reasoning."""

    @staticmethod
    def assert_identity(assessment_id: AssessmentId) -> AssessmentId:
        if not isinstance(assessment_id, AssessmentId):
            raise EducationalInvariantViolation(
                "assessment must possess an AssessmentId identity",
                invariant="MasteryAssessment.identity.required",
            )
        return assessment_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_assessed_at(assessed_at: datetime) -> datetime:
        if not isinstance(assessed_at, datetime):
            raise EducationalInvariantViolation(
                "assessed_at must be a datetime",
                invariant="MasteryAssessment.assessed_at.type",
            )
        return assessed_at

    @staticmethod
    def assert_overall_mastery(overall_mastery: MasteryScore) -> MasteryScore:
        if not isinstance(overall_mastery, MasteryScore):
            raise EducationalInvariantViolation(
                "assessment must own an overall MasteryScore",
                invariant="MasteryAssessment.overall_mastery.required",
            )
        return overall_mastery

    @staticmethod
    def assert_overall_confidence(
        overall_confidence: MasteryConfidence,
    ) -> MasteryConfidence:
        if not isinstance(overall_confidence, MasteryConfidence):
            raise EducationalInvariantViolation(
                "assessment must own an overall MasteryConfidence",
                invariant="MasteryAssessment.overall_confidence.required",
            )
        return overall_confidence

    @staticmethod
    def assert_overall_stability(
        overall_stability: LearningStability,
    ) -> LearningStability:
        if not isinstance(overall_stability, LearningStability):
            raise EducationalInvariantViolation(
                "assessment must own an overall LearningStability",
                invariant="MasteryAssessment.overall_stability.required",
            )
        return overall_stability

    @staticmethod
    def assert_subject_assessments(
        subject_assessments: list[SubjectAssessment] | tuple[SubjectAssessment, ...],
    ) -> tuple[SubjectAssessment, ...]:
        items = tuple(subject_assessments)
        seen: set[str] = set()
        for assessment in items:
            if not isinstance(assessment, SubjectAssessment):
                raise EducationalInvariantViolation(
                    "subject_assessments must contain SubjectAssessment "
                    "value objects",
                    invariant="MasteryAssessment.subject_assessments.type",
                )
            key = assessment.subject_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate subject_id in mastery assessment",
                    invariant="MasteryAssessment.subject_assessments.unique",
                )
            seen.add(key)
        return items

    @staticmethod
    def assert_knowledge_gaps(
        knowledge_gaps: list[KnowledgeGap] | tuple[KnowledgeGap, ...],
        subject_assessments: tuple[SubjectAssessment, ...],
    ) -> tuple[KnowledgeGap, ...]:
        items = tuple(knowledge_gaps)
        tracked_competency_ids = {
            competency_assessment.competency_id.value
            for subject_assessment in subject_assessments
            for competency_assessment in subject_assessment.competency_assessments
        }
        for gap in items:
            if not isinstance(gap, KnowledgeGap):
                raise EducationalInvariantViolation(
                    "knowledge_gaps must contain KnowledgeGap value objects",
                    invariant="MasteryAssessment.knowledge_gaps.type",
                )
            reference_key = (
                gap.related_competency_id.value
                if gap.related_competency_id is not None
                else gap.competency_id.value
            )
            if reference_key not in tracked_competency_ids:
                raise EducationalInvariantViolation(
                    "a knowledge gap must reference a competency tracked "
                    "by this assessment",
                    invariant="MasteryAssessment.knowledge_gaps.scope",
                )
        return items

    @staticmethod
    def assert_supporting_evidence(
        supporting_evidence: list[EvidenceContribution]
        | tuple[EvidenceContribution, ...],
    ) -> tuple[EvidenceContribution, ...]:
        items = tuple(supporting_evidence)
        for contribution in items:
            if not isinstance(contribution, EvidenceContribution):
                raise EducationalInvariantViolation(
                    "supporting_evidence must contain EvidenceContribution "
                    "value objects",
                    invariant="MasteryAssessment.supporting_evidence.type",
                )
        return items

    @staticmethod
    def assert_reasons(
        reasons: list[AssessmentReason] | tuple[AssessmentReason, ...],
    ) -> tuple[AssessmentReason, ...]:
        items = tuple(reasons)
        for reason in items:
            if not isinstance(reason, AssessmentReason):
                raise EducationalInvariantViolation(
                    "reasons must contain AssessmentReason value objects",
                    invariant="MasteryAssessment.reasons.type",
                )
        return items
