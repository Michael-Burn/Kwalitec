"""Confidence and evidence quality tests for Exam Readiness (XP-003)."""

from __future__ import annotations

from application.student_experience.readiness import (
    AssessmentConfidenceCategory,
    ConsistencyBand,
    EvidenceQualityBand,
    EvidenceQuantityBand,
    ExamReadinessService,
)
from domain.education.mastery_estimation import AssessmentId
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.value_objects.learning_stability import (
    LearningStability,
)
from domain.education.mastery_estimation.value_objects.mastery_score import MasteryScore
from tests.application.student_experience.home.conftest import (
    AS_OF,
    STUDENT_ID,
    make_evaluation,
    make_mastery_confidence,
)
from tests.application.student_experience.readiness.conftest import (
    make_empty_inputs,
    make_full_inputs,
)


def test_confidence_projects_assessment_signals(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(make_full_inputs())
    confidence = view.confidence
    assert confidence.available is True
    assert confidence.assessment_confidence is AssessmentConfidenceCategory.HIGH
    assert confidence.assessment_confidence_label == "High"
    assert confidence.evidence_quality is EvidenceQualityBand.STRONG
    assert confidence.evidence_quantity is EvidenceQuantityBand.SUBSTANTIAL
    assert confidence.consistency is ConsistencyBand.CONSISTENT
    assert confidence.evidence_count >= 1
    assert "student confidence" not in confidence.message.lower()


def test_evidence_quality_card_mirrors_confidence(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(make_full_inputs())
    assert view.evidence_quality.available is True
    assert view.evidence_quality.quality is view.confidence.evidence_quality
    assert view.evidence_quality.quantity is view.confidence.evidence_quantity
    assert view.evidence_quality.evidence_count == view.confidence.evidence_count


def test_confidence_from_evaluation_when_no_assessment(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(
        make_empty_inputs(evaluation=make_evaluation(mastery_magnitude=0.55))
    )
    assert view.confidence.available is True
    assert (
        view.confidence.assessment_confidence
        is AssessmentConfidenceCategory.HIGH
    )


def test_limited_confidence_for_low_magnitude(
    service: ExamReadinessService,
) -> None:
    assessment = MasteryAssessment(
        assessment_id=AssessmentId("assessment-low-conf"),
        student_id=STUDENT_ID,
        assessed_at=AS_OF,
        overall_mastery=MasteryScore(magnitude=0.40, evidence_count=1),
        overall_confidence=make_mastery_confidence(magnitude=0.25, evidence_count=1),
        overall_stability=LearningStability.insufficient_data(),
        subject_assessments=(),
        knowledge_gaps=(),
    )
    view = service.build_readiness(make_empty_inputs(assessment=assessment))
    assert (
        view.confidence.assessment_confidence
        is AssessmentConfidenceCategory.LIMITED
    )
    assert view.confidence.evidence_quality is EvidenceQualityBand.LIMITED
    assert view.confidence.consistency is ConsistencyBand.UNKNOWN
    assert view.confidence.assessment_confidence_label == "Limited"


def test_confidence_unavailable_without_inputs(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(make_empty_inputs())
    assert view.confidence.available is False
    assert (
        view.confidence.assessment_confidence
        is AssessmentConfidenceCategory.UNKNOWN
    )
    assert view.evidence_quality.available is False
