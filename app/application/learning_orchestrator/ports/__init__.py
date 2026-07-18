"""Learning Orchestrator ports — Protocol contracts only."""

from __future__ import annotations

from typing import Any

__all__ = [
    "AdaptiveLearningPort",
    "AnalyticsPort",
    "EvidencePort",
    "MissionPort",
    "TwinPort",
]

_EXPORT_MODULES = {
    "AdaptiveLearningPort": (
        "app.application.learning_orchestrator.ports.adaptive_learning_port"
    ),
    "AnalyticsPort": (
        "app.application.learning_orchestrator.ports.analytics_port"
    ),
    "EvidencePort": (
        "app.application.learning_orchestrator.ports.evidence_port"
    ),
    "MissionPort": (
        "app.application.learning_orchestrator.ports.mission_port"
    ),
    "TwinPort": "app.application.learning_orchestrator.ports.twin_port",
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
