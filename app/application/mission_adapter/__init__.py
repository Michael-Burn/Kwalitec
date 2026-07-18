"""Mission Adapter — sole public entry point for mission generation.

Routes between Mission Engine V1 and Mission Engine 2.0 contracts.
Responsible only for routing, comparison, auditing, and migration safety.
Contains NO educational logic.

Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.mission_adapter.adapter.MissionAdapter``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "AdapterRequest",
    "AdapterResult",
    "AuditFailure",
    "AuditRecord",
    "AuditService",
    "ComparisonFailure",
    "ComparisonPolicy",
    "ComparisonResult",
    "ComparisonService",
    "DimensionMatch",
    "EngineUnavailable",
    "FeatureGate",
    "HealthMonitor",
    "MigrationManager",
    "MigrationPhase",
    "MigrationStateError",
    "MissionAdapter",
    "MissionAdapterError",
    "MissionEnginePort",
    "MissionRouter",
    "MissionSnapshot",
    "RolloutPolicy",
    "RoutingDecision",
    "RoutingError",
    "RoutingMode",
    "RoutingPolicy",
    "SelectedEngine",
]

_EXPORT_MODULES = {
    "AdapterRequest": "app.application.mission_adapter.dto.adapter_request",
    "AdapterResult": "app.application.mission_adapter.dto.adapter_result",
    "AuditFailure": "app.application.mission_adapter.exceptions",
    "AuditRecord": "app.application.mission_adapter.dto.audit_record",
    "AuditService": "app.application.mission_adapter.audit_service",
    "ComparisonFailure": "app.application.mission_adapter.exceptions",
    "ComparisonPolicy": (
        "app.application.mission_adapter.policies.comparison_policy"
    ),
    "ComparisonResult": "app.application.mission_adapter.dto.comparison_result",
    "ComparisonService": "app.application.mission_adapter.comparison_service",
    "DimensionMatch": "app.application.mission_adapter.dto.comparison_result",
    "EngineUnavailable": "app.application.mission_adapter.exceptions",
    "FeatureGate": "app.application.mission_adapter.feature_gate",
    "HealthMonitor": "app.application.mission_adapter.health_monitor",
    "MigrationManager": "app.application.mission_adapter.migration_manager",
    "MigrationPhase": "app.application.mission_adapter.migration_manager",
    "MigrationStateError": "app.application.mission_adapter.exceptions",
    "MissionAdapter": "app.application.mission_adapter.adapter",
    "MissionAdapterError": "app.application.mission_adapter.exceptions",
    "MissionEnginePort": "app.application.mission_adapter.contracts",
    "MissionRouter": "app.application.mission_adapter.router",
    "MissionSnapshot": "app.application.mission_adapter.dto.mission_snapshot",
    "RolloutPolicy": "app.application.mission_adapter.policies.rollout_policy",
    "RoutingDecision": "app.application.mission_adapter.dto.routing_decision",
    "RoutingError": "app.application.mission_adapter.exceptions",
    "RoutingMode": "app.application.mission_adapter.dto.routing_decision",
    "RoutingPolicy": "app.application.mission_adapter.policies.routing_policy",
    "SelectedEngine": "app.application.mission_adapter.dto.routing_decision",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
