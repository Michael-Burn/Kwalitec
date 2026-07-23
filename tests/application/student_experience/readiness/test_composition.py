"""Exam Readiness composition tests (XP-003)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.student_experience.readiness import (
    ActionPlanItemKind,
    AssessmentConfidenceCategory,
    ExamReadinessService,
    ReadinessCategory,
    ReadinessDirection,
    ReadinessId,
    ReadinessMilestoneKind,
)
from tests.application.student_experience.readiness.conftest import (
    STUDENT_ID,
    RecordingReadinessPublisher,
    make_full_inputs,
)


def test_build_readiness_composes_all_sections(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(
        make_full_inputs(), readiness_id=ReadinessId("readiness-001")
    )

    assert view.student_id == STUDENT_ID
    assert view.readiness_id.value == "readiness-001"
    assert view.readiness.available is True
    assert view.readiness.readiness_percent == 72.0
    assert view.readiness.readiness_category is ReadinessCategory.APPROACHING
    assert view.readiness.days_remaining == 10
    assert view.trend.has_trend_data is True
    assert view.confidence.available is True
    assert view.strengths.has_strengths is True
    assert view.risks.has_risks is True
    assert view.action_plan.has_actions is True
    assert view.upcoming_milestones.has_milestones is True
    assert view.evidence_quality.available is True


def test_readiness_never_exposes_domain_type_names(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(make_full_inputs())
    blob = " ".join(
        [
            view.readiness.readiness_label,
            view.readiness.direction_message,
            view.trend.summary,
            view.confidence.message,
            view.strengths.summary,
            *(item.message for item in view.strengths.items),
            view.risks.summary,
            *(item.message for item in view.risks.items),
            view.action_plan.summary,
            *(item.guidance for item in view.action_plan.items),
            view.upcoming_milestones.summary,
            *(item.detail for item in view.upcoming_milestones.milestones),
            view.evidence_quality.message,
        ]
    )
    for forbidden in (
        "MasteryAssessment",
        "RecommendationSet",
        "MissionPlan",
        "EducationalEvaluation",
        "StudySchedule",
        "MissionExecution",
        "ExecutionHistory",
        "HomeSnapshot",
        "JourneySnapshot",
        "Education OS",
    ):
        assert forbidden not in blob


def test_action_plan_composes_existing_recommendations(
    service: ExamReadinessService,
) -> None:
    plan = service.compose_action_plan(make_full_inputs())
    assert plan.has_actions is True
    kinds = {item.kind for item in plan.items}
    assert ActionPlanItemKind.COMPLETE_NEXT_MISSION in kinds
    assert ActionPlanItemKind.FINISH_REVISION_CYCLE in kinds
    assert any("Bayes Theorem" in item.guidance for item in plan.items)


def test_milestones_include_exam_and_revision(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(make_full_inputs())
    kinds = {item.kind for item in view.upcoming_milestones.milestones}
    assert ReadinessMilestoneKind.EXAM in kinds
    assert ReadinessMilestoneKind.REVISION_CYCLE in kinds
    assert ReadinessMilestoneKind.READINESS_TARGET in kinds


def test_refresh_readiness_publishes() -> None:
    publisher = RecordingReadinessPublisher()
    service = ExamReadinessService(readiness_publisher=publisher)
    view = service.refresh_readiness(
        make_full_inputs(), readiness_id="readiness-refresh"
    )
    assert len(publisher.readiness_views) == 1
    assert len(publisher.snapshots) == 1
    assert publisher.readiness_views[0].readiness_id.value == "readiness-refresh"
    assert publisher.snapshots[0].student_id == view.student_id


def test_deterministic_readiness_id_from_as_of(
    service: ExamReadinessService,
) -> None:
    inputs = make_full_inputs(as_of=datetime(2026, 7, 23, 8, 0, tzinfo=UTC))
    view = service.build_readiness(inputs)
    assert view.readiness_id.value == "readiness:student-001:20260723T080000"


def test_direction_improving_from_journey(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(make_full_inputs())
    assert view.trend.direction is ReadinessDirection.IMPROVING
    assert view.confidence.assessment_confidence is AssessmentConfidenceCategory.HIGH
