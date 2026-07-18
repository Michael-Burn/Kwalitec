"""Version 2 Mission Engine 2.0 — application-layer orchestration.

Composes Daily Mission commitments from Version 2 educational services.
Owns mission creation, scheduling, lifecycle, and dashboard-ready DTOs.
Does NOT own educational reasoning.

Framework-independent: no Flask, SQLAlchemy, UI, migrations, or feature flags.
Depends only on injected ports (Mission Adapter contracts, Journey Engine,
Session Runtime, Curriculum Navigation).

Prefer explicit imports such as
``app.application.mission_engine_v2.engine.MissionEngineV2``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActiveMissionExists",
    "CurriculumNavigationPort",
    "DailyMission",
    "DispatchAction",
    "DispatchError",
    "DispatchPolicy",
    "DuplicateMission",
    "InvalidJourneyReference",
    "InvalidMissionState",
    "InvalidSessionReference",
    "JourneyEnginePort",
    "LifecyclePolicy",
    "MissionAlreadyArchived",
    "MissionAlreadyCompleted",
    "MissionCard",
    "MissionCoordinator",
    "MissionDashboard",
    "MissionDispatcher",
    "MissionEngineV2",
    "MissionEngineV2Error",
    "MissionExecution",
    "MissionFactory",
    "MissionFactoryError",
    "MissionNotFound",
    "MissionScheduler",
    "MissionSlot",
    "MissionState",
    "MissionTimeline",
    "MissionTransitionEvent",
    "MissionValidator",
    "SchedulingError",
    "SchedulingPolicy",
    "SessionRuntimePort",
    "TopicUnavailable",
    "WorkloadAssessment",
    "WorkloadBalancer",
    "WorkloadExceeded",
    "WorkloadPolicy",
]

_EXPORT_MODULES = {
    "ActiveMissionExists": "app.application.mission_engine_v2.exceptions",
    "CurriculumNavigationPort": (
        "app.application.mission_engine_v2.ports.curriculum_navigation_port"
    ),
    "DailyMission": "app.application.mission_engine_v2.dto.daily_mission",
    "DispatchAction": "app.application.mission_engine_v2.lifecycle",
    "DispatchError": "app.application.mission_engine_v2.exceptions",
    "DispatchPolicy": "app.application.mission_engine_v2.policies.dispatch_policy",
    "DuplicateMission": "app.application.mission_engine_v2.exceptions",
    "InvalidJourneyReference": "app.application.mission_engine_v2.exceptions",
    "InvalidMissionState": "app.application.mission_engine_v2.exceptions",
    "InvalidSessionReference": "app.application.mission_engine_v2.exceptions",
    "JourneyEnginePort": (
        "app.application.mission_engine_v2.ports.journey_engine_port"
    ),
    "LifecyclePolicy": "app.application.mission_engine_v2.policies.lifecycle_policy",
    "MissionAlreadyArchived": "app.application.mission_engine_v2.exceptions",
    "MissionAlreadyCompleted": "app.application.mission_engine_v2.exceptions",
    "MissionCard": "app.application.mission_engine_v2.dto.mission_card",
    "MissionCoordinator": "app.application.mission_engine_v2.coordinator",
    "MissionDashboard": "app.application.mission_engine_v2.dto.mission_dashboard",
    "MissionDispatcher": "app.application.mission_engine_v2.dispatcher",
    "MissionEngineV2": "app.application.mission_engine_v2.engine",
    "MissionEngineV2Error": "app.application.mission_engine_v2.exceptions",
    "MissionExecution": "app.application.mission_engine_v2.dto.mission_execution",
    "MissionFactory": "app.application.mission_engine_v2.mission_factory",
    "MissionFactoryError": "app.application.mission_engine_v2.exceptions",
    "MissionNotFound": "app.application.mission_engine_v2.exceptions",
    "MissionScheduler": "app.application.mission_engine_v2.scheduler",
    "MissionSlot": "app.application.mission_engine_v2.lifecycle",
    "MissionState": "app.application.mission_engine_v2.lifecycle",
    "MissionTimeline": "app.application.mission_engine_v2.dto.mission_timeline",
    "MissionTransitionEvent": "app.application.mission_engine_v2.lifecycle",
    "MissionValidator": "app.application.mission_engine_v2.validator",
    "SchedulingError": "app.application.mission_engine_v2.exceptions",
    "SchedulingPolicy": (
        "app.application.mission_engine_v2.policies.scheduling_policy"
    ),
    "SessionRuntimePort": (
        "app.application.mission_engine_v2.ports.session_runtime_port"
    ),
    "TopicUnavailable": "app.application.mission_engine_v2.exceptions",
    "WorkloadAssessment": "app.application.mission_engine_v2.workload_balancer",
    "WorkloadBalancer": "app.application.mission_engine_v2.workload_balancer",
    "WorkloadExceeded": "app.application.mission_engine_v2.exceptions",
    "WorkloadPolicy": "app.application.mission_engine_v2.policies.workload_policy",
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
