"""Unit tests for the MasteryAssessment aggregate."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
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
from domain.education.mastery_estimation.policies.assessment_validation_policy import (  # noqa: E501
    AssessmentValidationPolicy,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
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


def make_competency_assessment(
    *,
    competency_id: str = "comp-1",
    subject_id: str = "algebra",
    magnitude: float = 0.4,
    evidence_count: int = 1,
    gaps: tuple[KnowledgeGap, ...] = (),
) -> CompetencyAssessment:
    return CompetencyAssessment(
        competency_id=CompetencyId(competency_id),
        subject_id=SubjectId(subject_id),
        mastery=MasteryScore(magnitude=magnitude, evidence_count=evidence_count),
        confidence=MasteryConfidence.zero(),
        stability=LearningStability.insufficient_data(),
        gaps=gaps,
    )


def make_subject_assessment(
    *,
    subject_id: str = "algebra",
    competency_assessments: tuple[CompetencyAssessment, ...] = (),
) -> SubjectAssessment:
    return SubjectAssessment(
        subject_id=SubjectId(subject_id),
        mastery=MasteryScore(magnitude=0.4, evidence_count=1),
        confidence=MasteryConfidence.zero(),
        stability=LearningStability.insufficient_data(),
        competency_assessments=competency_assessments,
    )


def minimal_assessment_kwargs() -> dict:
    return {
        "assessment_id": AssessmentId("assessment-1"),
        "student_id": "student-001",
        "assessed_at": AS_OF,
        "overall_mastery": MasteryScore.not_assessed(),
        "overall_confidence": MasteryConfidence.zero(),
        "overall_stability": LearningStability.insufficient_data(),
    }


class TestMasteryAssessmentConstruction:
    def test_minimal_construction(self) -> None:
        assessment = MasteryAssessment(**minimal_assessment_kwargs())
        assert assessment.subject_count() == 0
        assert not assessment.has_knowledge_gaps()

    def test_rejects_wrong_assessment_id_type(self) -> None:
        kwargs = minimal_assessment_kwargs()
        kwargs["assessment_id"] = "not-an-id"
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)

    def test_rejects_blank_student_id(self) -> None:
        kwargs = minimal_assessment_kwargs()
        kwargs["student_id"] = "  "
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)

    def test_rejects_non_datetime_assessed_at(self) -> None:
        kwargs = minimal_assessment_kwargs()
        kwargs["assessed_at"] = "not-a-datetime"
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)

    def test_rejects_wrong_overall_mastery_type(self) -> None:
        kwargs = minimal_assessment_kwargs()
        kwargs["overall_mastery"] = 0.5
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)

    def test_rejects_duplicate_subject_assessments(self) -> None:
        subject_assessment = make_subject_assessment()
        kwargs = minimal_assessment_kwargs()
        kwargs["subject_assessments"] = (subject_assessment, subject_assessment)
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)

    def test_rejects_wrong_subject_assessment_member_type(self) -> None:
        kwargs = minimal_assessment_kwargs()
        kwargs["subject_assessments"] = ("not-a-subject-assessment",)
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)

    def test_rejects_knowledge_gap_referencing_untracked_competency(self) -> None:
        gap = KnowledgeGap(
            competency_id=CompetencyId("untracked"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MINOR,
            mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
        )
        kwargs = minimal_assessment_kwargs()
        kwargs["knowledge_gaps"] = (gap,)
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)

    def test_accepts_knowledge_gap_referencing_tracked_competency(self) -> None:
        gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MINOR,
            mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
        )
        competency_assessment = make_competency_assessment(gaps=(gap,))
        subject_assessment = make_subject_assessment(
            competency_assessments=(competency_assessment,)
        )
        kwargs = minimal_assessment_kwargs()
        kwargs["subject_assessments"] = (subject_assessment,)
        kwargs["knowledge_gaps"] = (gap,)
        assessment = MasteryAssessment(**kwargs)
        assert assessment.has_knowledge_gaps()

    def test_rejects_wrong_supporting_evidence_member_type(self) -> None:
        kwargs = minimal_assessment_kwargs()
        kwargs["supporting_evidence"] = ("not-a-contribution",)
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)

    def test_rejects_wrong_reason_member_type(self) -> None:
        kwargs = minimal_assessment_kwargs()
        kwargs["reasons"] = ("not-a-reason",)
        with pytest.raises(EducationalInvariantViolation):
            MasteryAssessment(**kwargs)


class TestMasteryAssessmentBehaviour:
    def _assessment_with_gaps(self) -> MasteryAssessment:
        direct_gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MINOR,
            mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
        )
        from domain.education.knowledge_graph.value_objects.dependency_strength import (
            DependencyStrength,
        )

        prereq_gap = KnowledgeGap(
            competency_id=CompetencyId("comp-2"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            related_competency_id=CompetencyId("comp-1"),
            dependency_strength=DependencyStrength.critical(),
        )
        competency_assessment = make_competency_assessment(
            gaps=(direct_gap, prereq_gap)
        )
        subject_assessment = make_subject_assessment(
            competency_assessments=(competency_assessment,)
        )
        kwargs = minimal_assessment_kwargs()
        kwargs["subject_assessments"] = (subject_assessment,)
        kwargs["knowledge_gaps"] = (direct_gap, prereq_gap)
        return MasteryAssessment(**kwargs)

    def test_weak_prerequisites_and_direct_gaps_filter_correctly(self) -> None:
        assessment = self._assessment_with_gaps()
        assert len(assessment.weak_prerequisites()) == 1
        assert len(assessment.direct_gaps()) == 1

    def test_subject_and_competency_lookup(self) -> None:
        assessment = self._assessment_with_gaps()
        assert assessment.subject_assessment_for(SubjectId("algebra")) is not None
        assert assessment.subject_assessment_for("missing") is None
        assert assessment.competency_assessment_for(CompetencyId("comp-1")) is not None
        assert assessment.competency_assessment_for("missing") is None

    def test_produce_snapshot_mirrors_assessment(self) -> None:
        assessment = self._assessment_with_gaps()
        snapshot = assessment.produce_snapshot()
        assert snapshot.assessment_id == assessment.assessment_id
        assert snapshot.student_id == assessment.student_id
        assert snapshot.subject_assessments == assessment.subject_assessments
        assert snapshot.knowledge_gaps == assessment.knowledge_gaps

    def test_equality_is_structural(self) -> None:
        first = MasteryAssessment(**minimal_assessment_kwargs())
        second = MasteryAssessment(**minimal_assessment_kwargs())
        assert first == second
        assert hash(first) == hash(second)

    def test_inequality_with_different_type(self) -> None:
        assessment = MasteryAssessment(**minimal_assessment_kwargs())
        assert assessment != "not-an-assessment"

    def test_repr_contains_key_fields(self) -> None:
        assessment = MasteryAssessment(**minimal_assessment_kwargs())
        text = repr(assessment)
        assert "MasteryAssessment" in text
        assert "student-001" in text

    def test_public_properties_expose_immutable_tuples(self) -> None:
        assessment = self._assessment_with_gaps()
        subjects = assessment.subject_assessments
        assert isinstance(subjects, tuple)
        assert subjects == assessment.subject_assessments


class TestAssessmentValidationPolicyDirectly:
    def test_assert_identity_rejects_non_assessment_id(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentValidationPolicy.assert_identity("not-an-id")

    def test_assert_student_id_rejects_blank(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentValidationPolicy.assert_student_id("   ")

    def test_assert_assessed_at_rejects_non_datetime(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentValidationPolicy.assert_assessed_at("not-a-datetime")

    def test_assert_overall_confidence_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentValidationPolicy.assert_overall_confidence(0.5)

    def test_assert_overall_stability_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentValidationPolicy.assert_overall_stability(0.5)

    def test_assert_subject_assessments_passthrough(self) -> None:
        subject_assessment = make_subject_assessment()
        result = AssessmentValidationPolicy.assert_subject_assessments(
            [subject_assessment]
        )
        assert result == (subject_assessment,)
