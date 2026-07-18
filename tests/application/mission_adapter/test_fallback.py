"""Fallback and engine unavailability tests."""

from __future__ import annotations

import pytest

from app.application.mission_adapter.exceptions import EngineUnavailable
from app.application.mission_adapter.migration_manager import MigrationPhase
from tests.application.mission_adapter.helpers import (
    make_adapter,
    make_request,
    make_v1,
    make_v2,
)


def test_v2_only_falls_back_to_v1():
    v1 = make_v1()
    v2 = make_v2(fail_ops={"generate_mission"})
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request())
    assert result.fallback_used is True
    assert result.mission.engine_id == "v1"
    assert "v1" in result.audit.fallbacks


def test_v2_only_without_fallback_raises():
    v2 = make_v2(fail_ops={"generate_mission"})
    adapter = make_adapter(
        v1=None,
        v2=v2,
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    # Need to bind only v2 — create with v1=None still creates default v1
    # in helpers. Build manually:
    from app.application.mission_adapter.adapter import MissionAdapter
    from app.application.mission_adapter.migration_manager import MigrationManager

    migration = MigrationManager(initial_phase=MigrationPhase.FULL_V2)
    adapter = MissionAdapter.create(
        v1_engine=None,
        v2_engine=v2,
        global_v2_enabled=True,
        migration_manager=migration,
    )
    with pytest.raises(EngineUnavailable):
        adapter.generate_mission(make_request())


def test_legacy_unavailable_raises():
    v1 = make_v1(available=False)
    adapter = make_adapter(v1=v1)
    with pytest.raises(EngineUnavailable):
        adapter.generate_mission(make_request())


def test_ab_bucket_b_fallback_on_v2_failure():
    # Find a learner that maps to bucket B
    from app.application.mission_adapter.policies.routing_policy import (
        RoutingPolicy,
    )

    learner = None
    for i in range(200):
        lid = f"candidate-{i}"
        if RoutingPolicy.ab_bucket(lid) == RoutingPolicy.BUCKET_B:
            learner = lid
            break
    assert learner is not None

    v1 = make_v1()
    v2 = make_v2(fail_ops={"generate_mission"})
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.LIMITED_V2,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request(learner_id=learner))
    assert result.routing.primary_engine.value in {"v1", "v2"}
    if result.routing.primary_engine.value == "v2":
        assert result.fallback_used is True
        assert result.mission.engine_id == "v1"


def test_both_engines_fail_raises():
    v1 = make_v1(fail_ops={"generate_mission"})
    v2 = make_v2(fail_ops={"generate_mission"})
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    with pytest.raises(EngineUnavailable):
        adapter.generate_mission(make_request())


@pytest.mark.parametrize(
    "op",
    ["resume_mission", "pause_mission", "skip_mission", "archive_mission"],
)
def test_fallback_on_lifecycle_ops(op):
    v1 = make_v1()
    v2 = make_v2(fail_ops={op})
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    result = getattr(adapter, op)(make_request(operation=op, mission_id="m"))
    assert result.fallback_used is True


def test_audit_records_fallback():
    v1 = make_v1()
    v2 = make_v2(fail_ops={"generate_mission"})
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request())
    assert result.audit.fallbacks == ("v1",)
    assert result.audit.success is True


def test_health_tracks_fallbacks():
    v1 = make_v1()
    v2 = make_v2(fail_ops={"generate_mission"})
    adapter = make_adapter(
        v1=v1,
        v2=v2,
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    adapter.generate_mission(make_request())
    status = adapter.health_status()
    assert status["fallback_frequency"] > 0
