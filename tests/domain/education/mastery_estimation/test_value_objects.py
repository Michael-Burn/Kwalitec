"""Unit tests for Mastery Estimation value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from domain.education.educational_evidence.enums import EvidenceType
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.educational_evidence.value_objects.evidence_timestamp import (
    EvidenceTimestamp,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.mastery_estimation.enums import (
    AssessmentReasonCode,
    KnowledgeGapKind,
    KnowledgeGapSeverity,
    LearningStabilityBand,
    MasteryBand,
)
from domain.education.mastery_estimation.ids import CompetencyId, SubjectId
from domain.education.mastery_estimation.value_objects.assessment_reason import (
    AssessmentReason,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.confidence_score import (
    ConfidenceScore,
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

AS_OF = datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)


def make_contribution(
    *,
    evidence_id: str = "ev-1",
    contribution: float = 1.0,
    weight: float = 0.5,
    occurred_at: datetime = AS_OF,
    evidence_type: EvidenceType = EvidenceType.QUESTION_ANSWERED,
) -> EvidenceContribution:
    return EvidenceContribution(
        evidence_id=EvidenceId(evidence_id),
        evidence_type=evidence_type,
        contribution=contribution,
        weight=weight,
        occurred_at=EvidenceTimestamp.of(occurred_at),
    )


class TestMasteryScore:
    def test_not_assessed_has_zero_evidence(self) -> None:
        score = MasteryScore.not_assessed()
        assert score.evidence_count == 0
        assert score.band is MasteryBand.NOT_ASSESSED

    def test_band_derived_from_magnitude_when_evidenced(self) -> None:
        assert MasteryScore(magnitude=0.10, evidence_count=1).band is (
            MasteryBand.NOT_STARTED
        )
        assert MasteryScore(magnitude=0.40, evidence_count=1).band is (
            MasteryBand.DEVELOPING
        )
        assert MasteryScore(magnitude=0.70, evidence_count=1).band is (
            MasteryBand.SECURE
        )
        assert MasteryScore(magnitude=0.90, evidence_count=1).band is (
            MasteryBand.MASTERED
        )

    def test_zero_evidence_is_always_not_assessed_regardless_of_magnitude(
        self,
    ) -> None:
        score = MasteryScore(magnitude=0.95, evidence_count=0)
        assert score.band is MasteryBand.NOT_ASSESSED

    def test_rejects_out_of_range_magnitude(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryScore(magnitude=1.5, evidence_count=1)
        with pytest.raises(EducationalInvariantViolation):
            MasteryScore(magnitude=-0.1, evidence_count=1)

    def test_rejects_negative_evidence_count(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryScore(magnitude=0.5, evidence_count=-1)

    def test_is_at_least(self) -> None:
        higher = MasteryScore(magnitude=0.8, evidence_count=1)
        lower = MasteryScore(magnitude=0.3, evidence_count=1)
        assert higher.is_at_least(lower)
        assert not lower.is_at_least(higher)

    def test_has_evidence(self) -> None:
        assert MasteryScore(magnitude=0.5, evidence_count=1).has_evidence()
        assert not MasteryScore.not_assessed().has_evidence()

    def test_is_immutable(self) -> None:
        score = MasteryScore(magnitude=0.5, evidence_count=1)
        with pytest.raises(FrozenInstanceError):
            score.magnitude = 0.9  # type: ignore[misc]


class TestConfidenceScore:
    def test_zero_factory(self) -> None:
        score = ConfidenceScore.zero()
        assert score.magnitude == 0.0
        assert score.band is ConfidenceLevel.VERY_LOW

    def test_band_thresholds(self) -> None:
        assert ConfidenceScore(magnitude=0.85).band is ConfidenceLevel.VERY_HIGH
        assert ConfidenceScore(magnitude=0.65).band is ConfidenceLevel.HIGH
        assert ConfidenceScore(magnitude=0.45).band is ConfidenceLevel.MEDIUM
        assert ConfidenceScore(magnitude=0.25).band is ConfidenceLevel.LOW
        assert ConfidenceScore(magnitude=0.05).band is ConfidenceLevel.VERY_LOW

    def test_rejects_out_of_range(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceScore(magnitude=1.1)

    def test_is_at_least(self) -> None:
        assert ConfidenceScore(magnitude=0.6).is_at_least(ConfidenceScore(0.5))


class TestLearningStability:
    def test_insufficient_data_factory(self) -> None:
        stability = LearningStability.insufficient_data()
        assert stability.band is LearningStabilityBand.INSUFFICIENT_DATA

    def test_below_min_evidence_is_always_insufficient(self) -> None:
        stability = LearningStability(magnitude=0.99, evidence_count=1, variance=0.0)
        assert stability.band is LearningStabilityBand.INSUFFICIENT_DATA

    def test_band_thresholds_with_enough_evidence(self) -> None:
        assert LearningStability(
            magnitude=0.90, evidence_count=3, variance=0.10
        ).band is LearningStabilityBand.STABLE
        assert LearningStability(
            magnitude=0.60, evidence_count=3, variance=0.40
        ).band is LearningStabilityBand.MODERATE
        assert LearningStability(
            magnitude=0.20, evidence_count=3, variance=0.80
        ).band is LearningStabilityBand.VOLATILE

    def test_rejects_out_of_range_variance(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningStability(magnitude=0.5, evidence_count=2, variance=1.5)


class TestEvidenceContribution:
    def test_directional_helpers(self) -> None:
        positive = make_contribution(contribution=0.6)
        negative = make_contribution(contribution=-0.6)
        neutral = make_contribution(contribution=0.0)
        assert positive.is_positive() and not positive.is_negative()
        assert negative.is_negative() and not negative.is_positive()
        assert neutral.is_neutral()

    def test_weighted_magnitude(self) -> None:
        contribution = make_contribution(contribution=0.5, weight=0.4)
        assert contribution.weighted_magnitude() == pytest.approx(0.2)

    def test_rejects_out_of_range_contribution(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_contribution(contribution=1.5)

    def test_rejects_out_of_range_weight(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_contribution(weight=-0.1)

    def test_rejects_wrong_types(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContribution(
                evidence_id="not-an-id",  # type: ignore[arg-type]
                evidence_type=EvidenceType.QUESTION_ANSWERED,
                contribution=0.5,
                weight=0.5,
                occurred_at=EvidenceTimestamp.of(AS_OF),
            )


class TestKnowledgeGap:
    def test_weak_evidence_gap_has_no_relation(self) -> None:
        gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MODERATE,
            mastery_score=MasteryScore(magnitude=0.3, evidence_count=2),
        )
        assert gap.is_direct_gap()
        assert not gap.is_prerequisite_gap()

    def test_weak_prerequisite_gap_requires_relation_fields(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id=CompetencyId("comp-1"),
                kind=KnowledgeGapKind.WEAK_PREREQUISITE,
                severity=KnowledgeGapSeverity.SEVERE,
                mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            )

    def test_weak_prerequisite_gap_requires_dependency_strength(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id=CompetencyId("comp-1"),
                kind=KnowledgeGapKind.WEAK_PREREQUISITE,
                severity=KnowledgeGapSeverity.SEVERE,
                mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
                related_competency_id=CompetencyId("comp-2"),
            )

    def test_weak_prerequisite_gap_well_formed(self) -> None:
        gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            related_competency_id=CompetencyId("comp-2"),
            dependency_strength=DependencyStrength.critical(),
        )
        assert gap.is_prerequisite_gap()

    def test_related_competency_must_differ_from_competency(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id=CompetencyId("comp-1"),
                kind=KnowledgeGapKind.WEAK_PREREQUISITE,
                severity=KnowledgeGapSeverity.SEVERE,
                mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
                related_competency_id=CompetencyId("comp-1"),
                dependency_strength=DependencyStrength.critical(),
            )


class TestAssessmentReason:
    def test_minimal_reason(self) -> None:
        reason = AssessmentReason(
            reason_code=AssessmentReasonCode.INSUFFICIENT_EVIDENCE
        )
        assert reason.subject_id is None
        assert reason.competency_id is None
        assert reason.detail is None

    def test_reason_with_scoping_and_detail(self) -> None:
        reason = AssessmentReason(
            reason_code=AssessmentReasonCode.CONTRADICTORY_EVIDENCE,
            subject_id=SubjectId("algebra"),
            competency_id=CompetencyId("comp-1"),
            detail=0.5,
        )
        assert reason.detail == 0.5

    def test_rejects_wrong_reason_code_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentReason(reason_code="not-a-code")  # type: ignore[arg-type]


class TestMasteryConfidence:
    def test_zero_factory(self) -> None:
        confidence = MasteryConfidence.zero()
        assert confidence.evidence_count == 0
        assert not confidence.is_contradicted()

    def test_is_contradicted(self) -> None:
        confidence = MasteryConfidence(
            score=ConfidenceScore(magnitude=0.5),
            evidence_count=2,
            contradiction_ratio=0.3,
        )
        assert confidence.is_contradicted()

    def test_rejects_out_of_range_contradiction_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryConfidence(
                score=ConfidenceScore.zero(),
                contradiction_ratio=1.5,
            )

    def test_rejects_negative_evidence_count(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryConfidence(score=ConfidenceScore.zero(), evidence_count=-1)


class TestCompetencyAssessment:
    def _base_kwargs(self) -> dict:
        return {
            "competency_id": CompetencyId("comp-1"),
            "subject_id": SubjectId("algebra"),
            "mastery": MasteryScore(magnitude=0.4, evidence_count=2),
            "confidence": MasteryConfidence.zero(),
            "stability": LearningStability.insufficient_data(),
        }

    def test_direct_gap_must_reference_own_competency(self) -> None:
        mismatched_gap = KnowledgeGap(
            competency_id=CompetencyId("other-comp"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MINOR,
            mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
        )
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._base_kwargs(), gaps=(mismatched_gap,))

    def test_prerequisite_gap_must_reference_own_competency_as_dependent(
        self,
    ) -> None:
        mismatched_gap = KnowledgeGap(
            competency_id=CompetencyId("prereq"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            related_competency_id=CompetencyId("some-other-competency"),
            dependency_strength=DependencyStrength.critical(),
        )
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._base_kwargs(), gaps=(mismatched_gap,))

    def test_helper_methods(self) -> None:
        direct_gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MINOR,
            mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
        )
        prereq_gap = KnowledgeGap(
            competency_id=CompetencyId("prereq"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            related_competency_id=CompetencyId("comp-1"),
            dependency_strength=DependencyStrength.critical(),
        )
        contribution = make_contribution()
        assessment = CompetencyAssessment(
            **self._base_kwargs(),
            supporting_evidence=(contribution,),
            gaps=(direct_gap, prereq_gap),
        )
        assert assessment.has_gaps()
        assert assessment.direct_gaps() == (direct_gap,)
        assert assessment.weak_prerequisites() == (prereq_gap,)
        assert assessment.evidence_count() == 1


class TestSubjectAssessment:
    def test_rejects_competency_assessment_from_different_subject(self) -> None:
        mismatched = CompetencyAssessment(
            competency_id=CompetencyId("comp-1"),
            subject_id=SubjectId("geometry"),
            mastery=MasteryScore.not_assessed(),
            confidence=MasteryConfidence.zero(),
            stability=LearningStability.insufficient_data(),
        )
        with pytest.raises(EducationalInvariantViolation):
            SubjectAssessment(
                subject_id=SubjectId("algebra"),
                mastery=MasteryScore.not_assessed(),
                confidence=MasteryConfidence.zero(),
                stability=LearningStability.insufficient_data(),
                competency_assessments=(mismatched,),
            )

    def test_rejects_duplicate_competency_ids(self) -> None:
        one = CompetencyAssessment(
            competency_id=CompetencyId("comp-1"),
            subject_id=SubjectId("algebra"),
            mastery=MasteryScore.not_assessed(),
            confidence=MasteryConfidence.zero(),
            stability=LearningStability.insufficient_data(),
        )
        duplicate = CompetencyAssessment(
            competency_id=CompetencyId("comp-1"),
            subject_id=SubjectId("algebra"),
            mastery=MasteryScore(magnitude=0.5, evidence_count=1),
            confidence=MasteryConfidence.zero(),
            stability=LearningStability.insufficient_data(),
        )
        with pytest.raises(EducationalInvariantViolation):
            SubjectAssessment(
                subject_id=SubjectId("algebra"),
                mastery=MasteryScore.not_assessed(),
                confidence=MasteryConfidence.zero(),
                stability=LearningStability.insufficient_data(),
                competency_assessments=(one, duplicate),
            )

    def test_lookup_and_aggregation_helpers(self) -> None:
        contribution = make_contribution()
        gap = KnowledgeGap(
            competency_id=CompetencyId("comp-1"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MINOR,
            mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
        )
        competency_assessment = CompetencyAssessment(
            competency_id=CompetencyId("comp-1"),
            subject_id=SubjectId("algebra"),
            mastery=MasteryScore(magnitude=0.4, evidence_count=1),
            confidence=MasteryConfidence.zero(),
            stability=LearningStability.insufficient_data(),
            supporting_evidence=(contribution,),
            gaps=(gap,),
        )
        subject_assessment = SubjectAssessment(
            subject_id=SubjectId("algebra"),
            mastery=MasteryScore(magnitude=0.4, evidence_count=1),
            confidence=MasteryConfidence.zero(),
            stability=LearningStability.insufficient_data(),
            competency_assessments=(competency_assessment,),
        )
        assert subject_assessment.competency_count() == 1
        assert (
            subject_assessment.competency_assessment_for(CompetencyId("comp-1"))
            is competency_assessment
        )
        assert subject_assessment.competency_assessment_for("missing") is None
        assert subject_assessment.knowledge_gaps() == (gap,)
        assert subject_assessment.weak_prerequisites() == ()
        assert subject_assessment.supporting_evidence() == (contribution,)
