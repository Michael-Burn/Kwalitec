"""UX-001 — Student Home / Study Session presentation split."""

from __future__ import annotations

from pathlib import Path

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
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
)
from app.presentation.student.view_models import (
    StudentPageViewModel,
    StudentShellViewModel,
    home_vm,
)

ROOT = Path(__file__).resolve().parents[3]
HOME_TMPL = ROOT / "app/templates/student/home.html"
SESSION_BODY = ROOT / "app/templates/session/partials/session_body.html"


def _page(home_vm_obj) -> StudentPageViewModel:
    return StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=home_vm_obj,
    )


def test_home_template_is_decision_only():
    text = HOME_TMPL.read_text(encoding="utf-8")
    assert "ds_mission_hero" in text
    assert 'data-workspace-section="greeting"' in text
    assert 'data-workspace-section="todays-mission"' in text
    assert 'data-workspace-section="why-this-matters"' in text
    assert 'data-workspace-section="recent-progress"' in text
    assert 'data-workspace-section="study-signals"' in text
    assert 'data-workspace-section="tomorrow-preview"' in text
    assert 'data-workspace-section="quick-actions"' in text
    for removed in (
        "explanation_card",
        "readiness_card",
        "015-learning-episode",
        "Why this Session?",
        "Learning Episode",
        "Current Focus",
        "Morning Brief",
        'data-workspace-section="session-plan"',
        'data-workspace-section="forecast"',
        'data-workspace-section="learning-journey"',
        'data-workspace-section="morning-brief"',
        'data-workspace-section="current-focus"',
    ):
        assert removed not in text


def test_session_overview_hosts_briefing():
    text = SESSION_BODY.read_text(encoding="utf-8")
    assert 'data-ux="session-briefing"' in text
    assert "Why today's topic" in text
    assert "Learning objectives" in text
    assert "Concept focus" in text
    assert "Session stages" in text
    assert "Expected outcome" in text
    assert "Checkpoint" in text
    assert "Reflection" in text


def test_home_render_mission_hero_without_educational_stack(app, ctx):
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome",
            examination_label="CS1",
            has_recommendation=True,
            recommendation_title="Conditional probability",
            can_start_session=True,
            estimated_study_minutes=25,
            explanation=ExplanationSnapshot(
                summary="Practice conditional probability.",
                why_recommended="Builds on recent weak recall.",
                evidence_points=("Recent practice below average.",),
                expected_benefit="Strengthen readiness.",
                confidence_label="Suggested",
                suggested_next_action="Start a focused practice session.",
                review_point="Reassess after practice.",
                confidence_basis="Based on recent practice.",
                is_complete=True,
            ),
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="m1",
                topic_title="Conditional probability",
                estimated_minutes=25,
            ),
        ),
        unified_journey=False,
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
        html = render_template(
            "student/home.html", page=_page(home), home=page, form=None
        )
    assert "ds-mission-hero" in html
    assert "Conditional probability" in html
    assert "Why this Session?" not in html
    assert "Learning Episode" not in html
    assert "Expected outcome" not in html
    assert html.count("Conditional probability") <= 2
    assert page.greeting
    assert page.signals is not None
    assert not page.signals.estimated_study_label


def test_start_session_lands_on_overview(student_client, experience_app):
    from tests.application.student_experience.helpers import FakeMissionPort
    from tests.presentation.student.helpers import wire_experience

    mission = FakeMissionPort()
    wire_experience(experience_app, mission=mission)
    resp = student_client.post(
        "/student/session/start",
        data={
            "mission_id": "m1",
            "session_id": "sess-ux001",
            "submit": "Start Session",
        },
        follow_redirects=False,
    )
    assert resp.status_code in {302, 303}
    location = resp.headers["Location"]
    assert "/session/" in location
    assert "/activity" not in location


def test_overview_briefing_fields_render(app, ctx):
    study = StudySessionPage(
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
        concept_focus=("Present value", "Timing of cash flows"),
        session_stages=("Read", "Worked example", "Practice", "Reflection"),
        expected_outcome="You can price a simple cash-flow stream.",
        checkpoint_preview="Can you explain the timing choice?",
        reflection_preview="What still feels unclear?",
    )
    with app.test_request_context("/session/sess-1/"):
        from app.presentation.session.forms import BeginSessionForm

        form = BeginSessionForm()
        form.session_id.data = "sess-1"
        html = render_template(
            "session/partials/session_body.html",
            study=study,
            form=form,
            answer_form=None,
            advance_form=None,
        )
    assert 'data-ux="session-briefing"' in html
    assert "Why today's topic" in html
    assert "Builds on recent weak recall" in html
    assert "Apply discount factors correctly." in html
    assert "Present value" in html
    assert "Begin Session" in html
