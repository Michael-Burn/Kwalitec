"""EP-006.2 — Home template MES smoke (L1 why/next + explanation_card)."""

from __future__ import annotations

from types import SimpleNamespace

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.presentation.student.view_models import home_vm


def test_home_template_renders_mes_l1_and_explanation_card(app, ctx):
    snap = HomeSnapshot(
        student_id="stu-1",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        exam_readiness_label="Exam Readiness",
        recommendation_title="Cash flow statements",
        recommendation_summary="Focus on cash flow statements next.",
        estimated_study_minutes=25,
        expected_readiness_improvement=0.03,
        explanation=ExplanationSnapshot(
            summary="Focus on cash flow statements next.",
            why_recommended=(
                "Your recent practice shows soft recall on cash flow statements."
            ),
            evidence_points=(
                "Two recent practice attempts scored below your topic average.",
                "Cash flow is on the near-term revision list.",
            ),
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
    page_home = home_vm(snap, unified_journey=False)
    page = SimpleNamespace(
        home=page_home,
        shell=SimpleNamespace(active_surface="home", navigation=()),
    )
    with app.test_request_context("/student/"):
        html = render_template("student/home.html", page=page, form=None)
    assert 'data-mes-field="why_recommended"' in html
    assert "soft recall on cash flow" in html
    assert 'data-mes-field="suggested_next_action"' in html
    assert "25-minute cash flow" in html
    assert 'data-mes-disclosure="true"' in html
    assert "Why this tip?" in html
    assert "Reassess after tonight" in html
    assert "Two recent practice attempts" in html
