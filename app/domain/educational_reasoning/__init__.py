"""Educational Reasoning Engine (SDT-002).

Deterministic, explainable educational inference. Independent of UI, missions,
tutoring, and LLMs. Every educational decision that updates the Student Digital
Twin must flow through this engine.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ENGINE_VERSION",
    "ConfidenceAdjustmentRule",
    "ConsistencyRule",
    "CurriculumEvidenceBundle",
    "EducationalDecision",
    "EducationalReasoningEngine",
    "Explanation",
    "KnowledgeGapDetectionRule",
    "LearningMomentumRule",
    "MasteryUpdateRule",
    "PrerequisiteAnalysisRule",
    "ReadinessContributionRule",
    "RecommendationRule",
    "ReasoningContext",
    "ReasoningResult",
    "ReasoningRule",
    "RuleExecution",
    "RuleRegistry",
    "build_default_registry",
]

_EXPORT_MODULES = {
    "ENGINE_VERSION": "app.domain.educational_reasoning.reasoning_engine",
    "EducationalReasoningEngine": "app.domain.educational_reasoning.reasoning_engine",
    "ReasoningRule": "app.domain.educational_reasoning.reasoning_rule",
    "RuleExecution": "app.domain.educational_reasoning.reasoning_rule",
    "ReasoningResult": "app.domain.educational_reasoning.reasoning_result",
    "ReasoningContext": "app.domain.educational_reasoning.reasoning_context",
    "CurriculumEvidenceBundle": "app.domain.educational_reasoning.reasoning_context",
    "RuleRegistry": "app.domain.educational_reasoning.rule_registry",
    "build_default_registry": "app.domain.educational_reasoning.rule_registry",
    "EducationalDecision": "app.domain.educational_reasoning.decision",
    "Explanation": "app.domain.educational_reasoning.explanation",
    "MasteryUpdateRule": "app.domain.educational_reasoning.mastery_update",
    "ConfidenceAdjustmentRule": "app.domain.educational_reasoning.confidence_update",
    "KnowledgeGapDetectionRule": "app.domain.educational_reasoning.gap_analysis",
    "PrerequisiteAnalysisRule": "app.domain.educational_reasoning.gap_analysis",
    "RecommendationRule": "app.domain.educational_reasoning.recommendation_rule",
    "LearningMomentumRule": "app.domain.educational_reasoning.momentum_rule",
    "ConsistencyRule": "app.domain.educational_reasoning.consistency_rule",
    "ReadinessContributionRule": "app.domain.educational_reasoning.readiness_rule",
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
