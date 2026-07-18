"""Learning Orchestrator — live learner event coordination layer.

Coordinates Evidence → Twin → Adaptive Decision → Mission → Analytics
via injected ports. Owns NO educational rules. Never mutates curriculum.
Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.learning_orchestrator.learning_orchestrator.LearningOrchestrator``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "AdaptiveLearningPort",
    "AnalyticsPipeline",
    "AnalyticsPort",
    "DEPENDENCY_CHAIN",
    "DecisionPipeline",
    "DependencyError",
    "DiagnosticReport",
    "Diagnostics",
    "EventDispatchError",
    "EventDispatcher",
    "EvidencePipeline",
    "EvidencePort",
    "ExecutionSummary",
    "HealthService",
    "LearningOrchestrator",
    "LearningOrchestratorError",
    "MissionPipeline",
    "MissionPort",
    "OrchestrationError",
    "OrchestrationPolicy",
    "OrchestrationRequest",
    "OrchestrationResponse",
    "PORT_NAMES",
    "PipelineEngine",
    "PipelineError",
    "PipelinePolicy",
    "PipelineSnapshot",
    "PolicyViolation",
    "PortError",
    "PortUnavailable",
    "RetryPolicy",
    "TwinPipeline",
    "TwinPort",
]

_EXPORT_MODULES = {
    "AdaptiveLearningPort": (
        "app.application.learning_orchestrator.ports.adaptive_learning_port"
    ),
    "AnalyticsPipeline": (
        "app.application.learning_orchestrator.analytics_pipeline"
    ),
    "AnalyticsPort": (
        "app.application.learning_orchestrator.ports.analytics_port"
    ),
    "DEPENDENCY_CHAIN": (
        "app.application.learning_orchestrator.policies.orchestration_policy"
    ),
    "DecisionPipeline": (
        "app.application.learning_orchestrator.decision_pipeline"
    ),
    "DependencyError": "app.application.learning_orchestrator.exceptions",
    "DiagnosticReport": "app.application.learning_orchestrator.diagnostics",
    "Diagnostics": "app.application.learning_orchestrator.diagnostics",
    "EventDispatchError": "app.application.learning_orchestrator.exceptions",
    "EventDispatcher": (
        "app.application.learning_orchestrator.event_dispatcher"
    ),
    "EvidencePipeline": (
        "app.application.learning_orchestrator.evidence_pipeline"
    ),
    "EvidencePort": (
        "app.application.learning_orchestrator.ports.evidence_port"
    ),
    "ExecutionSummary": (
        "app.application.learning_orchestrator.dto.execution_summary"
    ),
    "HealthService": "app.application.learning_orchestrator.health_service",
    "LearningOrchestrator": (
        "app.application.learning_orchestrator.learning_orchestrator"
    ),
    "LearningOrchestratorError": (
        "app.application.learning_orchestrator.exceptions"
    ),
    "MissionPipeline": (
        "app.application.learning_orchestrator.mission_pipeline"
    ),
    "MissionPort": (
        "app.application.learning_orchestrator.ports.mission_port"
    ),
    "OrchestrationError": "app.application.learning_orchestrator.exceptions",
    "OrchestrationPolicy": (
        "app.application.learning_orchestrator.policies.orchestration_policy"
    ),
    "OrchestrationRequest": (
        "app.application.learning_orchestrator.dto.orchestration_request"
    ),
    "OrchestrationResponse": (
        "app.application.learning_orchestrator.dto.orchestration_response"
    ),
    "PORT_NAMES": (
        "app.application.learning_orchestrator.policies.orchestration_policy"
    ),
    "PipelineEngine": "app.application.learning_orchestrator.pipeline_engine",
    "PipelineError": "app.application.learning_orchestrator.exceptions",
    "PipelinePolicy": (
        "app.application.learning_orchestrator.policies.pipeline_policy"
    ),
    "PipelineSnapshot": (
        "app.application.learning_orchestrator.dto.pipeline_snapshot"
    ),
    "PolicyViolation": "app.application.learning_orchestrator.exceptions",
    "PortError": "app.application.learning_orchestrator.exceptions",
    "PortUnavailable": "app.application.learning_orchestrator.exceptions",
    "RetryPolicy": (
        "app.application.learning_orchestrator.policies.retry_policy"
    ),
    "TwinPipeline": "app.application.learning_orchestrator.twin_pipeline",
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
