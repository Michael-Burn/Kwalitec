"""EP-006.2 — Home template mission projection (DX-005A; MES stack off Home)."""

from __future__ import annotations

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.presentation.student.view_models import home_vm
from tests.presentation.student.helpers import render_student_home


def test_home_template_shows_mission_why_now_without_mes_stack(app, ctx):
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
        can_start_session=True,
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m1",
            estimated_minutes=25,
            topic_title="Cash flow statements",
        ),
    )
    page_home = home_vm(snap, unified_journey=False)
    html = render_student_home(app, page_home)
    assert "Today&#39;s Mission" in html or "Continue Session" in html
    assert "Why now" in html
    assert "soft recall on cash flow" in html
    assert "data-mes-field" not in html
    assert "data-mes-disclosure" not in html
    assert "Study Sensei" not in html
    assert 'data-narrator="study-sensei"' not in html
    assert "Why this guidance?" not in html
    assert "Two recent practice attempts" not in html
