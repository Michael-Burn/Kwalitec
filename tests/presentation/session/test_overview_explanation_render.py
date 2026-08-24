"""Pass (b) — Overview renders explanation_card; Home stays MES-free."""

from __future__ import annotations

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.presentation.session.dto.study_session import (
    LearningTask,
    SessionPersistentContext,
    StudySessionPage,
)
from app.presentation.student.view_models import (
    ExplanationViewModel,
    home_vm,
)
from tests.presentation.student.helpers import render_student_home


def _overview_study(*, explanation: ExplanationViewModel | None) -> StudySessionPage:
    return StudySessionPage(
        page_title="Today: Cash flows",
        surface="overview",
        context=SessionPersistentContext(
            subject="CS1",
            chapter="Cash flows",
            objective="Strengthen cash-flow timing",
            activity_label="Begin practice",
            session_progress="Session step 1 of 4",
        ),
        task=LearningTask(
            activity="Begin practice",
            expected_outcome="Strengthen cash-flow timing",
            estimated_duration="25 min",
            next_milestone="First activity",
            instruction="Review why this topic, then begin.",
        ),
        primary_label="Begin Session",
        primary_kind="begin_form",
        primary_enabled=True,
        blocking_issue="",
        exit_href="/student/",
        exit_label="Exit",
        content_title="Today's Session",
        content_body="Strengthen cash-flow timing",
        content_support="",
        answer_prompt="",
        show_answer_input=False,
        feedback_outcome="",
        feedback_explanation="",
        disclosures=(),
        technical_lines=(),
        session_id="sess-1",
        activity_id="",
        why_today="Builds on recent weak recall of discounting.",
        learning_objectives=("Apply discount factors correctly.",),
        explanation=explanation,
    )


def _render_overview(app, study: StudySessionPage) -> str:
    with app.test_request_context("/session/sess-1/overview"):
        from app.presentation.session.forms import BeginSessionForm

        form = BeginSessionForm()
        form.session_id.data = "sess-1"
        return render_template(
            "session/partials/session_body.html",
            study=study,
            form=form,
            answer_form=None,
            advance_form=None,
        )


def test_overview_html_renders_explanation_mes_fields(app, ctx):
    explanation = ExplanationViewModel(
        summary="Focus on cash-flow timing.",
        why_recommended="Recent practice shows soft recall on discounting.",
        evidence_points=(
            "Two recent practice attempts scored below your topic average.",
        ),
        expected_benefit="Strengthen exam readiness on cash-flow analysis.",
        confidence_label="Suggested",
        suggested_next_action="Begin today's Session on cash flows.",
        review_point="Reassess after tonight's practice set.",
        confidence_basis="Based on recent practice outcomes.",
        is_complete=True,
        has_content=True,
        has_disclosure=True,
    )
    html = _render_overview(app, _overview_study(explanation=explanation))

    assert 'data-ux="session-explanation"' in html
    assert "<summary>Why this topic</summary>" in html
    assert "data-mes-field" in html
    assert 'data-mes-field="supporting_evidence"' in html
    assert "Two recent practice attempts" in html
    assert 'data-ux="session-briefing"' in html
    # Sibling disclosures — explanation is not nested inside Session details.
    briefing_end = html.index("</details>", html.index('data-ux="session-briefing"'))
    explanation_start = html.index('data-ux="session-explanation"')
    assert explanation_start > briefing_end


def test_overview_html_omits_empty_explanation_disclosure(app, ctx):
    html = _render_overview(app, _overview_study(explanation=None))
    assert 'data-ux="session-explanation"' not in html
    assert "Why this topic" not in html
    assert "data-mes-field" not in html

    empty = ExplanationViewModel(has_content=False)
    html_empty = _render_overview(app, _overview_study(explanation=empty))
    assert 'data-ux="session-explanation"' not in html_empty
    assert "Why this topic" not in html_empty
    assert "data-mes-field" not in html_empty


def test_activity_surface_does_not_render_overview_explanation(app, ctx):
    explanation = ExplanationViewModel(
        summary="Should not appear on activity.",
        why_recommended="Hidden from non-overview surfaces.",
        evidence_points=("Evidence that must not render.",),
        has_content=True,
    )
    study = _overview_study(explanation=explanation)
    # StudySessionPage is frozen — rebuild with activity surface.
    study = StudySessionPage(
        **{
            **study.__dict__,
            "surface": "activity",
            "why_today": "",
            "learning_objectives": (),
        }
    )
    html = _render_overview(app, study)
    assert 'data-ux="session-explanation"' not in html
    assert "Why this topic" not in html
    assert "Evidence that must not render." not in html


def test_home_html_still_omits_mes_fields(app, ctx):
    """DX-005A calm-Home boundary — full MES stack stays off Home."""
    snap = HomeSnapshot(
        student_id="stu-1",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        recommendation_title="Cash flow statements",
        recommendation_summary="Focus on cash flow statements next.",
        estimated_study_minutes=25,
        explanation=ExplanationSnapshot(
            summary="Focus on cash flow statements next.",
            why_recommended=(
                "Your recent practice shows soft recall on cash flow statements."
            ),
            evidence_points=(
                "Two recent practice attempts scored below your topic average.",
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
    html = render_student_home(app, home_vm(snap, unified_journey=False))
    assert "data-mes-field" not in html
    assert "Why this guidance?" not in html
