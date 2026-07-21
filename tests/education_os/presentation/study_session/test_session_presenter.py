"""Presenter mapping, null-safety, determinism, and immutability (V3-003)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from types import SimpleNamespace

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from presentation.design_system import ContainerWidth, MissionCard, PageHeader
from presentation.mission_workspace import WorkspacePresenter
from presentation.study_session import (
    SECTION_ORDER,
    SessionPresenter,
    StudySessionViewModel,
)
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


@pytest.fixture(scope="module")
def pipeline_result() -> PipelineResult:
    return EducationalPipeline().run(make_pipeline_request())


def test_presenter_maps_pipeline_result(pipeline_result: PipelineResult) -> None:
    view = SessionPresenter.present(pipeline_result)

    assert isinstance(view, StudySessionViewModel)
    assert isinstance(view.header, PageHeader)
    assert isinstance(view.mission_card, MissionCard)
    assert view.header.title
    assert view.objective.description == pipeline_result.mission.objective.statement
    assert view.explanation.description == pipeline_result.explanation.summary
    assert "minute" in view.duration.value.lower() or view.duration.value
    assert view.resources
    assert view.progress_bar.label
    assert view.study_notes.description
    assert view.reflection.description
    assert view.completion.actions
    assert view.next_step.headline
    assert view.next_step.primary_button is not None
    assert view.container_width is ContainerWidth.CONTENT
    assert len(view.sections) == len(SECTION_ORDER)
    assert [section.key for section in view.sections] == list(SECTION_ORDER)


def test_presenter_accepts_workspace_view_model(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    view = SessionPresenter.present(workspace=workspace)

    assert view.header.title == workspace.mission_title
    assert view.objective.description == workspace.mission_objective
    assert view.greeting == workspace.greeting
    assert view.completion.actions
    assert len(view.resources) == len(
        [r for r in workspace.study_resources if r.kind != "example"]
    )


def test_presenter_prefers_explicit_workspace_over_result(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    overridden = replace(workspace, mission_title="Override Title")
    view = SessionPresenter.present(pipeline_result, workspace=overridden)
    assert view.header.title == "Override Title"


def test_null_safe_rendering_for_missing_inputs() -> None:
    view = SessionPresenter.present(None)

    assert view.header.title == "Today's Session"
    assert view.objective.description
    assert view.explanation.description
    assert view.duration.value == "Duration not available"
    assert view.resources == ()
    assert view.worked_examples == ()
    assert view.progress_bar.percent == 0.0
    assert view.completion.actions
    assert view.next_step.action_key == "return_home"
    assert view.timeline.items
    assert view.stepper.steps


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
    view = SessionPresenter.present(sparse)

    assert view.header.title
    assert view.resources == ()
    assert view.completion.actions[-1].action_key == "return_home"
    assert view.next_step.primary_button is not None


def test_deterministic_output(pipeline_result: PipelineResult) -> None:
    first = SessionPresenter.present(pipeline_result)
    second = SessionPresenter.present(pipeline_result)

    assert first == second
    assert first.sections == second.sections
    assert first.timeline == second.timeline
    assert first.completion == second.completion
    assert first.next_step == second.next_step


def test_view_model_is_immutable(pipeline_result: PipelineResult) -> None:
    view = SessionPresenter.present(pipeline_result)

    with pytest.raises(FrozenInstanceError):
        view.greeting = "mutated"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        view.header.title = "mutated"  # type: ignore[misc]

    updated = replace(view, greeting="Hello again")
    assert updated.greeting == "Hello again"
    assert view.greeting != "Hello again"


def test_uses_design_system_components(pipeline_result: PipelineResult) -> None:
    view = SessionPresenter.present(pipeline_result)

    assert view.header.accessibility().role == "banner"
    assert view.objective.accessibility().role == "region"
    assert view.mission_card.accessibility().role == "region"
    assert view.progress_bar.accessibility().role == "progressbar"
    assert view.timeline.accessibility().role == "list"
    assert view.stepper.accessibility().role == "list"
    assert view.next_step.card is not None
    assert view.next_step.primary_button.accessibility().keyboard_focusable
    for resource in view.resources:
        assert resource.card is not None
        assert resource.card.accessibility().label_required
