"""Missing optional inputs degrade gracefully for Exam Readiness (XP-003)."""

from __future__ import annotations

from application.student_experience.readiness import (
    AssessmentConfidenceCategory,
    ExamReadinessService,
    ReadinessCategory,
    ReadinessDirection,
)
from tests.application.student_experience.home.conftest import (
    make_assessment,
    make_exam_target,
)
from tests.application.student_experience.readiness.conftest import make_empty_inputs


def test_empty_inputs_produce_unavailable_readiness(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(make_empty_inputs())
    assert view.readiness.available is False
    assert view.readiness.readiness_category is ReadinessCategory.UNAVAILABLE
    assert view.readiness.direction is ReadinessDirection.UNKNOWN
    assert view.confidence.available is False
    assert view.strengths.has_strengths is False
    assert view.risks.has_risks is False
    assert view.action_plan.has_actions is False
    assert view.upcoming_milestones.has_milestones is False
    assert view.evidence_quality.available is False


def test_assessment_without_exam_still_projects_percent(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(
        make_empty_inputs(assessment=make_assessment(overall_mastery=0.55))
    )
    assert view.readiness.available is True
    assert view.readiness.readiness_percent == 55.0
    assert view.readiness.readiness_category is ReadinessCategory.APPROACHING
    assert view.readiness.target_exam_label is None
    assert view.readiness.days_remaining is None
    assert view.confidence.assessment_confidence is not (
        AssessmentConfidenceCategory.UNKNOWN
    )


def test_exam_target_without_assessment_shows_countdown(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(
        make_empty_inputs(exam_target=make_exam_target())
    )
    assert view.readiness.available is True
    assert view.readiness.readiness_percent is None
    assert view.readiness.days_remaining == 45
    assert view.readiness.target_exam_label is not None
    assert view.upcoming_milestones.has_milestones is True
