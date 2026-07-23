"""Workflow 4 — Console Assessments → Learning → Content navigation."""

from __future__ import annotations

import pytest

from app.founder.dashboard.nav import (
    COMMAND_CENTRE_NAV,
    COMMAND_CENTRE_SECONDARY_NAV,
    active_section_id,
)
from tests.presentation.workflows.helpers import (
    ALPHA_PRIMARY_NAV,
    login_founder,
    primary_nav_labels,
    wire_studio,
)


@pytest.fixture
def founder_client(app, client, ctx):
    wire_studio(app)
    login_founder(client, app)
    return client


@pytest.mark.parametrize("label", ALPHA_PRIMARY_NAV)
def test_alpha_destinations_in_primary_nav(label):
    assert label in primary_nav_labels()


def test_nav_order_content_learning_assessments():
    labels = primary_nav_labels()
    content = labels.index("Content")
    learning = labels.index("Learning")
    assessments = labels.index("Assessments")
    assert learning < assessments < content


def test_assessments_not_secondary_only():
    secondary = [item.section_id for item in COMMAND_CENTRE_SECONDARY_NAV]
    assert "assessments" not in secondary
    primary = [item.section_id for item in COMMAND_CENTRE_NAV]
    assert "assessments" in primary


@pytest.mark.parametrize(
    ("path", "marker", "section"),
    (
        ("/console/studio/", "Curriculum Studio", "content"),
        ("/console/intelligence", "Founder Intelligence", "learning"),
        ("/console/evidence-gates", "Evidence Gates", "assessments"),
    ),
)
def test_founder_alpha_pages_render(founder_client, path, marker, section):
    response = founder_client.get(path)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert marker in html
    assert "console-nav" in html or "console-sidebar" in html
    assert active_section_id(
        {
            "/console/studio/": "curriculum_studio.index",
            "/console/intelligence": "founder_dashboard.founder_intelligence",
            "/console/evidence-gates": "founder_dashboard.evidence_gates",
        }[path]
    ) == section


def test_intelligence_links_to_evidence_and_studio(founder_client):
    html = founder_client.get("/console/intelligence").get_data(as_text=True)
    assert "/console/evidence-gates" in html
    assert "/console/studio" in html


def test_evidence_gates_links_to_intelligence_and_studio(founder_client):
    html = founder_client.get("/console/evidence-gates").get_data(as_text=True)
    assert "/console/intelligence" in html
    assert "/console/studio" in html


def test_breadcrumbs_present_on_alpha_pages(founder_client):
    paths = (
        "/console/intelligence",
        "/console/evidence-gates",
        "/console/studio/",
    )
    for path in paths:
        html = founder_client.get(path).get_data(as_text=True)
        assert "founder-breadcrumb" in html or "breadcrumb" in html.lower()


def test_dual_run_label_visible_on_intelligence(founder_client):
    html = founder_client.get("/console/intelligence").get_data(as_text=True).lower()
    assert "dual-run" in html or "dual run" in html


def test_dual_run_label_visible_on_evidence_gates(founder_client):
    html = founder_client.get("/console/evidence-gates").get_data(as_text=True).lower()
    assert "dual-run" in html or "dual run" in html


def test_nav_section_ids_unique():
    ids = [item.section_id for item in COMMAND_CENTRE_NAV]
    assert len(ids) == len(set(ids))


def test_nav_labels_unique():
    labels = [item.label for item in COMMAND_CENTRE_NAV]
    assert len(labels) == len(set(labels))


@pytest.mark.parametrize(
    "endpoint",
    (
        "curriculum_studio.index",
        "curriculum_studio.workspace",
        "curriculum_studio.validate",
        "curriculum_studio.publish",
    ),
)
def test_studio_endpoints_map_to_content_section(endpoint):
    assert active_section_id(endpoint) == "content"
