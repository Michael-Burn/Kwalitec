"""RR-001.3D — Educational consistency & experience refinement.

Verifies Home naming density, Mission Intelligence educational chrome,
Session readiness honesty, Revision Mission primacy, Feedback Loop
student terminology, success/empty honesty, and Quick Check residual
policy — without changing recommendation or MI algorithms.
"""

from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.dto.revision_snapshot import (
    RevisionOptionSnapshot,
    RevisionSnapshot,
)
from app.domain.session_experience.completion_projection import (
    readiness_change_label,
)
from app.domain.student_experience.revision_projection import RevisionProjection
from app.presentation.product_language import (
    FEEDBACK_LOOP_STUDENT_TERM,
    FEEDBACK_LOOP_TERMINOLOGY_POLICY,
    HOME_SENSEI_NAMING_POLICY,
    REJECTED_SYNONYMS,
    REVISION_MISSION_PRIMACY_SENTENCE,
)
from app.presentation.student.view_models import home_vm, revision_vm
from tests.presentation.student.helpers import render_student_home


def test_home_naming_density_policy_published():
    assert "once in the hero" in HOME_SENSEI_NAMING_POLICY.lower()
    assert "guidance panel" in HOME_SENSEI_NAMING_POLICY.lower()


def test_feedback_loop_student_term_is_sensei_reflection():
    assert FEEDBACK_LOOP_STUDENT_TERM == "Sensei reflection"
    assert "feedback loop" in REJECTED_SYNONYMS
    assert "Feedback Loop" in FEEDBACK_LOOP_TERMINOLOGY_POLICY
    assert "does not re-rank" in FEEDBACK_LOOP_TERMINOLOGY_POLICY


def test_revision_mission_primacy_sentence():
    assert "not a second Mission" in REVISION_MISSION_PRIMACY_SENTENCE
    assert "supports today's Mission" in REVISION_MISSION_PRIMACY_SENTENCE
    assert "today's best revision" in REJECTED_SYNONYMS


def test_home_template_mission_first_without_legacy_chrome(app, ctx):
    snap = HomeSnapshot(
        student_id="stu-rr13d",
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
            expected_benefit="Support progress toward exam readiness.",
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
    assert "Readiness, journey, and guidance" not in html
    assert "Readiness, journey, and coach" not in html
    assert "Today&#39;s Mission" in html or "Continue Session" in html
    assert "Optimising for" not in html
    assert "Focusing on" not in html
    assert "Mission confidence" not in html
    assert "coach insight" not in html.lower()
    assert "Prepare Checkpoint" not in html
    assert "Review Reflection" not in html


def test_home_mi_chrome_not_on_home(app, ctx):
    mi = SimpleNamespace(
        has_mission=True,
        eyebrow="Today's Mission",
        focus_question="What should I focus on today?",
        educational_purpose="Practice cash flow",
        why_today="Soft recall needs attention",
        why_not_something_else="",
        supporting_evidence=(),
        evidence_heading="Supporting evidence",
        estimated_effort="25 min",
        expected_learning_outcome="Support progress toward exam readiness",
        what_happens_after_completion="",
        after_heading="After you finish",
        mission_confidence="Suggested",
        uncertainty="Sparse recent practice",
        mission_explanation="Chosen from today's Mission evidence",
        explainability_heading="Why this Mission",
        skip_consequence="",
        skip_heading="If you skip today",
        reflection_prompt="Did this guidance help?",
        reflection_heading="Sensei reflection",
        optimisation_axis_label="Learning value",
        lifecycle_phase="presented",
    )
    snap = HomeSnapshot(
        student_id="stu-rr13d-mi",
        greeting="Welcome",
        examination_label="ACCA AA",
        recommendation_title="Cash flow",
        recommendation_summary="Focus next.",
        has_recommendation=True,
        can_start_session=False,
    )
    page_home = home_vm(snap, unified_journey=False)
    page_home = replace(page_home, mission_intelligence=mi)
    html = render_student_home(app, page_home)
    assert "Educational priority: learning value" not in html
    assert "How sure this guidance feels" not in html
    assert "What is still uncertain" not in html
    assert "Sensei reflection" not in html
    assert "data-mission-intelligence" not in html
    assert "Today&#39;s Mission" in html or "Continue Session" in html
    assert "Focusing on" not in html
    assert "Optimising for" not in html


def test_session_readiness_labels_are_honest():
    assert readiness_change_label(0.05) == "Readiness estimate moved up a little"
    assert readiness_change_label(-0.05) == "Readiness estimate eased a little"
    assert readiness_change_label(0.0) == "Readiness estimate held steady"
    assert "Exam readiness improved" not in {
        readiness_change_label(0.05),
        readiness_change_label(-0.05),
        readiness_change_label(0.0),
    }


def test_session_completion_omits_readiness_kpi(app, ctx):
    """DX-005C / DX-006B Phase 6: Session must not show readiness theatre."""
    from app.presentation.session.dto.study_session import (
        LearningTask,
        SessionPersistentContext,
        StudySessionPage,
    )

    study = StudySessionPage(
        page_title="Session",
        surface="summary",
        context=SessionPersistentContext(
            subject="Cash flow",
            chapter="Cash flow",
            objective="Complete the current practice step",
            activity_label="Session complete",
            session_progress="Session step 4 of 4",
        ),
        task=LearningTask(
            activity="Complete session",
            expected_outcome="Close practice and return to Home",
            estimated_duration="",
            next_milestone="Home",
            instruction="Practice on Cash flow is finished.",
        ),
        primary_label="Return Home",
        primary_kind="complete_form",
        primary_enabled=True,
        blocking_issue="",
        exit_href="/student/",
        exit_label="Exit",
        content_title="Session complete",
        content_body="Session practice on Cash flow is complete.",
        content_support="",
        answer_prompt="Your answer",
        show_answer_input=False,
        feedback_outcome="",
        feedback_explanation="",
        disclosures=(),
        technical_lines=(),
        session_id="sess-1",
        activity_id="",
    )
    with app.test_request_context("/session/complete"):
        html = render_template(
            "session/summary.html", study=study, form=None, page=None
        )
    assert "Cash flow" in html
    assert "Readiness estimate" not in html
    assert "Exam readiness" not in html


def test_revision_template_declares_mission_primacy(app, ctx):
    """PX-001: primacy is product law in constants — UI guides, does not lecture."""
    from app.presentation.product_language import REVISION_MISSION_PRIMACY_SENTENCE

    assert "not a second Mission" in REVISION_MISSION_PRIMACY_SENTENCE
    snap = RevisionSnapshot(
        student_id="stu-rr13d-rev",
        primary=RevisionOptionSnapshot(
            option_id="rev-1",
            topic_title="Cash flow revision",
            priority_label="High",
            estimated_study_minutes=20,
            expected_benefit="Strengthen cash flow recall",
            is_primary=True,
        ),
        alternatives=(),
        has_revision=True,
        option_count=1,
    )
    page = SimpleNamespace(
        shell=SimpleNamespace(page_title="Revision", navigation=()),
        revision=revision_vm(snap),
    )
    with app.test_request_context("/student/revision"):
        html = render_template("student/revision.html", page=page, form=None)
    assert "Strengthen what you practised." in html
    assert "Cash flow revision" in html
    assert "Today's best revision" not in html
    assert "Begin Revision" in html or "ds-os-recommend" in html

def test_revision_empty_teaches_mission_next_step(app, ctx):
    proj = RevisionProjection.create("stu-empty")
    assert "Mission" in proj.empty_message
    assert "today's session" not in proj.empty_message.lower()
    page = SimpleNamespace(
        shell=SimpleNamespace(page_title="Revision", navigation=()),
        revision=revision_vm(
            RevisionSnapshot(
                student_id="stu-empty",
                primary=None,
                alternatives=(),
                empty_message=proj.empty_message,
                has_revision=False,
                option_count=0,
            )
        ),
    )
    with app.test_request_context("/student/revision"):
        html = render_template("student/revision.html", page=page, form=None)
    assert (
        "Return to today's Mission" in html or "Return to today&#39;s Mission" in html
    )
    assert "Nothing to revise yet" in html
    assert "Quick Check" not in html
    assert "Mission tip" not in html


def test_help_teaches_sensei_reflection_not_feedback_loop(client, ctx):
    from tests.test_alpha_001_infrastructure import _login, _make_alpha_user

    _make_alpha_user(onboarding_done=True)
    _login(client)
    html = client.get("/alpha/help").get_data(as_text=True)
    assert "Sensei reflection" in html
    assert "Feedback Loop" in html  # policy disclosure only
    assert "Students do not see" in html or "does not re-rank" in html
    assert "never a second Mission" in html
    assert "Students do not see" in html
    assert "does not re-rank" in html
    lowered = html.lower()
    assert "sensei reflection" in lowered


def test_assessment_complete_avoids_overclaim(app, ctx):
    page = SimpleNamespace(
        after_completion="Return to today's Mission when ready.",
        observation_count=0,
        shell=SimpleNamespace(
            page_eyebrow="Learning check",
            page_title="Check complete",
            status="complete",
        ),
    )
    with app.test_request_context("/student/assessment/complete"):
        html = render_template(
            "student/assessment/complete.html",
            page=page,
            title="Check complete",
        )
    assert "supports today's Session" in html or "supports today&#39;s Session" in html
    assert "without claiming mastery" in html
    assert "helps Kwalitec understand how to support you" not in html
    assert "gathers evidence that supports today's Mission" not in html


def test_product_language_rejects_engineering_and_competing_focus():
    rejected = " ".join(REJECTED_SYNONYMS)
    assert "optimising for" in rejected
    assert "today's best revision" in rejected
    assert "feedback loop" in rejected
    assert "coach insight" in rejected
    assert "mission tip" in rejected
