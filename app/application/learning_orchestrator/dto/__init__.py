"""Learning Orchestrator DTOs — immutable request/response envelopes."""

from __future__ import annotations

from typing import Any

__all__ = [
    "ExecutionSummary",
    "OrchestrationRequest",
    "OrchestrationResponse",
    "PipelineSnapshot",
]

_EXPORT_MODULES = {
    "ExecutionSummary": (
        "app.application.learning_orchestrator.dto.execution_summary"
    ),
    "OrchestrationRequest": (
        "app.application.learning_orchestrator.dto.orchestration_request"
    ),
    "OrchestrationResponse": (
        "app.application.learning_orchestrator.dto.orchestration_response"
    ),
    "PipelineSnapshot": (
        "app.application.learning_orchestrator.dto.pipeline_snapshot"
    ),
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
