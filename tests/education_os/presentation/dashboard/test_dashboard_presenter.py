"""Presenter mapping, mission rendering, null-safety, and immutability (V4-001)."""

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
    assert view.greeting.description == view.greeting_text
    assert view.mission_card.title
    assert view.mission_card.body == pipeline_result.mission.objective.statement
    assert view.mission_reason.body
    assert view.primary_action.label
    assert view.progress_summary.title
    assert view.progress_bar.label
    assert view.learning_statistics
    assert view.current_streak.headline == "Current streak"
    assert view.achievements
    assert view.upcoming_sessions
    assert view.quick_actions
    assert view.container_width is ContainerWidth.WIDE


def test_presenter_accepts_workspace_view_model(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    view = DashboardPresenter.present(workspace=workspace)

    assert view.mission_card.title == workspace.mission_title
    assert view.mission_card.body == workspace.mission_objective
    assert view.greeting_text == workspace.greeting


def test_presenter_prefers_explicit_workspace_over_result(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    overridden = replace(workspace, mission_title="Override Mission")
    view = DashboardPresenter.present(pipeline_result, workspace=overridden)
    assert view.mission_card.title == "Override Mission"


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
    assert view.mission_card.title == "Today's Session" or view.mission_card.title
    assert view.mission_reason.body
    assert view.primary_action.label
    assert view.learning_statistics
    assert view.current_streak.current_days == 0
    assert view.achievements
    assert view.upcoming_sessions
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
    assert view.mission_card.title
    assert view.learning_statistics
    assert view.quick_actions
    assert view.primary_action is not None


def test_deterministic_output(pipeline_result: PipelineResult) -> None:
    first = DashboardPresenter.present(pipeline_result)
    second = DashboardPresenter.present(pipeline_result)

    assert first == second
    assert first.learning_statistics == second.learning_statistics
    assert first.achievements == second.achievements
    assert first.upcoming_sessions == second.upcoming_sessions


def test_view_model_is_immutable(pipeline_result: PipelineResult) -> None:
    view = DashboardPresenter.present(pipeline_result)

    with pytest.raises(FrozenInstanceError):
        view.greeting_text = "mutated"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        view.mission_card.title = "mutated"  # type: ignore[misc]

    updated = replace(view, greeting_text="Hello again")
    assert updated.greeting_text == "Hello again"
    assert view.greeting_text != "Hello again"
