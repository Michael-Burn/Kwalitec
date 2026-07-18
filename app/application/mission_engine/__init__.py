"""Version 2 Mission Engine 2.0 — application-layer orchestration.

Coordinates Curriculum Graph → Learning Journey Engine → Learning Session
Runtime → Daily Mission → Student Dashboard DTOs.

Framework-independent: no Flask, SQLAlchemy, UI, migrations, or feature flags.
Educational reasoning belongs in Journey Engine / Session Runtime — this
package owns mission generation, scheduling, lifecycle, and delivery only.

Prefer explicit imports such as
``app.application.mission_engine.engine.MissionEngine``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActiveMissionExists",
    "DailyMission",
    "DeliveryAction",
    "DeliveryError",
    "DeliveryPolicy",
    "DuplicateMission",
    "InvalidJourneyReference",
    "InvalidMissionState",
    "InvalidSessionReference",
    "MissionAlreadyArchived",
    "MissionAlreadyCompleted",
    "MissionArchive",
    "MissionBuildError",
    "MissionBuilder",
    "MissionCoordinator",
    "MissionDelivery",
    "MissionDispatcher",
    "MissionEngine",
    "MissionEngineError",
    "MissionNotFound",
    "MissionSchedule",
    "MissionScheduler",
    "MissionSlot",
    "MissionState",
    "MissionSummary",
    "MissionTransitionEvent",
    "MissionValidator",
    "SchedulingError",
    "SchedulingPolicy",
    "V1MissionAdapter",
    "V1MissionView",
    "WorkloadExceeded",
    "WorkloadPolicy",
]

_EXPORT_MODULES = {
    "ActiveMissionExists": "app.application.mission_engine.exceptions",
    "DailyMission": "app.application.mission_engine.dto.daily_mission",
    "DeliveryAction": "app.application.mission_engine.mission_state",
    "DeliveryError": "app.application.mission_engine.exceptions",
    "DeliveryPolicy": "app.application.mission_engine.policies.delivery_policy",
    "DuplicateMission": "app.application.mission_engine.exceptions",
    "InvalidJourneyReference": "app.application.mission_engine.exceptions",
    "InvalidMissionState": "app.application.mission_engine.exceptions",
    "InvalidSessionReference": "app.application.mission_engine.exceptions",
    "MissionAlreadyArchived": "app.application.mission_engine.exceptions",
    "MissionAlreadyCompleted": "app.application.mission_engine.exceptions",
    "MissionArchive": "app.application.mission_engine.mission_archive",
    "MissionBuildError": "app.application.mission_engine.exceptions",
    "MissionBuilder": "app.application.mission_engine.mission_builder",
    "MissionCoordinator": "app.application.mission_engine.mission_coordinator",
    "MissionDelivery": "app.application.mission_engine.dto.mission_delivery",
    "MissionDispatcher": "app.application.mission_engine.mission_dispatcher",
    "MissionEngine": "app.application.mission_engine.engine",
    "MissionEngineError": "app.application.mission_engine.exceptions",
    "MissionNotFound": "app.application.mission_engine.exceptions",
    "MissionSchedule": "app.application.mission_engine.dto.mission_schedule",
    "MissionScheduler": "app.application.mission_engine.mission_scheduler",
    "MissionSlot": "app.application.mission_engine.mission_state",
    "MissionState": "app.application.mission_engine.mission_state",
    "MissionSummary": "app.application.mission_engine.dto.mission_summary",
    "MissionTransitionEvent": "app.application.mission_engine.mission_state",
    "MissionValidator": "app.application.mission_engine.mission_validator",
    "SchedulingError": "app.application.mission_engine.exceptions",
    "SchedulingPolicy": "app.application.mission_engine.policies.scheduling_policy",
    "V1MissionAdapter": (
        "app.application.mission_engine.adapters.v1_mission_adapter"
    ),
    "V1MissionView": (
        "app.application.mission_engine.adapters.v1_mission_adapter"
    ),
    "WorkloadExceeded": "app.application.mission_engine.exceptions",
    "WorkloadPolicy": "app.application.mission_engine.policies.workload_policy",
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
