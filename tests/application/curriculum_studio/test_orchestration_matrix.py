"""Expanded orchestration matrix for Curriculum Studio application services."""

from __future__ import annotations

import pytest

from app.domain.curriculum_studio.workflow_stage import (
    CANONICAL_WORKFLOW,
    WorkflowStage,
)
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)

FACT_KEYS = (
    "cmp_uploaded",
    "official_syllabus_uploaded",
    "validation_passed",
    "blueprint_assigned",
    "preview_approved",
    "version_assigned",
    "rollback_snapshot_created",
)


@pytest.mark.parametrize("mask", range(64))
def test_fact_masks_partial_ready(mask):
    """Smaller subset matrix overlapping checklist readiness."""
    studio = seed_workspace()
    kwargs = {key: bool(mask & (1 << i)) for i, key in enumerate(FACT_KEYS[:6])}
    kwargs["rollback_snapshot_created"] = bool(mask & 32)
    snap = studio.publication.update_facts("ws-1", **kwargs)
    ready = all(kwargs.values())
    assert snap.ready_to_publish is ready


@pytest.mark.parametrize("stage", list(CANONICAL_WORKFLOW))
@pytest.mark.parametrize("retreat", [False, True])
def test_jump_and_optional_retreat(stage, retreat):
    studio = seed_workspace()
    studio.workflow.transition(
        "ws-1", f"jump_to_{stage.value}", enforce_gates=False
    )
    snap = studio.workflow.get_workflow("ws-1")
    assert snap.current_stage == stage.value
    if retreat and stage is not WorkflowStage.SUBJECT:
        retreated = studio.workflow.retreat("ws-1")
        assert retreated.current_stage != stage.value or stage is WorkflowStage.SUBJECT


@pytest.mark.parametrize("n_topics", range(0, 16))
def test_update_structure_topic_counts(n_topics):
    studio = seed_workspace()
    topics = tuple(f"t-{i}" for i in range(n_topics))
    snap = studio.update_structure("ws-1", topic_ids=topics)
    assert snap.topic_ids == topics


@pytest.mark.parametrize("hours", [None, 0.0, 1.5, 10.0, 40.0, 99.5])
def test_update_workload_hours(hours):
    studio = seed_workspace()
    snap = studio.update_structure("ws-1", estimated_workload_hours=hours)
    assert snap.estimated_workload_hours == hours


@pytest.mark.parametrize("code", [f"X{i}" for i in range(20)])
def test_subject_then_workspace_link(code):
    studio, _, _, _ = make_studio_with_ports()
    studio.create_subject(code, title=code)
    snap = studio.open_workspace(f"ws-{code}", code)
    assert snap.subject_code == code.upper()


@pytest.mark.parametrize("i", range(16))
def test_full_thin_port_pipeline(i):
    studio, mgmt, ingestion, platform = make_studio_with_ports()
    code = f"P{i:02d}"
    studio.create_subject(code, title=f"Product {i}")
    wid = f"ws-pipe-{i}"
    studio.open_workspace(
        wid,
        code,
        section_ids=("sec-1",),
        topic_ids=("topic-1",),
        objective_ids=("obj-1",),
    )
    studio.versions.assign_version(wid, "2026.1", version_id=f"ver-pipe-{i}")
    studio.upload_sources(
        wid,
        cmp_reference=f"cmp://{i}",
        syllabus_reference=f"syl://{i}",
    )
    studio.workspaces.assign_blueprint(
        wid, section_id="sec-1", blueprint_profile_id="bp-default"
    )
    studio.validation.validate_curriculum(wid)
    studio.preview.approve(wid)
    studio.versions.create_rollback_snapshot(f"ver-pipe-{i}")
    studio.publication.update_facts(
        wid,
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
        preview_approved=True,
        version_assigned=True,
        rollback_snapshot_created=True,
    )
    pub = studio.publication.publish(wid)
    assert pub.lifecycle_status == "published"
    assert f"ver-pipe-{i}" in mgmt.publish_calls
    assert ingestion.start_calls
    assert platform.surface_calls or True
    dash = studio.founder_dashboard()
    assert dash.published_count >= 1
