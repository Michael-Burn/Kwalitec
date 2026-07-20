"""Compact volume checks for Founder UX presentation (ARP-002)."""

from __future__ import annotations

import pytest

from app.presentation.curriculum_studio.view_models import (
    dashboard_view,
    friendly_checklist_summary,
    friendly_preview_summary,
)
from tests.presentation.curriculum_studio.helpers import (
    make_empty_dashboard,
    make_populated_dashboard,
)


@pytest.mark.parametrize("ready,total", ((0, 5), (5, 5)))
def test_checklist_summary_edges(ready, total):
    summary = friendly_checklist_summary(ready=ready, total=total)
    assert summary


@pytest.mark.parametrize("nodes", (0, 1, 4))
def test_preview_summary_edges(nodes):
    assert str(nodes) in friendly_preview_summary(
        readiness="ready", node_count=nodes
    )


@pytest.mark.parametrize("populated", (False, True))
def test_dashboard_toggle(populated):
    snap = make_populated_dashboard() if populated else make_empty_dashboard()
    view = dashboard_view(snap)
    assert view.has_workspaces is populated
