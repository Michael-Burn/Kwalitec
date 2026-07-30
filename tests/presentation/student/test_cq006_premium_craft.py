"""CQ-006 — Premium Craft presentation contracts (no behaviour change)."""

from __future__ import annotations

from pathlib import Path

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
    """DX-006B Phase 6: Session chrome lives in design_system.css."""
    ds = _css("design_system.css")
    assert ".ds-btn--ghost" in ds
    assert ".ds-session-context" in ds
    assert ".ds-learning-task" in ds
    assert ".ds-session-content" in ds
    assert ".ds-disclosure" in ds
    legacy = ROOT / "app/static/css/session/session.css"
    assert not legacy.exists()


def test_home_hero_craft_hooks_are_styled():
    """SOP-001 / UX-005: command-centre craft lives in design_system + student.css."""
    student = _css("student/student.css")
    ds = _css("design_system.css")
    assert ".ds-os-exam" in ds
    assert ".ds-os-health" in ds
    assert ".ds-os-actions" in ds
    assert ".ds-os-path" in ds
    assert ".student-card--current" in student
    assert ".student-narrative-entry" in student
    assert 'body[data-nav-pending="true"]' in student


def test_home_suppresses_shell_page_header(app, ctx):
    from app.application.student_experience.dto.home_snapshot import (
        StartSessionActionSnapshot,
    )
    from tests.presentation.student.helpers import render_student_home

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
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m1",
            topic_title="Cash flows",
            estimated_minutes=25,
        ),
    )
    html = render_student_home(app, home_vm(snap, unified_journey=False))
    assert "student-page-header" not in html
    assert "ds-os-home" in html
    assert "What should I do next?" in html
    assert "Cash flows" in html


def test_welcome_modal_uses_eos_primary_button():
    modal = _template("partials/welcome_modal.html")
    assert "student-btn-primary" in modal
    assert "btn-outline" in modal


def test_session_overview_why_uses_dedicated_label(app, ctx):
    """DX-005C: why-copy becomes one instructional sentence on the learning task."""
    from app.presentation.session.dto.study_session import (
        LearningTask,
        SessionPersistentContext,
        StudySessionPage,
    )

    study = StudySessionPage(
        page_title="Session",
        surface="overview",
        context=SessionPersistentContext(
            subject="Cash flows",
            chapter="Cash flows",
            objective="Strengthen Cash flows",
            activity_label="Begin practice",
            session_progress="Session step 1 of 4",
            elapsed_label="About 30 minutes",
        ),
        task=LearningTask(
            activity="Begin practice",
            expected_outcome="Strengthen Cash flows",
            estimated_duration="About 30 minutes",
            next_milestone="3 activities",
            instruction="Soft recall needs deliberate practice.",
        ),
        primary_label="Start Session",
        primary_kind="begin_form",
        primary_enabled=True,
        blocking_issue="",
        exit_href="/student/",
        exit_label="Exit",
        content_title="Current objective",
        content_body="Strengthen Cash flows",
        content_support="",
        answer_prompt="Your answer",
        show_answer_input=False,
        feedback_outcome="",
        feedback_explanation="",
        disclosures=(),
        technical_lines=(),
        session_id="sess-1",
        activity_id="",
        mission_id="m1",
    )
    with app.test_request_context("/session/sess-1/overview"):
        html = render_template(
            "session/overview.html",
            page=None,
            study=study,
            form=None,
            quick_check_embed=None,
        )
    assert "Soft recall needs deliberate practice." in html
    assert "Current Learning Task" in html
    assert "Why this Session" not in html
    assert "session-why-label" not in html
    assert "Study Sensei" not in html


def test_history_and_journey_craft_markers():
    history = _template("student/history.html")
    journey = _template("student/journey.html")
    assert "ds-os-history" in history
    assert "ds-os-archive-stats" in history
    assert "ds-os-journey" in journey
    assert "ds-os-path" in journey


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
