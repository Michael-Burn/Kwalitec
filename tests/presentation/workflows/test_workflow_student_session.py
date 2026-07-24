"""Workflow 2 — Student Home → Session → Complete → Home."""

from __future__ import annotations

import pytest

from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.navigation import page_meta
from app.presentation.session.view_models import FORBIDDEN_LEARNER_TERMS
from tests.presentation.workflows.helpers import (
    STUDENT_SESSION_FLOW,
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


def test_student_home_reachable(student_client):
    response = student_client.get("/student/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Dashboard" in html or "dashboard" in html.lower() or "Home" in html


def test_session_overview_from_home_handoff(student_client):
    response = student_client.get("/session/sess-wf2/overview")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Begin Session" in html or "begin" in html.lower()
    assert "Session · Step" in html
    assert "Learning Session ·" not in html


def test_begin_advances_to_activity(student_client):
    student_client.get("/session/sess-wf2/overview")
    response = student_client.post(
        "/session/sess-wf2/begin",
        data={"session_id": "sess-wf2", "submit": "Begin Session"},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "/activity" in response.headers.get("Location", "")


def test_full_session_happy_path(student_client, app):
    wire_session(app, activity_engine=FakeActivityEnginePort(activities=1))
    assert student_client.get("/session/sess-full/overview").status_code == 200
    begin = student_client.post(
        "/session/sess-full/begin",
        data={"session_id": "sess-full", "submit": "Begin Session"},
        follow_redirects=False,
    )
    assert "/activity" in begin.headers.get("Location", "")
    student_client.post(
        "/session/sess-full/activity/answer",
        data={
            "session_id": "sess-full",
            "activity_id": "act-1",
            "response": "Equity method applies under significant influence.",
            "submit": "Submit Answer",
        },
        follow_redirects=True,
    )
    advance = student_client.post(
        "/session/sess-full/activity/advance",
        data={"session_id": "sess-full", "submit": "Continue"},
        follow_redirects=False,
    )
    assert "/reflection" in advance.headers.get("Location", "")
    cont = student_client.post(
        "/session/sess-full/reflection/continue",
        data={"session_id": "sess-full", "submit": "Continue to Summary"},
        follow_redirects=False,
    )
    assert "/summary" in cont.headers.get("Location", "")
    summary = student_client.get("/session/sess-full/summary")
    assert summary.status_code == 200
    finish = student_client.post(
        "/session/sess-full/complete",
        data={"session_id": "sess-full", "submit": "Return Home"},
        follow_redirects=False,
    )
    assert "/student" in finish.headers.get("Location", "")


@pytest.mark.parametrize("surface", list(STUDENT_SESSION_FLOW))
def test_surface_page_meta_titles(surface):
    eyebrow, title, description = page_meta(surface)
    assert eyebrow.startswith("Session · Step")
    assert "Learning Session" not in eyebrow
    assert title
    assert description


@pytest.mark.parametrize(
    "surface",
    (
        SessionSurface.OVERVIEW,
        SessionSurface.SUMMARY,
        SessionSurface.COMPLETE,
    ),
)
def test_aligned_surface_renders(student_client, app, surface):
    svc = wire_session(app)
    student_client.get("/session/sess-align/overview")
    advance_workspace_to(svc, "sess-align", surface)
    response = student_client.get(surface_path("sess-align", surface))
    assert response.status_code == 200


def test_finish_flash_mentions_home_updates(student_client, app):
    svc = wire_session(app)
    student_client.get("/session/sess-done/overview")
    advance_workspace_to(svc, "sess-done", SessionSurface.COMPLETE)
    response = student_client.post(
        "/session/sess-done/complete",
        data={"session_id": "sess-done", "submit": "Return Home"},
        follow_redirects=True,
    )
    html = response.get_data(as_text=True).lower()
    assert "session complete" in html or "home" in html


def test_session_chrome_has_brand_exit(student_client):
    html = student_client.get("/session/sess-chrome/overview").get_data(as_text=True)
    assert "/student/" in html or "student.home" in html or "Kwalitec" in html


def test_student_nav_surfaces_present(student_client):
    html = student_client.get("/student/").get_data(as_text=True)
    for label in (
        "Dashboard",
        "Journey",
        "Revision",
        "Analytics",
        "Settings",
        "Study Plan",
        "Help",
    ):
        assert label in html


@pytest.mark.parametrize(
    "path",
    ("/student/journey", "/student/history", "/student/profile"),
)
def test_secondary_student_surfaces_ok(student_client, path):
    assert student_client.get(path).status_code == 200


def test_forbidden_terms_absent_from_session(student_client):
    html = (
        student_client.get("/session/sess-terms/overview")
        .get_data(as_text=True)
        .lower()
    )
    for term in FORBIDDEN_LEARNER_TERMS:
        assert term not in html


def test_progress_chrome_lists_linear_steps(student_client):
    html = student_client.get("/session/sess-steps/overview").get_data(as_text=True)
    assert "Session Overview" in html or "overview" in html.lower()
    assert "Learning Activity" in html or "Reflection" in html
