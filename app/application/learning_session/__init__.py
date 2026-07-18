"""Version 2 Learning Session Runtime — application-layer execution.

Manages a student's interaction with an individual Learning Session.
Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.learning_session.runtime.LearningSessionRuntime``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActivityScheduler",
    "CompletionEvaluator",
    "CompletionPolicy",
    "CompletionResult",
    "EvidenceCollector",
    "EvidenceCollectionError",
    "EvidenceSummary",
    "InvalidSessionState",
    "LearningSessionPlan",
    "LearningSessionPlanner",
    "LearningSessionRuntime",
    "LearningSessionRuntimeError",
    "LifecycleManager",
    "LifecycleResult",
    "NextAction",
    "PlanningError",
    "PlanningPolicy",
    "ReflectionManager",
    "ReflectionPolicy",
    "ReflectionRequired",
    "ReflectionSummary",
    "RuntimePhase",
    "RuntimeSnapshot",
    "RuntimeTransitionEvent",
    "SchedulingPolicy",
    "SessionAlreadyArchived",
    "SessionAlreadyCompleted",
    "SessionHandle",
    "SessionNotFound",
]

_EXPORT_MODULES = {
    "ActivityScheduler": "app.application.learning_session.activity_scheduler",
    "CompletionEvaluator": "app.application.learning_session.completion_evaluator",
    "CompletionPolicy": (
        "app.application.learning_session.policies.completion_policy"
    ),
    "CompletionResult": "app.application.learning_session.dto.completion_result",
    "EvidenceCollector": "app.application.learning_session.evidence_collector",
    "EvidenceCollectionError": "app.application.learning_session.exceptions",
    "EvidenceSummary": "app.application.learning_session.dto.evidence_summary",
    "InvalidSessionState": "app.application.learning_session.exceptions",
    "LearningSessionPlan": (
        "app.application.learning_session.dto.learning_session_plan"
    ),
    "LearningSessionPlanner": "app.application.learning_session.planner",
    "LearningSessionRuntime": "app.application.learning_session.runtime",
    "LearningSessionRuntimeError": "app.application.learning_session.exceptions",
    "LifecycleManager": "app.application.learning_session.lifecycle_manager",
    "LifecycleResult": "app.application.learning_session.lifecycle_manager",
    "NextAction": "app.application.learning_session.policies.scheduling_policy",
    "PlanningError": "app.application.learning_session.exceptions",
    "PlanningPolicy": "app.application.learning_session.policies.planning_policy",
    "ReflectionManager": "app.application.learning_session.reflection_manager",
    "ReflectionPolicy": (
        "app.application.learning_session.policies.reflection_policy"
    ),
    "ReflectionRequired": "app.application.learning_session.exceptions",
    "ReflectionSummary": "app.application.learning_session.dto.reflection_summary",
    "RuntimePhase": "app.application.learning_session.runtime_phase",
    "RuntimeSnapshot": "app.application.learning_session.dto.runtime_snapshot",
    "RuntimeTransitionEvent": "app.application.learning_session.runtime_phase",
    "SchedulingPolicy": (
        "app.application.learning_session.policies.scheduling_policy"
    ),
    "SessionAlreadyArchived": "app.application.learning_session.exceptions",
    "SessionAlreadyCompleted": "app.application.learning_session.exceptions",
    "SessionHandle": "app.application.learning_session.runtime",
    "SessionNotFound": "app.application.learning_session.exceptions",
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
