"""View-model tests for Curriculum Studio Founder UX."""

from __future__ import annotations

import pytest

from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from app.presentation.curriculum_studio.view_models import (
    EMPTY_ACTIVITY_GUIDANCE,
    EMPTY_VERSION_HISTORY_GUIDANCE,
    EMPTY_WORKSPACES_GUIDANCE,
    FLASH_SUCCESS,
    FLASH_WARNING,
    NEXT_ACTION_BY_STAGE,
    PRIMARY_ACTION_BY_STAGE,
    STAGE_LABELS,
    dashboard_view,
    friendly_checklist_summary,
    friendly_preview_summary,
    friendly_validation_summary,
    workspace_page,
)
from tests.presentation.curriculum_studio.helpers import (
    make_empty_dashboard,
    make_populated_dashboard,
    make_workspace,
)


def test_empty_dashboard_flags_and_guidance():
    view = dashboard_view(make_empty_dashboard())
    assert view.has_workspaces is False
    assert view.has_activity is False
    assert view.empty_workspaces_message == EMPTY_WORKSPACES_GUIDANCE
    assert view.empty_activity_message == EMPTY_ACTIVITY_GUIDANCE
    assert "workspace" in view.next_step_hint.lower()
    assert len(view.breadcrumbs) == 2
    assert view.breadcrumbs[-1].endpoint is None


def test_populated_dashboard_lists_workspaces_and_activity():
    view = dashboard_view(make_populated_dashboard())
    assert view.has_workspaces is True
    assert view.has_activity is True
    assert view.draft_count == 1
    assert view.workspaces[0].subject_code == "CS1"
    assert "Open a workspace" in view.next_step_hint


@pytest.mark.parametrize("stage", list(WorkflowStage))
def test_workspace_page_next_action_and_primary(stage: WorkflowStage):
    ws = make_workspace(current_stage=stage.value)
    view = workspace_page(ws)
    assert view.stage_label == STAGE_LABELS[stage.value]
    assert view.next_action_label == NEXT_ACTION_BY_STAGE[stage.value]
    assert view.primary_action == PRIMARY_ACTION_BY_STAGE[stage.value]
    assert view.has_version_history is False
    assert view.empty_version_message == EMPTY_VERSION_HISTORY_GUIDANCE
    assert any(active for _, _, active in view.workflow_stages)


def test_workspace_page_version_history_present():
    view = workspace_page(
        make_workspace(current_stage="publication"),
        version_history=("1.0.0 (published)",),
    )
    assert view.has_version_history is True
    assert view.version_history[0].startswith("1.0.0")


def test_workspace_breadcrumbs_include_studio():
    view = workspace_page(make_workspace())
    labels = [c.label for c in view.breadcrumbs]
    assert labels[0] == "Overview"
    assert labels[1] == "Curriculum Studio"
    assert labels[2] == "CS1"
    assert view.breadcrumbs[0].endpoint == "founder_dashboard.index"
    assert view.breadcrumbs[1].endpoint == "curriculum_studio.index"


def test_friendly_validation_summaries():
    ok = friendly_validation_summary(readiness="ready", passed=True)
    blocked = friendly_validation_summary(readiness="blocked", passed=False)
    assert "Validation completed successfully" in ok
    assert "needs attention" in blocked


def test_friendly_preview_and_checklist():
    preview = friendly_preview_summary(readiness="ready", node_count=1)
    assert "1 node" in preview
    multi = friendly_preview_summary(readiness="ready", node_count=4)
    assert "4 nodes" in multi
    assert "All 3 checklist items are ready." in friendly_checklist_summary(
        ready=3, total=3
    )
    assert "2 of 5" in friendly_checklist_summary(ready=2, total=5)


def test_flash_success_copy_is_professional():
    for message in FLASH_SUCCESS.values():
        assert message.endswith(".")
        assert "execute" not in message.lower()
        assert message[0].isupper()


def test_flash_warning_copy_guides_recovery():
    for message in FLASH_WARNING.values():
        lowered = message.lower()
        assert "try again" in lowered or "check" in lowered


def test_stage_labels_avoid_jargon():
    assert STAGE_LABELS[WorkflowStage.CONTENT_SOURCES.value] == "Content Sources"
    assert STAGE_LABELS[WorkflowStage.PUBLICATION.value] == "Publish"


def test_workflow_stages_mark_exactly_one_active():
    view = workspace_page(make_workspace(current_stage="preview"))
    active = [label for _, label, on in view.workflow_stages if on]
    assert active == ["Preview"]
    assert len(view.workflow_stages) == len(WorkflowStage)
