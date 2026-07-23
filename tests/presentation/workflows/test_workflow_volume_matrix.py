"""Volume matrix — many workflow navigation permutations for ARP-003."""

from __future__ import annotations

import pytest

from app.domain.session_experience.session_workspace import SessionSurface
from app.founder.dashboard.nav import COMMAND_CENTRE_NAV, active_section_id
from app.presentation.curriculum_studio.view_models import PRIMARY_ACTION_BY_STAGE
from app.presentation.session.navigation import SURFACE_ENDPOINTS, page_meta
from tests.presentation.workflows.helpers import (
    STUDENT_SESSION_FLOW,
    advance_workspace_to,
    login_founder,
    login_student,
    surface_path,
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


@pytest.mark.parametrize("idx", range(12))
def test_many_session_overviews(student_client, idx):
    response = student_client.get(f"/session/sess-vol-{idx}/overview")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "surface",
    (
        SessionSurface.OVERVIEW,
        SessionSurface.ACTIVITY,
        SessionSurface.REFLECTION,
        SessionSurface.SUMMARY,
        SessionSurface.COMPLETE,
    ),
)
def test_resume_matrix_earlier_urls(student_client, app, surface):
    if surface is SessionSurface.OVERVIEW:
        pytest.skip("overview is the baseline surface")
    svc = wire_session(app)
    sid = f"sess-matrix-{surface.value}"
    student_client.get(f"/session/{sid}/overview")
    advance_workspace_to(svc, sid, surface)
    # Hitting every earlier surface URL must redirect back to active.
    for earlier in STUDENT_SESSION_FLOW:
        if earlier is surface:
            break
        response = student_client.get(
            surface_path(sid, earlier), follow_redirects=False
        )
        assert response.status_code in {302, 303}
        assert surface.value in response.headers.get("Location", "")


@pytest.mark.parametrize("nav_item", COMMAND_CENTRE_NAV)
def test_each_primary_nav_endpoint_resolves(nav_item):
    assert nav_item.endpoint
    assert nav_item.label
    assert nav_item.section_id
    assert active_section_id(nav_item.endpoint) == nav_item.section_id or (
        nav_item.section_id == "vision"
        and active_section_id(nav_item.endpoint) == "vision"
    )


@pytest.mark.parametrize("stage,primary", list(PRIMARY_ACTION_BY_STAGE.items()))
def test_primary_action_keys_stable(stage, primary):
    assert stage
    assert primary in {
        "advance",
        "validate",
        "preview",
        "approve",
        "publish",
        "version",
    }


@pytest.mark.parametrize("surface", list(SessionSurface))
def test_surface_endpoints_registered(app, surface):
    endpoint = SURFACE_ENDPOINTS[surface]
    assert endpoint in app.view_functions


@pytest.mark.parametrize("surface", list(SessionSurface))
def test_page_meta_step_counts(surface):
    eyebrow, title, description = page_meta(surface)
    assert "of 5" in eyebrow
    assert title
    assert description


def test_founder_studio_and_workspace_share_css(founder_client):
    index = founder_client.get("/console/studio/").get_data(as_text=True)
    workspace = founder_client.get("/console/studio/workspaces/ws-cs1").get_data(
        as_text=True
    )
    assert "founder_dashboard.css" in index
    assert "founder_dashboard.css" in workspace


def test_intelligence_and_gates_share_nav_shell(founder_client):
    intel = founder_client.get("/console/intelligence").get_data(as_text=True)
    gates = founder_client.get("/console/evidence-gates").get_data(as_text=True)
    assert "Assessments" in intel
    assert "Learning" in gates
    assert "Content" in intel and "Content" in gates
    assert "console-sidebar" in intel and "console-sidebar" in gates
