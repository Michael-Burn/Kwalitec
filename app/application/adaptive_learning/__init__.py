"""Version 2 Adaptive Decision Engine — application layer.

Deterministic revision decisions from Twin educational state.
Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.adaptive_learning.decision_engine.AdaptiveDecisionEngine``.
"""

from __future__ import annotations

from typing import Any

from app.application.adaptive_learning.decision_engine import (
    AdaptiveDecisionEngine,
    CurriculumContextInput,
    JourneyPositionInput,
)
from app.application.adaptive_learning.diagnostics import (
    AdaptiveDiagnostics,
    AdaptiveDiagnosticsReport,
)
from app.application.adaptive_learning.explanation_service import ExplanationService
from app.application.adaptive_learning.intervention_selector import InterventionSelector
from app.application.adaptive_learning.priority_calculator import PriorityCalculator
from app.application.adaptive_learning.revision_planner import RevisionPlanner
from app.application.adaptive_learning.revision_scheduler import RevisionScheduler
from app.application.adaptive_learning.roi_estimator import ROIEstimator

__all__ = [
    "AdaptiveDecisionEngine",
    "AdaptiveDiagnostics",
    "AdaptiveDiagnosticsReport",
    "AdaptiveLearningError",
    "CurriculumContextInput",
    "DecisionError",
    "DecisionExplanationDTO",
    "DecisionSnapshotDTO",
    "ExplanationError",
    "ExplanationService",
    "InsufficientEvidence",
    "InterventionPolicy",
    "InterventionSelectionError",
    "InterventionSelector",
    "InterventionSnapshot",
    "JourneyPositionInput",
    "PolicyViolation",
    "PriorityCalculator",
    "PriorityError",
    "PriorityPolicy",
    "ROIError",
    "ROIEstimator",
    "ROIPolicy",
    "ROISnapshot",
    "RevisionCandidateSnapshot",
    "RevisionPlanError",
    "RevisionPlanner",
    "RevisionScheduler",
    "RevisionSnapshot",
    "RevisionWindowSnapshot",
    "UnsupportedIntervention",
]

_EXPORT_MODULES = {
    "AdaptiveLearningError": "app.application.adaptive_learning.exceptions",
    "DecisionError": "app.application.adaptive_learning.exceptions",
    "DecisionExplanationDTO": (
        "app.application.adaptive_learning.dto.decision_snapshot"
    ),
    "DecisionSnapshotDTO": "app.application.adaptive_learning.dto.decision_snapshot",
    "ExplanationError": "app.application.adaptive_learning.exceptions",
    "InsufficientEvidence": "app.application.adaptive_learning.exceptions",
    "InterventionPolicy": (
        "app.application.adaptive_learning.policies.intervention_policy"
    ),
    "InterventionSelectionError": "app.application.adaptive_learning.exceptions",
    "InterventionSnapshot": (
        "app.application.adaptive_learning.dto.intervention_snapshot"
    ),
    "PolicyViolation": "app.application.adaptive_learning.exceptions",
    "PriorityError": "app.application.adaptive_learning.exceptions",
    "PriorityPolicy": "app.application.adaptive_learning.policies.priority_policy",
    "ROIError": "app.application.adaptive_learning.exceptions",
    "ROIPolicy": "app.application.adaptive_learning.policies.roi_policy",
    "ROISnapshot": "app.application.adaptive_learning.dto.roi_snapshot",
    "RevisionCandidateSnapshot": (
        "app.application.adaptive_learning.dto.revision_snapshot"
    ),
    "RevisionPlanError": "app.application.adaptive_learning.exceptions",
    "RevisionSnapshot": "app.application.adaptive_learning.dto.revision_snapshot",
    "RevisionWindowSnapshot": (
        "app.application.adaptive_learning.dto.revision_snapshot"
    ),
    "UnsupportedIntervention": "app.application.adaptive_learning.exceptions",
}


def __getattr__(name: str) -> Any:
    if name in globals():
        return globals()[name]
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
