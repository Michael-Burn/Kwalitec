"""Completion and resource mapping for the Study Session Runner (V3-003)."""

from __future__ import annotations

from dataclasses import replace

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from presentation.mission_workspace import (
    CompletionActionView,
    WorkspacePresenter,
)
from presentation.study_session import (
    CompletionMapper,
    ResourceMapper,
    SessionPresenter,
)
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


@pytest.fixture(scope="module")
def pipeline_result() -> PipelineResult:
    return EducationalPipeline().run(make_pipeline_request())


def test_completion_mapper_forwards_actions(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    completion = CompletionMapper.map_completion(workspace)
    next_step = CompletionMapper.map_next_step(workspace)

    assert completion.headline
    assert completion.detail
    assert completion.actions
    assert all(action.label for action in completion.actions)
    assert next_step.headline
    assert next_step.detail
    assert next_step.action_label
    assert next_step.action_key
    assert next_step.card is not None
    assert next_step.primary_button is not None
    assert next_step.primary_button.label == next_step.action_label


def test_completion_mapper_null_safe() -> None:
    completion = CompletionMapper.map_completion(None)
    next_step = CompletionMapper.map_next_step(None)

    assert completion.headline == "Completion"
    assert completion.actions[-1].action_key == "return_home"
    assert next_step.action_key == "return_home"
    assert next_step.action_label == "Return Home"
    assert next_step.primary_button is not None


def test_completion_mapper_prefers_non_home_action(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    workspace = replace(
        workspace,
        completion_actions=(
            CompletionActionView(
                label="Continue Session",
                detail="Resume the current session work.",
                action_key="continue_mission",
            ),
            CompletionActionView(
                label="Return Home",
                detail="Return to Home when you are finished.",
                action_key="return_home",
            ),
        ),
    )
    next_step = CompletionMapper.map_next_step(workspace)
    assert next_step.action_key == "continue_mission"
    assert next_step.action_label == "Continue Session"


def test_completion_section_body_includes_checklist(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    completion = CompletionMapper.map_completion(workspace)
    body = CompletionMapper.completion_section_body(completion)
    assert body
    for item in completion.checklist:
        assert item in body


def test_resource_mapper_separates_examples(
    pipeline_result: PipelineResult,
) -> None:
    workspace = WorkspacePresenter.present(pipeline_result)
    resources = ResourceMapper.map_resources(workspace, result=pipeline_result)
    examples = ResourceMapper.map_worked_examples(workspace, result=pipeline_result)

    assert all(resource.kind != "example" for resource in resources)
    assert all(resource.card is not None for resource in resources)
    for example in examples:
        assert example.label
        assert example.card is not None


def test_resource_mapper_null_safe() -> None:
    assert ResourceMapper.map_resources(None) == ()
    assert ResourceMapper.map_worked_examples(None) == ()
    assert "note" in ResourceMapper.study_notes_body(None).lower() or (
        "session" in ResourceMapper.study_notes_body(None).lower()
    )
    assert "resource" in ResourceMapper.resources_summary_body(()).lower()
    assert "example" in ResourceMapper.examples_summary_body(()).lower()


def test_session_presenter_wires_completion_mapping(
    pipeline_result: PipelineResult,
) -> None:
    view = SessionPresenter.present(pipeline_result)
    workspace = WorkspacePresenter.present(pipeline_result)
    expected = CompletionMapper.map_next_step(workspace)

    assert view.next_step.action_key == expected.action_key
    assert view.next_step.headline == expected.headline
    assert view.completion.actions == CompletionMapper.map_completion(workspace).actions
