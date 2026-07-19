"""Regression guards for Student Experience UI."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.presentation.student.helpers import STUDENT_ROUTES

REQUIRED_TEMPLATES = (
    "base.html",
    "home.html",
    "journey.html",
    "revision.html",
    "history.html",
    "profile.html",
    "components/recommendation_card.html",
    "components/readiness_card.html",
    "components/journey_card.html",
    "components/progress_card.html",
    "components/explanation_card.html",
    "components/history_card.html",
    "components/countdown_card.html",
    "components/navigation.html",
)

REQUIRED_STATIC = (
    "app/static/css/student.css",
    "app/static/js/student.js",
)

REQUIRED_MODULES = (
    "app/presentation/student/routes.py",
    "app/presentation/student/views.py",
    "app/presentation/student/forms.py",
    "app/presentation/student/navigation.py",
    "app/presentation/student/view_models.py",
    "app/presentation/student/factory.py",
)


@pytest.mark.parametrize("name", REQUIRED_TEMPLATES)
def test_required_templates_exist(name):
    assert Path("app/templates/student", name).is_file()


@pytest.mark.parametrize("path", REQUIRED_STATIC)
def test_required_static_exist(path):
    assert Path(path).is_file()


@pytest.mark.parametrize("path", REQUIRED_MODULES)
def test_required_modules_exist(path):
    assert Path(path).is_file()


def test_design_system_doc_exists():
    assert Path("knowledge/version2/DESIGN_SYSTEM.md").is_file()


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_no_confetti_or_gamification_chrome(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True).lower()
    assert "confetti" not in html
    assert "level up" not in html
    assert "earn xp" not in html
    assert "leaderboard" not in html


def test_student_blueprint_registered(experience_app):
    rules = {rule.endpoint for rule in experience_app.url_map.iter_rules()}
    assert "student.home" in rules
    assert "student.journey" in rules
    assert "student.revision" in rules
    assert "student.history" in rules
    assert "student.profile" in rules
    assert "student.start_session" in rules


def test_css_defines_primary_tokens():
    css = Path("app/static/css/student.css").read_text(encoding="utf-8")
    assert "--student-font-display" in css
    assert "--student-space-4" in css
    assert ".student-btn-primary" in css
    assert "prefers-reduced-motion" in css


def test_js_is_presentation_only():
    js = Path("app/static/js/student.js").read_text(encoding="utf-8")
    assert "readiness" not in js.lower() or "No educational" in js
    assert "recommendation score" not in js.lower()
