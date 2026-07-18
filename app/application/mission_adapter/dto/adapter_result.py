"""Immutable AdapterResult — public outcome of a Mission Adapter call."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.mission_adapter.dto.audit_record import AuditRecord
from app.application.mission_adapter.dto.comparison_result import ComparisonResult
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot
from app.application.mission_adapter.dto.routing_decision import RoutingDecision


@dataclass(frozen=True)
class AdapterResult:
    """Public result returned by MissionAdapter operations.

    ``mission`` is the engine result exposed under the routing decision.
    Shadow / parallel secondary results are never exposed unless
    ``routing.expose_v2`` (or primary selection) permits it — they live
    only on the comparison / audit trail.
    """

    mission: MissionSnapshot | None
    routing: RoutingDecision
    audit: AuditRecord
    comparison: ComparisonResult | None = None
    fallback_used: bool = False
    shadow_executed: bool = False
