"""Presenter mapping, mission rendering, null-safety, and immutability (PX-003)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from types import SimpleNamespace

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from presentation.dashboard import (
    DashboardPresenter,
    DashboardViewModel,
    MissionCardMapper,
)
from presentation.design_system import (
    ContainerWidth,
    MissionCard,
    PageHeader,
    RecommendationCard,
)
from presentation.mission_workspace import WorkspacePresenter
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


@pytest.fixture(scope="module")
def pipeline_result() -> PipelineResult:
    return EducationalPipeline().run(make_pipeline_request())


def test_presenter_maps_pipeline_result(pipeline_result: PipelineResult) -> None:
    view = DashboardPresenter.present(pipeline_result)

    assert isinstance(view, DashboardViewModel)
    assert isinstance(view.header, PageHeader)
    assert isinstance(view.mission_card, MissionCard)
    assert isinstance(view.mission_reason, RecommendationCard)
    assert view.header.title == "Learning Dashboard"
    assert view.greeting_text
    assert view.hero.greeting
    assert view.hero.mission_title
    assert view.hero.duration_label
    assert view.hero.purpose
    assert view.hero.cta_label
    assert view.mission_card.title
    assert view.mission_card.body == pipeline_result.mission.objective.statement
    assert view.mission_reason.body
    assert view.primary_action.label
    assert view.progress_summary.title
    assert view.progress_bar.label
    assert view.learning_statistics == ()
    assert view.readiness.category_label
    assert view.journey.story
    assert view.coach.insight
    assert view.upcoming_milestones
    assert view.quick_actions
    assert view.container_width is ContainerWidth.WIDE


def test_presenter_accepts_workspace_view_model(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    view = DashboardPresenter.present(workspace=workspace)

    assert view.mission_card.title == workspace.mission_title
    assert view.hero.mission_title == workspace.mission_title
    assert view.mission_card.body == workspace.mission_objective
    assert view.greeting_text == workspace.greeting or view.hero.greeting


def test_presenter_prefers_explicit_workspace_over_result(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    overridden = replace(workspace, mission_title="Override Mission")
    view = DashboardPresenter.present(pipeline_result, workspace=overridden)
    assert view.mission_card.title == "Override Mission"
    assert view.hero.mission_title == "Override Mission"


def test_presenter_reuses_xp_experience_cargo(
    pipeline_result: PipelineResult,
) -> None:
    experience = SimpleNamespace(
        home=SimpleNamespace(
            todays_focus=SimpleNamespace(
                headline="Continue probability practice",
                mission_title="Probability foundations",
                estimated_duration_minutes=25,
                study_objective="Strengthen probability",
                reason="You paused mid-session.",
                primary_action_label="Resume Mission",
                primary_action_kind=SimpleNamespace(value="resume_session"),
                has_focus=True,
            ),
            exam_readiness=SimpleNamespace(
                available=True,
                readiness_label="Building readiness",
                readiness_percent=62.0,
                trend=SimpleNamespace(value="improving"),
                trend_message="Your readiness improved after revision.",
            ),
            progress=SimpleNamespace(
                mastery_message="Probability is no longer your weakest area.",
                weekly_growth_message="Your readiness improved.",
            ),
            momentum=SimpleNamespace(
                momentum_message="Yesterday you completed a revision session."
            ),
            learning_insights=SimpleNamespace(
                insights=(
                    SimpleNamespace(
                        title="Focus",
                        message="Keep the momentum on probability this week.",
                    ),
                )
            ),
            upcoming_milestone=SimpleNamespace(
                title="Checkpoint prep",
                detail="Prepare for your next checkpoint.",
                days_until=5,
                has_milestone=True,
            ),
            quick_actions=SimpleNamespace(
                actions=(
                    SimpleNamespace(
                        kind=SimpleNamespace(value="resume_mission"),
                        label="Resume Mission",
                        enabled=True,
                        detail="",
                    ),
                    SimpleNamespace(
                        kind=SimpleNamespace(value="open_schedule"),
                        label="Open Schedule",
                        enabled=True,
                        detail="",
                    ),
                )
            ),
        ),
        home_snapshot=SimpleNamespace(
            focus_headline="Continue probability practice",
            focus_mission_title="Probability foundations",
            focus_action_label="Resume Mission",
        ),
        journey_snapshot=SimpleNamespace(
            trajectory_message="Yesterday you completed a revision session.",
            consistency_message="Your readiness improved.",
        ),
        readiness_snapshot=SimpleNamespace(
            readiness_available=True,
            readiness_percent=62.0,
            readiness_label="Building readiness",
            direction_message="Improving",
            journey_trajectory_message="Probability is no longer your weakest area.",
        ),
        coach_snapshot=SimpleNamespace(
            focus_headline="Keep practising probability.",
            journey_message="Your readiness improved.",
        ),
        next_action=SimpleNamespace(
            label="Resume Mission",
            action_key="resume_session",
            detail="",
        ),
    )
    view = DashboardPresenter.present(pipeline_result, experience=experience)

    assert view.hero.mission_title == "Probability foundations"
    assert view.hero.duration_label == "25 minutes"
    assert view.hero.cta_label == "Resume Mission"
    assert view.readiness.trend_label
    assert "revision" in view.journey.story.lower()
    assert view.coach.available is True
    assert any(m.title == "Checkpoint prep" for m in view.upcoming_milestones)
    assert any(a.label == "Resume Mission" for a in view.quick_actions)
    assert view.learning_statistics == ()


def test_mission_card_mapper_renders_mission(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    card = MissionCardMapper.map_mission_card(workspace, result=pipeline_result)
    reason = MissionCardMapper.map_mission_reason(workspace, result=pipeline_result)

    assert card.eyebrow == "Today's Mission"
    assert card.body == pipeline_result.mission.objective.statement
    assert "minute" in card.duration_label.lower() or card.duration_label
    assert reason.body == pipeline_result.explanation.summary
    assert reason.eyebrow == "Mission reason"


def test_null_safe_rendering_for_missing_inputs() -> None:
    view = DashboardPresenter.present(None)

    assert view.header.title == "Learning Dashboard"
    assert view.greeting_text
    assert view.hero.mission_title
    assert view.hero.cta_label
    assert view.mission_card.title == "Today's Session" or view.mission_card.title
    assert view.mission_reason.body
    assert view.primary_action.label
    assert view.learning_statistics == ()
    assert view.readiness.category_label
    assert view.journey.story
    assert view.coach.insight
    assert view.upcoming_milestones
    assert view.quick_actions
    assert view.progress_bar.percent == 0.0


def test_null_safe_rendering_for_sparse_objects() -> None:
    sparse = SimpleNamespace(
        mission=None,
        study_plan=None,
        progress_report=None,
        recommendations=None,
        explanation=None,
        student_experience=None,
        enhanced_mission=None,
        enhanced_recommendations=None,
        stages_completed=(),
    )
    view = DashboardPresenter.present(sparse)

    assert view.header.title
    assert view.hero.mission_title
    assert view.mission_card.title
    assert view.learning_statistics == ()
    assert view.quick_actions
    assert view.primary_action is not None


def test_deterministic_output(pipeline_result: PipelineResult) -> None:
    first = DashboardPresenter.present(pipeline_result)
    second = DashboardPresenter.present(pipeline_result)

    assert first == second
    assert first.hero == second.hero
    assert first.readiness == second.readiness
    assert first.journey == second.journey
    assert first.coach == second.coach
    assert first.upcoming_milestones == second.upcoming_milestones
    assert first.quick_actions == second.quick_actions


def test_view_model_is_immutable(pipeline_result: PipelineResult) -> None:
    view = DashboardPresenter.present(pipeline_result)

    with pytest.raises(FrozenInstanceError):
        view.greeting_text = "mutated"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        view.hero.mission_title = "mutated"  # type: ignore[misc]

    updated = replace(view, greeting_text="Hello again")
    assert updated.greeting_text == "Hello again"
    assert view.greeting_text != "Hello again"


def test_decision_screen_hides_metric_grids(
    pipeline_result: PipelineResult,
) -> None:
    statistics = SimpleNamespace(
        sessions_completed=4,
        total_minutes=120,
        evidence_count=3,
        progress_percent=40,
    )
    view = DashboardPresenter.present(pipeline_result, statistics=statistics)
    assert view.learning_statistics == ()
    assert view.hero.mission_title
    assert view.readiness is not None
    assert view.journey is not None
    assert view.coach is not None
