"""Projection wiring tests for DashboardApplicationService (WEB-004)."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from application.dto.learner import LearnerStateDTO
from application.dto.teaching_plan import TeachingPlanDTO, TeachingPlanStepDTO
from application.dto.trajectory import LearningTrajectoryDTO, TrajectoryPointDTO
from application.errors import NotFoundError
from application.queries.get_dashboard import GetDashboard
from application.queries.get_progress_summary import GetProgressSummary
from application.queries.get_recommendations import GetRecommendations
from application.queries.get_timeline import GetTimeline
from application.queries.get_todays_mission import GetTodaysMission
from application.services.dashboard_application_service import (
    DashboardApplicationService,
)
from tests.education_os.application.fakes import FixedClock


@pytest.fixture
def twin() -> MagicMock:
    return MagicMock()


@pytest.fixture
def planning() -> MagicMock:
    return MagicMock()


@pytest.fixture
def service(twin, planning) -> DashboardApplicationService:
    return DashboardApplicationService(
        twin=twin,
        planning=planning,
        clock=FixedClock(datetime(2026, 7, 20, 10, 0, tzinfo=UTC)),
    )


def _plan() -> TeachingPlanDTO:
    return TeachingPlanDTO(
        plan_id="plan-001",
        episode_id="episode-001",
        student_id="student-ada",
        teaching_goal_statement="Repair confusion",
        teaching_strategy_id="strategy-1",
        primary_dimension="understanding",
        status="planned",
        learning_objective_ids=("lo-1",),
        concept_ids=("concept-1",),
        steps=(
            TeachingPlanStepDTO(
                step_id="step-001",
                kind="explanation",
                sequence_index=0,
                label="Explanation",
                required=True,
                status="pending",
            ),
        ),
    )


def test_get_progress_projects_learner_state(service, twin) -> None:
    twin.get_learner_state.return_value = LearnerStateDTO(
        twin_id="twin-001",
        student_id="student-ada",
        learner_state_id="ls-001",
        activity_status="engaged",
        twin_status="active",
        concept_count=2,
        evidence_count=3,
        intervention_count=0,
    )

    progress = service.get_progress(GetProgressSummary(student_id="student-ada"))

    assert progress.student_id == "student-ada"
    assert progress.concept_count == 2
    assert "activity:engaged" in progress.progress_cues


def test_get_timeline_projects_trajectory(service, twin) -> None:
    twin.get_learning_trajectory.return_value = LearningTrajectoryDTO(
        twin_id="twin-001",
        student_id="student-ada",
        points=(
            TrajectoryPointDTO(sequence=0, kind="created", label="Twin created"),
        ),
    )

    timeline = service.get_timeline(GetTimeline(student_id="student-ada"))

    assert timeline.event_count == 1
    assert timeline.events[0].kind == "created"


def test_get_todays_mission_projects_plan(service, planning) -> None:
    planning.get_teaching_plan.return_value = _plan()

    mission = service.get_todays_mission(
        GetTodaysMission(student_id="student-ada", episode_id="episode-001")
    )

    assert mission.episode_id == "episode-001"
    assert mission.task_count == 1
    assert mission.tasks[0].headline == "Explanation"


def test_get_todays_mission_rejects_foreign_plan(service, planning) -> None:
    plan = _plan()
    planning.get_teaching_plan.return_value = TeachingPlanDTO(
        plan_id=plan.plan_id,
        episode_id=plan.episode_id,
        student_id="other-student",
        teaching_goal_statement=plan.teaching_goal_statement,
        teaching_strategy_id=plan.teaching_strategy_id,
        primary_dimension=plan.primary_dimension,
        status=plan.status,
        learning_objective_ids=plan.learning_objective_ids,
        concept_ids=plan.concept_ids,
        steps=plan.steps,
    )

    with pytest.raises(NotFoundError):
        service.get_todays_mission(
            GetTodaysMission(student_id="student-ada", episode_id="episode-001")
        )


def test_get_recommendations_sparse_without_episode(service) -> None:
    assert (
        service.get_recommendations(GetRecommendations(student_id="student-ada"))
        is None
    )


def test_get_recommendations_packages_plan_fields(service, planning) -> None:
    planning.get_teaching_plan.return_value = _plan()

    recommendation = service.get_recommendations(
        GetRecommendations(student_id="student-ada", episode_id="episode-001")
    )

    assert recommendation is not None
    assert recommendation.title == "Continue studying"
    assert recommendation.subtitle == "Repair confusion"
    assert recommendation.can_start is True
    assert recommendation.recommendation_id == "plan-001"


def test_get_dashboard_composes_sparse_sections(service, twin) -> None:
    twin.get_learner_state.side_effect = NotFoundError(
        "EducationalDigitalTwin", "student-ada"
    )
    twin.get_learning_trajectory.side_effect = NotFoundError(
        "EducationalDigitalTwin", "student-ada"
    )

    dashboard = service.get_dashboard(GetDashboard(student_id="student-ada"))

    assert dashboard.student_id == "student-ada"
    assert dashboard.progress is None
    assert dashboard.timeline is None
    assert dashboard.todays_mission is None
    assert dashboard.recommendation is None
    assert "no_progress" in dashboard.empty_states
    assert "no_timeline" in dashboard.empty_states
    assert "no_mission" in dashboard.empty_states
    assert dashboard.composed_at == "2026-07-20T10:00:00+00:00"


def test_get_dashboard_wires_projection_builders(service, twin, planning) -> None:
    twin.get_learner_state.return_value = LearnerStateDTO(
        twin_id="twin-001",
        student_id="student-ada",
        learner_state_id="ls-001",
        activity_status="engaged",
        twin_status="active",
        concept_count=1,
        evidence_count=1,
        intervention_count=0,
    )
    twin.get_learning_trajectory.return_value = LearningTrajectoryDTO(
        twin_id="twin-001",
        student_id="student-ada",
        points=(
            TrajectoryPointDTO(sequence=0, kind="created", label="Twin created"),
        ),
    )
    planning.get_teaching_plan.return_value = _plan()

    dashboard = service.get_dashboard(
        GetDashboard(student_id="student-ada", episode_id="episode-001")
    )

    assert dashboard.progress is not None
    assert dashboard.timeline is not None
    assert dashboard.todays_mission is not None
    assert dashboard.recommendation is not None
    assert dashboard.todays_mission.tasks[0].headline == "Explanation"
    assert dashboard.recommendation.subtitle == "Repair confusion"
    assert dashboard.empty_states == ()
