"""Educational Composition Layer — sole public entry to the Educational Core.

Coordinates Curriculum Graph, Blueprint Engine, Journey Engine, Session
Runtime, Activity Engine, Mission Engine, and Mission Adapter via ports.

Owns NO educational rules. Framework-independent: no Flask, SQLAlchemy,
UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.education_platform.platform.EducationPlatform``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActivityPort",
    "BlueprintPort",
    "CompositionError",
    "CompositionRoot",
    "CurriculumPort",
    "DEPENDENCY_CHAIN",
    "DependencyError",
    "DependencyRegistry",
    "DiagnosticReport",
    "Diagnostics",
    "EducationPlatform",
    "EducationPlatformError",
    "EducationRequest",
    "EducationResponse",
    "GeneratedMission",
    "GeneratedSession",
    "HealthService",
    "JourneyPort",
    "MissionPort",
    "OrchestrationError",
    "OrchestrationPolicy",
    "OrchestrationService",
    "PlatformContext",
    "PlatformSnapshot",
    "PlatformValidationResult",
    "PlatformValidator",
    "PortUnavailable",
    "SessionPort",
    "SubjectPlan",
    "ValidationError",
    "ValidationPolicy",
    "WorkflowError",
    "WorkflowExecutor",
    "WorkflowResult",
]

_EXPORT_MODULES = {
    "ActivityPort": "app.application.education_platform.ports.activity_port",
    "BlueprintPort": "app.application.education_platform.ports.blueprint_port",
    "CompositionError": "app.application.education_platform.exceptions",
    "CompositionRoot": "app.application.education_platform.composition_root",
    "CurriculumPort": "app.application.education_platform.ports.curriculum_port",
    "DEPENDENCY_CHAIN": (
        "app.application.education_platform.policies.orchestration_policy"
    ),
    "DependencyError": "app.application.education_platform.exceptions",
    "DependencyRegistry": (
        "app.application.education_platform.dependency_registry"
    ),
    "DiagnosticReport": "app.application.education_platform.diagnostics",
    "Diagnostics": "app.application.education_platform.diagnostics",
    "EducationPlatform": "app.application.education_platform.platform",
    "EducationPlatformError": "app.application.education_platform.exceptions",
    "EducationRequest": (
        "app.application.education_platform.dto.education_request"
    ),
    "EducationResponse": (
        "app.application.education_platform.dto.education_response"
    ),
    "GeneratedMission": (
        "app.application.education_platform.dto.generated_mission"
    ),
    "GeneratedSession": (
        "app.application.education_platform.dto.generated_session"
    ),
    "HealthService": "app.application.education_platform.health_service",
    "JourneyPort": "app.application.education_platform.ports.journey_port",
    "MissionPort": "app.application.education_platform.ports.mission_port",
    "OrchestrationError": "app.application.education_platform.exceptions",
    "OrchestrationPolicy": (
        "app.application.education_platform.policies.orchestration_policy"
    ),
    "OrchestrationService": (
        "app.application.education_platform.orchestration_service"
    ),
    "PlatformContext": "app.application.education_platform.platform_context",
    "PlatformSnapshot": (
        "app.application.education_platform.dto.platform_snapshot"
    ),
    "PlatformValidationResult": (
        "app.application.education_platform.platform_validator"
    ),
    "PlatformValidator": (
        "app.application.education_platform.platform_validator"
    ),
    "PortUnavailable": "app.application.education_platform.exceptions",
    "SessionPort": "app.application.education_platform.ports.session_port",
    "SubjectPlan": "app.application.education_platform.dto.subject_plan",
    "ValidationError": "app.application.education_platform.exceptions",
    "ValidationPolicy": (
        "app.application.education_platform.policies.validation_policy"
    ),
    "WorkflowError": "app.application.education_platform.exceptions",
    "WorkflowExecutor": "app.application.education_platform.workflow_executor",
    "WorkflowResult": "app.application.education_platform.dto.workflow_result",
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
