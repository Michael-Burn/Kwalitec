"""Accessibility-oriented presentation checks for Founder Studio UX."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
STUDIO = REPO / "app" / "templates" / "curriculum_studio"
FOUNDER = (
    REPO
    / "app"
    / "founder"
    / "dashboard"
    / "templates"
    / "founder_dashboard"
)
CSS = (
    REPO
    / "app"
    / "founder"
    / "dashboard"
    / "static"
    / "css"
    / "founder_dashboard.css"
)


@pytest.mark.parametrize(
    "path",
    (
        STUDIO / "dashboard.html",
        STUDIO / "workspace.html",
        FOUNDER / "founder_intelligence.html",
        FOUNDER / "evidence_gates.html",
    ),
)
def test_pages_have_breadcrumb_nav(path):
    text = path.read_text(encoding="utf-8")
    assert 'aria-label="Breadcrumb"' in text
    assert "aria-current=\"page\"" in text or "aria-current='page'" in text


def test_dashboard_forms_have_labels_and_help():
    text = (STUDIO / "dashboard.html").read_text(encoding="utf-8")
    assert 'for="{{ create_subject_form.subject_code.id }}"' in text
    assert 'id="help-subject-code"' in text
    assert 'id="help-workspace-code"' in text
    assert "aria-describedby" in text or "help-subject-code" in text


def test_workspace_actions_have_accessible_labels():
    text = (STUDIO / "workspace.html").read_text(encoding="utf-8")
    assert "visually-hidden" in text
    assert 'aria-label="Curriculum Studio workflow stages"' in text
    assert "(current)" in text


def test_empty_states_use_status_role():
    for path in (
        STUDIO / "dashboard.html",
        STUDIO / "workspace.html",
        FOUNDER / "founder_intelligence.html",
        FOUNDER / "evidence_gates.html",
    ):
        text = path.read_text(encoding="utf-8")
        assert 'role="status"' in text


def test_focus_and_button_size_in_css():
    css = CSS.read_text(encoding="utf-8")
    assert "founder-btn:focus-visible" in css or ".founder-btn:focus-visible" in css
    assert "min-height:2.5rem" in css
    assert "min-width:2.75rem" in css


def test_required_indicators_are_aria_hidden():
    dash = (STUDIO / "dashboard.html").read_text(encoding="utf-8")
    assert 'aria-hidden="true"' in dash
    assert "founder-required" in dash


def test_evidence_gates_status_has_screen_reader_text():
    text = (FOUNDER / "evidence_gates.html").read_text(encoding="utf-8")
    assert "technically ready" in text
    assert "awaiting evidence" in text
