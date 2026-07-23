"""Founder surface HTTP smoke for Internal Alpha."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from tests.operational.helpers import (
    FOUNDER_SMOKE_PATHS,
    alpha_flags,
    login_founder,
    wire_studio,
)


@pytest.fixture
def founder_client(app, client, ctx):
    wire_studio(app)
    login_founder(client, app)
    return client


def test_founder_alpha_surfaces_return_200(founder_client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=alpha_flags(),
    ):
        for path in FOUNDER_SMOKE_PATHS:
            response = founder_client.get(path)
            assert response.status_code == 200, path
            assert b"Internal Server Error" not in response.data


def test_studio_dashboard_chrome(founder_client):
    html = founder_client.get("/console/studio/").get_data(as_text=True)
    assert "Studio" in html
    assert "subject" in html.lower()


def test_intelligence_advisory_surface(founder_client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=alpha_flags(),
    ):
        html = founder_client.get("/console/intelligence").get_data(as_text=True)
    assert "Intelligence" in html
    lowered = html.lower()
    assert "advisory" in lowered or "dual-run" in lowered or "signal" in lowered


def test_evidence_gates_checklist_surface(founder_client):
    html = founder_client.get("/console/evidence-gates").get_data(as_text=True)
    assert "Evidence" in html


def test_founder_nav_includes_alpha_trio():
    from app.founder.dashboard.nav import COMMAND_CENTRE_NAV

    labels = [item.label for item in COMMAND_CENTRE_NAV]
    assert "Content" in labels
    assert "Learning" in labels
    assert "Assessments" in labels


def test_founder_surfaces_require_auth(client):
    for path in FOUNDER_SMOKE_PATHS:
        response = client.get(path)
        assert response.status_code in {302, 401}, path


def test_studio_workspace_missing_recovers(founder_client):
    response = founder_client.get(
        "/console/studio/workspaces/does-not-exist",
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_founder_endpoints_registered(app):
    assert "founder_dashboard.founder_intelligence" in app.view_functions
    assert "founder_dashboard.evidence_gates" in app.view_functions
