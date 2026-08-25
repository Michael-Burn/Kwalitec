"""DX-006B Phase 6 — Study Session service unit tests."""

from __future__ import annotations

from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
    ReturnHomeActionSnapshot,
)
from app.application.session_experience.dto.overview_snapshot import (
    BeginSessionActionSnapshot,
    OverviewSnapshot,
)
from app.application.session_experience.dto.progress_snapshot import ProgressSnapshot
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.application.session_experience.facade import SessionFlowSnapshot
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    SessionWorkspace,
    SessionWorkspaceStatus,
)
from app.presentation.session.services.study_session_service import StudySessionService
from app.presentation.session.view_models import page_from_flow


def _workspace(surface: SessionSurface = SessionSurface.OVERVIEW) -> SessionWorkspace:
    return SessionWorkspace.create(
        workspace_id="ws-1",
        student_id="1",
        session_id="sess-1",
        status=SessionWorkspaceStatus.ACTIVE,
        active_surface=surface,
        topic_title="Probability",
    )


def test_overview_page_has_start_primary(app):
    flow = SessionFlowSnapshot(
        workspace=_workspace(SessionSurface.OVERVIEW),
        surface=SessionSurface.OVERVIEW.value,
        overview=OverviewSnapshot(
            experience_session_id="es-1",
            student_id="1",
            session_id="sess-1",
            objective="Apply Bayes to exam-style items",
            estimated_minutes=25,
            activity_count=3,
            topics=("Bayes' theorem",),
            can_begin=True,
            begin_action=BeginSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_begin=True,
                session_id="sess-1",
                mission_id="m1",
            ),
        ),
    )
    with app.test_request_context("/session/sess-1/overview"):
        study = StudySessionService().build_page(page_from_flow(flow))
    assert study.page_title == "Today: Probability"
    assert study.surface == "overview"
    assert study.primary_kind == "begin_form"
    assert study.primary_label in {"Start Session", "Begin Session"}
    assert study.primary_enabled is True
    assert study.context.subject == "Probability"
    assert "Bayes" in study.context.chapter or "Bayes" in study.context.objective
    assert study.task.activity == "Begin practice"
    assert "study session" not in study.page_title.lower()


def test_activity_answer_primary(app):
    flow = SessionFlowSnapshot(
        workspace=_workspace(SessionSurface.ACTIVITY),
        surface=SessionSurface.ACTIVITY.value,
        activity=ActivitySnapshot(
            activity_id="act-1",
            session_id="sess-1",
            question="What is P(A|B)?",
            context="Condition on evidence.",
            activity_index=2,
            activities_total=5,
            topic_title="Bayes' theorem",
            has_hints=True,
            hints=("Start from the definition.",),
        ),
        progress=ProgressSnapshot(
            session_id="sess-1",
            activities_completed=1,
            activities_remaining=4,
            activities_total=5,
            progress_percent=20,
            current_topic="Bayes' theorem",
        ),
    )
    with app.test_request_context("/session/sess-1/activity"):
        study = StudySessionService().build_page(page_from_flow(flow))
    assert study.primary_kind == "answer_form"
    assert study.primary_label == "Submit Answer"
    assert study.show_answer_input is True
    assert study.task.activity == "Answer question"
    assert any(d.title == "Hint" for d in study.disclosures)
    assert study.context.session_progress.startswith("Session step")


def test_activity_feedback_continue_primary(app):
    flow = SessionFlowSnapshot(
        workspace=_workspace(SessionSurface.ACTIVITY),
        surface=SessionSurface.ACTIVITY.value,
        activity=ActivitySnapshot(
            activity_id="act-1",
            session_id="sess-1",
            question="What is P(A|B)?",
            explanation="Review Bayes' theorem before continuing.",
            has_explanation=True,
            next_action_label="Continue",
            activity_index=2,
            activities_total=5,
        ),
    )
    with app.test_request_context("/session/sess-1/activity"):
        study = StudySessionService().build_page(page_from_flow(flow))
    assert study.primary_kind == "advance_form"
    assert study.primary_label == "Continue"
    assert study.show_answer_input is False
    assert study.feedback_outcome == "Reviewed"
    assert "Bayes" in study.feedback_explanation


def test_reading_activity_sticky_objective_not_full_body(app):
    """Sticky Objective must stay short — never dump Reading activity.context."""
    reading_body = "\n".join(
        [
            "Topic: t-statistic (2.6)",
            "Mission: Describe the distribution of the t-statistic",
            "",
            "Open the CMP:",
            "• Open your CMP at Syllabus 2.6.5",
            "",
            "Focus questions:",
            "• What is the core move of Syllabus 2.6.5?",
            "• What claim must you refuse today?",
            "",
            "Misconception watch:",
            "• Watch for using z when S replaces σ",
            "",
            "Out of scope today:",
            "• F distribution as primary (2.6.6)",
        ]
    )
    flow = SessionFlowSnapshot(
        workspace=_workspace(SessionSurface.ACTIVITY),
        surface=SessionSurface.ACTIVITY.value,
        activity=ActivitySnapshot(
            activity_id="act-read-1",
            session_id="sess-1",
            question="Purpose of this reading: extract Syllabus 2.6.5",
            context=reading_body,
            activity_type="read",
            stage_label="Reading",
            activity_index=1,
            activities_total=4,
            topic_title="t-statistic",
        ),
    )
    with app.test_request_context("/session/sess-1/activity"):
        study = StudySessionService().build_page(page_from_flow(flow))
    assert study.context.objective == "Complete today's reading"
    assert reading_body not in study.context.objective
    assert "Focus questions" not in study.context.objective
    assert study.content_sections
    assert any(s.label == "Focus questions" for s in study.content_sections)


def test_reflection_and_complete_primaries(app):
    reflection_flow = SessionFlowSnapshot(
        workspace=_workspace(SessionSurface.REFLECTION),
        surface=SessionSurface.REFLECTION.value,
        reflection=ReflectionSnapshot(
            session_id="sess-1",
            reflection_prompt="What mattered in this practice?",
            topic_title="Probability",
            next_action_label="Continue to Summary",
            concept_confidence="Improving",
        ),
    )
    complete_flow = SessionFlowSnapshot(
        workspace=_workspace(SessionSurface.COMPLETE),
        surface=SessionSurface.COMPLETE.value,
        completion=CompletionSnapshot(
            session_id="sess-1",
            student_id="1",
            topics_completed=("Probability",),
            activities_completed=3,
            can_return_home=True,
            return_home=ReturnHomeActionSnapshot(label="Return Home"),
            time_studied_minutes=25,
        ),
    )
    with app.test_request_context("/session/sess-1/"):
        reflection = StudySessionService().build_page(page_from_flow(reflection_flow))
        complete = StudySessionService().build_page(page_from_flow(complete_flow))
    assert reflection.primary_kind == "reflection_form"
    assert reflection.primary_label == "Continue to Summary"
    assert any(d.title == "Concept confidence" for d in reflection.disclosures)
    assert complete.primary_kind == "complete_form"
    assert complete.primary_label == "Return Home"
    assert "Probability" in complete.content_body


def test_overview_template_structure(app, client, ctx, user):
    from tests.presentation.workflows.helpers import login_student, wire_session

    wire_session(app)
    login_student(client)
    html = client.get("/session/sess-dx6/overview").get_data(as_text=True)
    assert 'id="session-page-title"' in html
    assert "Today:" in html or ">Session<" in html
    assert "Current Learning Task" in html
    assert "data-session-cta=\"primary\"" in html
    assert html.count("ds-btn--primary") == 1 or "ds-btn--primary" in html
    assert "design_system.css" in html or "ds-page" in html
    assert "Study Sensei" not in html
    assert "Readiness estimate" not in html
    assert "progressbar" not in html
    assert "study session" not in html.lower()
