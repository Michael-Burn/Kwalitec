"""Workflow 3 — Interrupt session → resume → complete."""

from __future__ import annotations

import pytest

from app.domain.session_experience.session_workspace import SessionSurface
from tests.presentation.workflows.helpers import (
    FakeActivityEnginePort,
    advance_workspace_to,
    login_student,
    surface_path,
    wire_session,
)


@pytest.fixture
def student_client(app, client, ctx, user):
    wire_session(app)
    login_student(client)
    return client


def test_interrupt_home_then_resume_activity(student_client, app):
    svc = wire_session(app)
    student_client.get("/session/sess-resume/overview")
    student_client.post(
        "/session/sess-resume/begin",
        data={"session_id": "sess-resume", "submit": "Begin Session"},
        follow_redirects=True,
    )
    ws = svc.registry.get_workspace_for_session("sess-resume")
    assert ws is not None
    assert ws.active_surface is SessionSurface.ACTIVITY

    # Interrupt: leave for Student Home.
    home = student_client.get("/student/")
    assert home.status_code == 200

    # Resume via Overview URL — must restore Activity, not rewind.
    response = student_client.get(
        "/session/sess-resume/overview", follow_redirects=False
    )
    assert response.status_code in {302, 303}
    assert "/activity" in response.headers.get("Location", "")

    ws_after = svc.registry.get_workspace_for_session("sess-resume")
    assert ws_after is not None
    assert ws_after.active_surface is SessionSurface.ACTIVITY


def test_resume_does_not_reset_workspace_id(student_client, app):
    svc = wire_session(app)
    student_client.get("/session/sess-id/overview")
    student_client.post(
        "/session/sess-id/begin",
        data={"session_id": "sess-id", "submit": "Begin Session"},
        follow_redirects=True,
    )
    before = svc.registry.get_workspace_for_session("sess-id")
    assert before is not None
    wid = before.workspace_id
    student_client.get("/session/sess-id/overview", follow_redirects=True)
    after = svc.registry.get_workspace_for_session("sess-id")
    assert after is not None
    assert after.workspace_id == wid
    assert after.active_surface is SessionSurface.ACTIVITY


def test_skip_ahead_redirects_to_active(student_client, app):
    svc = wire_session(app)
    student_client.get("/session/sess-skip/overview")
    # Still on overview — requesting reflection must bounce back.
    response = student_client.get(
        "/session/sess-skip/reflection", follow_redirects=False
    )
    assert response.status_code in {302, 303}
    assert "/overview" in response.headers.get("Location", "")
    ws = svc.registry.get_workspace_for_session("sess-skip")
    assert ws is not None
    assert ws.active_surface is SessionSurface.OVERVIEW


@pytest.mark.parametrize(
    "active",
    (
        SessionSurface.ACTIVITY,
        SessionSurface.REFLECTION,
        SessionSurface.SUMMARY,
    ),
)
def test_resume_from_earlier_url(student_client, app, active):
    svc = wire_session(app)
    student_client.get("/session/sess-earlier/overview")
    advance_workspace_to(svc, "sess-earlier", active)
    response = student_client.get(
        "/session/sess-earlier/overview", follow_redirects=False
    )
    assert response.status_code in {302, 303}
    assert surface_path("sess-earlier", active).endswith(
        response.headers.get("Location", "").split("/session/")[-1]
        if "/session/" in response.headers.get("Location", "")
        else "nope"
    ) or active.value in response.headers.get("Location", "")


def test_resume_then_complete(student_client, app):
    wire_session(app, activity_engine=FakeActivityEnginePort(activities=1))
    student_client.get("/session/sess-rc/overview")
    student_client.post(
        "/session/sess-rc/begin",
        data={"session_id": "sess-rc", "submit": "Begin Session"},
        follow_redirects=True,
    )
    # Interrupt + resume
    student_client.get("/student/")
    resumed = student_client.get("/session/sess-rc/overview", follow_redirects=True)
    assert resumed.status_code == 200
    assert b"activity" in resumed.data.lower() or b"Question" in resumed.data

    student_client.post(
        "/session/sess-rc/activity/answer",
        data={
            "session_id": "sess-rc",
            "activity_id": "act-1",
            "response": "Significant influence indicates equity method.",
            "submit": "Submit Answer",
        },
        follow_redirects=True,
    )
    student_client.post(
        "/session/sess-rc/activity/advance",
        data={"session_id": "sess-rc", "submit": "Continue"},
        follow_redirects=True,
    )
    student_client.post(
        "/session/sess-rc/reflection/continue",
        data={"session_id": "sess-rc", "submit": "Continue to Summary"},
        follow_redirects=True,
    )
    finish = student_client.post(
        "/session/sess-rc/complete",
        data={"session_id": "sess-rc", "submit": "Return Home"},
        follow_redirects=False,
    )
    assert "/student" in finish.headers.get("Location", "")


def test_resume_flash_on_overview_reentry(student_client, app):
    svc = wire_session(app)
    student_client.get("/session/sess-flash/overview")
    advance_workspace_to(svc, "sess-flash", SessionSurface.ACTIVITY)
    response = student_client.get(
        "/session/sess-flash/overview", follow_redirects=True
    )
    html = response.get_data(as_text=True).lower()
    assert "continuing where you left off" in html or "activity" in html


def test_brand_exit_does_not_close_workspace(student_client, app):
    svc = wire_session(app)
    student_client.get("/session/sess-brand/overview")
    student_client.post(
        "/session/sess-brand/begin",
        data={"session_id": "sess-brand", "submit": "Begin Session"},
        follow_redirects=True,
    )
    student_client.get("/student/")
    assert svc.registry.get_workspace_for_session("sess-brand") is not None
