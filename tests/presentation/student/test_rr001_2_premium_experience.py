"""RR-001.2 — Premium experience remediation presentation markers."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.presentation.student.view_models import home_vm
from tests.presentation.workflows.helpers import dual_run_flags, login_student

ROOT = Path(__file__).resolve().parents[3]


def _base_snap(**overrides) -> HomeSnapshot:
    data = dict(
        student_id="stu-1",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        exam_readiness_label="Exam Readiness",
        recommendation_title="Cash flow statements",
        recommendation_summary="Focus on cash flow statements next.",
        estimated_study_minutes=25,
        explanation=ExplanationSnapshot(
            summary="Focus on cash flow statements next.",
            why_recommended="Soft recall on cash flow statements.",
            evidence_points=("Recent practice below average.",),
            expected_benefit="Strengthen exam readiness on cash flow analysis.",
            confidence_label="Suggested",
            suggested_next_action="Start a 25-minute cash flow practice session.",
            review_point="Reassess after tonight's practice set.",
            confidence_basis="Based on recent practice outcomes.",
            is_complete=True,
        ),
        has_recommendation=True,
        can_start_session=False,
    )
    data.update(overrides)
    return HomeSnapshot(**data)


def _render_home(app, page_home, **template_kwargs):
    from app.presentation.student.services.student_home_service import (
        StudentHomeService,
    )
    from app.presentation.student.view_models import (
        StudentPageViewModel,
        StudentShellViewModel,
    )

    page = StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=page_home,
        educational=None,
    )
    with app.test_request_context("/student/"):
        home = StudentHomeService().build_home(page)
        return render_template(
            "student/home.html",
            page=page,
            home=home,
            form=template_kwargs.pop("form", None),
            **template_kwargs,
        )


def test_home_mission_intelligence_relocated_off_home(app, ctx):
    """DX-005A: Mission Intelligence leaves Home; one why-now remains in L0."""
    snap = _base_snap(
        recommendation_title="Revise equity",
        recommendation_summary="Focus on equity today.",
        has_recommendation=True,
        can_start_session=True,
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m1",
            estimated_minutes=25,
            topic_title="Revise equity",
        ),
        explanation=ExplanationSnapshot(
            summary="Focus on equity today.",
            why_recommended="Purpose text.",
            evidence_points=("Evidence point.",),
            expected_benefit="Benefit text.",
            confidence_label="Suggested",
            suggested_next_action="Start practice.",
            review_point="Reassess after practice.",
            confidence_basis="Based on recent practice.",
            timeliness_line="Why today text.",
            is_complete=True,
        ),
    )
    html = _render_home(app, home_vm(snap, unified_journey=False))
    assert 'data-mission-intelligence="true"' not in html
    assert "student-mission-intelligence-disclosure" not in html
    assert 'data-home-density="tertiary"' not in html
    assert "Current Mission" in html
    assert "Why now" in html


def test_home_empty_state_is_honest_with_cta(app, ctx):
    """DX-005A empty: Reason + Choose Exam Primary."""
    html = _render_home(app, None)
    assert 'data-student-state="empty"' in html
    assert "Choose Exam" in html
    assert "ds-btn--primary" in html
    assert "insights will appear" not in html.lower()


def test_flash_success_uses_student_success(app, ctx):
    """XR-17: success flashes use EOS student-success craft."""
    flash = (ROOT / "app/templates/partials/flash_messages.html").read_text(
        encoding="utf-8"
    )
    assert "student-success" in flash
    assert 'data-student-state="success"' in flash
    assert "student-flash-stack" in flash


def test_educational_empty_macro_uses_student_empty():
    """XR-04 / XR-17: shared empty macro speaks EOS empty language."""
    macro = (ROOT / "app/templates/partials/empty_state.html").read_text(
        encoding="utf-8"
    )
    assert "student-empty" in macro
    assert "student-btn-primary" in macro
    assert 'data-student-state="empty"' in macro


def test_compact_nav_markers_present():
    """XR-05: navigation exposes compact mobile toggle markers."""
    nav = (
        ROOT / "app/templates/student/components/navigation.html"
    ).read_text(encoding="utf-8")
    css = (ROOT / "app/static/css/student/student.css").read_text(encoding="utf-8")
    js = (ROOT / "app/static/js/student.js").read_text(encoding="utf-8")
    assert "data-student-nav-toggle" in nav
    assert "student-nav-toggle" in css
    assert "wireCompactNav" in js
    assert "@media (max-width: 767.98px)" in css


def test_workspace_pages_use_eos_page_header(app, client, ctx, user):
    """XR-01 / XR-11: Help / Onboarding / Settings / Wizard use EOS primitives."""
    login_student(client)
    sole = dual_run_flags(SOLE_RUNTIME=True)
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=sole,
    ):
        help_html = client.get("/alpha/help", follow_redirects=True).get_data(
            as_text=True
        )
        onboarding_html = client.get(
            "/alpha/onboarding", follow_redirects=True
        ).get_data(as_text=True)
        settings_html = client.get(
            "/settings/preferences", follow_redirects=True
        ).get_data(as_text=True)
        wizard_html = client.get(
            "/study-plan/wizard/1", follow_redirects=True
        ).get_data(as_text=True)

    assert "student-page-header" in help_html
    assert "student-page-title" in help_html
    assert 'for="help-search"' in help_html
    assert "student-panel" in help_html

    assert "student-page-header" in onboarding_html
    assert "student-btn-primary" in onboarding_html

    assert "student-page-header" in settings_html
    assert "student-panel" in settings_html

    assert "student-page-header" in wizard_html
    assert "student-btn-primary" in wizard_html
    assert 'aria-label="Study Plan wizard progress"' in wizard_html
