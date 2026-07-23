"""Unit tests for Mastery Estimation specifications."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.enums import (
    KnowledgeGapKind,
    KnowledgeGapSeverity,
)
from domain.education.mastery_estimation.ids import (
    AssessmentId,
    CompetencyId,
    SubjectId,
)
from domain.education.mastery_estimation.specifications.assessment_confidence_specification import (  # noqa: E501
    AssessmentConfidenceSpecification,
)
from domain.education.mastery_estimation.specifications.knowledge_gap_specification import (  # noqa: E501
    KnowledgeGapSpecification,
)
from domain.education.mastery_estimation.specifications.mastery_assessment_consistency_specification import (  # noqa: E501
    MasteryAssessmentConsistencySpecification,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.confidence_score import (
    ConfidenceScore,
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

AS_OF = datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)


def _competency_assessment(
    *, magnitude: float, evidence_count: int, competency_id: str = "comp-1"
) -> CompetencyAssessment:
    return CompetencyAssessment(
        competency_id=CompetencyId(competency_id),
        subject_id=SubjectId("algebra"),
        mastery=MasteryScore(magnitude=magnitude, evidence_count=evidence_count),
        confidence=MasteryConfidence(
            score=ConfidenceScore(magnitude=0.6), evidence_count=evidence_count
        ),
        stability=LearningStability.insufficient_data(),
    )


class TestMasteryAssessmentConsistencySpecification:
    def test_correctly_aggregated_assessment_is_satisfied(self) -> None:
        competency_a = _competency_assessment(
            magnitude=1.0, evidence_count=1, competency_id="comp-1"
        )
        competency_b = _competency_assessment(
            magnitude=0.0, evidence_count=3, competency_id="comp-2"
        )
        subject_assessment = SubjectAssessment(
            subject_id=SubjectId("algebra"),
            mastery=MasteryScore(magnitude=0.25, evidence_count=4),
            confidence=MasteryConfidence(
                score=ConfidenceScore(magnitude=0.6), evidence_count=4
            ),
            stability=LearningStability.insufficient_data(),
            competency_assessments=(competency_a, competency_b),
        )
        assessment = MasteryAssessment(
            assessment_id=AssessmentId("assessment-1"),
            student_id="student-001",
            assessed_at=AS_OF,
            overall_mastery=MasteryScore(magnitude=0.25, evidence_count=4),
            overall_confidence=MasteryConfidence(
                score=ConfidenceScore(magnitude=0.6), evidence_count=4
            ),
            overall_stability=LearningStability.insufficient_data(),
            subject_assessments=(subject_assessment,),
        )
        assert MasteryAssessmentConsistencySpecification.is_satisfied_by(assessment)
        MasteryAssessmentConsistencySpecification.assert_satisfied_by(assessment)

    def test_drifted_overall_mastery_is_not_satisfied(self) -> None:
        competency = _competency_assessment(magnitude=1.0, evidence_count=1)
        subject_assessment = SubjectAssessment(
            subject_id=SubjectId("algebra"),
            mastery=MasteryScore(magnitude=1.0, evidence_count=1),
            confidence=MasteryConfidence.zero(),
            stability=LearningStability.insufficient_data(),
            competency_assessments=(competency,),
        )
        assessment = MasteryAssessment(
            assessment_id=AssessmentId("assessment-1"),
            student_id="student-001",
            assessed_at=AS_OF,
            overall_mastery=MasteryScore(magnitude=0.10, evidence_count=1),
            overall_confidence=MasteryConfidence.zero(),
            overall_stability=LearningStability.insufficient_data(),
            subject_assessments=(subject_assessment,),
        )
        assert not MasteryAssessmentConsistencySpecification.is_satisfied_by(
            assessment
        )
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessmentConsistencySpecification.assert_satisfied_by(assessment)

    def test_empty_assessment_is_satisfied(self) -> None:
        assessment = MasteryAssessment(
            assessment_id=AssessmentId("assessment-1"),
            student_id="student-001",
            assessed_at=AS_OF,
            overall_mastery=MasteryScore.not_assessed(),
            overall_confidence=MasteryConfidence.zero(),
            overall_stability=LearningStability.insufficient_data(),
        )
        assert MasteryAssessmentConsistencySpecification.is_satisfied_by(assessment)


class TestAssessmentConfidenceSpecification:
    def test_zero_evidence_zero_confidence_is_satisfied(self) -> None:
        confidence = MasteryConfidence.zero()
        assert AssessmentConfidenceSpecification.is_satisfied_by(confidence)

    def test_zero_evidence_nonzero_confidence_is_not_satisfied(self) -> None:
        confidence = MasteryConfidence(
            score=ConfidenceScore(magnitude=0.5), evidence_count=0
        )
        assert not AssessmentConfidenceSpecification.is_satisfied_by(confidence)
        with pytest.raises(EducationalInvariantViolation):
            AssessmentConfidenceSpecification.assert_satisfied_by(confidence)

    def test_fully_contradictory_evidence_cannot_be_maximal_confidence(self) -> None:
        confidence = MasteryConfidence(
            score=ConfidenceScore(magnitude=1.0),
            evidence_count=2,
            contradiction_ratio=1.0,
        )
        assert not AssessmentConfidenceSpecification.is_satisfied_by(confidence)

    def test_fully_contradictory_evidence_with_eroded_confidence_is_satisfied(
        self,
    ) -> None:
        confidence = MasteryConfidence(
            score=ConfidenceScore(magnitude=0.4),
            evidence_count=2,
            contradiction_ratio=1.0,
        )
        assert AssessmentConfidenceSpecification.is_satisfied_by(confidence)

    def test_ordinary_confidence_is_satisfied(self) -> None:
        confidence = MasteryConfidence(
            score=ConfidenceScore(magnitude=0.7),
            evidence_count=3,
            contradiction_ratio=0.2,
        )
        assert AssessmentConfidenceSpecification.is_satisfied_by(confidence)


class TestKnowledgeGapSpecification:
    def test_well_formed_direct_gap_is_satisfied(self) -> None:
        gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MODERATE,
            mastery_score=MasteryScore(magnitude=0.3, evidence_count=2),
        )
        assert KnowledgeGapSpecification.is_satisfied_by(gap)
        KnowledgeGapSpecification.assert_satisfied_by(gap)

    def test_gap_without_evidence_is_not_satisfied(self) -> None:
        gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MODERATE,
            mastery_score=MasteryScore.not_assessed(),
        )
        assert not KnowledgeGapSpecification.is_satisfied_by(gap)
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGapSpecification.assert_satisfied_by(gap)

    def test_gap_at_or_above_secure_threshold_is_not_satisfied(self) -> None:
        gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MINOR,
            mastery_score=MasteryScore(magnitude=0.65, evidence_count=2),
        )
        assert not KnowledgeGapSpecification.is_satisfied_by(gap)

    def test_well_formed_prerequisite_gap_is_satisfied(self) -> None:
        gap = KnowledgeGap(
            competency_id=CompetencyId("prereq"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            related_competency_id=CompetencyId("dependent"),
            dependency_strength=DependencyStrength.critical(),
        )
        assert KnowledgeGapSpecification.is_satisfied_by(gap)
