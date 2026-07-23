"""Snapshot tests for Adaptive Study Workspace (XP-004)."""

from __future__ import annotations

from application.student_experience.workspace import (
    StudyWorkspaceService,
    WorkspaceSnapshotId,
)
from tests.application.student_experience.workspace.conftest import (
    STUDENT_ID,
    make_full_inputs,
)


def test_build_snapshot_projects_compact_fields(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(make_full_inputs(), workspace_id="workspace-snap")
    snapshot = service.build_snapshot(
        view, snapshot_id=WorkspaceSnapshotId("wsnap-001")
    )
    assert snapshot.snapshot_id.value == "wsnap-001"
    assert snapshot.student_id == STUDENT_ID
    assert snapshot.session_available is True
    assert snapshot.mission_title == view.current_session.mission_title
    assert snapshot.completion_percent == view.progress.completion_percent
    assert snapshot.objective_count == len(view.objectives.items)
    assert snapshot.completed_objective_count == len(view.objectives.completed)
    assert snapshot.remaining_objective_count == len(view.objectives.remaining)
    assert snapshot.next_session_preview == view.completion.next_session_preview
    assert (
        snapshot.readiness_impact_summary == view.completion.readiness_impact_summary
    )


def test_deterministic_snapshot_id(service: StudyWorkspaceService) -> None:
    view = service.build_workspace(make_full_inputs(), workspace_id="workspace-det")
    snapshot = service.build_snapshot(view)
    assert snapshot.snapshot_id.value.startswith("wsnap:workspace-det:")
