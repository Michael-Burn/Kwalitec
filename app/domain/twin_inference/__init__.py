"""Twin Inference Engine domain (EI-006).

Derives explainable educational beliefs from immutable Learning Evidence.
Does not generate recommendations, study missions, mutate evidence, or
modify curriculum content. Pure domain only: no Flask or SQLAlchemy.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "BeliefExplanation",
    "ConfidenceCalculation",
    "EmptyBeliefFactory",
    "INFERENCE_VERSION",
    "InferenceContext",
    "InferenceResult",
    "InferenceRule",
    "LearningState",
    "RuleContribution",
    "RuleContributionRecord",
    "SubjectKnowledgeState",
    "TwinBelief",
    "TwinInferenceEngine",
    "aggregate_knowledge_state",
    "clamp01",
    "default_rule_pack",
    "derive_learning_state",
    "filter_usable_evidence",
    "recency_factor",
]

_EXPORT_MODULES = {
    "INFERENCE_VERSION": "app.domain.twin_inference.version",
    "LearningState": "app.domain.twin_inference.learning_state",
    "TwinBelief": "app.domain.twin_inference.belief",
    "EmptyBeliefFactory": "app.domain.twin_inference.belief",
    "clamp01": "app.domain.twin_inference.belief",
    "BeliefExplanation": "app.domain.twin_inference.explanation",
    "ConfidenceCalculation": "app.domain.twin_inference.explanation",
    "RuleContributionRecord": "app.domain.twin_inference.explanation",
    "InferenceContext": "app.domain.twin_inference.rules.base",
    "InferenceRule": "app.domain.twin_inference.rules.base",
    "RuleContribution": "app.domain.twin_inference.rules.base",
    "default_rule_pack": "app.domain.twin_inference.rules",
    "recency_factor": "app.domain.twin_inference.rules.recency",
    "TwinInferenceEngine": "app.domain.twin_inference.engine",
    "InferenceResult": "app.domain.twin_inference.engine",
    "SubjectKnowledgeState": "app.domain.twin_inference.knowledge_state",
    "aggregate_knowledge_state": "app.domain.twin_inference.knowledge_state",
    "derive_learning_state": "app.domain.twin_inference.derive_state",
    "filter_usable_evidence": "app.domain.twin_inference.evidence_prep",
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
