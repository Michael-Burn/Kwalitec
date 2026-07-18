"""Learning Orchestrator policies — stateless coordination rules."""

from __future__ import annotations

from typing import Any

__all__ = [
    "DEPENDENCY_CHAIN",
    "PORT_NAMES",
    "OrchestrationPolicy",
    "PipelinePolicy",
    "RetryPolicy",
]

_EXPORT_MODULES = {
    "DEPENDENCY_CHAIN": (
        "app.application.learning_orchestrator.policies.orchestration_policy"
    ),
    "PORT_NAMES": (
        "app.application.learning_orchestrator.policies.orchestration_policy"
    ),
    "OrchestrationPolicy": (
        "app.application.learning_orchestrator.policies.orchestration_policy"
    ),
    "PipelinePolicy": (
        "app.application.learning_orchestrator.policies.pipeline_policy"
    ),
    "RetryPolicy": (
        "app.application.learning_orchestrator.policies.retry_policy"
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
