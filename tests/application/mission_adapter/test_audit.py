"""Audit service and record tests."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from app.application.mission_adapter.audit_service import AuditService
from app.application.mission_adapter.dto.routing_decision import (
    RoutingMode,
    SelectedEngine,
)
from app.application.mission_adapter.exceptions import AuditFailure
from app.application.mission_adapter.migration_manager import MigrationPhase
from tests.application.mission_adapter.helpers import (
    NOW,
    make_adapter,
    make_request,
    make_v2,
)


def test_audit_generated_on_success():
    adapter = make_adapter()
    result = adapter.generate_mission(make_request())
    assert result.audit.operation == "generate_mission"
    assert result.audit.learner_id == "learner-1"
    assert result.audit.routing_mode == RoutingMode.LEGACY
    assert result.audit.selected_engine == SelectedEngine.V1
    assert result.audit.success is True
    assert result.audit.comparison_executed is False
    assert "adapter" in result.audit.engine_versions
    assert result.audit.duration_ms >= 0


def test_audit_immutable():
    adapter = make_adapter()
    result = adapter.generate_mission(make_request())
    with pytest.raises(Exception):
        result.audit.success = False  # type: ignore[misc]


def test_audit_service_requires_operation():
    svc = AuditService(clock=lambda: NOW)
    with pytest.raises(AuditFailure):
        svc.record(
            operation="",
            learner_id="l1",
            routing_mode=RoutingMode.LEGACY,
            selected_engine=SelectedEngine.V1,
        )


def test_audit_service_requires_learner():
    svc = AuditService(clock=lambda: NOW)
    with pytest.raises(AuditFailure):
        svc.record(
            operation="generate_mission",
            learner_id="",
            routing_mode=RoutingMode.LEGACY,
            selected_engine=SelectedEngine.V1,
        )


def test_audit_engine_versions_proxy():
    svc = AuditService(clock=lambda: NOW, id_factory=lambda: "a1")
    record = svc.record(
        operation="generate_mission",
        learner_id="l1",
        routing_mode=RoutingMode.LEGACY,
        selected_engine=SelectedEngine.V1,
        engine_versions={"v1": "1.0"},
    )
    assert isinstance(record.engine_versions, MappingProxyType)
    with pytest.raises(TypeError):
        record.engine_versions["v1"] = "x"  # type: ignore[index]


def test_audit_for_learner_filter():
    adapter = make_adapter()
    adapter.generate_mission(make_request(learner_id="a"))
    adapter.generate_mission(make_request(learner_id="b"))
    assert len(adapter.audit_service.for_learner("a")) == 1
    assert len(adapter.audit_service.for_learner("b")) == 1


def test_audit_latest():
    adapter = make_adapter()
    assert adapter.audit_service.latest() is None
    adapter.generate_mission(make_request())
    assert adapter.audit_service.latest() is not None


def test_audit_clear():
    adapter = make_adapter()
    adapter.generate_mission(make_request())
    adapter.audit_service.clear()
    assert adapter.audit_service.records == ()


def test_audit_on_failure():
    from app.application.mission_adapter.exceptions import EngineUnavailable
    from tests.application.mission_adapter.helpers import make_v1

    adapter = make_adapter(v1=make_v1(available=False))
    with pytest.raises(EngineUnavailable):
        adapter.generate_mission(make_request())
    latest = adapter.audit_service.latest()
    assert latest is not None
    assert latest.success is False
    assert latest.error_type == "EngineUnavailable"


def test_audit_captures_organisation():
    adapter = make_adapter()
    result = adapter.generate_mission(
        make_request(organisation_id="org-9")
    )
    assert result.audit.organisation_id == "org-9"


def test_audit_captures_correlation():
    adapter = make_adapter()
    result = adapter.generate_mission(
        make_request(correlation_id="corr-xyz")
    )
    assert result.audit.correlation_id == "corr-xyz"


def test_parallel_audit_has_comparison_id():
    adapter = make_adapter(
        v2=make_v2(),
        phase=MigrationPhase.PARALLEL_VALIDATION,
        global_v2_enabled=True,
    )
    result = adapter.generate_mission(make_request())
    assert result.audit.comparison_executed is True
    assert result.audit.comparison_id is not None


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
def test_each_operation_audited(op):
    adapter = make_adapter()
    getattr(adapter, op)(make_request(operation=op, mission_id="m"))
    assert adapter.audit_service.latest().operation == op


def test_audit_timestamp_uses_clock():
    adapter = make_adapter()
    result = adapter.generate_mission(make_request())
    assert result.audit.timestamp == NOW
