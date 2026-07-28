"""CQ-005 — Guidance Trust presentation and continuity contracts."""

from __future__ import annotations

from types import SimpleNamespace

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
    assert "Cash flows" in _why_studying_from_recommendation(
        {}, topic="Cash flows"
    )


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
    page = SimpleNamespace(
        shell=SimpleNamespace(
            session_id="sess-1",
            topic_title="Cash flows",
            steps=(),
            page_eyebrow="Session",
            page_title="Overview",
            page_description="",
            active_surface="overview",
        ),
        overview=SimpleNamespace(
            objective="Strengthen Cash flows",
            learning_goal="",
            why_studying="Soft recall needs deliberate practice.",
            estimated_duration_label="About 30 minutes",
            activity_count_label="3 activities",
            topics=("Cash flows",),
            expected_improvement_label="",
            begin_label="Start Session",
            begin_enabled=True,
            mission_id="m1",
        ),
        progress=None,
        activity=None,
    )
    with app.test_request_context("/session/sess-1/overview"):
        html = render_template(
            "session/overview.html",
            page=page,
            form=None,
            quick_check_embed=None,
        )
    assert "Why this Session" in html
    assert "Soft recall needs deliberate practice." in html
    assert 'data-session="why"' in html


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
    page = SimpleNamespace(
        home=page_home,
        shell=SimpleNamespace(active_surface="home", navigation=()),
        educational=None,
    )
    with app.test_request_context("/student/"):
        html = render_template("student/home.html", page=page, form=None)
    assert 'data-habit="resume"' in html
    assert 'data-habit="resume-why"' in html
    assert "Still on this because" in html
    assert "Soft recall needs deliberate practice." in html
    assert "Why now" not in html
    assert "I’m doing this next" not in html


def test_home_guidance_surfaces_basis_instead_of_pointer(app, ctx):
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
    page = SimpleNamespace(
        home=page_home,
        shell=SimpleNamespace(active_surface="home", navigation=()),
        educational=None,
    )
    with app.test_request_context("/student/"):
        html = render_template("student/home.html", page=page, form=None)
    assert 'data-trust-coach="alternatives"' in html
    assert "Also considered" in html
    assert "Ethics" in html
    assert "Mission card above" not in html


def test_readiness_disclosure_avoids_evidence_label(app, ctx):
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
    page = SimpleNamespace(
        home=page_home,
        shell=SimpleNamespace(active_surface="home", navigation=()),
        educational=None,
    )
    with app.test_request_context("/student/"):
        html = render_template("student/home.html", page=page, form=None)
    assert "What this is based on" in html
    assert ">Evidence<" not in html


def test_cold_start_why_avoids_learning_evidence_jargon():
    expl = build_explanation(topic_title="Leases")
    assert "learning evidence" not in expl.why_recommended.lower()
    assert "recent practice" in expl.why_recommended.lower()
