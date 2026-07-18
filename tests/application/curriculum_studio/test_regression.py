"""Regression and mapping tests for Curriculum Studio."""

from __future__ import annotations

import pytest

from app.application.curriculum_studio._snapshots import (
    preview_snapshot,
    publication_snapshot,
    validation_snapshot,
    version_snapshot,
    workflow_snapshot,
    workspace_snapshot,
)
from app.domain.curriculum_studio.preview_summary import (
    PreviewNode,
    PreviewSummary,
)
from app.domain.curriculum_studio.publication_checklist import PublicationChecklist
from app.domain.curriculum_studio.publication_summary import PublicationSummary
from app.domain.curriculum_studio.validation_summary import (
    ValidationFinding,
    ValidationSummary,
)
from app.domain.curriculum_studio.version_history import VersionHistory
from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_publishable,
)
from tests.domain.curriculum_studio.helpers import (
    make_ready_facts,
    make_version_record,
    make_workflow,
    make_workspace,
)


def test_workspace_snapshot_mapping():
    ws = make_workspace(facts=make_ready_facts())
    snap = workspace_snapshot(ws)
    assert snap.ready_to_publish is True
    assert snap.checklist_satisfied_count == 8


def test_workflow_snapshot_mapping():
    wf = make_workflow(stage=WorkflowStage.PREVIEW)
    snap = workflow_snapshot(wf)
    assert snap.current_stage == "preview"
    assert snap.stage_label == "Preview"
    assert snap.can_advance is True
    assert snap.can_retreat is True


def test_validation_snapshot_mapping():
    summary = ValidationSummary.create(
        "s1",
        "ws-1",
        detected_sections=("a",),
        warnings=[ValidationFinding.create("w", "warn")],
    )
    snap = validation_snapshot(summary)
    assert snap.section_count == 1
    assert snap.warning_count == 1


def test_preview_snapshot_mapping():
    summary = PreviewSummary.create(
        "p1",
        "ws-1",
        hierarchy=[PreviewNode.create("n1", "T")],
        objectives=("o1",),
        validation_passed=True,
    )
    snap = preview_snapshot(summary)
    assert snap.node_count == 1
    assert snap.objective_count == 1


def test_publication_snapshot_mapping():
    checklist = PublicationChecklist.compute(make_ready_facts())
    summary = PublicationSummary.create(
        "ps", "ws-1", "CS1", checklist=checklist
    )
    snap = publication_snapshot(summary)
    assert snap.ready_to_publish is True
    assert snap.checklist_item_count == 8


def test_version_snapshot_mapping():
    hist = VersionHistory.create(
        "CS1",
        [
            make_version_record("v1"),
            make_version_record("v2", version_label="2026.2"),
        ],
    )
    snap = version_snapshot(hist)
    assert snap.version_count == 2
    assert snap.draft_count == 2


def test_end_to_end_founder_path():
    """Subject → sources → validate → preview → version → publish."""
    studio, mgmt, _, _ = make_studio_with_ports()
    studio.create_workspace(
        "ws-e2e",
        "CS1",
        section_ids=("s1",),
        topic_ids=("t1",),
        objective_ids=("o1",),
    )
    studio.publication.update_facts(
        "ws-e2e",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        blueprint_assigned=True,
    )
    studio.workflow.advance("ws-e2e")  # → content_sources
    studio.workflow.advance("ws-e2e")  # → validation
    studio.validation.mark_passed("ws-e2e")
    studio.workflow.advance("ws-e2e")  # → preview
    studio.preview.approve("ws-e2e")
    studio.workflow.advance("ws-e2e")  # → approval
    studio.versions.assign_version("ws-e2e", "2026.1", version_id="ver-e2e")
    studio.versions.create_rollback_snapshot("ver-e2e")
    studio.publication.update_facts(
        "ws-e2e",
        version_assigned=True,
        rollback_snapshot_created=True,
        preview_approved=True,
        validation_passed=True,
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        blueprint_assigned=True,
    )
    studio.workflow.advance("ws-e2e")  # → publication
    pub = studio.publication.publish("ws-e2e")
    assert pub.ready_to_publish is True
    assert pub.lifecycle_status == "published"
    assert "ver-e2e" in mgmt.publish_calls


def test_publishable_helper_regression():
    studio = seed_publishable()
    assert studio.publication.checklist("ws-1").ready_to_publish is True


@pytest.mark.parametrize(
    "method",
    [
        "get_workspace",
        "list_workspaces",
        "health",
        "diagnostic_report",
        "founder_dashboard",
        "create_subject",
        "open_workspace",
        "upload_sources",
    ],
)
def test_facade_methods_exist(method):
    studio, _, _, _ = make_studio_with_ports()
    assert callable(getattr(studio, method))


def test_docs_exist():
    from pathlib import Path

    doc = (
        Path(__file__).resolve().parents[3]
        / "knowledge"
        / "version2"
        / "CURRICULUM_STUDIO.md"
    )
    assert doc.is_file()
    text = doc.read_text(encoding="utf-8")
    assert "Is this curriculum ready to publish?" in text
    assert "Curriculum Studio" in text
