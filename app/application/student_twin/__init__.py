"""Version 2 Student Digital Twin — application layer.

Deterministic evidence-driven learner state engine.
Framework-independent: no Flask, SQLAlchemy, UI, migrations, or persistence.

Prefer explicit imports such as
``app.application.student_twin.twin_engine.StudentTwinEngine``.
"""

from __future__ import annotations

from typing import Any

from app.application.student_twin.comparison_service import ComparisonService
from app.application.student_twin.confidence_calculator import ConfidenceCalculator
from app.application.student_twin.diagnostics import TwinDiagnostics
from app.application.student_twin.evidence_aggregator import EvidenceAggregator
from app.application.student_twin.explanation_service import ExplanationService
from app.application.student_twin.learning_velocity_service import (
    LearningVelocityService,
)
from app.application.student_twin.mastery_calculator import MasteryCalculator
from app.application.student_twin.readiness_estimator import ReadinessEstimator
from app.application.student_twin.recommendation_service import RecommendationService
from app.application.student_twin.retention_estimator import RetentionEstimator
from app.application.student_twin.snapshot_service import SnapshotService
from app.application.student_twin.timeline_service import TimelineService
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.application.student_twin.weakness_analyser import WeaknessAnalyser

__all__ = [
    "ComparisonError",
    "ComparisonService",
    "ComparisonSnapshot",
    "ConfidenceCalculator",
    "ConfidencePolicy",
    "DuplicateEvidence",
    "EvidenceAggregator",
    "EvidencePolicy",
    "EvidenceRejected",
    "EvidenceSummary",
    "ExplanationError",
    "ExplanationService",
    "IllegalState",
    "LearnerNotFound",
    "LearnerSnapshot",
    "LearningVelocityService",
    "MasteryCalculator",
    "MasteryPolicy",
    "MasterySummary",
    "PolicyViolation",
    "ReadinessEstimator",
    "ReadinessSummary",
    "RecommendationExplanation",
    "RecommendationPolicy",
    "RecommendationService",
    "RecommendationSnapshot",
    "RetentionEstimator",
    "SnapshotError",
    "SnapshotService",
    "StudentTwinEngine",
    "StudentTwinError",
    "TimelineService",
    "TwinDiagnostics",
    "TwinDiagnosticsReport",
    "TwinNotFound",
    "TwinSnapshotDTO",
    "WeaknessAnalyser",
]

_EXPORT_MODULES = {
    "ComparisonError": "app.application.student_twin.exceptions",
    "ComparisonService": "app.application.student_twin.comparison_service",
    "ComparisonSnapshot": "app.application.student_twin.dto.comparison_snapshot",
    "ConfidenceCalculator": "app.application.student_twin.confidence_calculator",
    "ConfidencePolicy": "app.application.student_twin.policies.confidence_policy",
    "DuplicateEvidence": "app.application.student_twin.exceptions",
    "EvidenceAggregator": "app.application.student_twin.evidence_aggregator",
    "EvidencePolicy": "app.application.student_twin.policies.evidence_policy",
    "EvidenceRejected": "app.application.student_twin.exceptions",
    "EvidenceSummary": "app.application.student_twin.dto.evidence_summary",
    "ExplanationError": "app.application.student_twin.exceptions",
    "ExplanationService": "app.application.student_twin.explanation_service",
    "IllegalState": "app.application.student_twin.exceptions",
    "LearnerNotFound": "app.application.student_twin.exceptions",
    "LearnerSnapshot": "app.application.student_twin.dto.learner_snapshot",
    "LearningVelocityService": (
        "app.application.student_twin.learning_velocity_service"
    ),
    "MasteryCalculator": "app.application.student_twin.mastery_calculator",
    "MasteryPolicy": "app.application.student_twin.policies.mastery_policy",
    "MasterySummary": "app.application.student_twin.dto.mastery_summary",
    "PolicyViolation": "app.application.student_twin.exceptions",
    "ReadinessEstimator": "app.application.student_twin.readiness_estimator",
    "ReadinessSummary": "app.application.student_twin.dto.readiness_summary",
    "RecommendationExplanation": (
        "app.application.student_twin.dto.recommendation_snapshot"
    ),
    "RecommendationPolicy": (
        "app.application.student_twin.policies.recommendation_policy"
    ),
    "RecommendationService": "app.application.student_twin.recommendation_service",
    "RecommendationSnapshot": (
        "app.application.student_twin.dto.recommendation_snapshot"
    ),
    "RetentionEstimator": "app.application.student_twin.retention_estimator",
    "SnapshotError": "app.application.student_twin.exceptions",
    "SnapshotService": "app.application.student_twin.snapshot_service",
    "StudentTwinEngine": "app.application.student_twin.twin_engine",
    "StudentTwinError": "app.application.student_twin.exceptions",
    "TimelineService": "app.application.student_twin.timeline_service",
    "TwinDiagnostics": "app.application.student_twin.diagnostics",
    "TwinDiagnosticsReport": "app.application.student_twin.diagnostics",
    "TwinNotFound": "app.application.student_twin.exceptions",
    "TwinSnapshotDTO": "app.application.student_twin.dto.twin_snapshot",
    "WeaknessAnalyser": "app.application.student_twin.weakness_analyser",
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
