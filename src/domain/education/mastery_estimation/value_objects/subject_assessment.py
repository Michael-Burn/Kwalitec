"""Subject assessment — computed mastery aggregated across one subject.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Subject Assessment
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.ids import SubjectId
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
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
class SubjectAssessment(EducationalValueObject):
    """Immutable mastery assessment aggregated across one subject.

    The subject-level mastery, confidence, and stability are always
    derived from the subject's own competency assessments — never
    estimated independently — so a subject assessment can never disagree
    with the competencies that compose it.
    """

    subject_id: SubjectId
    mastery: MasteryScore
    confidence: MasteryConfidence
    stability: LearningStability
    competency_assessments: tuple[CompetencyAssessment, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.subject_id, SubjectId):
            raise EducationalInvariantViolation(
                "subject_id must be a SubjectId",
                invariant="SubjectAssessment.subject_id.type",
            )
        if not isinstance(self.mastery, MasteryScore):
            raise EducationalInvariantViolation(
                "mastery must be a MasteryScore",
                invariant="SubjectAssessment.mastery.type",
            )
        if not isinstance(self.confidence, MasteryConfidence):
            raise EducationalInvariantViolation(
                "confidence must be a MasteryConfidence",
                invariant="SubjectAssessment.confidence.type",
            )
        if not isinstance(self.stability, LearningStability):
            raise EducationalInvariantViolation(
                "stability must be a LearningStability",
                invariant="SubjectAssessment.stability.type",
            )
        object.__setattr__(
            self, "competency_assessments", tuple(self.competency_assessments)
        )
        seen: set[str] = set()
        for assessment in self.competency_assessments:
            if not isinstance(assessment, CompetencyAssessment):
                raise EducationalInvariantViolation(
                    "competency_assessments must contain "
                    "CompetencyAssessment value objects",
                    invariant=(
                        "SubjectAssessment.competency_assessments.type"
                    ),
                )
            if assessment.subject_id != self.subject_id:
                raise EducationalInvariantViolation(
                    "every competency assessment must belong to this "
                    "subject",
                    invariant=(
                        "SubjectAssessment.competency_assessments.subject"
                    ),
                )
            key = assessment.competency_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate competency_id in subject assessment",
                    invariant=(
                        "SubjectAssessment.competency_assessments.unique"
                    ),
                )
            seen.add(key)

    def competency_count(self) -> int:
        return len(self.competency_assessments)

    def competency_assessment_for(
        self, competency_id: object
    ) -> CompetencyAssessment | None:
        key = (
            competency_id.value
            if hasattr(competency_id, "value")
            else competency_id
        )
        for assessment in self.competency_assessments:
            if assessment.competency_id.value == key:
                return assessment
        return None

    def knowledge_gaps(self) -> tuple[KnowledgeGap, ...]:
        return tuple(
            gap
            for assessment in self.competency_assessments
            for gap in assessment.gaps
        )

    def weak_prerequisites(self) -> tuple[KnowledgeGap, ...]:
        return tuple(
            gap
            for assessment in self.competency_assessments
            for gap in assessment.weak_prerequisites()
        )

    def supporting_evidence(self) -> tuple[EvidenceContribution, ...]:
        return tuple(
            contribution
            for assessment in self.competency_assessments
            for contribution in assessment.supporting_evidence
        )
