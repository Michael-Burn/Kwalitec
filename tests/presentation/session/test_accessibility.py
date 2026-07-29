"""Accessibility markers for Learning Session Experience UI."""

from __future__ import annotations

from pathlib import Path

import pytest

TEMPLATE_ROOT = (
    Path(__file__).resolve().parents[3] / "app" / "templates" / "session"
)
BODY = TEMPLATE_ROOT / "partials" / "session_body.html"


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


def test_session_body_has_one_h1_marker():
    text = BODY.read_text(encoding="utf-8")
    assert 'id="session-page-title"' in text
    assert "ds-page-header__title" in text


def test_base_has_banner_main():
    text = (TEMPLATE_ROOT / "base.html").read_text(encoding="utf-8")
    assert 'role="banner"' in text
    assert 'role="main"' in text
    assert "Skip to content" in text


def test_primary_has_accessible_group():
    text = BODY.read_text(encoding="utf-8")
    assert 'aria-label="Primary actions"' in text
    assert "ds-btn--primary" in text


def test_session_context_labelled():
    text = BODY.read_text(encoding="utf-8")
    assert "ds_session_context" in text
    assert "ds_learning_task" in text


def test_disclosures_use_details():
    text = BODY.read_text(encoding="utf-8")
    assert "ds_disclosure" in text
    assert "Technical details" in text


def test_answer_input_labelled():
    text = BODY.read_text(encoding="utf-8")
    assert "session-answer-label" in text
    assert "aria-labelledby" in text
