"""Empty-state behaviour for Founder Studio view models and templates."""

from __future__ import annotations

import pytest

from app.presentation.curriculum_studio.view_models import (
    EMPTY_ACTIVITY_GUIDANCE,
    EMPTY_CHECKLIST_SUMMARY,
    EMPTY_PREVIEW_SUMMARY,
    EMPTY_VALIDATION_SUMMARY,
    EMPTY_VERSION_HISTORY_GUIDANCE,
    EMPTY_WORKSPACES_GUIDANCE,
    dashboard_view,
    friendly_checklist_summary,
    workspace_page,
)
from tests.presentation.curriculum_studio.helpers import (
    make_empty_dashboard,
    make_workspace,
)


def test_empty_dashboard_never_implies_blank_lists():
    view = dashboard_view(make_empty_dashboard())
    assert view.workspaces == ()
    assert view.recent_activity == ()
    assert view.empty_workspaces_message
    assert view.empty_activity_message


def test_empty_workspace_summaries_are_guiding():
    view = workspace_page(make_workspace())
    assert view.validation_summary == EMPTY_VALIDATION_SUMMARY
    assert view.preview_summary == EMPTY_PREVIEW_SUMMARY
    assert view.checklist_summary == EMPTY_CHECKLIST_SUMMARY
    assert view.empty_version_message == EMPTY_VERSION_HISTORY_GUIDANCE


def test_zero_checklist_uses_empty_guidance():
    assert friendly_checklist_summary(ready=0, total=0) == EMPTY_CHECKLIST_SUMMARY


@pytest.mark.parametrize(
    "message",
    (
        EMPTY_WORKSPACES_GUIDANCE,
        EMPTY_ACTIVITY_GUIDANCE,
        EMPTY_VERSION_HISTORY_GUIDANCE,
        EMPTY_VALIDATION_SUMMARY,
    ),
)
def test_empty_guidance_is_actionable(message):
    lowered = message.lower()
    assert any(
        token in lowered
        for token in ("create", "open", "assign", "run", "build", "until", "validate")
    )
