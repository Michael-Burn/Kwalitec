"""RR-001.3A — Educational identity & narrator consistency.

Verifies Kwalitec → Study Sensei handoff, lexicon compliance on
educational surfaces, and narrator ownership without changing
recommendation selection or Mission Intelligence composition.
"""

from __future__ import annotations

from types import SimpleNamespace

from flask import render_template, render_template_string

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.recommendation_commitment import (
    CONTINUITY_REFLECTION,
    WHAT_WAS_LEARNED_HUMBLE,
    compose_reflection,
)
from app.presentation.product_language import APPROVED_TERMS, REJECTED_SYNONYMS
from app.presentation.student.view_models import home_vm
from app.services.alpha_onboarding_service import (
    SENSEI_HANDOFF_SENTENCE,
    AlphaOnboardingService,
)
from tests.presentation.student.helpers import render_student_home

HANDOFF = "Study Sensei is how Kwalitec guides your daily learning decisions."


def test_handoff_sentence_matches_board_authority():
    assert SENSEI_HANDOFF_SENTENCE == HANDOFF


def test_onboarding_steps_hand_off_to_study_sensei():
    """Orientation is four practical steps; Sensei handoff lives in Help."""
    steps = AlphaOnboardingService.steps()
    ids = [step["id"] for step in steps]
    assert ids == ["what", "choose", "focus", "explainable"]
    bodies = " ".join(step["body"] for step in steps)
    titles = " ".join(step["title"] for step in steps)
    assert "What Kwalitec is" in titles
    assert "Choose your exam" in titles
    assert "Today's Focus" in titles
    assert "Guidance you can understand" in titles
    assert "Study Plan" in bodies
    assert "black box" in bodies
    assert SENSEI_HANDOFF_SENTENCE == HANDOFF


def test_product_language_approves_mission_and_rejects_tip_system():
    assert "Mission" in APPROVED_TERMS
    assert "Today's Mission" in APPROVED_TERMS
    assert "Study Sensei" in APPROVED_TERMS
    assert "Start Today's Session" in APPROVED_TERMS or "Session" in APPROVED_TERMS
    rejected = " ".join(REJECTED_SYNONYMS)
    assert "why this tip" in rejected
    assert "mission tip" in rejected
    assert "the system chose" in rejected


def test_commitment_continuity_retires_tip_noun():
    assert "tip" not in CONTINUITY_REFLECTION.lower()
    assert "Mission" in CONTINUITY_REFLECTION
    assert "tip" not in WHAT_WAS_LEARNED_HUMBLE.lower()
    assert "Mission" in WHAT_WAS_LEARNED_HUMBLE
    reflection = compose_reflection(title="Topic A")
    assert "tip" not in reflection.what_was_learned.lower()
    assert "tip" not in reflection.what_happens_next.lower()


def test_home_template_mission_first_without_guidance_panel(app, ctx):
    snap = HomeSnapshot(
        student_id="stu-rr13a",
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
            why_recommended="Soft recall on cash flow statements.",
            evidence_points=("Recent practice below topic average.",),
            expected_benefit="Strengthen cash flow analysis.",
            confidence_label="Suggested",
            suggested_next_action="Start a 25-minute practice Session.",
            review_point="Reassess after tonight's practice.",
            confidence_basis="Based on recent practice outcomes.",
            is_complete=True,
        ),
        has_recommendation=True,
        can_start_session=False,
    )
    page_home = home_vm(snap, unified_journey=False)
    html = render_student_home(app, page_home)
    assert 'data-narrator="study-sensei"' not in html
    assert "Study Sensei" not in html
    assert "Why this guidance?" not in html
    assert "Why this tip?" not in html
    assert "Coach insight" not in html
    assert ">Guidance<" not in html
    assert "Guidance</h2>" not in html
    assert "Today&#39;s Mission" in html or "Continue Session" in html
    assert "Optimising for" not in html


def test_runtime_c_panel_retires_system_narrator(app, ctx):
    edu = SimpleNamespace(
        active=True,
        today_topic_title="Cash flow",
        today_topic_code="CF",
        section_title="",
        position_label="",
        learning_objectives=(),
        mission_rationale="Practice cash flow",
        why_this_mission="Practice cash flow",
        estimated_duration_label="",
        completion_definition="",
        suggested_next_action="",
        unlocks_next="",
        prerequisite_status_label="",
        why_today="",
        why_previous_complete="",
        progress_label="",
        coverage_label="",
        pacing_summary="",
        feasibility_label="",
        exam_date_label="",
        supporting_evidence=("Plan position.",),
        journey_evidence=(),
        confidence_label="Suggested",
        expected_benefit="",
        review_point="",
    )
    tmpl = (
        '{% from "student/components/educational_experience.html" '
        "import educational_experience_panel %}"
        "{{ educational_experience_panel(edu, surface='home') }}"
    )
    with app.test_request_context("/student/"):
        html = render_template_string(tmpl, edu=edu)
    assert "Why this Mission?" in html
    assert "Why the system chose this" not in html


def test_session_overview_introduces_sensei_and_mission(app, ctx):
    """DX-005C: overview is a calm learning task — no Sensei chrome theatre."""
    from app.presentation.session.dto.study_session import (
        LearningTask,
        SessionPersistentContext,
        StudySessionPage,
    )

    study = StudySessionPage(
        page_title="Session",
        surface="overview",
        context=SessionPersistentContext(
            subject="Cash flow statements",
            chapter="Cash flow statements",
            objective="Practice cash flow statements",
            activity_label="Begin practice",
            session_progress="Session step 1 of 4",
            elapsed_label="25 min",
        ),
        task=LearningTask(
            activity="Begin practice",
            expected_outcome="Practice cash flow statements",
            estimated_duration="25 min",
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
        content_body="Practice cash flow statements",
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
    form = SimpleNamespace(
        hidden_tag=lambda: "",
        session_id=lambda: "",
        mission_id=lambda: "",
        submit=lambda **kwargs: '<button type="submit">Start Session</button>',
    )
    with app.test_request_context("/session/sess-1"):
        html = render_template(
            "session/overview.html",
            page=None,
            study=study,
            form=form,
            quick_check_embed=None,
        )
    assert "Soft recall needs deliberate practice." in html
    assert "Start Session" in html
    assert "Study Sensei" not in html
    assert 'data-narrator="study-sensei"' not in html
