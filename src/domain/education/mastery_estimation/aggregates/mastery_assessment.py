"""MasteryAssessment aggregate — the Mastery Estimation Engine's product.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
    STUDENT_DIGITAL_TWIN.md
Concept
    Mastery Assessment

MasteryAssessment represents educational reasoning, not storage: a
deterministic, explainable judgement of a student's mastery, confidence,
stability, and knowledge gaps at one point in time.
"""

from __future__ import annotations

from datetime import datetime

from domain.education.mastery_estimation.enums import KnowledgeGapKind
from domain.education.mastery_estimation.ids import AssessmentId
from domain.education.mastery_estimation.policies.assessment_validation_policy import (  # noqa: E501
    AssessmentValidationPolicy,
)
from domain.education.mastery_estimation.value_objects.assessment_reason import (
    AssessmentReason,
)
from domain.education.mastery_estimation.value_objects.assessment_snapshot import (
    AssessmentSnapshot,
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


class MasteryAssessment:
    """Aggregate root modelling one deterministic mastery assessment.

    MasteryAssessment is the Mastery Estimation Engine's product: an
    immutable, explainable judgement of a student's mastery, confidence,
    stability, and knowledge gaps, built entirely from a
    ``StudentEducationalState``, a collection of ``EducationalEvidence``,
    and a ``KnowledgeGraph`` at one caller-supplied point in time.

    It never mutates after construction — a revised assessment is always a
    new instance, never a silent edit — and it never persists itself,
    orchestrates, mutates ``StudentEducationalState``, mutates the
    knowledge graph, or produces recommendations or missions.
    """

    def __init__(
        self,
        assessment_id: AssessmentId,
        student_id: str,
        assessed_at: datetime,
        *,
        overall_mastery: MasteryScore,
        overall_confidence: MasteryConfidence,
        overall_stability: LearningStability,
        subject_assessments: list[SubjectAssessment]
        | tuple[SubjectAssessment, ...] = (),
        knowledge_gaps: list[KnowledgeGap] | tuple[KnowledgeGap, ...] = (),
        supporting_evidence: list[EvidenceContribution]
        | tuple[EvidenceContribution, ...] = (),
        reasons: list[AssessmentReason] | tuple[AssessmentReason, ...] = (),
    ) -> None:
        self._assessment_id = AssessmentValidationPolicy.assert_identity(
            assessment_id
        )
        self._student_id = AssessmentValidationPolicy.assert_student_id(student_id)
        self._assessed_at = AssessmentValidationPolicy.assert_assessed_at(
            assessed_at
        )
        self._overall_mastery = AssessmentValidationPolicy.assert_overall_mastery(
            overall_mastery
        )
        self._overall_confidence = (
            AssessmentValidationPolicy.assert_overall_confidence(
                overall_confidence
            )
        )
        self._overall_stability = (
            AssessmentValidationPolicy.assert_overall_stability(overall_stability)
        )
        self._subject_assessments = (
            AssessmentValidationPolicy.assert_subject_assessments(
                subject_assessments
            )
        )
        self._knowledge_gaps = AssessmentValidationPolicy.assert_knowledge_gaps(
            knowledge_gaps, self._subject_assessments
        )
        self._supporting_evidence = (
            AssessmentValidationPolicy.assert_supporting_evidence(
                supporting_evidence
            )
        )
        self._reasons = AssessmentValidationPolicy.assert_reasons(reasons)

    # --- identity / read models (no setters; assessments are immutable) ---

    @property
    def assessment_id(self) -> AssessmentId:
        return self._assessment_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def assessed_at(self) -> datetime:
        return self._assessed_at

    @property
    def overall_mastery(self) -> MasteryScore:
        return self._overall_mastery

    @property
    def overall_confidence(self) -> MasteryConfidence:
        return self._overall_confidence

    @property
    def overall_stability(self) -> LearningStability:
        return self._overall_stability

    @property
    def subject_assessments(self) -> tuple[SubjectAssessment, ...]:
        return tuple(self._subject_assessments)

    @property
    def knowledge_gaps(self) -> tuple[KnowledgeGap, ...]:
        return tuple(self._knowledge_gaps)

    @property
    def supporting_evidence(self) -> tuple[EvidenceContribution, ...]:
        return tuple(self._supporting_evidence)

    @property
    def reasons(self) -> tuple[AssessmentReason, ...]:
        return tuple(self._reasons)

    def subject_count(self) -> int:
        return len(self._subject_assessments)

    def subject_assessment_for(self, subject_id: object) -> SubjectAssessment | None:
        key = subject_id.value if hasattr(subject_id, "value") else subject_id
        for assessment in self._subject_assessments:
            if assessment.subject_id.value == key:
                return assessment
        return None

    def competency_assessment_for(self, competency_id: object):
        key = (
            competency_id.value
            if hasattr(competency_id, "value")
            else competency_id
        )
        for subject_assessment in self._subject_assessments:
            found = subject_assessment.competency_assessment_for(key)
            if found is not None:
                return found
        return None

    def weak_prerequisites(self) -> tuple[KnowledgeGap, ...]:
        return tuple(
            gap
            for gap in self._knowledge_gaps
            if gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE
        )

    def direct_gaps(self) -> tuple[KnowledgeGap, ...]:
        return tuple(
            gap
            for gap in self._knowledge_gaps
            if gap.kind is KnowledgeGapKind.WEAK_EVIDENCE
        )

    def has_knowledge_gaps(self) -> bool:
        return len(self._knowledge_gaps) > 0

    def produce_snapshot(self) -> AssessmentSnapshot:
        """Produce an immutable, accurate snapshot of this assessment."""
        return AssessmentSnapshot(
            assessment_id=self._assessment_id,
            student_id=self._student_id,
            overall_mastery=self._overall_mastery,
            overall_confidence=self._overall_confidence,
            overall_stability=self._overall_stability,
            subject_assessments=tuple(self._subject_assessments),
            knowledge_gaps=tuple(self._knowledge_gaps),
            supporting_evidence=tuple(self._supporting_evidence),
            reasons=tuple(self._reasons),
            assessed_at=self._assessed_at,
        )

    # --- structural equality (an assessment is compared by content, not
    #     just identity, so determinism can be verified meaningfully) ---

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, MasteryAssessment):
            return NotImplemented
        return (
            self._assessment_id == other._assessment_id
            and self._student_id == other._student_id
            and self._assessed_at == other._assessed_at
            and self._overall_mastery == other._overall_mastery
            and self._overall_confidence == other._overall_confidence
            and self._overall_stability == other._overall_stability
            and self._subject_assessments == other._subject_assessments
            and self._knowledge_gaps == other._knowledge_gaps
            and self._supporting_evidence == other._supporting_evidence
            and self._reasons == other._reasons
        )

    def __hash__(self) -> int:
        return hash((type(self), self._assessment_id))

    def __repr__(self) -> str:
        return (
            f"MasteryAssessment(assessment_id={self._assessment_id!r}, "
            f"student_id={self._student_id!r}, "
            f"overall_mastery={self._overall_mastery!r}, "
            f"subjects={len(self._subject_assessments)}, "
            f"knowledge_gaps={len(self._knowledge_gaps)})"
        )
