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

HANDOFF = "Study Sensei is how Kwalitec guides your daily learning decisions."


def test_handoff_sentence_matches_board_authority():
    assert SENSEI_HANDOFF_SENTENCE == HANDOFF


def test_onboarding_steps_hand_off_to_study_sensei():
    steps = AlphaOnboardingService.steps()
    ids = [step["id"] for step in steps]
    assert ids[0] == "what"
    assert ids[1] == "sensei"
    bodies = " ".join(step["body"] for step in steps)
    titles = " ".join(step["title"] for step in steps)
    assert HANDOFF in bodies
    assert "Meet Study Sensei" in titles
    assert "Kwalitec prepares" not in bodies
    assert "reasons Kwalitec used" not in bodies
    assert "helps Kwalitec understand" not in bodies
    assert "Study Sensei prepares one focused Mission" in bodies
    assert "Start today's Session" in bodies
    assert "reasons Study Sensei used" in bodies


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


def test_home_template_names_study_sensei_and_guidance(app, ctx):
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
    page = SimpleNamespace(
        home=page_home,
        shell=SimpleNamespace(active_surface="home", navigation=()),
    )
    with app.test_request_context("/student/"):
        html = render_template("student/home.html", page=page, form=None)
    assert 'data-narrator="study-sensei"' in html
    assert "Study Sensei" in html
    assert "Why this guidance?" in html
    assert "Why this tip?" not in html
    assert "Coach insight" not in html
    assert ">Guidance<" in html or "Guidance</h2>" in html
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
    page = SimpleNamespace(
        shell=SimpleNamespace(session_id="sess-1"),
        overview=SimpleNamespace(
            objective="Practice cash flow statements",
            why_studying="Soft recall needs deliberate practice.",
            learning_goal="",
            estimated_duration_label="25 min",
            activity_count_label="3 activities",
            expected_improvement_label="",
            topics=("Cash flow",),
            begin_enabled=True,
        ),
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
            page=page,
            form=form,
            quick_check_embed=None,
        )
    assert 'data-narrator="study-sensei"' in html
    assert "Study Sensei" in html
    assert "focused practice on today's Mission" in html
