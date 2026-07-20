"""Curriculum Studio presentation smoke tests."""

from __future__ import annotations

from app.presentation.curriculum_studio.factory import build_studio_service
from app.presentation.curriculum_studio.view_models import dashboard_view


def test_build_studio_service_wires_ports():
    svc = build_studio_service()
    assert svc.port_available("curriculum_management") is True
    assert svc.port_available("curriculum_ingestion") is True
    dash = svc.founder_dashboard()
    view = dashboard_view(dash)
    assert view.published_count >= 0
    assert isinstance(view.workspaces, tuple)
