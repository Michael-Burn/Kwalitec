"""Template consistency and empty-state tests for Founder Studio UX."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.presentation.curriculum_studio.helpers import (
    FORBIDDEN_FOUNDER_COPY,
    STUDIO_TEMPLATE_MARKERS,
)

REPO = Path(__file__).resolve().parents[3]
STUDIO_TEMPLATES = REPO / "app" / "templates" / "curriculum_studio"
FOUNDER_TEMPLATES = (
    REPO
    / "app"
    / "founder"
    / "dashboard"
    / "templates"
    / "founder_dashboard"
)
CSS_PATH = (
    REPO
    / "app"
    / "founder"
    / "dashboard"
    / "static"
    / "css"
    / "founder_dashboard.css"
)


@pytest.mark.parametrize(
    "name",
    ("dashboard.html", "workspace.html"),
)
def test_studio_templates_include_polish_markers(name):
    text = (STUDIO_TEMPLATES / name).read_text(encoding="utf-8")
    for marker in STUDIO_TEMPLATE_MARKERS:
        assert marker in text, f"{name} missing {marker}"


@pytest.mark.parametrize(
    "name",
    ("founder_intelligence.html", "evidence_gates.html"),
)
def test_founder_advisory_templates_include_empty_and_breadcrumb(name):
    text = (FOUNDER_TEMPLATES / name).read_text(encoding="utf-8")
    assert "founder-breadcrumb" in text
    assert "founder-empty-state" in text
    assert "founder-next-action" in text
    assert "founder_dashboard.css" in text


def test_dashboard_empty_workspace_copy():
    text = (STUDIO_TEMPLATES / "dashboard.html").read_text(encoding="utf-8")
    assert "No workspaces yet" in text
    assert "empty_workspaces_message" in text
    assert "No activity yet" in text
    assert "empty_activity_message" in text


def test_workspace_empty_version_copy():
    text = (STUDIO_TEMPLATES / "workspace.html").read_text(encoding="utf-8")
    assert "No versions yet" in text
    assert "empty_version_message" in text
    assert "Version history" in text
    assert "Publish Curriculum" not in text or "publish_form" in text


def test_workspace_primary_action_macro():
    text = (STUDIO_TEMPLATES / "workspace.html").read_text(encoding="utf-8")
    assert "page.primary_action" in text
    assert "btn-primary" in text
    assert "founder-workflow" in text


def test_forms_show_required_indicators():
    dash = (STUDIO_TEMPLATES / "dashboard.html").read_text(encoding="utf-8")
    workspace = (STUDIO_TEMPLATES / "workspace.html").read_text(encoding="utf-8")
    assert "founder-required" in dash
    assert "founder-required" in workspace
    assert 'role="alert"' in dash


@pytest.mark.parametrize("term", FORBIDDEN_FOUNDER_COPY)
def test_templates_avoid_harsh_copy(term):
    for path in (
        *STUDIO_TEMPLATES.glob("*.html"),
        FOUNDER_TEMPLATES / "founder_intelligence.html",
        FOUNDER_TEMPLATES / "evidence_gates.html",
    ):
        lowered = path.read_text(encoding="utf-8").lower()
        assert term not in lowered, f"{path.name} contains {term}"


def test_css_contains_responsive_and_focus_rules():
    text = CSS_PATH.read_text(encoding="utf-8")
    assert "founder-breadcrumb" in text
    assert "founder-empty-state" in text
    assert "founder-next-action" in text
    assert ":focus-visible" in text
    assert "min-height:2.5rem" in text
    assert "@media (max-width:767.98px)" in text


def test_intelligence_empty_signals_guidance():
    text = (FOUNDER_TEMPLATES / "founder_intelligence.html").read_text(
        encoding="utf-8"
    )
    assert "No intelligence signals yet" in text
    assert "Evidence Gates" in text


def test_evidence_gates_empty_items_guidance():
    text = (FOUNDER_TEMPLATES / "evidence_gates.html").read_text(encoding="utf-8")
    assert "No evidence gates available" in text
    assert "Gate checklist" in text
