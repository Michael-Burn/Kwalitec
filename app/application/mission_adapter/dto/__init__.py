"""Immutable DTOs for the Mission Adapter."""

from __future__ import annotations

from typing import Any

__all__ = [
    "AdapterRequest",
    "AdapterResult",
    "AuditRecord",
    "ComparisonResult",
    "DimensionMatch",
    "MissionSnapshot",
    "RoutingDecision",
    "RoutingMode",
    "SelectedEngine",
]

_EXPORT_MODULES = {
    "AdapterRequest": "app.application.mission_adapter.dto.adapter_request",
    "AdapterResult": "app.application.mission_adapter.dto.adapter_result",
    "AuditRecord": "app.application.mission_adapter.dto.audit_record",
    "ComparisonResult": "app.application.mission_adapter.dto.comparison_result",
    "DimensionMatch": "app.application.mission_adapter.dto.comparison_result",
    "MissionSnapshot": "app.application.mission_adapter.dto.mission_snapshot",
    "RoutingDecision": "app.application.mission_adapter.dto.routing_decision",
    "RoutingMode": "app.application.mission_adapter.dto.routing_decision",
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
