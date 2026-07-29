"""DX-006B Phase 3 — Founder Publication Workspace tests."""

from __future__ import annotations

import pytest

from app.founder.dashboard.services.founder_workspace_service import (
    PRIMARY_ADVANCE,
    PRIMARY_APPROVE,
    PRIMARY_PUBLISH,
    PRIMARY_RESOLVE,
    PRIMARY_REVIEW,
    PRIMARY_UPLOAD,
    PRIMARY_VALIDATE,
    FounderWorkspaceService,
)
from app.presentation.curriculum_studio.founder_stages import (
    FOUNDER_STAGES,
    founder_stage_label,
)
from app.presentation.curriculum_studio.view_models import (
    PRIMARY_ACTION_BY_STAGE,
    ValidationFindingView,
    workspace_page,
)
from tests.presentation.curriculum_studio.helpers import make_workspace
from tests.presentation.workflows.helpers import login_founder, wire_studio


@pytest.fixture
def founder_client(app, client, ctx):
    wire_studio(app, with_workspace=True)
    login_founder(client, app)
    return client


def test_founder_stages_are_five():
    assert FOUNDER_STAGES == (
        "Upload",
        "Validate",
        "Review",
        "Approve",
        "Publish",
    )


@pytest.mark.parametrize(
    ("domain", "founder"),
    (
        ("subject", "Upload"),
        ("content_sources", "Upload"),
        ("validation", "Validate"),
        ("preview", "Review"),
        ("approval", "Approve"),
        ("publication", "Publish"),
    ),
)
def test_domain_to_founder_stage(domain, founder):
    assert founder_stage_label(domain) == founder


@pytest.mark.parametrize(
    ("stage", "primary"),
    (
        ("subject", PRIMARY_ADVANCE),
        ("content_sources", PRIMARY_UPLOAD),
        ("validation", PRIMARY_VALIDATE),
        ("preview", PRIMARY_REVIEW),
        ("approval", PRIMARY_APPROVE),
        ("publication", PRIMARY_PUBLISH),
    ),
)
def test_primary_action_by_stage(stage, primary):
    assert PRIMARY_ACTION_BY_STAGE[stage] == primary
    version = "2026.1" if stage == "publication" else ""
    view = workspace_page(
        make_workspace(current_stage=stage, version_label=version)
    )
    assert view.primary_action == primary
    assert view.stage_label == founder_stage_label(stage)


def test_blocking_findings_override_primary():
    finding = ValidationFindingView(
        code="E1",
        message="Missing mapping",
        severity="error",
        is_blocking=True,
        why_it_matters="Cannot pass readiness",
        recovery_action="Re-process sources",
    )
    view = workspace_page(
        make_workspace(current_stage="validation"),
        validation_findings=(finding,),
    )
    assert view.primary_action == PRIMARY_RESOLVE


def test_workspace_strip_has_five_founder_stages():
    view = workspace_page(make_workspace(current_stage="approval"))
    labels = [label for _, label, _ in view.workflow_stages]
    assert labels == list(FOUNDER_STAGES)
    assert sum(1 for _, _, active in view.workflow_stages if active) == 1


def test_workspace_page_renders_dx004c_structure(founder_client):
    response = founder_client.get("/console/studio/workspaces/ws-cs1")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert 'id="workspace-subject-title"' in body
    assert "ds-persistent-context" in body
    assert "ds-stage-indicator" in body
    assert "Upload" in body
    assert "Validate" in body
    assert "Review" in body
    assert "Approve" in body
    assert "Publish" in body
    assert "ds-btn--primary" in body
    assert "command-metric" not in body
    assert "Validation findings" not in body or "Blocking findings" in body
    assert "cip-intel" not in body
    assert "Curriculum review" not in body
    assert "founder-action-grid" not in body
    assert "founder-breadcrumb" not in body
    assert body.count("<h1") == 1
    assert "Back to Subjects" in body
    assert "Technical details" in body


def test_workspace_upload_stage_shows_sources(founder_client):
    body = founder_client.get("/console/studio/workspaces/ws-cs1").get_data(
        as_text=True
    )
    assert "Official CMP" in body
    assert "Official Syllabus" in body
    assert "Upload documents" in body
    assert "data-document-upload" in body
    assert "document_upload.js" in body
    assert "curriculum_intelligence.js" not in body


def test_workspace_one_primary_class(founder_client):
    body = founder_client.get("/console/studio/workspaces/ws-cs1").get_data(
        as_text=True
    )
    # Exactly one primary button in the primary strip (Continue on subject stage).
    assert body.count("ds-btn--primary") == 1


def test_validate_stays_on_workspace(founder_client):
    response = founder_client.post(
        "/console/studio/workspaces/ws-cs1/validate",
        data={"workspace_id": "ws-cs1"},
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "/console/studio/workspaces/ws-cs1" in response.headers.get(
        "Location", ""
    )


def test_service_builds_page(app):
    from tests.application.curriculum_studio.helpers import (
        make_studio_with_ports,
        seed_workspace,
    )

    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-svc", subject_code="CS1")
    with app.test_request_context("/console/studio/workspaces/ws-svc"):
        page = FounderWorkspaceService(studio=studio).build_page("ws-svc")
    assert page.stage_label == "Upload"
    assert page.primary_key == PRIMARY_ADVANCE
    assert page.show_upload is True
    assert page.founder_stages == FOUNDER_STAGES
