"""Readiness Forecast & Study Trajectory DTOs (KWP-012).

Projection-layer vocabulary for where a learner is heading.
Never scores as product certainty — natural guidance only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ForecastLabel(StrEnum):
    """Deterministic forecast posture — student-safe titles."""

    ON_TRACK = "on_track"
    BUILDING_MOMENTUM = "building_momentum"
    NEEDS_GREATER_CONSISTENCY = "needs_greater_consistency"
    RECOVERY_REQUIRED = "recovery_required"
    AHEAD_OF_SCHEDULE = "ahead_of_schedule"
    BELOW_TARGET_PACE = "below_target_pace"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class ForecastConfidence(StrEnum):
    """Honesty about evidence density — never fabricate certainty."""

    LIMITED = "limited"
    EMERGING = "emerging"
    ESTABLISHED = "established"


class TrendDirection(StrEnum):
    """Observed readiness trend from sitting evidence."""

    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    RECOVERING = "recovering"
    UNKNOWN = "unknown"


# Student-safe forecast titles (product language).
FORECAST_TITLES: dict[ForecastLabel, str] = {
    ForecastLabel.ON_TRACK: "On Track",
    ForecastLabel.BUILDING_MOMENTUM: "Building Momentum",
    ForecastLabel.NEEDS_GREATER_CONSISTENCY: "Needs Greater Consistency",
    ForecastLabel.RECOVERY_REQUIRED: "Recovery Required",
    ForecastLabel.AHEAD_OF_SCHEDULE: "Ahead of Schedule",
    ForecastLabel.BELOW_TARGET_PACE: "Below Target Pace",
    ForecastLabel.INSUFFICIENT_EVIDENCE: "Not Enough Evidence Yet",
}

TREND_TITLES: dict[TrendDirection, str] = {
    TrendDirection.IMPROVING: "Improving",
    TrendDirection.STABLE: "Stable",
    TrendDirection.DECLINING: "Declining",
    TrendDirection.RECOVERING: "Recovering",
    TrendDirection.UNKNOWN: "Not yet clear",
}

CONFIDENCE_TITLES: dict[ForecastConfidence, str] = {
    ForecastConfidence.LIMITED: "Limited evidence",
    ForecastConfidence.EMERGING: "Emerging pattern",
    ForecastConfidence.ESTABLISHED: "Established pattern",
}

# Reuse Exam Week Briefing stage thresholds (KWP-006) — do not invent a second
# readiness band system. Target for sitting preparation is Ready for Revision.
TARGET_READINESS_STAGE = "Ready for Revision"
TARGET_READINESS_RATIO = 0.80


@dataclass(frozen=True)
class ForecastSignals:
    """Evidence-derived inputs for trajectory projection.

    Built only from existing packages / enrichments — never invented.
    """

    sitting_count: int = 0
    topic_count: int = 0
    strong_finish_ratio: float = 0.0
    recent_strong_ratio: float = 0.0
    early_strong_ratio: float = 0.0
    progress_advance_rate: float = 0.0
    consistency_score: float = 0.0
    sittings_per_week: float = 0.0
    recovery_pressure: float = 0.0
    retention_risk_rate: float = 0.0
    difficulty_demand_rate: float = 0.0
    intervention_help_rate: float = 0.0
    confidence_mismatch_rate: float = 0.0
    reflection_rate: float = 0.0
    memory_improving: bool = False
    memory_recovery_success: bool = False
    current_readiness_ratio: float | None = None
    days_to_exam: int | None = None
    exam_date_label: str = ""
    as_of: str = ""

    def to_opaque(self) -> dict[str, Any]:
        return {
            "sitting_count": self.sitting_count,
            "topic_count": self.topic_count,
            "strong_finish_ratio": round(self.strong_finish_ratio, 4),
            "recent_strong_ratio": round(self.recent_strong_ratio, 4),
            "early_strong_ratio": round(self.early_strong_ratio, 4),
            "progress_advance_rate": round(self.progress_advance_rate, 4),
            "consistency_score": round(self.consistency_score, 4),
            "sittings_per_week": round(self.sittings_per_week, 4),
            "recovery_pressure": round(self.recovery_pressure, 4),
            "retention_risk_rate": round(self.retention_risk_rate, 4),
            "difficulty_demand_rate": round(self.difficulty_demand_rate, 4),
            "intervention_help_rate": round(self.intervention_help_rate, 4),
            "confidence_mismatch_rate": round(self.confidence_mismatch_rate, 4),
            "reflection_rate": round(self.reflection_rate, 4),
            "memory_improving": self.memory_improving,
            "memory_recovery_success": self.memory_recovery_success,
            "current_readiness_ratio": (
                round(self.current_readiness_ratio, 4)
                if self.current_readiness_ratio is not None
                else None
            ),
            "days_to_exam": self.days_to_exam,
            "exam_date_label": self.exam_date_label,
            "as_of": self.as_of,
        }


@dataclass(frozen=True)
class StudyTrajectory:
    """Explainable trajectory projection — assumptions and factors included."""

    current_trend: TrendDirection = TrendDirection.UNKNOWN
    current_trend_title: str = ""
    current_readiness_stage: str = ""
    projected_readiness_ratio: float | None = None
    projected_readiness_stage: str = ""
    days_to_exam: int | None = None
    key_assumptions: tuple[str, ...] = ()
    influential_factors: tuple[str, ...] = ()
    confidence: ForecastConfidence = ForecastConfidence.LIMITED
    confidence_title: str = ""

    def to_opaque(self) -> dict[str, Any]:
        return {
            "current_trend": self.current_trend.value,
            "current_trend_title": self.current_trend_title,
            "current_readiness_stage": self.current_readiness_stage,
            "projected_readiness_ratio": (
                round(self.projected_readiness_ratio, 4)
                if self.projected_readiness_ratio is not None
                else None
            ),
            "projected_readiness_stage": self.projected_readiness_stage,
            "days_to_exam": self.days_to_exam,
            "key_assumptions": list(self.key_assumptions),
            "influential_factors": list(self.influential_factors),
            "confidence": self.confidence.value,
            "confidence_title": self.confidence_title,
        }


@dataclass(frozen=True)
class ReadinessForecast:
    """Full readiness forecast for one learner — projection only."""

    label: ForecastLabel = ForecastLabel.INSUFFICIENT_EVIDENCE
    title: str = ""
    guidance: str = ""
    explanation: str = ""
    rule_id: str = ""
    trajectory: StudyTrajectory = field(default_factory=StudyTrajectory)
    signals: ForecastSignals = field(default_factory=ForecastSignals)
    student_id: str = ""
    has_forecast: bool = False

    def to_opaque(self) -> dict[str, Any]:
        return {
            "label": self.label.value,
            "title": self.title,
            "guidance": self.guidance,
            "explanation": self.explanation,
            "rule_id": self.rule_id,
            "trajectory": self.trajectory.to_opaque(),
            "signals": self.signals.to_opaque(),
            "student_id": self.student_id,
            "has_forecast": self.has_forecast,
        }
