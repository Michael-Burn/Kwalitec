"""Health and diagnostics coverage."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from tests.application.learning_orchestrator.helpers import (
    EVENT_TYPES,
    FakeTwin,
    make_orchestrator,
    make_request,
)


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_diagnostics_after_each_event(event_type):
    orch = make_orchestrator()
    orch.orchestrate(make_request(event_type=event_type))
    report = orch.diagnostics()
    assert event_type in report.execution_timings
    assert report.canonical_pipeline[0] == "evidence"


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_event_readiness_in_health(event_type):
    orch = make_orchestrator()
    health = orch.health_status()
    assert health["event_readiness"][event_type] is True


def test_diagnostic_report_frozen():
    orch = make_orchestrator()
    orch.orchestrate(make_request())
    report = orch.diagnostics()
    with pytest.raises(FrozenInstanceError):
        report.orchestrator_version = "x"  # type: ignore[misc]


def test_dependency_status_structure():
    orch = make_orchestrator()
    status = orch.engine.dependency_status()
    for name in (
        "evidence",
        "twin",
        "adaptive_learning",
        "mission",
        "analytics",
    ):
        assert status[name]["bound"] is True
        assert status[name]["available"] is True


def test_unhealthy_when_bound_but_unavailable():
    orch = make_orchestrator(twin=FakeTwin(available=False))
    health = orch.health_status()
    assert health["orchestrator_status"] == "unhealthy"


@pytest.mark.parametrize("n", range(10))
def test_diagnostics_warning_window(n):
    orch = make_orchestrator()
    orch.orchestrate(make_request(event_id=f"w-{n}"))
    report = orch.diagnostics()
    assert isinstance(report.recent_warnings, tuple)
