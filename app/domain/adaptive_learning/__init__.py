"""Version 2 Adaptive Decision Engine — domain package.

Deterministic educational intervention selection (Phase 1: revision).
No teaching. No content generation. No Flask / SQLAlchemy / persistence.

Prefer explicit imports such as
``app.domain.adaptive_learning.adaptive_decision.AdaptiveDecision``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "AdaptiveDecision",
    "DecisionExplanation",
    "DecisionSnapshot",
    "EducationalROI",
    "Intervention",
    "InterventionPriority",
    "InterventionType",
    "PHASE1_IMPLEMENTED_TYPES",
    "PriorityBand",
    "RevisionCandidate",
    "RevisionPlan",
    "RevisionUrgency",
    "RevisionWindow",
    "is_phase1_implemented",
    "priority_band_from_score",
    "resolve_intervention_type",
    "resolve_priority_band",
    "urgency_from_priority",
]

_EXPORT_MODULES = {
    "AdaptiveDecision": "app.domain.adaptive_learning.adaptive_decision",
    "DecisionExplanation": "app.domain.adaptive_learning.decision_explanation",
    "DecisionSnapshot": "app.domain.adaptive_learning.decision_snapshot",
    "EducationalROI": "app.domain.adaptive_learning.educational_roi",
    "Intervention": "app.domain.adaptive_learning.intervention",
    "InterventionPriority": "app.domain.adaptive_learning.intervention_priority",
    "InterventionType": "app.domain.adaptive_learning.intervention_type",
    "PHASE1_IMPLEMENTED_TYPES": "app.domain.adaptive_learning.intervention_type",
    "PriorityBand": "app.domain.adaptive_learning.intervention_priority",
    "RevisionCandidate": "app.domain.adaptive_learning.revision_candidate",
    "RevisionPlan": "app.domain.adaptive_learning.revision_plan",
    "RevisionUrgency": "app.domain.adaptive_learning.revision_window",
    "RevisionWindow": "app.domain.adaptive_learning.revision_window",
    "is_phase1_implemented": "app.domain.adaptive_learning.intervention_type",
    "priority_band_from_score": "app.domain.adaptive_learning.intervention_priority",
    "resolve_intervention_type": "app.domain.adaptive_learning.intervention_type",
    "resolve_priority_band": "app.domain.adaptive_learning.intervention_priority",
    "urgency_from_priority": "app.domain.adaptive_learning.revision_window",
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
