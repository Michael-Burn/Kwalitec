"""Home composition tests for XP-001 Student Home Experience."""

from __future__ import annotations

from datetime import UTC, datetime

from application.education.mission_execution import ExecutionStatus
from application.education.mission_generation import MissionType
from application.student_experience.home import (
    FocusActionKind,
    HomeAchievement,
    HomeId,
    InsightKind,
    MasteryTrendLabel,
    StudentHomeService,
)
from tests.application.student_experience.home.conftest import (
    AS_OF,
    STUDENT_ID,
    FakeAchievementProvider,
    RecordingPublisher,
    make_execution,
    make_full_inputs,
    make_history,
    make_mission,
    make_plan,
)


def test_build_home_composes_all_cards(service: StudentHomeService) -> None:
    home = service.build_home(make_full_inputs(), home_id=HomeId("home-001"))

    assert home.student_id == STUDENT_ID
    assert home.home_id.value == "home-001"
    assert home.todays_focus.has_focus is True
    assert home.todays_focus.mission_title is not None
    assert home.todays_study_session.has_session is True
    assert home.progress.has_progress_data is True
    assert home.progress.mastery_trend is MasteryTrendLabel.STEADY_PROGRESS
    assert "steady progress" in home.progress.mastery_message.lower()
    assert home.exam_readiness.available is True
    assert home.exam_readiness.days_remaining == 45
    assert home.learning_insights.has_insights is True
    assert len(home.quick_actions.actions) >= 1


def test_home_never_exposes_domain_type_names(service: StudentHomeService) -> None:
    home = service.build_home(make_full_inputs())
    blob = " ".join(
        [
            home.todays_focus.headline,
            home.todays_focus.reason,
            home.progress.mastery_message,
            home.momentum.momentum_message,
            home.exam_readiness.readiness_label,
            home.exam_readiness.trend_message,
            *(insight.message for insight in home.learning_insights.insights),
        ]
    )
    for forbidden in (
        "MasteryAssessment",
        "RecommendationSet",
        "MissionPlan",
        "EducationalEvaluation",
        "StudySchedule",
        "MissionExecution",
    ):
        assert forbidden not in blob


def test_achievements_loaded_from_provider() -> None:
    provider = FakeAchievementProvider(
        (
            HomeAchievement(
                achievement_id="a1",
                title="First mission",
                description="Completed your first mission",
                earned_at=AS_OF,
            ),
        )
    )
    service = StudentHomeService(achievement_provider=provider)
    home = service.build_home(make_full_inputs())
    assert home.achievements.has_achievements is True
    assert home.achievements.items[0].title == "First mission"


def test_refresh_home_publishes() -> None:
    publisher = RecordingPublisher()
    service = StudentHomeService(home_publisher=publisher)
    home = service.refresh_home(make_full_inputs(), home_id="home-refresh")
    assert len(publisher.homes) == 1
    assert len(publisher.snapshots) == 1
    assert publisher.homes[0].home_id.value == "home-refresh"
    assert publisher.snapshots[0].student_id == home.student_id


def test_learning_insights_cover_expected_kinds(service: StudentHomeService) -> None:
    plan = make_plan(
        (
            make_mission("mission-001"),
            make_mission(
                "mission-pre",
                mission_type=MissionType.REVISE_PREREQUISITE,
                rank=2,
                competency="foundations",
            ),
        )
    )
    inputs = make_full_inputs(
        mission_plan=plan,
        execution_history=make_history(
            completed=("mission-x",), abandoned=("mission-y",)
        ),
    )
    home = service.build_home(inputs)
    kinds = {insight.kind for insight in home.learning_insights.insights}
    assert InsightKind.MOST_IMPROVED_SUBJECT in kinds
    assert InsightKind.WEAKEST_COMPETENCY in kinds
    assert InsightKind.BIGGEST_OPPORTUNITY in kinds
    assert InsightKind.MISSION_COMPLETION_QUALITY in kinds
    assert InsightKind.UPCOMING_PREREQUISITE in kinds


def test_paused_execution_shapes_focus(service: StudentHomeService) -> None:
    plan = make_plan()
    execution = make_execution(
        plan, status=ExecutionStatus.PAUSED, elapsed_seconds=600
    )
    home = service.build_home(
        make_full_inputs(mission_plan=plan, current_execution=execution)
    )
    assert home.todays_focus.primary_action_kind is FocusActionKind.RESUME_SESSION
    assert home.todays_focus.has_focus is True


def test_deterministic_home_id_from_as_of(service: StudentHomeService) -> None:
    inputs = make_full_inputs(as_of=datetime(2026, 7, 23, 8, 0, tzinfo=UTC))
    home = service.build_home(inputs)
    assert home.home_id.value == "home:student-001:20260723T080000"
