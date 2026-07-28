"""CQ-006 — Premium Craft presentation contracts (no behaviour change)."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.presentation.student.view_models import home_vm

ROOT = Path(__file__).resolve().parents[3]


def _css(name: str) -> str:
    return (ROOT / "app/static/css" / name).read_text(encoding="utf-8")


def _template(name: str) -> str:
    return (ROOT / "app/templates" / name).read_text(encoding="utf-8")


def test_eos_shell_owns_welcome_modal_and_contextual_help_styles():
    css = _css("student/student.css")
    assert ".welcome-modal-backdrop" in css
    assert ".welcome-modal-card" in css
    assert ".btn-outline" in css
    assert ".ctx-learn-more" in css
    assert ".ctx-learn-more-summary" in css


def test_session_shell_owns_secondary_button_styles():
    session_css = _css("session/session.css")
    assert ".session-btn-secondary" in session_css
    assert "session-btn-secondary:focus-visible" in session_css or (
        ".session-btn-secondary:focus" in session_css
    )
    assert ".session-support" in session_css
    assert ".session-reflection-framing" in session_css
    assert ".session-why-label" in session_css


def test_home_hero_craft_hooks_are_styled():
    css = _css("student/student.css")
    assert ".student-session-next" in css
    assert ".student-commitment-defer" in css
    assert ".student-defer-option" in css
    assert ".student-coach-trust" in css
    assert ".student-card--current" in css
    assert ".student-narrative-entry" in css
    assert 'body[data-nav-pending="true"]' in css
    subordinate = css.split(".student-secondary--subordinate {", 1)[1].split("}", 1)[0]
    assert "opacity:" not in subordinate


def test_home_suppresses_shell_page_header(app, ctx):
    snap = HomeSnapshot(
        student_id="stu-cq006",
        greeting="Welcome back",
        examination_label="ACCA AA",
        recommendation_title="Cash flows",
        recommendation_summary="Practice cash flows.",
        estimated_study_minutes=25,
        explanation=ExplanationSnapshot(
            summary="Practice cash flows.",
            why_recommended="Soft recall needs practice.",
            evidence_points=("Recent practice below average.",),
            expected_benefit="Strengthen readiness.",
            confidence_label="Suggested",
            suggested_next_action="Start a focused practice session.",
            review_point="Reassess after practice.",
            confidence_basis="Based on recent practice.",
            is_complete=True,
        ),
        has_recommendation=True,
        can_start_session=True,
    )
    page = SimpleNamespace(
        home=home_vm(snap, unified_journey=False),
        shell=SimpleNamespace(
            active_surface="home",
            navigation=(),
            page_title="Today",
            page_eyebrow="Your learning",
            page_description="What you should do next.",
        ),
        educational=None,
    )
    with app.test_request_context("/student/"):
        html = render_template(
            "student/home.html",
            page=page,
            form=None,
            show_welcome=False,
        )
    assert "student-page-header" not in html
    assert "student-hero-title" in html
    assert 'data-narrator="study-sensei"' in html
    assert "student-narrator" in html
    assert "Cash flows" in html


def test_welcome_modal_uses_eos_primary_button():
    modal = _template("partials/welcome_modal.html")
    assert "student-btn-primary" in modal
    assert "btn-outline" in modal


def test_session_overview_why_uses_dedicated_label(app, ctx):
    page = SimpleNamespace(
        shell=SimpleNamespace(
            session_id="sess-1",
            topic_title="Cash flows",
            steps=(),
            page_eyebrow="Session",
            page_title="Overview",
            page_description="",
            active_surface="overview",
        ),
        overview=SimpleNamespace(
            objective="Strengthen Cash flows",
            learning_goal="",
            why_studying="Soft recall needs deliberate practice.",
            estimated_duration_label="About 30 minutes",
            activity_count_label="3 activities",
            topics=("Cash flows",),
            expected_improvement_label="",
            begin_label="Start Session",
            begin_enabled=True,
            mission_id="m1",
        ),
        progress=None,
        activity=None,
    )
    with app.test_request_context("/session/sess-1/overview"):
        html = render_template(
            "session/overview.html",
            page=page,
            form=None,
            quick_check_embed=None,
        )
    assert "Why this Session" in html
    assert "session-why-label" in html
    assert 'data-session="why"' in html
    assert "Soft recall needs deliberate practice." in html


def test_history_and_journey_craft_markers():
    history = _template("student/history.html")
    journey = _template("student/journey.html")
    assert "student-action-row" in history
    assert "student-narrative-list" in history
    assert "student-card--current" in journey
    assert "student-empty-why" in journey


def test_assessment_base_meta_description_is_valid_html():
    base = _template("student/assessment/base.html")
    assert '<meta name="description"' in base
    assert not base.lstrip().startswith("meta name=")
    assert "\n    meta name=" not in base


def test_student_js_demotes_extra_primaries_to_eos_secondary():
    js = (ROOT / "app/static/js/student.js").read_text(encoding="utf-8")
    assert 'classList.add("student-btn-secondary")' in js
    assert 'classList.add("btn-outline-secondary")' not in js


def test_quick_check_ack_style_present():
    css = _css("adaptive_assessment/quick_check.css")
    assert ".qc-mission-ack" in css
