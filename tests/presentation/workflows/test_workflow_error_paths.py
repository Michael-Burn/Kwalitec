"""Error-path polishing for ARP-003 workflows."""

from __future__ import annotations

import pytest

from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.curriculum_studio.view_models import FLASH_WARNING
from tests.presentation.workflows.helpers import (
    advance_workspace_to,
    login_founder,
    login_student,
    wire_session,
    wire_studio,
)


@pytest.fixture
def student_client(app, client, ctx, user):
    wire_session(app)
    login_student(client)
    return client


@pytest.fixture
def founder_client(app, client, ctx):
    wire_studio(app, with_workspace=True)
    login_founder(client, app)
    return client


def test_session_ownership_returns_403(app, client, ctx, user):
    svc = wire_session(app)
    login_student(client)
    # Seed a workspace owned by a different student.
    svc.open_session("other-student", session_id="sess-foreign")
    response = client.get("/session/sess-foreign/overview")
    assert response.status_code == 403
    html = response.get_data(as_text=True).lower()
    assert "permission" in html or "access denied" in html
    assert "expired" in html or "shared" in html or "return" in html


def test_finish_validation_failure_stays_on_complete(student_client, app):
    svc = wire_session(app)
    student_client.get("/session/sess-fin/overview")
    advance_workspace_to(svc, "sess-fin", SessionSurface.COMPLETE)
    response = student_client.post(
        "/session/sess-fin/complete",
        data={},  # missing CSRF/fields when CSRF disabled still may fail validate
        follow_redirects=False,
    )
    # Empty post should not send the student to summary.
    if response.status_code in {302, 303}:
        loc = response.headers.get("Location", "")
        assert "/summary" not in loc
        assert "/complete" in loc or "/student" in loc


def test_begin_invalid_form_returns_to_overview(student_client):
    student_client.get("/session/sess-bad/overview")
    response = student_client.post(
        "/session/sess-bad/begin",
        data={},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "/overview" in response.headers.get("Location", "")


def test_answer_without_body_warns(student_client, app):
    student_client.get("/session/sess-ans/overview")
    student_client.post(
        "/session/sess-ans/begin",
        data={"session_id": "sess-ans", "submit": "Begin Session"},
        follow_redirects=True,
    )
    response = student_client.post(
        "/session/sess-ans/activity/answer",
        data={"session_id": "sess-ans", "activity_id": "act-1", "response": ""},
        follow_redirects=True,
    )
    html = response.get_data(as_text=True).lower()
    assert "answer" in html


def test_invalid_workspace_flash_copy():
    assert "could not be found" in FLASH_WARNING["workspace_missing"].lower()
    assert "curriculum studio" in FLASH_WARNING["workspace_missing"].lower()


def test_founder_invalid_workspace_redirect(founder_client):
    response = founder_client.get(
        "/console/studio/workspaces/missing-ws", follow_redirects=True
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True).lower()
    assert "workspace" in html


def test_unauthenticated_session_redirects_to_login(client):
    response = client.get("/session/sess-x/overview", follow_redirects=False)
    assert response.status_code in {302, 303}
    assert "login" in response.headers.get("Location", "").lower()


def test_unauthenticated_studio_redirects(client, app):
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    response = client.get("/console/studio/", follow_redirects=False)
    assert response.status_code in {302, 303}


@pytest.mark.parametrize(
    "path",
    (
        "/console/intelligence",
        "/console/evidence-gates",
        "/console/studio/",
    ),
)
def test_founder_pages_require_auth(client, app, path):
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    response = client.get(path, follow_redirects=False)
    assert response.status_code in {302, 303, 403}


def test_student_start_empty_post_does_not_500(student_client):
    response = student_client.post(
        "/student/session/start",
        data={},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    loc = response.headers.get("Location", "")
    # Either stays on home (form/port failure) or hands off to a session.
    assert "/student" in loc or "/session/" in loc
