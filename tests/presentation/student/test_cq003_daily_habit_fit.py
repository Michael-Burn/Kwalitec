"""CQ-003 — Daily Habit Fit presentation contracts."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from flask import render_template

from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.home_service import _start_action
from app.domain.student_experience.experience_session import (
    ExperienceSession,
    ExperienceSessionStatus,
)
from app.presentation.student.view_models import home_vm


def test_in_progress_start_action_uses_continue_label():
    action = _start_action(
        {
            "mission_id": "m1",
            "session_id": "s1",
            "status": "in_progress",
            "estimated_minutes": 25,
            "topic_title": "Cash flows",
        },
        {},
    )
    assert action is not None
    assert action.label == "Continue"
    assert action.enabled is True
    assert action.session_id == "s1"


def test_ready_start_action_uses_start_session_label():
    action = _start_action(
        {
            "mission_id": "m1",
            "session_id": None,
            "status": "ready",
            "topic_title": "Cash flows",
        },
        {},
    )
    assert action is not None
    assert action.label == "Start Session"


def test_experience_session_in_progress_cta_is_continue():
    handle = ExperienceSession.create(
        "exp-1",
        "1",
        status=ExperienceSessionStatus.IN_PROGRESS,
        mission_id="m1",
        session_id="s1",
    )
    assert handle.start_action().label == "Continue"


def test_home_resume_without_unified_journey(app, ctx):
    from app.presentation.student.services.student_home_service import (
        StudentHomeService,
    )
    from app.presentation.student.view_models import (
        StudentPageViewModel,
        StudentShellViewModel,
    )

    page_home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome back",
            has_recommendation=True,
            recommendation_title="Cash flows",
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
        ),
        unified_journey=False,
    )
    assert page_home.session_control == "resume"
    assert page_home.session_control_label == "Continue"
    assert page_home.session_id == "sess-abc"
    assert page_home.primary_cta_label == "Continue"
    assert page_home.quick_actions[0].href == "/session/sess-abc/overview"
    assert page_home.quick_actions[0].label == "Continue"

    page = StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=page_home,
    )
    with app.test_request_context("/student/"):
        home = StudentHomeService().build_home(page)
        html = render_template(
            "student/home.html", page=page, home=home, form=None
        )
    assert 'data-habit="resume"' in html
    assert 'data-habit="resume-cta"' in html
    assert 'data-session-control="resume"' in html
    assert "/session/sess-abc/overview" in html
    assert "Continue Session" in html
    assert "Not today" not in html
    assert "I’m doing this next" not in html
    # DX-005A allows one operational why-now on resume (not MES stack).
    assert html.count("Why now") <= 1


def test_begin_revision_lands_on_overview(
    student_client, experience_app, monkeypatch
):
    begin = MagicMock()
    monkeypatch.setattr(
        "app.presentation.session.views.begin_session",
        begin,
    )
    handle = SimpleNamespace(
        session_id="sess-rev-1",
        topic_title="Revision topic",
        student_id="1",
    )
    monkeypatch.setattr(
        "app.presentation.student.routes.start_todays_session",
        lambda **kwargs: handle,
    )
    monkeypatch.setattr(
        "app.presentation.student.routes.get_experience_composition",
        lambda: None,
    )
    resp = student_client.post(
        "/student/revision/begin",
        data={
            "mission_id": "m1",
            "session_id": "sess-rev-1",
            "option_id": "opt-1",
        },
        follow_redirects=False,
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/session/sess-rev-1/") or resp.headers[
        "Location"
    ].endswith("/session/sess-rev-1/overview")
    begin.assert_not_called()
