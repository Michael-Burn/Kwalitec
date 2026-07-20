"""HTTP rendering tests for Founder Studio / Intelligence / Evidence Gates."""

from __future__ import annotations

import pytest

from tests.presentation.curriculum_studio.helpers import login_founder, wire_studio


@pytest.fixture
def founder_client(client, ctx, app):
    login_founder(client, app)
    wire_studio(app, with_workspace=True)
    return client


def test_studio_dashboard_renders_empty_friendly_when_no_workspaces(
    client, ctx, app
):
    login_founder(client, app)
    wire_studio(app, with_workspace=False)
    response = client.get("/founder/studio/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Curriculum Studio" in body
    assert "No workspaces yet" in body
    assert "Next step" in body
    assert "founder-breadcrumb" in body


def test_studio_dashboard_lists_workspace(founder_client):
    response = founder_client.get("/founder/studio/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "CS1" in body
    assert "Workspaces" in body


def test_workspace_page_renders_workflow_and_next_step(founder_client):
    response = founder_client.get("/founder/studio/workspaces/ws-cs1")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Next step" in body
    assert "Validate Curriculum" in body or "Advance to Next Stage" in body
    assert "Publish Curriculum" in body
    assert "Version history" in body
    assert "No versions yet" in body


def test_create_subject_flash_message(founder_client):
    response = founder_client.post(
        "/founder/studio/subjects",
        data={"subject_code": "LANGMATH1", "title": "Language Math"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert (
        "created your subject successfully" in body
        or "couldn't create this subject" in body
        or "try again" in body.lower()
    )


def test_validate_flash_message(founder_client):
    response = founder_client.post(
        "/founder/studio/workspaces/ws-cs1/validate",
        data={"workspace_id": "ws-cs1"},
        follow_redirects=True,
    )
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert (
        "We've completed validation successfully." in body
        or "We couldn't complete validation" in body
        or "try again" in body.lower()
    )


def test_intelligence_page_renders(founder_client):
    response = founder_client.get("/founder/intelligence")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Founder Intelligence" in body
    assert "No intelligence signals yet" in body or "Signals" in body
    assert "Evidence Gates" in body


def test_evidence_gates_page_renders(founder_client):
    response = founder_client.get("/founder/evidence-gates")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Evidence Gates" in body
    assert "Gate checklist" in body
    assert "Next step" in body


def test_non_founder_blocked_from_studio(client, ctx, app):
    from app.extensions import db
    from app.models.user import User

    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    student = User(email="student@kwalitec.example", is_active_user=True)
    student.set_password("password123")
    db.session.add(student)
    db.session.commit()
    client.post(
        "/auth/login",
        data={"email": student.email, "password": "password123"},
        follow_redirects=True,
    )
    assert client.get("/founder/studio/").status_code == 403
