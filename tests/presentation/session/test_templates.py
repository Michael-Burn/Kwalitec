"""Template / accessibility / terminology / independence presentation tests."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tests.presentation.session.helpers import FORBIDDEN_TERMS

PRES_ROOT = (
    Path(__file__).resolve().parents[3] / "app" / "presentation" / "session"
)
TEMPLATE_ROOT = (
    Path(__file__).resolve().parents[3] / "app" / "templates" / "session"
)
DS_CSS_PATH = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "static"
    / "css"
    / "design_system.css"
)


def test_design_system_session_styles_exist():
    assert DS_CSS_PATH.is_file()
    text = DS_CSS_PATH.read_text(encoding="utf-8")
    assert ".ds-session-context" in text
    assert ".ds-learning-task" in text
    assert ".ds-btn--primary" in text


def test_legacy_session_css_removed():
    legacy = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "static"
        / "css"
        / "session"
        / "session.css"
    )
    assert not legacy.exists()


def test_base_template_skip_link_and_main():
    text = (TEMPLATE_ROOT / "base.html").read_text(encoding="utf-8")
    assert "Skip to content" in text
    assert 'id="session-main"' in text
    assert "design_system.css" in text


def test_overview_has_primary_cta_marker():
    text = (TEMPLATE_ROOT / "partials" / "session_body.html").read_text(
        encoding="utf-8"
    )
    assert "data-session-cta" in text
    assert "ds-btn--primary" in text


@pytest.mark.parametrize("term", FORBIDDEN_TERMS)
def test_templates_avoid_forbidden_terms(term):
    for path in TEMPLATE_ROOT.rglob("*.html"):
        lowered = path.read_text(encoding="utf-8").lower()
        assert term not in lowered, f"{path} contains {term}"


def test_presentation_does_not_import_engines():
    forbidden = (
        "app.application.learning_session",
        "app.application.learning_activity",
        "app.application.student_twin",
        "app.domain.student_twin",
    )
    found: list[str] = []
    for path in PRES_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if any(
                    node.module == f or node.module.startswith(f + ".")
                    for f in forbidden
                ):
                    found.append(f"{path.name}: {node.module}")
    assert found == []


def test_factory_module_present():
    assert (PRES_ROOT / "factory.py").is_file()
    assert (PRES_ROOT / "routes.py").is_file()
    assert (PRES_ROOT / "views.py").is_file()
    assert (PRES_ROOT / "view_models.py").is_file()
    assert (PRES_ROOT / "navigation.py").is_file()
    assert (PRES_ROOT / "forms.py").is_file()
    assert (PRES_ROOT / "services" / "study_session_service.py").is_file()
    assert (PRES_ROOT / "dto" / "study_session.py").is_file()


def test_activity_template_no_side_nav_dashboard():
    text = (TEMPLATE_ROOT / "activity.html").read_text(encoding="utf-8")
    assert "sidebar" not in text.lower()
    assert "dashboard" not in text.lower()


def test_reflection_template_no_scoring_words():
    body = (TEMPLATE_ROOT / "partials" / "session_body.html").read_text(
        encoding="utf-8"
    ).lower()
    for word in (" score ", " points ", " badge ", " streak ", " +xp", " xp "):
        assert word not in f" {body} ", word
    assert "leaderboard" not in body
    assert "confetti" not in body


def test_responsive_css_has_mobile_breakpoint():
    text = DS_CSS_PATH.read_text(encoding="utf-8")
    assert "@media" in text
    assert "768px" in text


def test_legacy_progress_theatre_components_removed():
    components = TEMPLATE_ROOT / "components"
    for name in (
        "progress_bar.html",
        "timer_card.html",
        "activity_card.html",
        "question_card.html",
        "explanation_card.html",
        "reflection_card.html",
        "completion_card.html",
        "navigation.html",
    ):
        assert not (components / name).exists(), name
