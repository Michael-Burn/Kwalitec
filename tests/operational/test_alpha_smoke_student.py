"""Student and session HTTP smoke for Internal Alpha."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from app.domain.session_experience.session_workspace import SessionSurface
from tests.operational.helpers import (
    STUDENT_SMOKE_PATHS,
    alpha_flags,
    login_student,
    wire_session,
    wire_student,
)


@pytest.fixture
def student_client(app, client, ctx, user):
    wire_student(app)
    wire_session(app)
    login_student(client)
    return client


def test_student_surfaces_return_200(student_client):
    for path in STUDENT_SMOKE_PATHS:
        response = student_client.get(path)
        assert response.status_code == 200, path
        assert b"Internal Server Error" not in response.data
        assert b"Kwalitec" in response.data


def test_student_home_journey_and_insights(student_client):
    home = student_client.get("/student/").get_data(as_text=True)
    assert "Start" in home or "session" in home.lower()
    journey = student_client.get("/student/journey").get_data(as_text=True)
    assert "Journey" in journey
    insights = student_client.get("/student/revision").get_data(as_text=True)
    assert "Revision" in insights or "insight" in insights.lower()


def test_dual_run_back_link_visibility(student_client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=alpha_flags(SOLE_RUNTIME=False),
    ):
        dual = student_client.get("/student/").get_data(as_text=True)
    assert "Back to Dashboard" in dual
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=alpha_flags(SOLE_RUNTIME=True),
    ):
        sole = student_client.get("/student/").get_data(as_text=True)
    assert "Back to Dashboard" not in sole


def test_student_surfaces_require_login(client):
    for path in STUDENT_SMOKE_PATHS:
        response = client.get(path)
        assert response.status_code in {302, 401}, path
        if response.status_code == 302:
            assert "/auth/login" in response.headers["Location"]


def test_session_overview_and_linear_surfaces(student_client, app):
    service = wire_session(app)
    session_id = "alpha-smoke-session"
    response = student_client.get(f"/session/{session_id}/overview")
    assert response.status_code == 200
    assert service.registry.get_workspace_for_session(session_id) is not None

    for surface, suffix in (
        (SessionSurface.ACTIVITY, "activity"),
        (SessionSurface.REFLECTION, "reflection"),
        (SessionSurface.SUMMARY, "summary"),
        (SessionSurface.COMPLETE, "complete"),
    ):
        ws = service.registry.get_workspace_for_session(session_id)
        assert ws is not None
        service.registry.put_workspace(ws.navigate_to(surface))
        page = student_client.get(f"/session/{session_id}/{suffix}")
        assert page.status_code == 200, suffix
        assert b"Internal Server Error" not in page.data


def test_session_resume_does_not_rewind_overview(student_client, app):
    service = wire_session(app)
    session_id = "alpha-smoke-resume"
    student_client.get(f"/session/{session_id}/overview")
    student_client.post(
        f"/session/{session_id}/begin",
        data={"session_id": session_id, "submit": "Begin Session"},
        follow_redirects=True,
    )
    ws = service.registry.get_workspace_for_session(session_id)
    assert ws is not None
    assert ws.active_surface is SessionSurface.ACTIVITY

    response = student_client.get(
        f"/session/{session_id}/overview",
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "activity" in response.headers["Location"]
