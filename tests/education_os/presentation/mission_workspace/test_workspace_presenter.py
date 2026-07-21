"""View-model mapping, presenter formatting, null-safety, and determinism."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from types import SimpleNamespace

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from presentation.mission_workspace import (
    MissionProgressMapper,
    MissionWorkspaceViewModel,
    WorkspacePresenter,
)
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


@pytest.fixture(scope="module")
def pipeline_result() -> PipelineResult:
    return EducationalPipeline().run(make_pipeline_request())


def test_view_model_mapping_from_pipeline_result(
    pipeline_result: PipelineResult,
) -> None:
    view = WorkspacePresenter.present(pipeline_result)

    assert isinstance(view, MissionWorkspaceViewModel)
    assert view.greeting
    assert view.mission_title
    assert view.mission_objective == pipeline_result.mission.objective.statement
    assert view.mission_explanation
    assert "minute" in view.estimated_duration
    assert view.study_resources
    assert view.progress_summary.detail == (
        pipeline_result.progress_report.educational_explanation
    )
    assert view.recommendation_summary.detail
    assert view.reflection_status.label
    assert view.session_progress.planned_minutes == (
        pipeline_result.student_experience.session_summary.planned_minutes
    )
    assert view.completion_actions
    assert all(action.label for action in view.completion_actions)


def test_presenter_formats_duration_and_resources(
    pipeline_result: PipelineResult,
) -> None:
    view = WorkspacePresenter.present(pipeline_result)
    minutes = pipeline_result.mission.duration.planned_minutes
    assert view.estimated_duration == f"{minutes} minutes"

    task_labels = [task.label for task in pipeline_result.mission.sequence.tasks]
    resource_labels = [resource.label for resource in view.study_resources]
    for label in task_labels:
        assert label in resource_labels


def test_progress_mapper_forwards_report_fields(
    pipeline_result: PipelineResult,
) -> None:
    summary = MissionProgressMapper.map_progress_summary(pipeline_result)
    session = MissionProgressMapper.map_session_progress(pipeline_result)

    assert summary.detail == pipeline_result.progress_report.educational_explanation
    assert summary.metric_lines
    assert session.completed_missions == (
        pipeline_result.student_experience.session_summary.completed_mission_count
    )
    assert session.mastery_trend_label
    assert session.progress_label


def test_null_safe_rendering_for_missing_result() -> None:
    view = WorkspacePresenter.present(None)

    assert view.greeting
    assert view.mission_title == "Today's Session"
    assert view.mission_objective
    assert view.mission_explanation
    assert view.estimated_duration == "Duration not available"
    assert view.study_resources == ()
    assert view.progress_summary.trend_label == "Not available"
    assert view.recommendation_summary.detail
    assert view.reflection_status.is_available is False
    assert view.session_progress.completed_missions == 0
    assert view.completion_actions
    assert view.completion_actions[-1].action_key == "return_home"


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
    view = WorkspacePresenter.present(sparse)

    assert view.greeting
    assert view.mission_title
    assert view.study_resources == ()
    assert view.progress_summary.detail
    assert view.recommendation_summary.category_label == ""
    assert view.completion_actions[-1].label == "Return Home"


def test_deterministic_output(pipeline_result: PipelineResult) -> None:
    first = WorkspacePresenter.present(pipeline_result)
    second = WorkspacePresenter.present(pipeline_result)

    assert first == second
    assert first.study_resources == second.study_resources
    assert first.completion_actions == second.completion_actions
    assert first.progress_summary == second.progress_summary


def test_view_model_is_immutable(pipeline_result: PipelineResult) -> None:
    view = WorkspacePresenter.present(pipeline_result)

    with pytest.raises(FrozenInstanceError):
        view.greeting = "mutated"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        view.progress_summary.headline = "mutated"  # type: ignore[misc]

    updated = replace(view, greeting="Hello again")
    assert updated.greeting == "Hello again"
    assert view.greeting != "Hello again"


def test_objective_and_explanation_prefer_pipeline_truth(
    pipeline_result: PipelineResult,
) -> None:
    view = WorkspacePresenter.present(pipeline_result)

    assert view.mission_objective == pipeline_result.mission.objective.statement
    assert view.mission_explanation == pipeline_result.explanation.summary
