"""Version 2 Learning Activity Engine — application-layer execution.

Owns activity sequencing, transitions, completion, evidence routing, and
reflection hooks inside a Learning Session.

Does NOT own session lifecycle, journey progression, or mission scheduling.
Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.learning_activity.engine.LearningActivityEngine``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActivityAlreadyCompleted",
    "ActivityAlreadySkipped",
    "ActivityHandle",
    "ActivityNotFound",
    "ActivityPlan",
    "ActivityPlanItem",
    "ActivityPlanner",
    "ActivityProgress",
    "ActivityResult",
    "ActivitySequence",
    "ActivitySnapshot",
    "ActivityState",
    "ActivityTransition",
    "ActivityTransitionEvent",
    "ActivityType",
    "ActivityValidator",
    "CompletionEvaluationError",
    "CompletionManager",
    "CompletionPolicy",
    "EvidenceRouteResult",
    "EvidenceRouter",
    "EvidenceRoutingError",
    "InvalidActivityState",
    "LearningActivity",
    "LearningActivityEngine",
    "LearningActivityEngineError",
    "PlanningError",
    "ProgressionManager",
    "ProgressionPolicy",
    "ReflectionRouteResult",
    "ReflectionRouter",
    "ReflectionRoutingError",
    "SequenceBuilder",
    "SequenceIntegrityError",
    "SequencingPolicy",
    "TransitionError",
    "TransitionManager",
    "TransitionPolicy",
    "TransitionResult",
    "ValidationError",
    "ValidationIssue",
    "ValidationResult",
]

_EXPORT_MODULES = {
    "ActivityAlreadyCompleted": "app.application.learning_activity.exceptions",
    "ActivityAlreadySkipped": "app.application.learning_activity.exceptions",
    "ActivityHandle": "app.application.learning_activity.engine",
    "ActivityNotFound": "app.application.learning_activity.exceptions",
    "ActivityPlan": "app.application.learning_activity.dto.activity_plan",
    "ActivityPlanItem": "app.application.learning_activity.dto.activity_plan",
    "ActivityPlanner": "app.application.learning_activity.planner",
    "ActivityProgress": "app.domain.learning_activity.entities.activity_progress",
    "ActivityResult": "app.application.learning_activity.dto.activity_result",
    "ActivitySequence": "app.application.learning_activity.dto.activity_sequence",
    "ActivitySnapshot": "app.application.learning_activity.dto.activity_snapshot",
    "ActivityState": "app.domain.learning_activity.value_objects.activity_state",
    "ActivityTransition": (
        "app.application.learning_activity.dto.activity_transition"
    ),
    "ActivityTransitionEvent": (
        "app.domain.learning_activity.value_objects.activity_state"
    ),
    "ActivityType": "app.domain.learning_activity.value_objects.activity_type",
    "ActivityValidator": "app.application.learning_activity.validator",
    "CompletionEvaluationError": "app.application.learning_activity.exceptions",
    "CompletionManager": "app.application.learning_activity.completion_manager",
    "CompletionPolicy": (
        "app.application.learning_activity.policies.completion_policy"
    ),
    "EvidenceRouteResult": "app.application.learning_activity.evidence_router",
    "EvidenceRouter": "app.application.learning_activity.evidence_router",
    "EvidenceRoutingError": "app.application.learning_activity.exceptions",
    "InvalidActivityState": "app.application.learning_activity.exceptions",
    "LearningActivity": (
        "app.domain.learning_activity.entities.learning_activity"
    ),
    "LearningActivityEngine": "app.application.learning_activity.engine",
    "LearningActivityEngineError": "app.application.learning_activity.exceptions",
    "PlanningError": "app.application.learning_activity.exceptions",
    "ProgressionManager": "app.application.learning_activity.progression_manager",
    "ProgressionPolicy": (
        "app.application.learning_activity.policies.progression_policy"
    ),
    "ReflectionRouteResult": "app.application.learning_activity.reflection_router",
    "ReflectionRouter": "app.application.learning_activity.reflection_router",
    "ReflectionRoutingError": "app.application.learning_activity.exceptions",
    "SequenceBuilder": "app.application.learning_activity.sequence_builder",
    "SequenceIntegrityError": "app.application.learning_activity.exceptions",
    "SequencingPolicy": (
        "app.application.learning_activity.policies.sequencing_policy"
    ),
    "TransitionError": "app.application.learning_activity.exceptions",
    "TransitionManager": "app.application.learning_activity.transition_manager",
    "TransitionPolicy": (
        "app.application.learning_activity.policies.transition_policy"
    ),
    "TransitionResult": "app.application.learning_activity.transition_manager",
    "ValidationError": "app.application.learning_activity.exceptions",
    "ValidationIssue": "app.application.learning_activity.validator",
    "ValidationResult": "app.application.learning_activity.validator",
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
