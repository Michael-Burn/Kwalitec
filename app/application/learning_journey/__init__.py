"""Version 2 Learning Journey Engine — application-layer orchestration.

Coordinates the Learning Journey domain into deterministic educational
progression. Framework-independent: no Flask, SQLAlchemy, UI, migrations,
or feature flags.

Prefer explicit imports such as
``app.application.learning_journey.engine.LearningJourneyEngine``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CompletionEvaluation",
    "CompletionManager",
    "CompletionPolicy",
    "EvidenceSummary",
    "InvalidJourneyState",
    "InvalidProgression",
    "JourneyAlreadyCompleted",
    "JourneyNotFound",
    "JourneySnapshot",
    "LearningJourneyCoordinator",
    "LearningJourneyEngine",
    "LearningJourneyEngineError",
    "ProgressionManager",
    "ProgressionPolicy",
    "ProgressionResult",
    "RecommendationBuilder",
    "RecommendationDecision",
    "RecommendationPolicy",
    "RecommendationResult",
    "ReflectionSummary",
    "SessionOrderingViolation",
    "SessionPlan",
    "SessionSelector",
]

_EXPORT_MODULES = {
    "CompletionEvaluation": (
        "app.application.learning_journey.policies.completion_policy"
    ),
    "CompletionManager": "app.application.learning_journey.completion_manager",
    "CompletionPolicy": (
        "app.application.learning_journey.policies.completion_policy"
    ),
    "EvidenceSummary": "app.application.learning_journey.dto.journey_snapshot",
    "InvalidJourneyState": "app.application.learning_journey.exceptions",
    "InvalidProgression": "app.application.learning_journey.exceptions",
    "JourneyAlreadyCompleted": "app.application.learning_journey.exceptions",
    "JourneyNotFound": "app.application.learning_journey.exceptions",
    "JourneySnapshot": "app.application.learning_journey.dto.journey_snapshot",
    "LearningJourneyCoordinator": "app.application.learning_journey.coordinator",
    "LearningJourneyEngine": "app.application.learning_journey.engine",
    "LearningJourneyEngineError": "app.application.learning_journey.exceptions",
    "ProgressionManager": "app.application.learning_journey.progression_manager",
    "ProgressionPolicy": (
        "app.application.learning_journey.policies.progression_policy"
    ),
    "ProgressionResult": "app.application.learning_journey.dto.progression_result",
    "RecommendationBuilder": (
        "app.application.learning_journey.recommendation_builder"
    ),
    "RecommendationDecision": (
        "app.application.learning_journey.policies.recommendation_policy"
    ),
    "RecommendationPolicy": (
        "app.application.learning_journey.policies.recommendation_policy"
    ),
    "RecommendationResult": (
        "app.application.learning_journey.dto.recommendation_result"
    ),
    "ReflectionSummary": "app.application.learning_journey.dto.journey_snapshot",
    "SessionOrderingViolation": "app.application.learning_journey.exceptions",
    "SessionPlan": "app.application.learning_journey.dto.session_plan",
    "SessionSelector": "app.application.learning_journey.session_selector",
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
