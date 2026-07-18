"""Health monitor tests — must never alter routing."""

from __future__ import annotations

from app.application.mission_adapter.dto.routing_decision import RoutingMode
from app.application.mission_adapter.health_monitor import HealthMonitor
from app.application.mission_adapter.migration_manager import MigrationPhase
from tests.application.mission_adapter.helpers import (
    NOW,
    make_adapter,
    make_request,
    make_v1,
    make_v2,
)


def test_health_status_shape():
    adapter = make_adapter(v2=make_v2(), global_v2_enabled=True)
    status = adapter.health_status()
    assert "v1_available" in status
    assert "v2_available" in status
    assert "routing_mode" in status
    assert "migration_phase" in status
    assert "healthy" in status
    assert status["invocations"] == 0


def test_health_tracks_invocations():
    adapter = make_adapter()
    adapter.generate_mission(make_request())
    adapter.resume_mission(make_request(mission_id="m"))
    status = adapter.health_status()
    assert status["invocations"] == 2
    assert status["successes"] == 2


def test_health_tracks_failures():
    adapter = make_adapter(v1=make_v1(available=False))
    try:
        adapter.generate_mission(make_request())
    except Exception:
        pass
    status = adapter.health_status()
    assert status["failures"] == 1
    assert status["healthy"] is False


def test_health_never_changes_routing():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    before = adapter.preview_routing(make_request())
    adapter.generate_mission(make_request())
    adapter.health_status()
    after = adapter.preview_routing(make_request())
    assert before == after


def test_note_invocation_counters():
    mon = HealthMonitor(clock=lambda: NOW)
    mon.note_invocation(
        mode=RoutingMode.PARALLEL,
        success=True,
        comparison_executed=True,
        comparison_diverged=True,
    )
    mon.note_invocation(
        mode=RoutingMode.LEGACY,
        success=False,
        error_type="EngineUnavailable",
        v1_unavailable=True,
    )
    c = mon.counters
    assert c.invocations == 2
    assert c.comparison_divergences == 1
    assert c.v1_unavailable == 1
    assert c.by_mode["parallel"] == 1
    assert c.by_error["EngineUnavailable"] == 1


def test_reset_clears():
    mon = HealthMonitor(clock=lambda: NOW)
    mon.note_invocation(mode=RoutingMode.LEGACY, success=True)
    mon.reset()
    assert mon.counters.invocations == 0
    assert mon.status(
        v1_available=True,
        v2_available=False,
        routing_mode=RoutingMode.LEGACY,
        migration_phase="legacy_only",
    )["last_event_at"] is None


def test_fallback_frequency():
    adapter = make_adapter(
        v1=make_v1(),
        v2=make_v2(fail_ops={"generate_mission"}),
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    adapter.generate_mission(make_request())
    status = adapter.health_status()
    assert status["fallback_frequency"] == 1.0


def test_comparison_failure_tracked():
    adapter = make_adapter(
        v1=make_v1(),
        v2=make_v2(fail_ops={"generate_mission"}),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    adapter.router.set_mode_override(RoutingMode.SHADOW)
    adapter.generate_mission(make_request())
    status = adapter.health_status()
    assert status["comparison_failures"] >= 1


def test_by_mode_populated():
    adapter = make_adapter()
    adapter.generate_mission(make_request())
    status = adapter.health_status()
    assert status["by_mode"]["legacy"] == 1
