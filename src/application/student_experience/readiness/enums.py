"""Exam Readiness Experience enumerations.

Presentation vocabulary only — never mastery bands, recommendation
categories, or educational reasoning codes exposed as domain types.
"""

from __future__ import annotations

from enum import StrEnum


class ReadinessCategory(StrEnum):
    """Student-facing readiness category projected from existing signals."""

    UNAVAILABLE = "unavailable"
    EARLY_STAGE = "early_stage"
    BUILDING = "building"
    APPROACHING = "approaching"
    STRONG = "strong"
    EXAM_READY = "exam_ready"


class ReadinessDirection(StrEnum):
    """Improving / Stable / Declining readiness direction — never a forecast."""

    UNKNOWN = "unknown"
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"


class AssessmentConfidenceCategory(StrEnum):
    """Confidence in the readiness assessment — not student confidence."""

    VERY_HIGH = "very_high"
    HIGH = "high"
    MODERATE = "moderate"
    LIMITED = "limited"
    UNKNOWN = "unknown"


class EvidenceQualityBand(StrEnum):
    """Projected evidence quality for the assessment."""

    UNKNOWN = "unknown"
    LIMITED = "limited"
    ADEQUATE = "adequate"
    STRONG = "strong"
    EXCELLENT = "excellent"


class EvidenceQuantityBand(StrEnum):
    """Projected evidence quantity for the assessment."""

    UNKNOWN = "unknown"
    SPARSE = "sparse"
    MODERATE = "moderate"
    SUBSTANTIAL = "substantial"
    RICH = "rich"


class ConsistencyBand(StrEnum):
    """Projected consistency of the readiness signal."""

    UNKNOWN = "unknown"
    UNEVEN = "uneven"
    MODERATE = "moderate"
    CONSISTENT = "consistent"


class StrengthKind(StrEnum):
    """Deterministic strength summary kinds."""

    STRONGEST_SUBJECT = "strongest_subject"
    STRONGEST_COMPETENCY = "strongest_competency"
    RECENT_IMPROVEMENT = "recent_improvement"
    MISSION_COMPLETION_QUALITY = "mission_completion_quality"


class RiskKind(StrEnum):
    """Deterministic risk summary kinds."""

    WEAKEST_COMPETENCY = "weakest_competency"
    INCOMPLETE_PREREQUISITE = "incomplete_prerequisite"
    REVISION_GAP = "revision_gap"
    OVERDUE_MISSION = "overdue_mission"
    SCHEDULE_PRESSURE = "schedule_pressure"


class ActionPlanItemKind(StrEnum):
    """Kinds of composed action-plan items — never newly generated advice."""

    FOLLOW_RECOMMENDATION = "follow_recommendation"
    COMPLETE_NEXT_MISSION = "complete_next_mission"
    FINISH_REVISION_CYCLE = "finish_revision_cycle"
    REVIEW_BEFORE_CHECKPOINT = "review_before_checkpoint"
    ADDRESS_PREREQUISITE = "address_prerequisite"
    VIEW_SCHEDULE = "view_schedule"
    NONE = "none"


class ReadinessMilestoneKind(StrEnum):
    """Upcoming milestone kinds on the readiness surface."""

    REVISION_CYCLE = "revision_cycle"
    READINESS_TARGET = "readiness_target"
    CHECKPOINT = "checkpoint"
    EXAM = "exam"
    STUDY_SESSION = "study_session"
