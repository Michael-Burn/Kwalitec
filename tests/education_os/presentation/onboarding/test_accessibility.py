"""Accessibility contracts for Student Onboarding chrome (BR-002)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.onboarding.results import OnboardingSnapshot
from domain.onboarding.enums import OnboardingStatus, OnboardingStep
from presentation.design_system import SEMANTIC_COLOURS, meets_contrast
from presentation.design_system.contrast import parse_hex
from presentation.onboarding import OnboardingPresenter


def _assert_a11y(component: object) -> None:
    a11y = component.accessibility()  # type: ignore[attr-defined]
    assert a11y.label_required
    if a11y.contrast_fg is not None and a11y.contrast_bg is not None:
        fg = SEMANTIC_COLOURS[a11y.contrast_fg].hex
        bg = SEMANTIC_COLOURS[a11y.contrast_bg].hex
        if parse_hex(fg) and parse_hex(bg):
            assert meets_contrast(fg, bg, minimum=a11y.min_contrast_ratio)


def test_onboarding_chrome_declares_accessibility() -> None:
    snapshot = OnboardingSnapshot(
        onboarding_id="ob-1",
        student_id="stu-1",
        status=OnboardingStatus.IN_PROGRESS,
        current_step=OnboardingStep.WELCOME,
        progress_percent=0.0,
        payloads={},
        saved_steps=(),
        updated_at=datetime(2026, 7, 20, tzinfo=UTC),
    )
    view = OnboardingPresenter.present(snapshot)
    for component in (
        view.header,
        view.stepper,
        view.progress_bar,
        view.current_step.section,
    ):
        _assert_a11y(component)
    assert view.primary_button is not None
    _assert_a11y(view.primary_button)
    assert view.primary_button.accessibility().keyboard_focusable


def test_empty_onboarding_remains_accessible() -> None:
    view = OnboardingPresenter.present(None)
    _assert_a11y(view.header)
    _assert_a11y(view.progress_bar)
    _assert_a11y(view.stepper)
