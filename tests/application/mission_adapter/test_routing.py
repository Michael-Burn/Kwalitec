"""Routing mode and MissionRouter tests."""

from __future__ import annotations

import pytest

from app.application.mission_adapter.dto.routing_decision import (
    RoutingMode,
    SelectedEngine,
)
from app.application.mission_adapter.exceptions import (
    EngineUnavailable,
    RoutingError,
)
from app.application.mission_adapter.feature_gate import FeatureGate
from app.application.mission_adapter.migration_manager import (
    MigrationManager,
    MigrationPhase,
)
from app.application.mission_adapter.policies.routing_policy import RoutingPolicy
from app.application.mission_adapter.router import MissionRouter
from tests.application.mission_adapter.helpers import (
    make_adapter,
    make_request,
    make_v1,
    make_v2,
)


@pytest.mark.parametrize(
    ("phase", "expected"),
    [
        (MigrationPhase.LEGACY_ONLY, RoutingMode.LEGACY),
        (MigrationPhase.PARALLEL_VALIDATION, RoutingMode.PARALLEL),
        (MigrationPhase.LIMITED_V2, RoutingMode.A_B),
        (MigrationPhase.FULL_V2, RoutingMode.V2_ONLY),
        (MigrationPhase.RETIRED_V1, RoutingMode.V2_ONLY),
    ],
)
def test_mode_for_phase(phase, expected):
    assert RoutingPolicy.mode_for_phase(phase) == expected


def test_mode_for_unknown_phase_raises():
    with pytest.raises(RoutingError):
        RoutingPolicy.mode_for_phase("nope")  # type: ignore[arg-type]


def test_legacy_routing():
    adapter = make_adapter(phase=MigrationPhase.LEGACY_ONLY)
    decision = adapter.preview_routing(make_request())
    assert decision.mode == RoutingMode.LEGACY
    assert decision.primary_engine == SelectedEngine.V1
    assert decision.compare is False
    assert decision.expose_v2 is False


def test_parallel_routing_with_v2():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    decision = adapter.preview_routing(make_request())
    assert decision.mode == RoutingMode.PARALLEL
    assert decision.primary_engine == SelectedEngine.V1
    assert decision.shadow_engine == SelectedEngine.V2
    assert decision.compare is True
    assert decision.expose_v2 is False


def test_parallel_degrades_without_v2_gate():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=False,
    )
    decision = adapter.preview_routing(make_request())
    assert decision.reason == "parallel_degraded_v1"
    assert decision.compare is False


def test_shadow_routing():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    adapter.router.set_mode_override(RoutingMode.SHADOW)
    decision = adapter.preview_routing(make_request())
    assert decision.mode == RoutingMode.SHADOW
    assert decision.primary_engine == SelectedEngine.V1
    assert decision.shadow_engine == SelectedEngine.V2
    assert decision.expose_v2 is False


def test_v2_only_routing():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    decision = adapter.preview_routing(make_request())
    assert decision.mode == RoutingMode.V2_ONLY
    assert decision.primary_engine == SelectedEngine.V2
    assert decision.expose_v2 is True
    assert decision.fallback_engine == SelectedEngine.V1


def test_ab_routing_deterministic():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.LIMITED_V2,
        global_v2_enabled=True,
    )
    r1 = adapter.preview_routing(make_request(learner_id="learner-alpha"))
    r2 = adapter.preview_routing(make_request(learner_id="learner-alpha"))
    assert r1.ab_bucket == r2.ab_bucket
    assert r1.primary_engine == r2.primary_engine


@pytest.mark.parametrize("learner_id", [f"learner-{i}" for i in range(14)])
def test_ab_bucket_stable_across_learners(learner_id):
    bucket_a = RoutingPolicy.ab_bucket(learner_id)
    bucket_b = RoutingPolicy.ab_bucket(learner_id)
    assert bucket_a == bucket_b
    assert bucket_a in {RoutingPolicy.BUCKET_A, RoutingPolicy.BUCKET_B}


def test_ab_buckets_differ_for_some_learners():
    buckets = {RoutingPolicy.ab_bucket(f"u-{i}") for i in range(50)}
    assert buckets == {RoutingPolicy.BUCKET_A, RoutingPolicy.BUCKET_B}


def test_legacy_requires_v1():
    migration = MigrationManager()
    gate = FeatureGate(migration_manager=migration, global_enabled=False)
    router = MissionRouter(
        migration_manager=migration,
        feature_gate=gate,
        v1_engine=None,
        v2_engine=None,
    )
    with pytest.raises(RoutingError):
        router.decide(make_request())


def test_v2_only_requires_gate():
    migration = MigrationManager(initial_phase=MigrationPhase.FULL_V2)
    gate = FeatureGate(migration_manager=migration, global_enabled=False)
    router = MissionRouter(
        migration_manager=migration,
        feature_gate=gate,
        v1_engine=make_v1(),
        v2_engine=make_v2(),
    )
    with pytest.raises(RoutingError, match="feature gate"):
        router.decide(make_request())


def test_v2_only_requires_engine():
    migration = MigrationManager(initial_phase=MigrationPhase.FULL_V2)
    gate = FeatureGate(migration_manager=migration, global_enabled=True)
    router = MissionRouter(
        migration_manager=migration,
        feature_gate=gate,
        v1_engine=make_v1(),
        v2_engine=None,
    )
    with pytest.raises(RoutingError, match="V2 engine"):
        router.decide(make_request())


def test_retired_v1_unavailable():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.RETIRED_V1,
        global_v2_enabled=True,
    )
    assert adapter.router.v1_available() is False
    assert adapter.router.v2_available() is True


def test_engine_for_v1():
    v1 = make_v1()
    adapter = make_adapter(v1=v1)
    assert adapter.router.engine_for(SelectedEngine.V1) is v1


def test_engine_for_missing_raises():
    adapter = make_adapter(v1=make_v1())
    with pytest.raises(EngineUnavailable):
        adapter.router.engine_for(SelectedEngine.V2)


def test_engine_for_none_raises():
    adapter = make_adapter()
    with pytest.raises(RoutingError):
        adapter.router.engine_for(SelectedEngine.NONE)


def test_mode_override_clears():
    adapter = make_adapter(v2=make_v2(), global_v2_enabled=True)
    adapter.router.set_mode_override(RoutingMode.SHADOW)
    assert adapter.router.resolve_mode() == RoutingMode.SHADOW
    adapter.router.set_mode_override(None)
    assert adapter.router.resolve_mode() == RoutingMode.LEGACY


def test_bind_engines():
    adapter = make_adapter()
    v2 = make_v2()
    adapter.router.bind_engines(v2_engine=v2)
    assert adapter.router.v2_engine is v2


def test_routing_decision_immutable():
    adapter = make_adapter()
    decision = adapter.preview_routing(make_request())
    with pytest.raises(Exception):
        decision.mode = RoutingMode.V2_ONLY  # type: ignore[misc]


@pytest.mark.parametrize(
    "mode",
    [
        RoutingMode.LEGACY,
        RoutingMode.V2_ONLY,
        RoutingMode.PARALLEL,
        RoutingMode.SHADOW,
        RoutingMode.A_B,
    ],
)
def test_routing_modes_exist(mode):
    assert isinstance(mode.value, str)


def test_unavailable_v1_reports_false():
    v1 = make_v1(available=False)
    adapter = make_adapter(v1=v1)
    assert adapter.router.v1_available() is False


def test_generate_uses_legacy_engine():
    v1 = make_v1()
    adapter = make_adapter(v1=v1)
    result = adapter.generate_mission(make_request())
    assert result.mission is not None
    assert result.mission.engine_id == "v1"
    assert "generate_mission" in v1.calls


def test_same_inputs_same_routing():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.LIMITED_V2,
        global_v2_enabled=True,
    )
    req = make_request(learner_id="stable-user")
    assert adapter.preview_routing(req) == adapter.preview_routing(req)
