"""Version 2 Learning Journey domain package.

Pure educational domain objects implementing the V2-001 Learning Journey
architecture (``knowledge/version2/``). No Flask, SQLAlchemy, routes, or
persistence implementations.

Domain structure::

    learning_journey/
        entities/          LearningJourney aggregate and related entities
        value_objects/     JourneyState, SessionState, EffortEstimate, …
        services/          Progress calculation and validation
        interfaces/        Repository contract only

Prefer explicit imports such as
``app.domain.learning_journey.entities.learning_journey``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CompletionStatus",
    "ConsistencyPosture",
    "EffortEstimate",
    "EvidenceConfidencePosture",
    "JourneyEvidence",
    "JourneyHistory",
    "JourneyHistoryEntry",
    "JourneyHistoryEventType",
    "JourneyProgress",
    "JourneyProgressService",
    "JourneyRecommendation",
    "JourneyReflection",
    "JourneyState",
    "JourneyTransitionEvent",
    "JourneyValidationService",
    "LearningJourney",
    "LearningJourneyRepository",
    "LearningObjective",
    "LearningSession",
    "ObjectiveKind",
    "RecommendationCertainty",
    "RecommendationKind",
    "RecommendationLifecycle",
    "ReflectionConfidence",
    "ReflectionPosture",
    "SessionState",
    "SessionTransitionEvent",
    "ValidationIssue",
    "ValidationResult",
]

_EXPORT_MODULES = {
    "CompletionStatus": "app.domain.learning_journey.value_objects.completion_status",
    "ConsistencyPosture": "app.domain.learning_journey.entities.journey_progress",
    "EffortEstimate": "app.domain.learning_journey.value_objects.effort_estimate",
    "EvidenceConfidencePosture": (
        "app.domain.learning_journey.entities.journey_progress"
    ),
    "JourneyEvidence": "app.domain.learning_journey.entities.journey_evidence",
    "JourneyHistory": "app.domain.learning_journey.entities.journey_history",
    "JourneyHistoryEntry": "app.domain.learning_journey.entities.journey_history",
    "JourneyHistoryEventType": "app.domain.learning_journey.entities.journey_history",
    "JourneyProgress": "app.domain.learning_journey.entities.journey_progress",
    "JourneyProgressService": (
        "app.domain.learning_journey.services.journey_progress_service"
    ),
    "JourneyRecommendation": (
        "app.domain.learning_journey.entities.journey_recommendation"
    ),
    "JourneyReflection": "app.domain.learning_journey.entities.journey_reflection",
    "JourneyState": "app.domain.learning_journey.value_objects.journey_state",
    "JourneyTransitionEvent": "app.domain.learning_journey.value_objects.journey_state",
    "JourneyValidationService": (
        "app.domain.learning_journey.services.journey_validation_service"
    ),
    "LearningJourney": "app.domain.learning_journey.entities.learning_journey",
    "LearningJourneyRepository": (
        "app.domain.learning_journey.interfaces.learning_journey_repository"
    ),
    "LearningObjective": "app.domain.learning_journey.entities.learning_objective",
    "LearningSession": "app.domain.learning_journey.entities.learning_session",
    "ObjectiveKind": "app.domain.learning_journey.entities.learning_objective",
    "RecommendationCertainty": (
        "app.domain.learning_journey.entities.journey_recommendation"
    ),
    "RecommendationKind": (
        "app.domain.learning_journey.entities.journey_recommendation"
    ),
    "RecommendationLifecycle": (
        "app.domain.learning_journey.entities.journey_recommendation"
    ),
    "ReflectionConfidence": "app.domain.learning_journey.entities.journey_reflection",
    "ReflectionPosture": "app.domain.learning_journey.entities.journey_reflection",
    "SessionState": "app.domain.learning_journey.value_objects.session_state",
    "SessionTransitionEvent": "app.domain.learning_journey.value_objects.session_state",
    "ValidationIssue": (
        "app.domain.learning_journey.services.journey_validation_service"
    ),
    "ValidationResult": (
        "app.domain.learning_journey.services.journey_validation_service"
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
