"""Explainable Recommendation Engine domain package.

Read-side packaging of Decision into an attributable Recommendation.
Not a Twin write domain. Not an Update Strategy. Not selection authority.
No ranking, scoring, readiness recomputation, Twin mutation, or missions.
Mission Intelligence (``app.domain.mission``) may surface Recommendation
language as an optional hook; packaging is not day composition, and Priority
never sequences mission execution order.

Imports are lazy via ``__getattr__`` so Twin write-path packages can load
without circular import deadlocks when recommendation is imported first.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "AFFORDANCE_OUTCOME_CATALOGUE",
    "PACKAGING_VERSION",
    "THIN_WARRANT_CONFIDENCE_POSTURES",
    "ActionableSuggestion",
    "AffordanceOutcome",
    "CandidateContrast",
    "CurriculumLayerPresentation",
    "DecisionLayerPresentation",
    "DecisionReference",
    "EvidenceLayerPresentation",
    "ExplanationChainLayer",
    "ExplanationChainPresentation",
    "JournalLinkageHook",
    "ReadinessLayerPresentation",
    "Recommendation",
    "RecommendationConfidencePosture",
    "RecommendationContext",
    "RecommendationEngine",
    "RecommendationReason",
    "ResponseAffordances",
    "TwinLayerPresentation",
    "inherit_confidence_posture",
    "project_candidate_contrast",
]

_EXPORT_MODULES = {
    "AFFORDANCE_OUTCOME_CATALOGUE": "app.domain.recommendation.affordances",
    "AffordanceOutcome": "app.domain.recommendation.affordances",
    "JournalLinkageHook": "app.domain.recommendation.affordances",
    "ResponseAffordances": "app.domain.recommendation.affordances",
    "CandidateContrast": "app.domain.recommendation.contrast",
    "project_candidate_contrast": "app.domain.recommendation.contrast",
    "RecommendationContext": "app.domain.recommendation.context",
    "CurriculumLayerPresentation": "app.domain.recommendation.explanation",
    "DecisionLayerPresentation": "app.domain.recommendation.explanation",
    "EvidenceLayerPresentation": "app.domain.recommendation.explanation",
    "ExplanationChainPresentation": "app.domain.recommendation.explanation",
    "ReadinessLayerPresentation": "app.domain.recommendation.explanation",
    "TwinLayerPresentation": "app.domain.recommendation.explanation",
    "RecommendationEngine": "app.domain.recommendation.engine",
    "PACKAGING_VERSION": "app.domain.recommendation.recommendation",
    "DecisionReference": "app.domain.recommendation.recommendation",
    "Recommendation": "app.domain.recommendation.recommendation",
    "ExplanationChainLayer": "app.domain.recommendation.reasons",
    "RecommendationReason": "app.domain.recommendation.reasons",
    "ActionableSuggestion": "app.domain.recommendation.suggestion",
    "THIN_WARRANT_CONFIDENCE_POSTURES": "app.domain.recommendation.warrant",
    "RecommendationConfidencePosture": "app.domain.recommendation.warrant",
    "inherit_confidence_posture": "app.domain.recommendation.warrant",
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
