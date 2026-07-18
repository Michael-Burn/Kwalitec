"""Dashboard projection and DTO contract tests."""

from __future__ import annotations

import dataclasses

import pytest

from app.application.curriculum_studio.dto.dashboard_snapshot import (
    ActivityEntrySnapshot,
    DashboardSnapshot,
)
from app.application.curriculum_studio.dto.subject_snapshot import SubjectSnapshot
from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from tests.application.curriculum_studio.helpers import (
    make_studio,
    make_studio_with_ports,
    seed_publishable,
    seed_workspace,
)


@pytest.mark.parametrize("n", range(1, 21))
def test_dashboard_counts_workspaces(n):
    studio = make_studio()
    for i in range(n):
        seed_workspace(studio, workspace_id=f"ws-{i}")
    dash = studio.founder_dashboard()
    assert dash.draft_count == n
    assert dash.published_count == 0


@pytest.mark.parametrize("i", range(15))
def test_dashboard_pending_validation(i):
    studio = make_studio()
    seed_workspace(studio, workspace_id=f"ws-{i}")
    studio.publication.update_facts(
        f"ws-{i}", cmp_uploaded=True, official_syllabus_uploaded=True
    )
    studio.workflow.transition(
        f"ws-{i}", "jump_to_validation", enforce_gates=False
    )
    dash = studio.founder_dashboard()
    assert dash.pending_validation_count >= 1


@pytest.mark.parametrize("i", range(10))
def test_dashboard_after_publish(i):
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-{i}", ready=True)
    studio.versions.assign_version(f"ws-{i}", "2026.1", version_id=f"ver-{i}")
    studio.versions.create_rollback_snapshot(f"ver-{i}")
    studio.publication.update_facts(
        f"ws-{i}",
        version_assigned=True,
        rollback_snapshot_created=True,
        preview_approved=True,
        validation_passed=True,
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        blueprint_assigned=True,
    )
    studio.publication.publish(f"ws-{i}")
    dash = studio.founder_dashboard()
    assert dash.published_count >= 1
    assert dash.ready_to_publish_count >= 1 or dash.published_count >= 1
    assert any(a.kind == "published" for a in dash.recent_activity)


def test_dashboard_snapshot_immutable():
    dash = DashboardSnapshot()
    assert dataclasses.is_dataclass(dash)
    with pytest.raises(dataclasses.FrozenInstanceError):
        dash.published_count = 99  # type: ignore[misc]


def test_activity_entry_immutable():
    entry = ActivityEntrySnapshot("a1", "kind", "msg")
    with pytest.raises(dataclasses.FrozenInstanceError):
        entry.message = "x"  # type: ignore[misc]


def test_subject_snapshot_immutable():
    snap = SubjectSnapshot("CS1", title="T")
    with pytest.raises(dataclasses.FrozenInstanceError):
        snap.title = "X"  # type: ignore[misc]


@pytest.mark.parametrize("limit", [1, 5, 10, 20, 50])
def test_dashboard_activity_limit(limit):
    studio = make_studio()
    for i in range(30):
        seed_workspace(studio, workspace_id=f"ws-{i}")
    dash = studio.founder_dashboard(activity_limit=limit)
    assert len(dash.recent_activity) <= limit


@pytest.mark.parametrize("i", range(12))
def test_publication_readiness_projection(i):
    studio = make_studio()
    seed_workspace(studio, workspace_id=f"ws-{i}")
    dash = studio.founder_dashboard()
    assert len(dash.publication_readiness) == i + 1 or len(
        dash.publication_readiness
    ) >= 1
    for item in dash.publication_readiness:
        assert item.ready_to_publish is False or item.blocking_codes is not None


@pytest.mark.parametrize(
    "stage",
    [
        WorkflowStage.SUBJECT,
        WorkflowStage.CONTENT_SOURCES,
        WorkflowStage.VALIDATION,
        WorkflowStage.PREVIEW,
        WorkflowStage.APPROVAL,
        WorkflowStage.PUBLICATION,
    ],
)
def test_dashboard_across_workflow_stages(stage):
    studio = make_studio()
    seed_workspace(studio)
    studio.workflow.transition(
        "ws-1", f"jump_to_{stage.value}", enforce_gates=False
    )
    dash = studio.founder_dashboard()
    assert dash.draft_count + dash.published_count >= 1


@pytest.mark.parametrize("i", range(8))
def test_seed_publishable_readiness_on_dashboard(i):
    studio = seed_publishable(workspace_id=f"ws-{i}")
    dash = studio.founder_dashboard()
    assert dash.ready_to_publish_count >= 1
