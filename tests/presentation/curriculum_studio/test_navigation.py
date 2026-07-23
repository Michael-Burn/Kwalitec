"""Navigation and workflow consistency for Console Content / Studio UX."""

from __future__ import annotations

import pytest

from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from app.founder.dashboard.nav import (
    COMMAND_CENTRE_NAV,
    COMMAND_CENTRE_SECONDARY_NAV,
    active_section_id,
)
from app.presentation.curriculum_studio.view_models import (
    PRIMARY_ACTION_BY_STAGE,
    STAGE_LABELS,
    workspace_page,
)
from tests.presentation.curriculum_studio.helpers import make_workspace


def test_content_is_primary_nav_item():
    labels = [item.label for item in COMMAND_CENTRE_NAV]
    assert "Content" in labels
    content = next(i for i in COMMAND_CENTRE_NAV if i.section_id == "content")
    assert content.endpoint == "curriculum_studio.index"


def test_assessments_primary_nav():
    labels = [item.label for item in COMMAND_CENTRE_NAV]
    assert "Assessments" in labels
    gates = next(i for i in COMMAND_CENTRE_NAV if i.section_id == "assessments")
    assert gates.endpoint == "founder_dashboard.evidence_gates"
    # Keep secondary list free of the alpha primary destinations.
    secondary_ids = [item.section_id for item in COMMAND_CENTRE_SECONDARY_NAV]
    assert "assessments" not in secondary_ids


@pytest.mark.parametrize(
    ("endpoint", "expected"),
    (
        ("curriculum_studio.index", "content"),
        ("curriculum_studio.workspace", "content"),
        ("founder_dashboard.founder_intelligence", "learning"),
        ("founder_dashboard.evidence_gates", "assessments"),
        ("founder_dashboard.index", "overview"),
    ),
)
def test_active_section_mapping(endpoint, expected):
    assert active_section_id(endpoint) == expected


def test_workflow_order_matches_founder_journey():
    expected = (
        "Subject",
        "Content Sources",
        "Validation",
        "Preview",
        "Approval",
        "Publish",
    )
    labels = tuple(STAGE_LABELS[stage.value] for stage in WorkflowStage)
    assert labels == expected


@pytest.mark.parametrize(
    ("stage", "primary"),
    (
        ("subject", "advance"),
        ("content_sources", "validate"),
        ("validation", "preview"),
        ("preview", "approve"),
        ("approval", "publish"),
        ("publication", "version"),
    ),
)
def test_primary_action_follows_workflow(stage, primary):
    assert PRIMARY_ACTION_BY_STAGE[stage] == primary
    view = workspace_page(make_workspace(current_stage=stage))
    assert view.primary_action == primary


def test_workspace_workflow_renders_all_stages():
    view = workspace_page(make_workspace(current_stage="approval"))
    values = [value for value, _, _ in view.workflow_stages]
    assert values == [stage.value for stage in WorkflowStage]
