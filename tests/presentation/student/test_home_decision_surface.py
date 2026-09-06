"""Home as a pure decision surface (redesign Home contract)."""

from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.presentation.student.services.student_home_service import (
    _SEQUENTIAL_WHY_NOW,
    StudentHomeService,
)
from app.presentation.student.view_models import (
    EducationalExperienceViewModel,
    HomePageViewModel,
    StudentPageViewModel,
    StudentShellViewModel,
    home_vm,
)
from tests.presentation.student.helpers import render_student_home

ROOT = Path(__file__).resolve().parents[3]
HOME_SERVICE = ROOT / "app/presentation/student/services/student_home_service.py"
HOME_TMPL = ROOT / "app/templates/student/home.html"
HOME_ROUTES = ROOT / "app/presentation/student/routes.py"

_DASHBOARD_MARKERS = (
    "Why this topic matters",
    "Recent progress",
    "Syllabus covered",
    "Quick Actions",
    "why-this-matters",
    "recent-progress",
    "study-signals",
    "Curriculum Map",
    "Ask Tutor",
    "Review Yesterday",
    "View My Learning Journey",
    "Tomorrow preview",
    "015-tomorrow-preview",
)


def _page(home_vm_obj, **kwargs) -> StudentPageViewModel:
    return StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=home_vm_obj,
        **kwargs,
    )


def _mission_home_vm(*, educational_active: bool = False) -> HomePageViewModel:
    base = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome back",
            examination_label="IFoA CS1",
            has_recommendation=True,
            recommendation_title="Conditional probability",
            can_start_session=True,
            estimated_study_minutes=25,
            explanation=ExplanationSnapshot(
                summary="Practice conditional probability.",
                why_recommended=(
                    "Your recent practice shows soft recall that is not "
                    "happening on Runtime C."
                ),
                evidence_points=("Recent practice below average.",),
                expected_benefit="Strengthen readiness after this sitting.",
                confidence_label="Suggested",
                suggested_next_action="Start a focused practice session.",
                review_point="Reassess after practice.",
                confidence_basis="Based on recent practice.",
                is_complete=True,
            ),
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="m1",
                topic_title="Conditional probability",
                estimated_minutes=25,
            ),
        ),
        unified_journey=False,
    )
    if not educational_active:
        return base
    edu = EducationalExperienceViewModel(
        active=True,
        subject_code="CS1",
        examination_label="IFoA CS1",
        today_topic_title="Conditional probability",
        today_topic_code="1.2",
        mission_title="Conditional probability",
        why_this_mission=(
            "Authored package why that must not appear on Home."
        ),
        why_today=(
            "Today's topic is Conditional probability because it is the "
            "next incomplete topic in published syllabus order with "
            "satisfied prerequisites."
        ),
        expected_benefit="Strengthen readiness after this sitting.",
    )
    return replace(base, educational=edu)


def test_home_template_is_decision_surface_only():
    text = HOME_TMPL.read_text(encoding="utf-8")
    assert 'data-home="decision-surface"' in text
    assert 'data-workspace-section="greeting"' in text
    assert 'data-workspace-section="todays-mission"' in text
    assert "ds_mission_hero" in text
    assert 'data-home-secondary="study"' in text
    assert 'data-honest-progress="streak"' in text
    for marker in _DASHBOARD_MARKERS:
        assert marker not in text


def test_home_renders_specified_sections_only(app, ctx):
    page_home = _mission_home_vm(educational_active=True)
    with app.test_request_context("/student/"):
        built = StudentHomeService().build_home(
            _page(page_home),
            current_streak_days=2,
            progress_href="/student/progress",
        )
        html = render_template(
            "student/home.html",
            page=_page(page_home),
            home=built,
            form=None,
        )
    assert 'data-home="decision-surface"' in html
    assert "Streak · 2" in html
    assert "Today&#39;s Mission" in html or "Today's Mission" in html
    assert "Conditional probability" in html
    assert _SEQUENTIAL_WHY_NOW in html
    assert "After this" in html or "Strengthen readiness" in html
    assert 'data-home-secondary="study"' in html
    assert 'href="/student/study"' in html
    assert "student-home-greeting" in html
    for marker in (
        "Why this topic matters",
        "Recent progress",
        "Syllabus covered",
        "Quick Actions",
        "Curriculum Map",
        "Ask Tutor",
        "Review Yesterday",
        "View My Learning Journey",
    ):
        assert marker not in html


def test_home_streak_appears_exactly_once(app, ctx):
    html = render_student_home(
        app,
        _mission_home_vm(),
        current_streak_days=4,
        progress_href="/student/progress",
    )
    assert html.count("Streak · 4") == 1
    assert html.count('data-honest-progress="streak"') == 1
    assert 'data-honest-progress="signals-streak"' not in html


def test_home_sequential_why_is_honest_for_runtime_c(app, ctx):
    page_home = _mission_home_vm(educational_active=True)
    with app.test_request_context("/student/"):
        built = StudentHomeService().build_home(_page(page_home))
    assert built.mission is not None
    assert built.mission.why_now == _SEQUENTIAL_WHY_NOW
    assert "soft recall" not in built.mission.why_now.lower()
    assert "adaptive" not in built.mission.why_now.lower()
    assert "Authored package why" not in built.mission.why_now


def test_home_study_secondary_points_to_study_not_knowledge_graph(app, ctx):
    page_home = _mission_home_vm(educational_active=True)
    with app.test_request_context("/student/"):
        built = StudentHomeService().build_home(_page(page_home))
        html = render_template(
            "student/home.html",
            page=_page(page_home),
            home=built,
            form=None,
        )
    assert built.study_href == "/student/study"
    assert 'data-home-action="study"' in html
    assert "knowledge_graph" not in html
    assert "Curriculum Map" not in html
    assert built.quick_actions == ()


def test_milestone_on_home_load_mechanism_unchanged():
    routes = HOME_ROUTES.read_text(encoding="utf-8")
    assert "announce_new_milestones_on_home" in routes
    assert "HonestProgressService" in routes
    text = HOME_TMPL.read_text(encoding="utf-8")
    assert "Quick Actions" not in text
    assert "Syllabus covered" not in text
    assert "announce_new_milestones" not in text


def test_home_service_has_no_content_authoring_imports():
    tree = ast.parse(HOME_SERVICE.read_text(encoding="utf-8"))
    forbidden = (
        "content_authoring",
        "editorial_workspace",
        "authoring",
        "composition_overlay",
    )
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if any(f in name for f in forbidden):
                    found.append(name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            if any(f in node.module for f in forbidden):
                found.append(node.module)
    assert found == []
