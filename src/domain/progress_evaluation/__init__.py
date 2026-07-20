"""Progress Evaluation Engine — deterministic Educational OS progress metrics.

EDU-003: Evaluate learner progress from Digital Twin, Learning Evidence,
Completed Missions, Study Plans, and Learning Trajectory.

Produce deterministic ProgressReports that can be explained from evidence.

Pure domain logic only. No AI, no prompting, no randomness, no persistence,
Flask, ORM, HTTP, visualization, or DTOs.
"""

from __future__ import annotations

from domain.progress_evaluation.completed_mission import CompletedMission
from domain.progress_evaluation.confidence_trend import ConfidenceTrend
from domain.progress_evaluation.enums import (
    InterventionUrgency,
    ProgressMetricCode,
    RevisionEffectivenessBand,
    StabilityBand,
    TrendDirection,
    VelocityBand,
)
from domain.progress_evaluation.ids import ProgressReportId
from domain.progress_evaluation.intervention_signal import InterventionSignal
from domain.progress_evaluation.learning_velocity import LearningVelocity
from domain.progress_evaluation.mastery_trend import MasteryTrend
from domain.progress_evaluation.progress_evaluator import (
    ProgressEvaluator,
    active_misconception_threshold,
    trend_delta_threshold,
)
from domain.progress_evaluation.progress_metric import ProgressMetric
from domain.progress_evaluation.progress_report import ProgressReport
from domain.progress_evaluation.revision_effectiveness import RevisionEffectiveness

__all__ = [
    # Aggregate / report
    "ProgressReport",
    "ProgressMetric",
    # Trends / velocity / revision / intervention
    "MasteryTrend",
    "ConfidenceTrend",
    "LearningVelocity",
    "RevisionEffectiveness",
    "InterventionSignal",
    # Input
    "CompletedMission",
    # Identities
    "ProgressReportId",
    # Enums
    "TrendDirection",
    "VelocityBand",
    "StabilityBand",
    "RevisionEffectivenessBand",
    "InterventionUrgency",
    "ProgressMetricCode",
    # Evaluator
    "ProgressEvaluator",
    "trend_delta_threshold",
    "active_misconception_threshold",
]
