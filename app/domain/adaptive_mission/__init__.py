"""Adaptive Mission Engine (AME-001) domain package.

Transforms educational decisions already produced by the Student Digital Twin,
Educational Reasoning Engine, and Learning Graph into one actionable daily
mission. This context never performs educational reasoning itself.

No LLM. Curriculum evidence enters only via CurriculumRetrievalService at the
application layer.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActivityType",
    "AdaptiveMission",
    "Mission",
    "MissionActivity",
    "MissionCandidate",
    "MissionCompletion",
    "MissionObjective",
    "MissionOutcome",
    "MissionPlan",
    "MissionPriority",
    "MissionPriorityScore",
    "MissionProgress",
    "MissionReason",
    "MissionSchedule",
    "MissionStatus",
    "MissionStep",
    "MissionValidationIssue",
    "MissionValidationResult",
    "PrioritisationResult",
    "ValidationSeverity",
    "construct_mission",
    "prioritise_candidates",
    "validate_mission",
]

_EXPORT_MODULES = {
    "ActivityType": "app.domain.adaptive_mission.mission_step",
    "MissionActivity": "app.domain.adaptive_mission.mission_step",
    "MissionStep": "app.domain.adaptive_mission.mission_step",
    "MissionPriority": "app.domain.adaptive_mission.mission_priority",
    "MissionPriorityScore": "app.domain.adaptive_mission.mission_priority",
    "MissionObjective": "app.domain.adaptive_mission.mission_objective",
    "MissionPlan": "app.domain.adaptive_mission.mission_plan",
    "MissionSchedule": "app.domain.adaptive_mission.mission_schedule",
    "MissionReason": "app.domain.adaptive_mission.mission_reason",
    "MissionOutcome": "app.domain.adaptive_mission.mission_outcome",
    "MissionProgress": "app.domain.adaptive_mission.mission_progress",
    "MissionCompletion": "app.domain.adaptive_mission.mission_completion",
    "MissionStatus": "app.domain.adaptive_mission.mission",
    "Mission": "app.domain.adaptive_mission.mission",
    "AdaptiveMission": "app.domain.adaptive_mission.adaptive_mission",
    "MissionCandidate": "app.domain.adaptive_mission.prioritisation",
    "PrioritisationResult": "app.domain.adaptive_mission.prioritisation",
    "prioritise_candidates": "app.domain.adaptive_mission.prioritisation",
    "construct_mission": "app.domain.adaptive_mission.construction",
    "MissionValidationIssue": "app.domain.adaptive_mission.validation",
    "MissionValidationResult": "app.domain.adaptive_mission.validation",
    "ValidationSeverity": "app.domain.adaptive_mission.validation",
    "validate_mission": "app.domain.adaptive_mission.validation",
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
