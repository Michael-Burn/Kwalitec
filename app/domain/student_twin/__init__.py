"""Version 2 Student Digital Twin domain package.

Deterministic, evidence-driven learner educational state.
No teaching. No curriculum storage. No Flask / SQLAlchemy / persistence.

Prefer explicit imports such as
``app.domain.student_twin.digital_twin.DigitalTwin``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ConfidenceBand",
    "ConfidenceState",
    "DigitalTwin",
    "EvidenceEvent",
    "EvidenceProfile",
    "EvidenceType",
    "KnowledgeState",
    "Learner",
    "LearningHistory",
    "LearningVelocity",
    "MasteryState",
    "NEGATIVE_OUTCOMES",
    "NEUTRAL_OUTCOMES",
    "POSITIVE_OUTCOMES",
    "ReadinessState",
    "Recommendation",
    "RecommendationKind",
    "RecommendationState",
    "RetentionState",
    "TopicConfidenceRecord",
    "TopicKnowledgeRecord",
    "TopicMasteryRecord",
    "TopicRetentionRecord",
    "TwinIdentity",
    "TwinSnapshot",
    "TwinVersion",
    "WeaknessItem",
    "WeaknessKind",
    "WeaknessProfile",
    "confidence_band_from_score",
    "confidence_score_from_band",
    "resolve_confidence_band",
    "resolve_evidence_type",
]

_EXPORT_MODULES = {
    "ConfidenceBand": "app.domain.student_twin.confidence_band",
    "ConfidenceState": "app.domain.student_twin.confidence_state",
    "DigitalTwin": "app.domain.student_twin.digital_twin",
    "EvidenceEvent": "app.domain.student_twin.evidence_event",
    "EvidenceProfile": "app.domain.student_twin.evidence_profile",
    "EvidenceType": "app.domain.student_twin.evidence_type",
    "KnowledgeState": "app.domain.student_twin.knowledge_state",
    "Learner": "app.domain.student_twin.learner",
    "LearningHistory": "app.domain.student_twin.learning_history",
    "LearningVelocity": "app.domain.student_twin.learning_velocity",
    "MasteryState": "app.domain.student_twin.mastery_state",
    "NEGATIVE_OUTCOMES": "app.domain.student_twin.evidence_type",
    "NEUTRAL_OUTCOMES": "app.domain.student_twin.evidence_type",
    "POSITIVE_OUTCOMES": "app.domain.student_twin.evidence_type",
    "ReadinessState": "app.domain.student_twin.readiness_state",
    "Recommendation": "app.domain.student_twin.recommendation_state",
    "RecommendationKind": "app.domain.student_twin.recommendation_state",
    "RecommendationState": "app.domain.student_twin.recommendation_state",
    "RetentionState": "app.domain.student_twin.retention_state",
    "TopicConfidenceRecord": "app.domain.student_twin.confidence_state",
    "TopicKnowledgeRecord": "app.domain.student_twin.knowledge_state",
    "TopicMasteryRecord": "app.domain.student_twin.mastery_state",
    "TopicRetentionRecord": "app.domain.student_twin.retention_state",
    "TwinIdentity": "app.domain.student_twin.twin_identity",
    "TwinSnapshot": "app.domain.student_twin.twin_snapshot",
    "TwinVersion": "app.domain.student_twin.twin_version",
    "WeaknessItem": "app.domain.student_twin.weakness_profile",
    "WeaknessKind": "app.domain.student_twin.weakness_profile",
    "WeaknessProfile": "app.domain.student_twin.weakness_profile",
    "confidence_band_from_score": "app.domain.student_twin.confidence_band",
    "confidence_score_from_band": "app.domain.student_twin.confidence_band",
    "resolve_confidence_band": "app.domain.student_twin.confidence_band",
    "resolve_evidence_type": "app.domain.student_twin.evidence_type",
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
