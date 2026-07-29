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


def test_curriculum_authority_primary_nav():
    labels = [item.label for item in COMMAND_CENTRE_NAV]
    for required in (
        "Home",
        "Subjects",
        "Curriculum Studio",
        "Students",
        "Support",
        "Settings",
    ):
        assert required in labels
    studio = next(i for i in COMMAND_CENTRE_NAV if i.section_id == "curriculum_studio")
    assert studio.endpoint == "curriculum_studio.index"
    # Hub peers demoted from primary curriculum chrome (DX-004A).
    assert "Review Queue" not in labels
    assert "Publishing" not in labels
    assert "Content" not in labels
    assert "Assessments" not in labels
    secondary_ids = [item.section_id for item in COMMAND_CENTRE_SECONDARY_NAV]
    assert "assessments" in secondary_ids
    assert "review_queue" not in secondary_ids
    assert "publishing" not in secondary_ids


@pytest.mark.parametrize(
    ("endpoint", "expected"),
    (
        ("curriculum_studio.index", "curriculum_studio"),
        ("curriculum_studio.workspace", "curriculum_studio"),
        ("curriculum_studio.subjects_hub", "subjects"),
        ("founder_dashboard.founder_intelligence", "settings"),
        ("founder_dashboard.evidence_gates", "settings"),
        ("founder_dashboard.index", "home"),
    ),
)
def test_active_section_mapping(endpoint, expected):
    assert active_section_id(endpoint) == expected


def test_workflow_order_matches_founder_journey():
    expected = (
        "Upload",
        "Upload",
        "Validate",
        "Review",
        "Approve",
        "Publish",
    )
    labels = tuple(STAGE_LABELS[stage.value] for stage in WorkflowStage)
    assert labels == expected


@pytest.mark.parametrize(
    ("stage", "primary"),
    (
        ("subject", "advance"),
        ("content_sources", "upload"),
        ("validation", "validate"),
        ("preview", "preview"),
        ("approval", "approve"),
        ("publication", "publish"),
    ),
)
def test_primary_action_follows_workflow(stage, primary):
    assert PRIMARY_ACTION_BY_STAGE[stage] == primary
    version = "2026.1" if stage == "publication" else ""
    view = workspace_page(make_workspace(current_stage=stage, version_label=version))
    assert view.primary_action == primary


def test_workspace_workflow_renders_all_stages():
    view = workspace_page(make_workspace(current_stage="approval"))
    labels = [label for _, label, _ in view.workflow_stages]
    assert labels == ["Upload", "Validate", "Review", "Approve", "Publish"]
