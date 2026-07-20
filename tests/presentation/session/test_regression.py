"""Additional volume / regression / e2e presentation coverage."""

from __future__ import annotations

import pytest

from app.domain.session_experience.session_workspace import SessionSurface
from tests.application.session_experience.helpers import FakeActivityEnginePort
from tests.presentation.session.helpers import FORBIDDEN_TERMS, wire_session_experience


@pytest.mark.parametrize("session_i", range(25))
def test_overview_many_session_ids(session_client, session_app, session_i):
    sess = f"sess-vol-{session_i}"
    response = session_client.get(f"/session/{sess}/overview")
    assert response.status_code == 200
    html = response.get_data(as_text=True).lower()
    for term in FORBIDDEN_TERMS:
        assert term not in html


@pytest.mark.parametrize("surface_name", ["overview", "summary", "complete"])
def test_surfaces_render_when_workspace_aligned(
    session_client, session_app, surface_name
):
    svc = wire_session_experience(session_app)
    # Discover authenticated student id via overview open from request path.
    session_client.get("/session/sess-align/overview")
    # Locate workspace created under whatever student id the view used.
    workspaces = svc.registry.list_workspaces()
    assert workspaces
    ws = workspaces[-1]
    target = SessionSurface(surface_name)
    # Move forward lawfully then request surface.
    order = list(SessionSurface)
    for surface in order:
        ws = ws.navigate_to(surface)
        svc.registry.put_workspace(ws)
        if surface is target:
            break
    response = session_client.get(f"/session/{ws.session_id}/{surface_name}")
    assert response.status_code == 200


def test_full_http_session_flow(session_client, session_app):
    wire_session_experience(
        session_app, activity_engine=FakeActivityEnginePort(activities=1)
    )
    assert session_client.get("/session/sess-e2e/overview").status_code == 200
    begin = session_client.post(
        "/session/sess-e2e/begin",
        data={"session_id": "sess-e2e", "submit": "Begin Session"},
        follow_redirects=False,
    )
    assert "/activity" in begin.headers.get("Location", "")
    session_client.post(
        "/session/sess-e2e/activity/answer",
        data={
            "session_id": "sess-e2e",
            "activity_id": "act-1",
            "response": "Equity method under significant influence.",
            "submit": "Submit Answer",
        },
        follow_redirects=True,
    )
    advance = session_client.post(
        "/session/sess-e2e/activity/advance",
        data={"session_id": "sess-e2e", "submit": "Continue"},
        follow_redirects=False,
    )
    assert "/reflection" in advance.headers.get("Location", "")
    cont = session_client.post(
        "/session/sess-e2e/reflection/continue",
        data={"session_id": "sess-e2e", "submit": "Continue to Summary"},
        follow_redirects=False,
    )
    assert "/summary" in cont.headers.get("Location", "")
    finish = session_client.post(
        "/session/sess-e2e/complete",
        data={"session_id": "sess-e2e", "submit": "Return Home"},
        follow_redirects=False,
    )
    assert "/student" in finish.headers.get("Location", "")
