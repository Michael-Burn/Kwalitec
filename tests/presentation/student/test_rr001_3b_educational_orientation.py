"""RR-001.3B — Educational orientation & reflection coherence.

Verifies Help ecosystem map, reflection family mental model (DG-001.3),
and Product Check-in rename (EGC-R03 / EGC-R04 / EGC-R05) without changing
recommendation, Mission Intelligence, or curriculum behaviour.
"""

from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

from flask import render_template

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
from tests.presentation.student.helpers import render_student_home


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
    """Reflection family map is taught in Help; onboarding stays practical."""
    steps = AlphaOnboardingService.steps()
    assert "reflection" not in {step["id"] for step in steps}
    assert REFLECTION_FAMILY_MAP_SENTENCE
    assert "Product Check-in is feedback for the product team" in (
        REFLECTION_FAMILY_MAP_SENTENCE
    )
    assert SENSEI_HANDOFF_SENTENCE


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
    """Session reflection is a Study Session surface label, not a Sensei card."""
    from app.presentation.session.dto.study_session import (
        LearningTask,
        SessionPersistentContext,
        StudySessionPage,
    )

    study = StudySessionPage(
        page_title="Today: Cash flow",
        surface="reflection",
        context=SessionPersistentContext(
            subject="Cash flow",
            chapter="Cash flow",
            objective="Reflect on practice",
            activity_label="Session reflection",
            session_progress="Session step 3 of 4",
            elapsed_label="",
        ),
        task=LearningTask(
            activity="Session reflection",
            expected_outcome="Reflect on Cash flow",
            estimated_duration="",
            next_milestone="Return Home",
            instruction="What felt clearer?",
        ),
        primary_label="Continue to Summary",
        primary_kind="reflection_form",
        primary_enabled=True,
        blocking_issue="",
        exit_href="/student/",
        exit_label="Exit",
        content_title="",
        content_body="",
        content_support="",
        answer_prompt="What felt clearer?",
        show_answer_input=True,
        feedback_outcome="",
        feedback_explanation="",
        disclosures=(),
        technical_lines=(),
        session_id="s-rr13b",
        activity_id="",
        mission_id="",
        stage_position_label="Reflection",
        content_stage="reflection",
    )

    class _Field:
        name = "reflection_note"
        id = "reflection_note"

        def __call__(self, **kwargs):
            return ""

    form = SimpleNamespace(
        hidden_tag=lambda: "",
        session_id=lambda: "",
        reflection_note=_Field(),
        confidence_rating=SimpleNamespace(
            name="confidence_rating",
            data=None,
            choices=(),
        ),
    )
    with app.test_request_context("/session/s-rr13b/reflection"):
        html = render_template(
            "session/reflection.html",
            page=None,
            study=study,
            form=form,
        )
    assert "ds-learning-task" not in html
    assert "A moment to reflect" not in html
    assert "What felt clearer?" in html
    assert "Reflection" in html
    assert 'class="ds-session-reflection__prompt"' in html
    assert (
        ReflectionProjection(
            session_id="s-rr13b",
            topic_title="Cash flow",
            reflection_prompt="What felt clearer?",
        ).reflection_prompt
        == "What felt clearer?"
    )


def test_guided_reflection_preview_not_on_home(app, ctx):
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
    page_home = replace(
        home_vm(snap),
        reflection_active=True,
        reflection_state="available",
        reflection_headline="Take a quiet minute",
        reflection_supporting_message="Think through what changed.",
        reflection_prompts=(),
        unified_journey_enabled=True,
    )
    html = render_student_home(app, page_home)
    assert "Guided Reflection preview" not in html
    assert "nothing here is recorded" not in html
    assert "Product Check-in" not in html
    assert "Today&#39;s Mission" in html or "Continue Session" in html
