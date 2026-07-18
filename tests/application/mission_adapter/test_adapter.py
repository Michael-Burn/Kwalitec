"""MissionAdapter facade and dependency-injection tests."""

from __future__ import annotations

import pytest

from app.application.mission_adapter.adapter import MissionAdapter
from app.application.mission_adapter.audit_service import AuditService
from app.application.mission_adapter.comparison_service import ComparisonService
from app.application.mission_adapter.contracts import MissionEnginePort
from app.application.mission_adapter.exceptions import MissionAdapterError
from app.application.mission_adapter.feature_gate import FeatureGate
from app.application.mission_adapter.health_monitor import HealthMonitor
from app.application.mission_adapter.migration_manager import (
    MigrationManager,
    MigrationPhase,
)
from app.application.mission_adapter.router import MissionRouter
from tests.application.mission_adapter.helpers import (
    NOW,
    FakeEngine,
    make_adapter,
    make_request,
    make_v1,
    make_v2,
)


@pytest.mark.parametrize(
    "op",
    [
        "generate_mission",
        "resume_mission",
        "pause_mission",
        "skip_mission",
        "archive_mission",
    ],
)
def test_public_operations(op):
    adapter = make_adapter()
    result = getattr(adapter, op)(make_request(operation=op, mission_id="m-1"))
    assert result.mission is not None
    assert result.routing is not None
    assert result.audit is not None


def test_create_injects_engines():
    v1, v2 = make_v1(), make_v2()
    adapter = MissionAdapter.create(
        v1_engine=v1,
        v2_engine=v2,
        global_v2_enabled=True,
        migration_manager=MigrationManager(
            initial_phase=MigrationPhase.PARALLEL_VALIDATION
        ),
        clock=lambda: NOW,
    )
    assert adapter.router.v1_engine is v1
    assert adapter.router.v2_engine is v2


def test_create_does_not_instantiate_real_engines():
    """Adapter must not import/construct MissionEngine or MissionService."""
    adapter = MissionAdapter.create(v1_engine=make_v1())
    assert isinstance(adapter.router.v1_engine, FakeEngine)


def test_explicit_di_constructor():
    migration = MigrationManager()
    gate = FeatureGate(migration_manager=migration, global_enabled=False)
    router = MissionRouter(
        migration_manager=migration,
        feature_gate=gate,
        v1_engine=make_v1(),
    )
    audit = AuditService(clock=lambda: NOW)
    comparison = ComparisonService(id_factory=lambda: "c")
    health = HealthMonitor(clock=lambda: NOW)
    adapter = MissionAdapter(
        router=router,
        feature_gate=gate,
        migration_manager=migration,
        comparison_service=comparison,
        audit_service=audit,
        health_monitor=health,
    )
    result = adapter.generate_mission(make_request())
    assert result.audit is audit.latest()
    assert adapter.comparison_service is comparison
    assert adapter.health_monitor is health


def test_fake_engine_satisfies_protocol():
    engine = make_v1()
    assert isinstance(engine, MissionEnginePort)


def test_operation_stamped_on_request():
    adapter = make_adapter()
    # Request says pause but method is generate — adapter stamps method name.
    result = adapter.generate_mission(
        make_request(operation="pause_mission")
    )
    assert result.audit.operation == "generate_mission"


def test_accessors():
    adapter = make_adapter()
    assert adapter.migration_manager.phase == MigrationPhase.LEGACY_ONLY
    assert adapter.feature_gate is not None
    assert adapter.router is not None


def test_adapter_version_constant():
    assert MissionAdapter.ADAPTER_VERSION == "mission-adapter-1"


def test_package_exports():
    import app.application.mission_adapter as pkg

    assert pkg.MissionAdapter is MissionAdapter
    assert pkg.MissionRouter is MissionRouter
    assert pkg.FeatureGate is FeatureGate
    assert pkg.MigrationManager is MigrationManager
    assert pkg.ComparisonService is ComparisonService
    assert pkg.AuditService is AuditService
    assert pkg.HealthMonitor is HealthMonitor


def test_package_dir():
    import app.application.mission_adapter as pkg

    assert "MissionAdapter" in dir(pkg)
    assert "RoutingMode" in dir(pkg)


def test_unknown_package_attr():
    import app.application.mission_adapter as pkg

    with pytest.raises(AttributeError):
        _ = pkg.DoesNotExist  # type: ignore[attr-defined]


def test_v2_only_exposes_v2():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.FULL_V2,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request())
    assert result.mission.engine_id == "v2"
    assert result.routing.expose_v2 is True


def test_ab_disabled_uses_v1():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.LIMITED_V2,
        global_v2_enabled=False,
    )
    result = adapter.generate_mission(make_request())
    assert result.mission.engine_id == "v1"


def test_engine_generic_exception_wrapped():
    class BoomEngine(FakeEngine):
        def generate_mission(self, request):
            raise RuntimeError("boom")

    adapter = make_adapter(v1=BoomEngine(engine_id="v1"))
    with pytest.raises(MissionAdapterError, match="boom"):
        adapter.generate_mission(make_request())


def test_comparison_summary_empty_initially():
    adapter = make_adapter()
    assert adapter.comparison_summary()["total"] == 0
