"""DTO immutability and export tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from types import MappingProxyType

import pytest

from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.dto.adapter_result import AdapterResult
from app.application.mission_adapter.dto.audit_record import AuditRecord
from app.application.mission_adapter.dto.comparison_result import (
    ComparisonResult,
    DimensionMatch,
)
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot
from app.application.mission_adapter.dto.routing_decision import (
    RoutingDecision,
    RoutingMode,
    SelectedEngine,
)


def test_adapter_request_frozen():
    req = AdapterRequest(operation="generate_mission", learner_id="l1")
    with pytest.raises(FrozenInstanceError):
        req.learner_id = "x"  # type: ignore[misc]


def test_adapter_request_context_proxy():
    req = AdapterRequest(
        operation="generate_mission",
        learner_id="l1",
        context={"a": "1"},
    )
    assert isinstance(req.context, MappingProxyType)
    with pytest.raises(TypeError):
        req.context["a"] = "2"  # type: ignore[index]


def test_adapter_request_default_context():
    req = AdapterRequest(operation="generate_mission", learner_id="l1")
    assert dict(req.context) == {}


def test_mission_snapshot_frozen():
    snap = MissionSnapshot(
        mission_id="m",
        learner_id="l",
        journey_id="j",
        topic_id="t",
        session_id="s",
        effort="medium",
        mission_type="today",
        is_revision=False,
        sequence_index=0,
    )
    with pytest.raises(FrozenInstanceError):
        snap.effort = "high"  # type: ignore[misc]


def test_mission_snapshot_metadata_proxy():
    snap = MissionSnapshot(
        mission_id="m",
        learner_id="l",
        journey_id="j",
        topic_id="t",
        session_id="s",
        effort="medium",
        mission_type="today",
        is_revision=False,
        sequence_index=0,
        metadata={"k": "v"},
    )
    assert isinstance(snap.metadata, MappingProxyType)


def test_routing_decision_frozen():
    d = RoutingDecision(
        mode=RoutingMode.LEGACY,
        primary_engine=SelectedEngine.V1,
        shadow_engine=None,
        compare=False,
        expose_v2=False,
        reason="legacy_only",
    )
    with pytest.raises(FrozenInstanceError):
        d.reason = "x"  # type: ignore[misc]


def test_comparison_result_frozen():
    result = ComparisonResult(
        comparison_id="c1",
        matched=True,
        dimensions=(),
        v1_mission_id="a",
        v2_mission_id="b",
        divergence_count=0,
    )
    with pytest.raises(FrozenInstanceError):
        result.matched = False  # type: ignore[misc]


def test_dimension_match_frozen():
    d = DimensionMatch(
        name="topic_selected",
        matched=True,
        v1_value="t",
        v2_value="t",
    )
    with pytest.raises(FrozenInstanceError):
        d.matched = False  # type: ignore[misc]


def test_audit_record_frozen():
    record = AuditRecord(
        audit_id="a1",
        timestamp=datetime(2026, 7, 18, tzinfo=UTC),
        operation="generate_mission",
        learner_id="l1",
        routing_mode=RoutingMode.LEGACY,
        selected_engine=SelectedEngine.V1,
        fallbacks=(),
        duration_ms=1.0,
        comparison_executed=False,
        comparison_id=None,
        engine_versions=MappingProxyType({"v1": "1"}),
        success=True,
    )
    with pytest.raises(FrozenInstanceError):
        record.success = False  # type: ignore[misc]


def test_adapter_result_frozen():
    routing = RoutingDecision(
        mode=RoutingMode.LEGACY,
        primary_engine=SelectedEngine.V1,
        shadow_engine=None,
        compare=False,
        expose_v2=False,
        reason="legacy_only",
    )
    audit = AuditRecord(
        audit_id="a1",
        timestamp=datetime(2026, 7, 18, tzinfo=UTC),
        operation="generate_mission",
        learner_id="l1",
        routing_mode=RoutingMode.LEGACY,
        selected_engine=SelectedEngine.V1,
        fallbacks=(),
        duration_ms=1.0,
        comparison_executed=False,
        comparison_id=None,
        engine_versions=MappingProxyType({}),
        success=True,
    )
    result = AdapterResult(mission=None, routing=routing, audit=audit)
    with pytest.raises(FrozenInstanceError):
        result.fallback_used = True  # type: ignore[misc]


def test_dto_package_exports():
    from app.application.mission_adapter import dto

    assert dto.AdapterRequest is AdapterRequest
    assert dto.AdapterResult is AdapterResult
    assert dto.AuditRecord is AuditRecord
    assert dto.ComparisonResult is ComparisonResult
    assert dto.RoutingDecision is RoutingDecision
    assert dto.MissionSnapshot is MissionSnapshot
    assert dto.RoutingMode is RoutingMode
    assert dto.SelectedEngine is SelectedEngine


def test_dto_dir_includes_exports():
    from app.application.mission_adapter import dto

    names = dir(dto)
    assert "AdapterRequest" in names
    assert "RoutingMode" in names


def test_dto_unknown_attr():
    from app.application.mission_adapter import dto

    with pytest.raises(AttributeError):
        _ = dto.NotARealExport  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "mode",
    list(RoutingMode),
)
def test_routing_mode_values(mode):
    assert mode.value == mode.name.lower() or "_" in mode.value


@pytest.mark.parametrize("engine", list(SelectedEngine))
def test_selected_engine_values(engine):
    assert isinstance(engine.value, str)
