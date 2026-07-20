"""Accessibility markers for Learning Session Experience UI."""

from __future__ import annotations

from pathlib import Path

import pytest

TEMPLATE_ROOT = (
    Path(__file__).resolve().parents[3] / "app" / "templates" / "session"
)


@pytest.mark.parametrize(
    "filename",
    [
        "overview.html",
        "activity.html",
        "reflection.html",
        "summary.html",
        "complete.html",
    ],
)
def test_pages_extend_base(filename):
    text = (TEMPLATE_ROOT / filename).read_text(encoding="utf-8")
    assert 'extends "session/base.html"' in text


def test_progress_bar_uses_progressbar_role():
    text = (TEMPLATE_ROOT / "components" / "progress_bar.html").read_text(
        encoding="utf-8"
    )
    assert 'role="progressbar"' in text
    assert "aria-valuenow" in text


def test_base_has_banner_main_contentinfo():
    text = (TEMPLATE_ROOT / "base.html").read_text(encoding="utf-8")
    assert 'role="banner"' in text
    assert 'role="main"' in text
    assert 'role="contentinfo"' in text


def test_navigation_has_aria_label():
    text = (TEMPLATE_ROOT / "components" / "navigation.html").read_text(
        encoding="utf-8"
    )
    assert "aria-label" in text


@pytest.mark.parametrize(
    "component",
    [
        "activity_card.html",
        "question_card.html",
        "explanation_card.html",
        "reflection_card.html",
        "completion_card.html",
        "timer_card.html",
    ],
)
def test_cards_have_labelledby(component):
    text = (TEMPLATE_ROOT / "components" / component).read_text(encoding="utf-8")
    assert "aria-labelledby" in text
