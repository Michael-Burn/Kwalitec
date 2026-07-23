"""Determinism tests for Adaptive Study Workspace (XP-004)."""

from __future__ import annotations

from application.student_experience.workspace import StudyWorkspaceService
from tests.application.student_experience.workspace.conftest import make_full_inputs


def test_identical_inputs_produce_identical_workspace(
    service: StudyWorkspaceService,
) -> None:
    inputs = make_full_inputs()
    first = service.build_workspace(inputs, workspace_id="workspace-det")
    second = service.build_workspace(inputs, workspace_id="workspace-det")
    assert first == second
    snap_a = service.build_snapshot(first, snapshot_id="wsnap-det")
    snap_b = service.build_snapshot(second, snapshot_id="wsnap-det")
    assert snap_a == snap_b


def test_focus_and_objectives_are_deterministic(
    service: StudyWorkspaceService,
) -> None:
    inputs = make_full_inputs()
    first = service.build_workspace(inputs)
    second = service.build_workspace(inputs)
    assert first.focus == second.focus
    assert first.objectives == second.objectives
    assert first.progress == second.progress
