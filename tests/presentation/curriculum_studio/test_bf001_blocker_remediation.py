"""BF-001 — Founder validation blocker remediation regression tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.domain.curriculum_studio.curriculum_workspace import (
    CurriculumWorkspace,
    WorkspaceStatus,
)
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.studio_workflow import WorkflowTransitionEvent
from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from app.presentation.curriculum_studio.factory import set_studio_service
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)
from tests.presentation.curriculum_studio.helpers import login_founder, wire_studio

_JUMP = {
    WorkflowStage.SUBJECT: WorkflowTransitionEvent.JUMP_TO_SUBJECT,
    WorkflowStage.CONTENT_SOURCES: WorkflowTransitionEvent.JUMP_TO_CONTENT_SOURCES,
    WorkflowStage.VALIDATION: WorkflowTransitionEvent.JUMP_TO_VALIDATION,
    WorkflowStage.PREVIEW: WorkflowTransitionEvent.JUMP_TO_PREVIEW,
    WorkflowStage.APPROVAL: WorkflowTransitionEvent.JUMP_TO_APPROVAL,
    WorkflowStage.PUBLICATION: WorkflowTransitionEvent.JUMP_TO_PUBLICATION,
}


def _jump_workspace(studio, workspace_id: str, stage: WorkflowStage) -> None:
    ws = studio.registry.get_workspace(workspace_id)
    assert ws is not None and ws.workflow is not None
    jumped = ws.workflow.with_transition(_JUMP[stage], reason="bf001-setup")
    studio.registry.put_workspace(ws.with_workflow(jumped))


def test_preview_tree_js_uses_plain_objects_not_object_constructor():
    """Blocker 1 — buildForest must initialise plain maps."""
    source = Path("app/static/js/curriculum_preview_tree.js").read_text(
        encoding="utf-8"
    )
    assert "var byId = {};" in source
    assert "var children = {};" in source
    assert "var byId = Object" not in source
    assert "var children = Object" not in source
    assert "expandAll" in source
    assert "keydown" in source


def test_catalogue_css_hides_mobile_list_on_desktop():
    """Blocker 6 — .ds-list must not override catalogue list hide."""
    css = Path("app/static/css/design_system.css").read_text(encoding="utf-8")
    assert ".ds-catalogue__list.ds-list" in css
    # First occurrence of the compound selector must hide the list.
    idx = css.index(".ds-catalogue__list.ds-list")
    snippet = css[idx : idx + 80]
    assert "display: none" in snippet


@pytest.mark.parametrize(
    ("stage", "expect_retreat"),
    [
        (WorkflowStage.SUBJECT, False),
        (WorkflowStage.CONTENT_SOURCES, True),
        (WorkflowStage.PREVIEW, True),
        (WorkflowStage.PUBLICATION, True),
    ],
)
def test_workspace_exposes_retreat_and_reset(
    client, ctx, app, stage, expect_retreat
):
    """Blocker 2/4 — Back and Restart controls when lawful."""
    login_founder(client, app)
    studio = wire_studio(app, with_workspace=True)
    _jump_workspace(studio, "ws-cs1", stage)

    resp = client.get("/console/studio/workspaces/ws-cs1")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    if expect_retreat:
        assert "/workspaces/ws-cs1/retreat" in html
        assert "Back" in html
    else:
        assert "/workspaces/ws-cs1/retreat" not in html
    assert "/workspaces/ws-cs1/reset" in html
    assert "Restart workflow" in html


def test_retreat_moves_stage_back_without_duplicate(client, ctx, app):
    """Blocker 2 — retreat preserves workspace identity."""
    login_founder(client, app)
    studio = wire_studio(app, with_workspace=True)
    _jump_workspace(studio, "ws-cs1", WorkflowStage.PREVIEW)

    before_id = studio.get_workspace("ws-cs1").workspace_id
    resp = client.post(
        "/console/studio/workspaces/ws-cs1/retreat",
        data={"workspace_id": "ws-cs1"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    after = studio.get_workspace("ws-cs1")
    assert after.workspace_id == before_id
    assert after.current_stage == "validation"
    assert len(studio.list_workspaces()) == 1


def test_reset_returns_to_upload_subject_stage(client, ctx, app):
    """Blocker 4 — restart restores SUBJECT (Founder Upload)."""
    login_founder(client, app)
    studio = wire_studio(app, with_workspace=True)
    _jump_workspace(studio, "ws-cs1", WorkflowStage.APPROVAL)

    resp = client.post(
        "/console/studio/workspaces/ws-cs1/reset",
        data={"workspace_id": "ws-cs1"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert studio.get_workspace("ws-cs1").current_stage == "subject"
    html = resp.get_data(as_text=True)
    assert "restart" in html.lower() or "Upload" in html


def test_assign_version_rejects_invalid_label_with_clear_flash(client, ctx, app):
    """Blocker 3 — invalid format must not silently fail."""
    login_founder(client, app)
    wire_studio(app, with_workspace=True)
    resp = client.post(
        "/console/studio/workspaces/ws-cs1/version",
        data={"workspace_id": "ws-cs1", "version_label": "1.0.0"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "YYYY.N" in html or "2026.1" in html


def test_assign_version_succeeds_with_year_dot_n(client, ctx, app):
    """Blocker 3 — YYYY.N assignment succeeds after subject restore."""
    login_founder(client, app)
    studio, mgmt, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id="ws-cs1", subject_code="CS1")
    # Simulate process restart: Management loses subject while Studio keeps it.
    mgmt._subjects.clear()
    set_studio_service(studio, app=app)

    resp = client.post(
        "/console/studio/workspaces/ws-cs1/version",
        data={"workspace_id": "ws-cs1", "version_label": "2026.1"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    snap = studio.get_workspace("ws-cs1")
    assert snap.version_label == "2026.1"
    entity = studio.registry.get_workspace("ws-cs1")
    assert entity is not None
    assert entity.facts.version_assigned is True


def test_delete_draft_removes_workspace(client, ctx, app):
    """Blocker 5 — draft delete removes catalogue row."""
    login_founder(client, app)
    studio = wire_studio(app, with_workspace=True)
    assert studio.registry.has_workspace("ws-cs1")
    resp = client.post(
        "/console/studio/workspaces/ws-cs1/delete-draft",
        data={"workspace_id": "ws-cs1"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert not studio.registry.has_workspace("ws-cs1")
    html = resp.get_data(as_text=True)
    assert 'data-subject-id="ws-cs1"' not in html


def test_archive_published_protects_from_delete(client, ctx, app):
    """Blocker 5 — published subjects archive; delete is blocked."""
    login_founder(client, app)
    studio = wire_studio(app, with_workspace=True)
    ws = studio.registry.get_workspace("ws-cs1")
    assert ws is not None
    facts = WorkspacePublicationFacts.create(
        version_assigned=True,
        preview_approved=True,
        preview_built=True,
        validation_passed=True,
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
    )
    published = CurriculumWorkspace.create(
        ws.workspace_id,
        ws.subject_code,
        subject_title=ws.subject_title,
        version_label="2026.1",
        version_id="ver-cs1",
        status=WorkspaceStatus.PUBLISHED,
        workflow=ws.workflow,
        facts=facts,
    )
    studio.registry.put_workspace(published)

    blocked = client.post(
        "/console/studio/workspaces/ws-cs1/delete-draft",
        data={"workspace_id": "ws-cs1"},
        follow_redirects=True,
    )
    assert studio.registry.has_workspace("ws-cs1")
    body = blocked.get_data(as_text=True).lower()
    assert "cannot be deleted" in body or "archive" in body

    ok = client.post(
        "/console/studio/workspaces/ws-cs1/archive",
        data={"workspace_id": "ws-cs1"},
        follow_redirects=True,
    )
    assert ok.status_code == 200
    assert studio.get_workspace("ws-cs1").status == "archived"


def test_subjects_catalogue_renders_one_logical_row_per_subject(client, ctx, app):
    """Blocker 6 — each subject appears once in table and once in mobile list."""
    login_founder(client, app)
    studio = wire_studio(app, with_workspace=True)
    seed_workspace(studio, workspace_id="ws-cs2", subject_code="CS2")
    resp = client.get("/console/studio/subjects")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert html.count('data-subject-id="ws-cs1"') == 2  # table + mobile list
    assert html.count('data-subject-id="ws-cs2"') == 2
    assert "ds-catalogue__table" in html
    assert "ds-catalogue__list" in html
