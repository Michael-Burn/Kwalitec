"""Workflow 4 — Founder Evidence Gates → Intelligence → Studio navigation."""

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


def test_nav_order_studio_intelligence_evidence():
    labels = primary_nav_labels()
    studio = labels.index("Studio")
    intelligence = labels.index("Intelligence")
    evidence = labels.index("Evidence Gates")
    assert studio < intelligence < evidence


def test_evidence_gates_not_secondary_only():
    secondary = [item.section_id for item in COMMAND_CENTRE_SECONDARY_NAV]
    assert "evidence_gates" not in secondary
    primary = [item.section_id for item in COMMAND_CENTRE_NAV]
    assert "evidence_gates" in primary


@pytest.mark.parametrize(
    ("path", "marker", "section"),
    (
        ("/founder/studio/", "Curriculum Studio", "studio"),
        ("/founder/intelligence", "Founder Intelligence", "intelligence"),
        ("/founder/evidence-gates", "Evidence Gates", "evidence_gates"),
    ),
)
def test_founder_alpha_pages_render(founder_client, path, marker, section):
    response = founder_client.get(path)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert marker in html
    assert "founder-cc-nav" in html
    assert active_section_id(
        {
            "/founder/studio/": "curriculum_studio.index",
            "/founder/intelligence": "founder_dashboard.founder_intelligence",
            "/founder/evidence-gates": "founder_dashboard.evidence_gates",
        }[path]
    ) == section


def test_intelligence_links_to_evidence_and_studio(founder_client):
    html = founder_client.get("/founder/intelligence").get_data(as_text=True)
    assert "/founder/evidence-gates" in html
    assert "/founder/studio" in html


def test_evidence_gates_links_to_intelligence_and_studio(founder_client):
    html = founder_client.get("/founder/evidence-gates").get_data(as_text=True)
    assert "/founder/intelligence" in html
    assert "/founder/studio" in html


def test_breadcrumbs_present_on_alpha_pages(founder_client):
    paths = (
        "/founder/intelligence",
        "/founder/evidence-gates",
        "/founder/studio/",
    )
    for path in paths:
        html = founder_client.get(path).get_data(as_text=True)
        assert "founder-breadcrumb" in html or "breadcrumb" in html.lower()


def test_dual_run_label_visible_on_intelligence(founder_client):
    html = founder_client.get("/founder/intelligence").get_data(as_text=True).lower()
    assert "dual-run" in html or "dual run" in html


def test_dual_run_label_visible_on_evidence_gates(founder_client):
    html = founder_client.get("/founder/evidence-gates").get_data(as_text=True).lower()
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
def test_studio_endpoints_map_to_studio_section(endpoint):
    assert active_section_id(endpoint) == "studio"
