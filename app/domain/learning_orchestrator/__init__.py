"""Version 2 Learning Orchestrator — domain package.

Coordination vocabulary for live learner events. Owns no educational
rules, Twin math, or curriculum mutations.

Prefer explicit imports such as
``app.domain.learning_orchestrator.orchestration_event.OrchestrationEvent``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CANONICAL_PIPELINE",
    "STAGE_PORT_NAMES",
    "OrchestrationContext",
    "OrchestrationEvent",
    "OrchestrationEventType",
    "OrchestrationResult",
    "OrchestrationSnapshot",
    "OrchestrationState",
    "PipelineResult",
    "PipelineStageName",
    "StageOutcome",
]

_EXPORT_MODULES = {
    "CANONICAL_PIPELINE": "app.domain.learning_orchestrator.pipeline_stage",
    "STAGE_PORT_NAMES": "app.domain.learning_orchestrator.pipeline_stage",
    "OrchestrationContext": (
        "app.domain.learning_orchestrator.orchestration_context"
    ),
    "OrchestrationEvent": (
        "app.domain.learning_orchestrator.orchestration_event"
    ),
    "OrchestrationEventType": (
        "app.domain.learning_orchestrator.orchestration_event"
    ),
    "OrchestrationResult": (
        "app.domain.learning_orchestrator.orchestration_result"
    ),
    "OrchestrationSnapshot": (
        "app.domain.learning_orchestrator.orchestration_snapshot"
    ),
    "OrchestrationState": (
        "app.domain.learning_orchestrator.orchestration_state"
    ),
    "PipelineResult": "app.domain.learning_orchestrator.pipeline_result",
    "PipelineStageName": "app.domain.learning_orchestrator.pipeline_stage",
    "StageOutcome": "app.domain.learning_orchestrator.pipeline_stage",
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
