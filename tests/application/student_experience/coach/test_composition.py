"""Context composition tests for AI Learning Coach (XP-005)."""

from __future__ import annotations

from application.student_experience.coach import (
    CoachId,
    ExplanationCardKind,
    LearningCoachService,
)
from tests.application.student_experience.coach.conftest import (
    STUDENT_ID,
    RecordingCoachContextPublisher,
    RecordingCoachPublisher,
    make_empty_inputs,
    make_full_inputs,
)


def test_build_context_composes_all_sections(
    service: LearningCoachService,
) -> None:
    context = service.build_context(
        make_full_inputs(), coach_id=CoachId("coach-001")
    )

    assert context.student_id == STUDENT_ID
    assert context.coach_id.value == "coach-001"
    assert context.current_focus.has_focus is True
    assert context.learning_journey.available is True
    assert context.readiness.available is True
    assert context.current_mission.available is True
    assert context.recent_improvements
    assert context.explanation_cards.available is True
    assert context.celebration_moments.available is True


def test_context_never_exposes_domain_type_names(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_full_inputs())
    blob = " ".join(
        [
            context.current_focus.headline,
            context.current_focus.reason,
            context.learning_journey.trajectory_message,
            context.readiness.readiness_label,
            context.current_mission.purpose,
            context.current_mission.progress_summary,
            *(item.message for item in context.recent_improvements),
            *(item.message for item in context.current_risks),
            *(item.detail for item in context.upcoming_milestones),
            *(card.body for card in context.explanation_cards.cards),
            *(moment.message for moment in context.celebration_moments.moments),
        ]
    )
    for forbidden in (
        "MasteryAssessment",
        "RecommendationSet",
        "MissionPlan",
        "EducationalEvaluation",
        "StudySchedule",
        "MissionExecution",
        "HomeSnapshot",
        "JourneySnapshot",
        "ReadinessSnapshot",
        "WorkspaceSnapshot",
        "Education OS",
    ):
        assert forbidden not in blob


def test_explanation_cards_cover_expected_kinds(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_full_inputs())
    kinds = {card.kind for card in context.explanation_cards.cards}
    assert ExplanationCardKind.MISSION_PURPOSE in kinds
    assert ExplanationCardKind.RECOMMENDATION_RATIONALE in kinds
    assert ExplanationCardKind.PROGRESS_SUMMARY in kinds
    assert ExplanationCardKind.READINESS_REASONING in kinds
    assert ExplanationCardKind.JOURNEY_HIGHLIGHTS in kinds


def test_empty_inputs_degrade_gracefully(
    service: LearningCoachService,
) -> None:
    context = service.build_context(make_empty_inputs())
    assert context.current_focus.has_focus is False
    assert context.learning_journey.available is False
    assert context.readiness.available is False
    assert context.current_mission.available is False
    assert context.celebration_moments.available is False


def test_refresh_coach_publishes() -> None:
    coach_publisher = RecordingCoachPublisher()
    context_publisher = RecordingCoachContextPublisher()
    service = LearningCoachService(
        coach_publisher=coach_publisher,
        coach_context_publisher=context_publisher,
    )
    context = service.refresh_coach(make_full_inputs(), coach_id="coach-refresh")
    assert context.coach_id.value == "coach-refresh"
    assert len(context_publisher.contexts) == 1
    assert len(context_publisher.snapshots) == 1
    assert len(coach_publisher.conversations) == 1
    assert len(coach_publisher.reflections) == 1
    assert len(coach_publisher.snapshots) == 1
