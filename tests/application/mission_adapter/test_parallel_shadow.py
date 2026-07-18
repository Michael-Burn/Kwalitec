"""Parallel and shadow execution tests."""

from __future__ import annotations

import pytest

from app.application.mission_adapter.dto.routing_decision import (
    RoutingMode,
    SelectedEngine,
)
from app.application.mission_adapter.migration_manager import MigrationPhase
from tests.application.mission_adapter.helpers import (
    make_adapter,
    make_request,
    make_v1,
    make_v2,
)


def test_parallel_runs_both_engines():
    v1, v2 = make_v1(), make_v2()
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request())
    assert "generate_mission" in v1.calls
    assert "generate_mission" in v2.calls
    assert result.shadow_executed is True
    assert result.comparison is not None
    assert result.mission is not None
    assert result.mission.engine_id == "v1"
    assert result.routing.expose_v2 is False


def test_parallel_never_exposes_v2():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request())
    assert result.routing.primary_engine == SelectedEngine.V1
    assert result.mission.engine_id == "v1"


def test_shadow_runs_v2_without_exposure():
    v1, v2 = make_v1(), make_v2()
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    adapter.router.set_mode_override(RoutingMode.SHADOW)
    result = adapter.generate_mission(make_request())
    assert result.shadow_executed is True
    assert result.mission.engine_id == "v1"
    assert result.routing.expose_v2 is False
    assert result.comparison is not None


def test_shadow_v2_failure_does_not_break_primary():
    v1 = make_v1()
    v2 = make_v2(fail_ops={"generate_mission"})
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    adapter.router.set_mode_override(RoutingMode.SHADOW)
    result = adapter.generate_mission(make_request())
    assert result.mission is not None
    assert result.mission.engine_id == "v1"
    assert result.shadow_executed is False
    assert result.comparison is None


def test_parallel_comparison_match():
    adapter = make_adapter(
        v1=make_v1(),
        v2=make_v2(),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request())
    assert result.comparison is not None
    assert result.comparison.matched is True
    assert result.comparison.divergence_count == 0


def test_parallel_comparison_divergence():
    adapter = make_adapter(
        v1=make_v1(topic_id="topic-a"),
        v2=make_v2(topic_id="topic-b"),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request(topic_id=None))
    assert result.comparison is not None
    assert result.comparison.matched is False
    assert result.comparison.divergence_count >= 1


@pytest.mark.parametrize(
    "operation",
    [
        "generate_mission",
        "resume_mission",
        "pause_mission",
        "skip_mission",
        "archive_mission",
    ],
)
def test_parallel_all_operations(operation):
    v1, v2 = make_v1(), make_v2()
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    method = getattr(adapter, operation)
    result = method(make_request(operation=operation, mission_id="m-1"))
    assert operation in v1.calls
    assert operation in v2.calls
    assert result.audit.operation == operation


def test_shadow_without_v2_skips_compare():
    adapter = make_adapter(
        v2=None,
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    adapter.router.set_mode_override(RoutingMode.SHADOW)
    result = adapter.generate_mission(make_request())
    assert result.shadow_executed is False
    assert result.comparison is None


def test_parallel_audit_marks_comparison():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request())
    assert result.audit.comparison_executed is True
    assert result.audit.comparison_id == result.comparison.comparison_id


def test_comparison_summary_updates():
    adapter = make_adapter(
        v1=make_v1(),
        v2=make_v2(effort="high"),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    adapter.generate_mission(make_request())
    summary = adapter.comparison_summary()
    assert summary["total"] == 1
    assert summary["diverged"] == 1


def test_legacy_does_not_run_v2():
    v2 = make_v2()
    adapter = make_adapter(v2=v2, phase=MigrationPhase.LEGACY_ONLY)
    adapter.generate_mission(make_request())
    assert v2.calls == []
