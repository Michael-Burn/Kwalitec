"""FV-001B-R1 workflow completion tests."""

from __future__ import annotations

import pytest

from app.application.curriculum_studio.exceptions import PreviewError, ValidationError
from app.application.curriculum_studio.preview_service import _nodes_from_payload
from app.application.curriculum_studio.structure_preparation_service import (
    StructurePreparationService,
)
from app.domain.curriculum_studio.preview_summary import PreviewNode
from app.presentation.curriculum_studio.view_models import friendly_preview_summary
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_publishable,
)


def test_nodes_from_payload_maps_section_refs():
    nodes = _nodes_from_payload(
        {
            "section_refs": ("A1", "A2"),
            "assignment_sections": ("A1", "B1"),
        }
    )
    assert [n.node_id for n in nodes] == ["A1", "A2", "B1"]
    assert all(isinstance(n, PreviewNode) for n in nodes)


def test_friendly_preview_rejects_contradictory_ready_zero():
    summary = friendly_preview_summary(readiness="not_ready", node_count=0)
    assert "Preview ready" not in summary
    assert "not ready" in summary.lower()


def test_structure_prepare_uses_workspace_fallback():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_workspace(
        "ws-struct",
        "CS9",
        section_ids=("s1",),
        topic_ids=("t1",),
    )
    prepared = StructurePreparationService(studio.registry).prepare_for_validation(
        "ws-struct"
    )
    assert prepared.section_ids == ("s1",)
    assert prepared.topic_ids == ("t1",)
    assert prepared.source == "workspace"


def test_structure_prepare_blocks_empty_workspace():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_workspace("ws-empty", "CS0")
    with pytest.raises(ValidationError, match="No extracted curriculum"):
        StructurePreparationService(studio.registry).prepare_for_validation("ws-empty")


def test_preview_build_for_review_requires_nodes():
    studio, _, _, _ = make_studio_with_ports()
    studio.create_workspace("ws-prev", "CS8")
    with pytest.raises(PreviewError, match="no curriculum topics"):
        studio.preview.build_for_review("ws-prev")


def test_validate_then_preview_publishable_path():
    """Seeded structure can validate → preview → approve → publish."""
    studio = seed_publishable()
    # seed_publishable already sets facts; ensure preview has nodes
    snap = studio.preview.build_for_review("ws-1")
    assert snap.node_count >= 1
    checklist = studio.publication.checklist("ws-1")
    assert checklist.ready_to_publish is True
    pub = studio.publication.publish("ws-1")
    assert pub.lifecycle_status == "published"


def test_end_to_end_validate_assigns_blueprint_fact():
    studio, mgmt, _, _ = make_studio_with_ports()
    studio.create_workspace(
        "ws-val",
        "CS7",
        section_ids=("sec-a",),
        topic_ids=("top-a",),
    )
    studio.publication.update_facts(
        "ws-val",
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
    )
    studio.versions.assign_version("ws-val", "2026.1", version_id="ver-val")
    studio.workspaces.upload_sources(
        "ws-val",
        cmp_reference="ref://cmp/cs7",
        syllabus_reference="ref://syl/cs7",
        start_ingestion=False,
    )
    snap = studio.validation.validate_curriculum("ws-val")
    assert snap.passed is True
    ws = studio.registry.get_workspace("ws-val")
    assert ws.facts.validation_passed is True
    assert ws.facts.blueprint_assigned is True
    assert "ver-val" in mgmt.validate_calls
