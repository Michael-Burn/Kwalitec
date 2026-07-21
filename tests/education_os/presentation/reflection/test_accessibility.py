"""Accessibility contracts for Reflection Workspace chrome (V3-005)."""

from __future__ import annotations

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from application.session_runtime import SessionStage, SessionState
from presentation.design_system import SEMANTIC_COLOURS, meets_contrast
from presentation.design_system.contrast import parse_hex
from presentation.reflection import ConfidenceLevel, ReflectionPresenter
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
    session = SessionPresenter.present(pipeline_result)
    state = SessionState(
        session_id="a11y-1",
        mission_title=session.header.title,
        stage=SessionStage.COMPLETED,
    )
    view = ReflectionPresenter.present(
        session,
        state,
        confidence=ConfidenceLevel.CONFIDENT.value,
        difficulty="hard",
        weak_concept="Standard deviation",
    )

    for component in (
        view.header,
        view.confidence.section,
        view.mission_completion.section,
        view.mission_completion.badge,
        view.difficulty.section,
        view.weak_concept.section,
        view.student_notes.section,
        view.reflection_summary.section,
        view.reflection_summary.card,
    ):
        _assert_a11y(component)

    assert view.primary_button is not None
    _assert_a11y(view.primary_button)
    assert view.primary_button.accessibility().keyboard_focusable

    for option in view.confidence.scale.options:
        assert option.chip is not None
        _assert_a11y(option.chip)
    for option in view.difficulty.scale.options:
        assert option.chip is not None
        _assert_a11y(option.chip)


def test_empty_reflection_chrome_remains_accessible() -> None:
    view = ReflectionPresenter.present(None, None)
    _assert_a11y(view.header)
    _assert_a11y(view.confidence.section)
    _assert_a11y(view.mission_completion.badge)
    _assert_a11y(view.reflection_summary.card)
    assert view.primary_button is not None
    _assert_a11y(view.primary_button)
