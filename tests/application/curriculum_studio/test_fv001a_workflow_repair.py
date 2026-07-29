"""FV-001A — Curriculum Studio workflow state-machine repairs."""

from __future__ import annotations

import pytest

from app.application.curriculum_studio.exceptions import WorkflowGateBlocked
from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from app.presentation.curriculum_studio.founder_stages import (
    FOUNDER_STAGES,
    founder_stage_label,
)
from app.presentation.curriculum_studio.operator_guidance import format_gate_blocked
from tests.application.curriculum_studio.helpers import make_studio_with_ports


def test_founder_strip_is_upload_preview_approve_publish():
    assert FOUNDER_STAGES == ("Upload", "Preview", "Approve", "Publish")
    assert founder_stage_label(WorkflowStage.VALIDATION) == "Upload"
    assert founder_stage_label(WorkflowStage.PREVIEW) == "Preview"


def test_preview_build_sets_preview_built_not_approved():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_workspace(
        "ws-fv1",
        "FV1",
        section_ids=("sec-a",),
        topic_ids=("top-a",),
    )
    studio.publication.update_facts(
        "ws-fv1",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
    )
    # Move to preview stage
    studio.workflow.advance("ws-fv1")  # content_sources
    studio.workflow.advance("ws-fv1")  # validation
    studio.workflow.advance("ws-fv1")  # preview

    snap = studio.preview.build_for_review("ws-fv1")
    assert snap.node_count >= 1
    ws = studio.registry.get_workspace("ws-fv1")
    assert ws.facts.preview_built is True
    assert ws.facts.preview_approved is False


def test_advance_to_approval_requires_preview_built_not_approved():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_workspace(
        "ws-fv2",
        "FV2",
        section_ids=("sec-a",),
        topic_ids=("top-a",),
    )
    studio.publication.update_facts(
        "ws-fv2",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
    )
    studio.workflow.advance("ws-fv2")
    studio.workflow.advance("ws-fv2")
    studio.workflow.advance("ws-fv2")  # preview

    with pytest.raises(WorkflowGateBlocked) as blocked:
        studio.workflow.advance("ws-fv2")  # approval without preview_built
    assert "preview_built" in blocked.value.missing_codes

    studio.preview.build_for_review("ws-fv2")
    wf = studio.workflow.advance("ws-fv2")  # approval
    assert wf.current_stage == WorkflowStage.APPROVAL.value
    ws = studio.registry.get_workspace("ws-fv2")
    assert ws.facts.preview_approved is False


def test_gate_blocked_message_lists_remaining_tasks():
    exc = WorkflowGateBlocked(
        "Cannot advance to approval; missing: preview_built",
        target_stage="approval",
        missing_codes=("preview_built",),
        satisfied_codes=(),
    )
    message = format_gate_blocked(exc)
    assert "Advancement blocked" in message
    assert "✗ Generate preview" in message
    assert "Go to Preview" in message
    assert "readiness gates are incomplete" not in message.lower()


def test_approve_sets_preview_approved_and_enables_publication_path():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_workspace(
        "ws-fv3",
        "FV3",
        section_ids=("sec-a",),
        topic_ids=("top-a",),
    )
    studio.publication.update_facts(
        "ws-fv3",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
    )
    studio.versions.assign_version("ws-fv3", "2026.1", version_id="ver-fv3")
    studio.workflow.advance("ws-fv3")
    studio.workflow.advance("ws-fv3")
    studio.workflow.advance("ws-fv3")
    studio.preview.build_for_review("ws-fv3")
    studio.workflow.advance("ws-fv3")  # approval

    studio.publication.approve("ws-fv3", actor_id="founder-1")
    ws = studio.registry.get_workspace("ws-fv3")
    assert ws.facts.preview_built is True
    assert ws.facts.preview_approved is True
    # Publication stage gate should now pass once version is assigned.
    wf = studio.workflow.advance("ws-fv3")
    assert wf.current_stage == WorkflowStage.PUBLICATION.value
