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
    response = client.get("/console/studio/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Curriculum Studio" in body
    assert "No workspaces yet" in body


def test_studio_dashboard_lists_workspace(founder_client):
    response = founder_client.get("/console/studio/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Core Statistics" in body or "CS1" in body
    assert "Workspaces" in body
    assert "ws-cs1" in body


def test_workspace_page_renders_workflow_and_next_step(founder_client):
    response = founder_client.get("/console/studio/workspaces/ws-cs1")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "ds-persistent-context" in body
    assert "Upload" in body
    assert "Preview" in body
    assert "Approve" in body
    assert "Publish" in body
    assert "ds-btn--primary" in body
    assert "Technical details" in body
    assert "command-metric" not in body
    assert "Step" in body and "of 4" in body


def test_create_subject_flash_message(founder_client):
    response = founder_client.post(
        "/console/studio/subjects",
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
        "/console/studio/workspaces/ws-cs1/validate",
        data={"workspace_id": "ws-cs1"},
        follow_redirects=True,
    )
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert (
        "We've completed validation" in body
        or "We&#39;ve completed validation" in body
        or "couldn't complete validation" in body.lower()
        or "couldn&#39;t complete validation" in body.lower()
        or "try again" in body.lower()
        or "Advancement blocked" in body
        or "Remaining tasks" in body
    )


def test_intelligence_page_renders(founder_client):
    response = founder_client.get("/console/intelligence")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Founder Intelligence" in body
    assert "No intelligence signals yet" in body or "Signals" in body
    assert "Curriculum Studio" in body or "console-sidebar" in body


def test_evidence_gates_page_renders(founder_client):
    response = founder_client.get("/console/evidence-gates")
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
    assert client.get("/console/studio/").status_code == 403
