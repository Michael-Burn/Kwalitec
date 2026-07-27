"""Student Digital Twin (SDT-001) domain package.

Canonical representation of the learner — sole source of truth for educational
state. Facts (observations) are append-only; inferences are reproducible via
StudentReasoningService.

Curriculum evidence is consumed only through CurriculumRetrievalService at the
application layer. No LLM. No AI inference.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "REASONING_VERSION",
    "ConfidenceBand",
    "ConfidenceState",
    "GapSeverity",
    "Goal",
    "GoalStatus",
    "KnowledgeGap",
    "LearningState",
    "MasteryMap",
    "MasteryRecord",
    "MasteryTrend",
    "Observation",
    "ObservationKind",
    "Prediction",
    "PredictionKind",
    "Recommendation",
    "RecommendationPriority",
    "ReasoningRecord",
    "ReasoningStep",
    "Student",
    "StudentDigitalTwin",
    "Timeline",
    "TimelineEvent",
    "TimelineEventKind",
    "confidence_band_from_score",
]

_EXPORT_MODULES = {
    "Student": "app.domain.student_digital_twin.student",
    "Observation": "app.domain.student_digital_twin.observation",
    "ObservationKind": "app.domain.student_digital_twin.observation",
    "LearningState": "app.domain.student_digital_twin.learning_state",
    "MasteryRecord": "app.domain.student_digital_twin.mastery",
    "MasteryMap": "app.domain.student_digital_twin.mastery",
    "MasteryTrend": "app.domain.student_digital_twin.mastery",
    "KnowledgeGap": "app.domain.student_digital_twin.knowledge_gap",
    "GapSeverity": "app.domain.student_digital_twin.knowledge_gap",
    "ConfidenceState": "app.domain.student_digital_twin.confidence",
    "ConfidenceBand": "app.domain.student_digital_twin.confidence",
    "confidence_band_from_score": "app.domain.student_digital_twin.confidence",
    "Goal": "app.domain.student_digital_twin.goal",
    "GoalStatus": "app.domain.student_digital_twin.goal",
    "Recommendation": "app.domain.student_digital_twin.recommendation",
    "RecommendationPriority": "app.domain.student_digital_twin.recommendation",
    "Prediction": "app.domain.student_digital_twin.prediction",
    "PredictionKind": "app.domain.student_digital_twin.prediction",
    "Timeline": "app.domain.student_digital_twin.timeline",
    "TimelineEvent": "app.domain.student_digital_twin.timeline",
    "TimelineEventKind": "app.domain.student_digital_twin.timeline",
    "ReasoningRecord": "app.domain.student_digital_twin.reasoning",
    "ReasoningStep": "app.domain.student_digital_twin.reasoning",
    "REASONING_VERSION": "app.domain.student_digital_twin.reasoning",
    "StudentDigitalTwin": "app.domain.student_digital_twin.student_digital_twin",
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
