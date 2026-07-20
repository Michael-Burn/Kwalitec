"""Workflow 1 — Founder Curriculum Studio happy path and messaging."""

from __future__ import annotations

import pytest

from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from app.presentation.curriculum_studio.view_models import (
    FLASH_SUCCESS,
    FLASH_WARNING,
    NEXT_ACTION_BY_STAGE,
    PRIMARY_ACTION_BY_STAGE,
    STAGE_LABELS,
    workspace_page,
)
from tests.presentation.curriculum_studio.helpers import make_workspace
from tests.presentation.workflows.helpers import (
    FOUNDER_WORKFLOW_STAGES,
    login_founder,
    wire_studio,
)


@pytest.fixture
def founder_client(app, client, ctx):
    wire_studio(app, with_workspace=True)
    login_founder(client, app)
    return client


def test_studio_index_reachable(founder_client):
    response = founder_client.get("/founder/studio/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Curriculum Studio" in html
    assert "founder-breadcrumb" in html


def test_workspace_reachable(founder_client):
    response = founder_client.get("/founder/studio/workspaces/ws-cs1")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Next step" in html
    assert "Validate" in html or "validate" in html.lower()


@pytest.mark.parametrize("stage_label", FOUNDER_WORKFLOW_STAGES)
def test_workflow_stage_label_present(stage_label):
    assert stage_label in STAGE_LABELS.values()


@pytest.mark.parametrize(
    ("stage", "primary"),
    (
        ("subject", "advance"),
        ("content_sources", "validate"),
        ("validation", "preview"),
        ("preview", "approve"),
        ("approval", "publish"),
        ("publication", "version"),
    ),
)
def test_primary_cta_matches_stage(stage, primary):
    assert PRIMARY_ACTION_BY_STAGE[stage] == primary
    view = workspace_page(make_workspace(current_stage=stage))
    assert view.primary_action == primary
    assert view.next_action_label


def test_preview_next_action_mentions_version():
    text = NEXT_ACTION_BY_STAGE[WorkflowStage.PREVIEW.value].lower()
    assert "version" in text


def test_approval_next_action_mentions_students():
    text = NEXT_ACTION_BY_STAGE[WorkflowStage.APPROVAL.value].lower()
    assert "student" in text


def test_publish_success_flash_confirms_outcome():
    msg = FLASH_SUCCESS["published"].lower()
    assert "published" in msg
    assert "successfully" in msg


def test_approve_warning_mentions_version():
    assert "version" in FLASH_WARNING["approve"].lower()


def test_publish_warning_mentions_version():
    assert "version" in FLASH_WARNING["publish"].lower()


def test_missing_workspace_redirects_with_guidance(founder_client):
    response = founder_client.get(
        "/founder/studio/workspaces/ws-does-not-exist",
        follow_redirects=False,
    )
    assert response.status_code in {302, 303}
    assert "/founder/studio" in response.headers.get("Location", "")
    followed = founder_client.get(
        "/founder/studio/workspaces/ws-does-not-exist",
        follow_redirects=True,
    )
    html = followed.get_data(as_text=True).lower()
    assert "workspace" in html
    assert "could not be found" in html or "curriculum studio" in html


@pytest.mark.parametrize(
    "action",
    ("validate", "preview", "approve", "publish"),
)
def test_workspace_action_posts_redirect_home_to_workspace(founder_client, action):
    response = founder_client.post(
        f"/founder/studio/workspaces/ws-cs1/{action}",
        data={"workspace_id": "ws-cs1", "submit": "Go"},
        follow_redirects=False,
    )
    # Form may fail validation or service may warn — always return to workspace.
    assert response.status_code in {302, 303}
    assert "ws-cs1" in response.headers.get("Location", "")


def test_create_subject_form_on_dashboard(founder_client):
    html = founder_client.get("/founder/studio/").get_data(as_text=True)
    assert "subject" in html.lower()
    assert "workspace" in html.lower()


def test_workspace_breadcrumb_includes_studio(founder_client):
    html = founder_client.get("/founder/studio/workspaces/ws-cs1").get_data(
        as_text=True
    )
    assert "Curriculum Studio" in html
    assert "Overview" in html


def test_all_stage_labels_unique():
    labels = list(STAGE_LABELS.values())
    assert len(labels) == len(set(labels))


def test_workflow_order_is_linear():
    stages = [stage.value for stage in WorkflowStage]
    assert stages[0] == "subject"
    assert stages[-1] == "publication"
    assert "validation" in stages
    assert stages.index("preview") < stages.index("approval")
    assert stages.index("approval") < stages.index("publication")
