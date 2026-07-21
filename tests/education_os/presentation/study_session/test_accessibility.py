"""Accessibility contracts for Study Session Runner chrome (V3-003)."""

from __future__ import annotations

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from presentation.design_system import SEMANTIC_COLOURS, meets_contrast
from presentation.design_system.contrast import parse_hex
from presentation.study_session import SessionPresenter
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


@pytest.fixture(scope="module")
def pipeline_result() -> PipelineResult:
    return EducationalPipeline().run(make_pipeline_request())


def _assert_a11y(component: object) -> None:
    a11y = component.accessibility()  # type: ignore[attr-defined]
    assert a11y.label_required
    if a11y.contrast_fg is not None and a11y.contrast_bg is not None:
        fg = SEMANTIC_COLOURS[a11y.contrast_fg].hex
        bg = SEMANTIC_COLOURS[a11y.contrast_bg].hex
        if parse_hex(fg) and parse_hex(bg):
            assert meets_contrast(fg, bg, minimum=a11y.min_contrast_ratio)


def test_core_chrome_declares_accessibility(
    pipeline_result: PipelineResult,
) -> None:
    view = SessionPresenter.present(pipeline_result)

    for component in (
        view.header,
        view.mission_card,
        view.objective,
        view.explanation,
        view.duration,
        view.progress_bar,
        view.progress_card,
        view.study_notes,
        view.reflection,
        view.timeline,
        view.stepper,
    ):
        _assert_a11y(component)

    assert view.next_step.card is not None
    _assert_a11y(view.next_step.card)
    assert view.next_step.primary_button is not None
    _assert_a11y(view.next_step.primary_button)
    assert view.next_step.primary_button.accessibility().keyboard_focusable


def test_resource_and_example_cards_are_accessible(
    pipeline_result: PipelineResult,
) -> None:
    view = SessionPresenter.present(pipeline_result)
    for resource in view.resources:
        assert resource.card is not None
        _assert_a11y(resource.card)
    for example in view.worked_examples:
        assert example.card is not None
        _assert_a11y(example.card)


def test_empty_session_chrome_remains_accessible() -> None:
    view = SessionPresenter.present(None)
    _assert_a11y(view.header)
    _assert_a11y(view.progress_bar)
    _assert_a11y(view.timeline)
    assert view.next_step.primary_button is not None
    _assert_a11y(view.next_step.primary_button)


def test_progress_bar_uses_progressbar_role(
    pipeline_result: PipelineResult,
) -> None:
    view = SessionPresenter.present(pipeline_result)
    assert view.progress_bar.accessibility().role == "progressbar"
    assert 0.0 <= view.progress_bar.percent <= 100.0
