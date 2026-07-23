"""Accessibility contracts for Student Dashboard decision screen (PX-003)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from application.pipeline import EducationalPipeline, PipelineResult
from presentation.dashboard import DashboardPresenter
from presentation.design_system import SEMANTIC_COLOURS, meets_contrast
from presentation.design_system.contrast import parse_hex
from presentation.design_system.layout import (
    BREAKPOINTS,
    ContainerWidth,
    breakpoint_at_width,
    columns_at_width,
)
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
    view = DashboardPresenter.present(pipeline_result)

    for component in (
        view.header,
        view.greeting,
        view.mission_card,
        view.mission_reason,
        view.primary_action,
        view.progress_summary,
        view.progress_bar,
        view.hero.mission_card,
        view.hero.primary_action,
        view.readiness.card,
        view.journey.card,
        view.coach.card,
    ):
        if component is not None:
            _assert_a11y(component)

    assert view.primary_action.accessibility().keyboard_focusable
    assert view.progress_bar.accessibility().role == "progressbar"
    assert 0.0 <= view.progress_bar.percent <= 100.0


def test_decision_panels_and_actions_are_accessible(
    pipeline_result: PipelineResult,
) -> None:
    statistics = SimpleNamespace(
        sessions_completed=3,
        total_minutes=90,
        evidence_count=2,
        progress_percent=50,
        current_streak_days=4,
        longest_streak_days=4,
    )
    view = DashboardPresenter.present(
        pipeline_result,
        statistics=statistics,
    )

    assert view.learning_statistics == ()
    assert view.readiness.card is not None
    _assert_a11y(view.readiness.card)
    assert view.journey.card is not None
    _assert_a11y(view.journey.card)
    assert view.coach.card is not None
    _assert_a11y(view.coach.card)

    for milestone in view.upcoming_milestones:
        if milestone.card is not None:
            _assert_a11y(milestone.card)

    for action in view.quick_actions:
        assert action.button is not None
        _assert_a11y(action.button)
        assert action.button.accessibility().keyboard_focusable


def test_empty_dashboard_chrome_remains_accessible() -> None:
    view = DashboardPresenter.present(None)
    _assert_a11y(view.header)
    _assert_a11y(view.mission_card)
    _assert_a11y(view.progress_bar)
    _assert_a11y(view.primary_action)
    assert view.hero.mission_card is not None
    _assert_a11y(view.hero.mission_card)


def test_dashboard_uses_wide_responsive_container(
    pipeline_result: PipelineResult,
) -> None:
    view = DashboardPresenter.present(pipeline_result)
    assert view.container_width is ContainerWidth.WIDE
    assert breakpoint_at_width(320) in BREAKPOINTS
    assert columns_at_width(320) == 4
    assert columns_at_width(768) == 8
    assert columns_at_width(1024) == 12
