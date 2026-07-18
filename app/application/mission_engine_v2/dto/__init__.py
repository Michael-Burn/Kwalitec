"""Immutable DTOs for Mission Engine 2.0."""

from __future__ import annotations

from typing import Any

__all__ = [
    "DailyMission",
    "MissionCard",
    "MissionDashboard",
    "MissionExecution",
    "MissionTimeline",
]

_EXPORT_MODULES = {
    "DailyMission": "app.application.mission_engine_v2.dto.daily_mission",
    "MissionCard": "app.application.mission_engine_v2.dto.mission_card",
    "MissionDashboard": "app.application.mission_engine_v2.dto.mission_dashboard",
    "MissionExecution": "app.application.mission_engine_v2.dto.mission_execution",
    "MissionTimeline": "app.application.mission_engine_v2.dto.mission_timeline",
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
