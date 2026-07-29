"""FV-001B — Experience Selection and nested curriculum preview certification."""

from __future__ import annotations

from app.domain.curriculum_studio.preview_summary import PreviewNode
from app.founder.dashboard.dto.founder_workspace import PreviewNodeRow
from app.founder.dashboard.services.founder_workspace_service import (
    _preview_nodes_json,
)
from tests.application.curriculum_studio.helpers import make_studio_with_ports


def test_preview_hierarchy_assigns_parent_id_from_structure():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_workspace(
        "ws-nest",
        "NEST1",
        section_ids=("sec-a", "sec-b"),
        topic_ids=("top-1", "top-2"),
    )
    studio.publication.update_facts(
        "ws-nest",
        validation_passed=True,
        blueprint_assigned=True,
    )
    snap = studio.preview.build_for_review("ws-nest")
    by_id = {n.node_id: n for n in snap.hierarchy}
    assert "sec-a" in by_id
    assert by_id["sec-a"].kind == "section"
    assert by_id["sec-a"].parent_id is None
    # Topics nest under first section when section_ref defaults that way.
    topics = [n for n in snap.hierarchy if n.kind == "topic"]
    assert topics
    assert all(t.parent_id in {"sec-a", "sec-b"} or t.parent_id is None for t in topics)
    assert any(t.parent_id == "sec-a" for t in topics)


def test_preview_nodes_json_round_trips_parent_links():
    nodes = (
        PreviewNodeRow("sec-1", "Section 1", kind="section", order_index=0),
        PreviewNodeRow(
            "top-1",
            "Topic 1",
            kind="topic",
            parent_id="sec-1",
            order_index=1,
        ),
    )
    raw = _preview_nodes_json(nodes)
    assert '"parent_id":"sec-1"' in raw
    assert '"kind":"section"' in raw


def test_preview_node_parent_is_optional():
    node = PreviewNode.create("t1", "Topic", kind="topic", parent_id=None)
    assert node.parent_id is None
    nested = PreviewNode.create(
        "t2", "Nested", kind="topic", parent_id="sec-1", order_index=2
    )
    assert nested.parent_id == "sec-1"


def test_workspace_preview_mount_includes_tree_hooks(app, client, ctx):
    """When preview is built, workspace HTML mounts the hierarchical tree."""
    from app.presentation.curriculum_studio.factory import set_studio_service
    from tests.presentation.curriculum_studio.helpers import (
        login_founder,
        wire_studio,
    )

    studio = wire_studio(app, with_workspace=True)
    login_founder(client, app)
    entity = studio.registry.get_workspace("ws-cs1")
    assert entity is not None
    # Seed reviewable hierarchy with parent links.
    from app.domain.curriculum_studio.publication_checklist import (
        WorkspacePublicationFacts,
    )
    from app.domain.curriculum_studio.studio_workflow import StudioWorkflow
    from app.domain.curriculum_studio.workflow_stage import WorkflowStage

    facts = WorkspacePublicationFacts.create(
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
        preview_built=True,
    )
    wf = StudioWorkflow.create(
        "wf-ws-cs1",
        "ws-cs1",
        current_stage=WorkflowStage.PREVIEW,
    )
    studio.registry.put_workspace(
        entity.__class__.create(
            entity.workspace_id,
            entity.subject_code,
            subject_title=entity.subject_title,
            version_label=entity.version_label or "Draft",
            version_id=entity.version_id,
            status=entity.status,
            workflow=wf,
            facts=facts,
            section_ids=("sec-a",),
            topic_ids=("top-a", "top-b"),
        )
    )
    set_studio_service(studio, app=app)
    html = client.get("/console/studio/workspaces/ws-cs1").get_data(as_text=True)
    assert "data-curriculum-preview-tree" in html
    assert "data-preview-expand-all" in html
    assert "data-preview-collapse-all" in html
    assert "curriculum_preview_tree.js" in html
    assert "parent_id" in html or "sec-a" in html
