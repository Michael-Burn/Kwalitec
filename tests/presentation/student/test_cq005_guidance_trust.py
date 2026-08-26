"""CQ-005 — Guidance Trust presentation and continuity contracts."""

from __future__ import annotations

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.dto.readiness_explanation_snapshot import (
    ReadinessExplanationSnapshot,
)
from app.application.student_experience.dto.recommendation_alternative_snapshot import (
    RecommendationAlternativeSnapshot,
)
from app.domain.student_experience.recommendation_explanation import (
    build_explanation,
)
from app.infrastructure.session.activity_adapter import SessionActivityAdapter
from app.infrastructure.session.composition import (
    SessionExperienceComposition,
    _why_studying_from_recommendation,
)
from app.infrastructure.session.defaults import (
    default_activity,
    default_session_overview,
)
from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.student.view_models import home_vm
from tests.presentation.student.helpers import render_student_home


def test_default_why_studying_is_humble_not_generic_roi():
    overview = default_session_overview("stu-1", session_id="sess-1")
    assert overview["why_studying"] == "This Session is today's recommended next step."
    assert "High value for exam readiness" not in overview["why_studying"]


def test_why_studying_from_recommendation_prefers_authored_why():
    why = _why_studying_from_recommendation(
        {
            "summary": "Summary fallback",
            "explanation": {
                "why_recommended": "Soft recall needs deliberate practice.",
            },
        },
        topic="Leases",
    )
    assert why == "Soft recall needs deliberate practice."


def test_why_studying_from_recommendation_uses_summary_then_topic():
    assert "Focused practice" in _why_studying_from_recommendation(
        {"summary": "Focused practice where readiness gains are strongest today."},
        topic="Core methods",
    )
    assert "Cash flows" in _why_studying_from_recommendation({}, topic="Cash flows")


def test_composition_seeds_overview_why_from_adaptive():
    composition = SessionExperienceComposition(seed_demo_learners=True)
    composition.seed_learner("stu-cq005", demo=True)
    today = composition.mission.get_todays_session("stu-cq005") or {}
    session_id = str(today.get("session_id") or "sess-1")
    overview = composition.runtime.get_session_overview(
        "stu-cq005", session_id=session_id
    )
    assert overview is not None
    assert overview["why_studying"]
    assert overview["why_studying"] != "High value for exam readiness"
    assert (
        "readiness" in overview["why_studying"].lower()
        or "core methods" in overview["why_studying"].lower()
        or "practice" in overview["why_studying"].lower()
    )


def test_activity_context_echoes_mission_why():
    activity = default_activity(
        "stu-1",
        session_id="sess-1",
        index=1,
        total=3,
        topic_title="Leases",
        why_studying="Soft recall needs deliberate practice.",
    )
    assert "You're practising Leases because" in activity["context"]
    assert "Soft recall needs deliberate practice." in activity["context"]


def test_activity_adapter_threads_overview_why_into_context():
    store = SessionDocumentStore()
    runtime = SessionRuntimeAdapter(store=store)
    runtime.put_overview(
        "stu-1",
        session_id="sess-why",
        document={
            "objective": "Strengthen Leases",
            "topics": ("Leases",),
            "mission_id": "m1",
            "why_studying": "Soft recall needs deliberate practice.",
            "activity_count": 3,
        },
    )
    adapter = SessionActivityAdapter(store=store, activity_count=3)
    current = adapter.get_current_activity("stu-1", session_id="sess-why")
    assert current is not None
    assert "Soft recall needs deliberate practice." in current["context"]
    assert "You're practising Leases because" in current["context"]


def test_overview_labels_why_this_session(app, ctx):
    """Overview card + Session details host why-copy (not Home MES theatre)."""
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
        why_today="Soft recall needs deliberate practice.",
        topic_display="Cash flows",
        context_eyebrow="CS1 · Cash flows",
        meta_duration="30 min",
        meta_mode="Learning",
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
    assert "ds-session-card--overview" in html
    assert "Why today's topic" in html
    assert "Why this Session" not in html


def test_home_canonicalises_why_label_and_resume_reconnection(app, ctx):
    page_home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome back",
            has_recommendation=True,
            recommendation_title="Cash flows",
            recommendation_summary="Focused practice on Cash flows.",
            can_start_session=True,
            estimated_study_minutes=25,
            start_session=StartSessionActionSnapshot(
                label="Continue",
                enabled=True,
                can_start=True,
                mission_id="m1",
                session_id="sess-abc",
                estimated_minutes=25,
                topic_title="Cash flows",
            ),
            explanation=ExplanationSnapshot(
                summary="Focus on Cash flows.",
                why_recommended="Soft recall needs deliberate practice.",
                evidence_points=("Recent practice showed soft recall.",),
                expected_benefit="Protect weak recall before the exam",
                suggested_next_action="Start today's Session",
                timeliness_line="Exam timing makes this useful tonight.",
                is_complete=True,
            ),
        ),
        unified_journey=False,
    )
    assert page_home.session_control == "resume"
    html = render_student_home(app, page_home)
    assert 'data-habit="resume"' in html
    assert "Continue" in html
    assert "Open session" in html or "continue where you left off" in html.lower() or "Cash flows" in html
    assert 'data-habit="resume-why"' not in html
    assert "Still on this because" not in html
    assert "I’m doing this next" not in html
    assert "data-trust-coach" not in html
    assert ">Guidance<" not in html


def test_home_guidance_panel_absent(app, ctx):
    page_home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome back",
            has_recommendation=True,
            recommendation_title="Cash flows",
            can_start_session=True,
            estimated_study_minutes=30,
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="m1",
                session_id="sess-1",
                estimated_minutes=30,
                topic_title="Cash flows",
            ),
            explanation=ExplanationSnapshot(
                summary="Focus on Cash flows.",
                why_recommended="Soft recall needs deliberate practice.",
                evidence_points=("Recent practice showed soft recall.",),
                expected_benefit="Protect weak recall",
                suggested_next_action="Start today's Session",
                timeliness_line="Useful tonight.",
                is_complete=True,
            ),
            recommendation_alternatives=(
                RecommendationAlternativeSnapshot(
                    title="Ethics",
                    why_recommended="Supporting topic for later this week.",
                ),
            ),
        ),
        unified_journey=False,
    )
    html = render_student_home(app, page_home)
    assert 'data-trust-coach="alternatives"' not in html
    assert "Also considered" not in html
    assert "Ethics" not in html
    assert "Today&#39;s Mission" in html or "Continue Session" in html
    assert "data-mes-field" not in html


def test_home_readiness_panel_absent(app, ctx):
    page_home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome",
            examination_label="ACCA AA",
            exam_countdown_days=30,
            exam_readiness=0.42,
            exam_readiness_label="Building",
            has_recommendation=True,
            recommendation_title="Cash flows",
            can_start_session=True,
            readiness_explanation=ReadinessExplanationSnapshot(
                why_this_estimate="Based on recent sessions.",
                supporting_evidence=("Two practice sessions this week.",),
                confidence_label="Emerging",
                is_complete=True,
            ),
            explanation=ExplanationSnapshot(
                summary="Focus.",
                why_recommended="Why.",
                evidence_points=("Point.",),
                is_complete=True,
            ),
        ),
        unified_journey=False,
    )
    html = render_student_home(app, page_home)
    assert 'data-dashboard-panel="readiness"' not in html
    assert "What this is based on" not in html
    assert 'data-mes-field="readiness_drivers"' not in html
    assert "Why this estimate?" not in html
    assert ">Evidence<" not in html


def test_cold_start_why_avoids_learning_evidence_jargon():
    expl = build_explanation(topic_title="Leases")
    assert "learning evidence" not in expl.why_recommended.lower()
    assert "recent practice" in expl.why_recommended.lower()
