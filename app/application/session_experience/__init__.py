"""Version 2 Learning Session Experience — application layer.

Focused study workflow / projection over Session Runtime, Activity Engine,
Mission, Twin, and Adaptive Decision ports.

Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.
Does not import or modify educational engine packages.

Prefer explicit imports such as
``app.application.session_experience.facade.SessionExperienceService``.
"""

from __future__ import annotations

from typing import Any

from app.application.session_experience.facade import SessionExperienceService

__all__ = [
    "ActivityEnginePort",
    "ActivityError",
    "ActivityService",
    "ActivitySnapshot",
    "AdaptiveDecisionPort",
    "BeginSessionActionSnapshot",
    "CompletionError",
    "CompletionService",
    "CompletionSnapshot",
    "DiagnosticReport",
    "Diagnostics",
    "MissionPort",
    "NavigationError",
    "OverviewError",
    "OverviewSnapshot",
    "PORT_NAMES",
    "PolicyViolation",
    "PortUnavailable",
    "ProgressError",
    "ProgressService",
    "ProgressSnapshot",
    "ProjectionError",
    "ReflectionError",
    "ReflectionService",
    "ReflectionSnapshot",
    "ReturnHomeActionSnapshot",
    "SESSION_EXPERIENCE_VERSION",
    "SessionExperienceError",
    "SessionExperienceService",
    "SessionFlowSnapshot",
    "SessionNotFound",
    "SessionOwnershipError",
    "SessionRuntimePort",
    "SessionService",
    "StudentTwinPort",
    "WorkspaceNotFound",
]

_EXPORT_MODULES = {
    "ActivityEnginePort": (
        "app.application.session_experience.ports.activity_engine_port"
    ),
    "ActivityError": "app.application.session_experience.exceptions",
    "ActivityService": "app.application.session_experience.activity_service",
    "ActivitySnapshot": (
        "app.application.session_experience.dto.activity_snapshot"
    ),
    "AdaptiveDecisionPort": (
        "app.application.session_experience.ports.adaptive_decision_port"
    ),
    "BeginSessionActionSnapshot": (
        "app.application.session_experience.dto.overview_snapshot"
    ),
    "CompletionError": "app.application.session_experience.exceptions",
    "CompletionService": (
        "app.application.session_experience.completion_service"
    ),
    "CompletionSnapshot": (
        "app.application.session_experience.dto.completion_snapshot"
    ),
    "DiagnosticReport": "app.application.session_experience.diagnostics",
    "Diagnostics": "app.application.session_experience.diagnostics",
    "MissionPort": "app.application.session_experience.ports.mission_port",
    "NavigationError": "app.application.session_experience.exceptions",
    "OverviewError": "app.application.session_experience.exceptions",
    "OverviewSnapshot": (
        "app.application.session_experience.dto.overview_snapshot"
    ),
    "PORT_NAMES": "app.application.session_experience.ports",
    "PolicyViolation": "app.application.session_experience.exceptions",
    "PortUnavailable": "app.application.session_experience.exceptions",
    "ProgressError": "app.application.session_experience.exceptions",
    "ProgressService": "app.application.session_experience.progress_service",
    "ProgressSnapshot": (
        "app.application.session_experience.dto.progress_snapshot"
    ),
    "ProjectionError": "app.application.session_experience.exceptions",
    "ReflectionError": "app.application.session_experience.exceptions",
    "ReflectionService": (
        "app.application.session_experience.reflection_service"
    ),
    "ReflectionSnapshot": (
        "app.application.session_experience.dto.reflection_snapshot"
    ),
    "ReturnHomeActionSnapshot": (
        "app.application.session_experience.dto.completion_snapshot"
    ),
    "SESSION_EXPERIENCE_VERSION": (
        "app.application.session_experience.diagnostics"
    ),
    "SessionExperienceError": "app.application.session_experience.exceptions",
    "SessionExperienceService": "app.application.session_experience.facade",
    "SessionFlowSnapshot": "app.application.session_experience.facade",
    "SessionNotFound": "app.application.session_experience.exceptions",
    "SessionOwnershipError": "app.application.session_experience.exceptions",
    "SessionRuntimePort": (
        "app.application.session_experience.ports.session_runtime_port"
    ),
    "SessionService": "app.application.session_experience.session_service",
    "StudentTwinPort": (
        "app.application.session_experience.ports.student_twin_port"
    ),
    "WorkspaceNotFound": "app.application.session_experience.exceptions",
}


def __getattr__(name: str) -> Any:
    if name == "SessionExperienceService":
        return SessionExperienceService
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
