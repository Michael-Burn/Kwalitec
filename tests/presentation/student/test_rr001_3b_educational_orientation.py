"""RR-001.3B — Educational orientation & reflection coherence.

Verifies Help ecosystem map, reflection family mental model (DG-001.3),
and Product Check-in rename (EGC-R03 / EGC-R04 / EGC-R05) without changing
recommendation, Mission Intelligence, or curriculum behaviour.
"""

from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

from flask import render_template, render_template_string

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.domain.session_experience.reflection_projection import ReflectionProjection
from app.presentation.product_language import (
    APPROVED_TERMS,
    REFLECTION_FAMILY_MAP_SENTENCE,
    REJECTED_SYNONYMS,
)
from app.presentation.student.view_models import home_vm
from app.services.alpha_onboarding_service import (
    SENSEI_HANDOFF_SENTENCE,
    AlphaOnboardingService,
)


def test_reflection_map_sentence_matches_board_authority():
    assert "Product Check-in is feedback for the product team" in (
        REFLECTION_FAMILY_MAP_SENTENCE
    )
    assert "not educational reflection" in REFLECTION_FAMILY_MAP_SENTENCE
    assert "Decision Journal" in REFLECTION_FAMILY_MAP_SENTENCE
    assert "Educational Timeline" in REFLECTION_FAMILY_MAP_SENTENCE


def test_product_language_approves_orientation_terms():
    for term in (
        "Decision Journal",
        "Educational Timeline",
        "Session reflection",
        "Guided Reflection preview",
        "Product Check-in",
        "Study Sensei",
    ):
        assert term in APPROVED_TERMS
    rejected = " ".join(REJECTED_SYNONYMS)
    assert "daily reflection" in rejected


def test_onboarding_publishes_reflection_family_map():
    steps = AlphaOnboardingService.steps()
    reflection = next(step for step in steps if step["id"] == "reflection")
    assert reflection["title"] == "How Reflections work"
    assert REFLECTION_FAMILY_MAP_SENTENCE in reflection["body"]
    assert "Product Check-in" in reflection["body"]
    assert "not educational reflection" in reflection["body"]
    assert SENSEI_HANDOFF_SENTENCE in " ".join(step["body"] for step in steps)


def test_help_teaches_educational_ecosystem(client, ctx):
    from tests.test_alpha_001_infrastructure import _login, _make_alpha_user

    _make_alpha_user(onboarding_done=True)
    _login(client)
    body = client.get("/alpha/help").get_data(as_text=True)
    assert "Your educational journey" in body
    assert "One reflection family" in body
    assert "Educational glossary" in body
    assert SENSEI_HANDOFF_SENTENCE in body
    assert "Decision Journal" in body
    assert "Educational Timeline" in body
    assert "Study Sensei" in body
    assert "Product Check-in is feedback for the product team" in body
    assert "not educational reflection" in body
    assert "Session reflection" in body
    assert "Guided Reflection preview" in body
    assert "What is a Reflection, and why complete one?" in body
    assert "What does Product Check-in do?" in body
    assert "closest to being tested on" not in body
    assert "Daily Reflection" not in body


def test_help_answers_acceptance_questions(client, ctx):
    from tests.test_alpha_001_infrastructure import _login, _make_alpha_user

    _make_alpha_user(onboarding_done=True)
    _login(client)
    body = client.get("/alpha/help").get_data(as_text=True)
    assert "What is a Reflection, and why complete one?" in body
    assert "How is Reflection different from a Mission or Study Session?" in body
    assert "How is Reflection different from the Decision Journal?" in body
    assert "What does Product Check-in do?" in body
    assert "Mission is the focus; Session is the practice" in body


def test_product_checkin_never_titled_reflection(client, ctx):
    from tests.test_alpha_001_infrastructure import _login, _make_alpha_user

    _make_alpha_user(onboarding_done=True)
    _login(client)
    body = client.get(
        "/research/checkin?source=settings", follow_redirects=True
    ).get_data(as_text=True)
    assert "Product Check-in" in body
    assert "Daily Reflection" not in body
    assert "not educational reflection" in body
    assert "does not change Missions" in body
    assert 'data-rip001-checkin="1"' in body


def test_session_reflection_framing_aligns_with_architecture(app, ctx):
    with app.test_request_context("/session/s-rr13b/reflection"):
        tmpl = (
            "{% from 'session/components/reflection_card.html' "
            "import reflection_card %}"
            "{{ reflection_card(reflection) }}"
        )
        html = render_template_string(
            tmpl,
            reflection=ReflectionProjection(
                session_id="s-rr13b",
                topic_title="Cash flow",
                reflection_prompt="What felt clearer?",
            ),
        )
    assert "Session reflection" in html
    assert 'data-reflection-kind="session"' in html
    assert "not your Decision Journal" in html
    assert "Study Sensei" in html
    assert "never rates you" in html


def test_guided_reflection_preview_named_on_home(app, ctx):
    snap = HomeSnapshot(
        student_id="stu-rr13b",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        exam_readiness_label="Exam Readiness",
        recommendation_title="Cash flow",
        recommendation_summary="Focus next.",
        estimated_study_minutes=25,
        expected_readiness_improvement=0.03,
        explanation=ExplanationSnapshot(
            summary="Focus next.",
            why_recommended="Soft recall.",
            evidence_points=("Recent practice below average.",),
            expected_benefit="Strengthen analysis.",
            confidence_label="Suggested",
            suggested_next_action="Start a practice Session.",
            review_point="Reassess after practice.",
            confidence_basis="Based on recent practice.",
            is_complete=True,
        ),
        has_recommendation=True,
        can_start_session=False,
    )
    page = SimpleNamespace(
        home=replace(
            home_vm(snap),
            reflection_active=True,
            reflection_state="available",
            reflection_headline="Take a quiet minute",
            reflection_supporting_message="Think through what changed.",
            reflection_prompts=(),
            unified_journey_enabled=True,
        ),
        shell=SimpleNamespace(active_surface="home", navigation=()),
    )
    with app.test_request_context("/student/"):
        html = render_template("student/home.html", page=page, form=None)
    assert "Guided Reflection preview" in html
    assert "nothing here is recorded" in html
    assert "Product Check-in" in html
    assert "Daily Reflection" not in html
