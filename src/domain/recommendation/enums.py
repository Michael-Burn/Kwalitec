"""Recommendation enumerations.

Vocabulary for deterministic RecommendationSpecification projections.
Categories are educational decisions — not UI presentation hints.
"""

from __future__ import annotations

from enum import StrEnum


class RecommendationCategory(StrEnum):
    """Catalogue of educational recommendation decisions.

    Each category names a lawful next educational move derived from
    Educational Operating System state. Categories are not mastery claims
    and not presentation chrome.
    """

    CONTINUE_MISSION = "continue_mission"
    REVIEW_PREVIOUS_TOPIC = "review_previous_topic"
    INCREASE_DIFFICULTY = "increase_difficulty"
    REDUCE_COGNITIVE_LOAD = "reduce_cognitive_load"
    REPEAT_ASSESSMENT = "repeat_assessment"
    SCHEDULE_REVISION = "schedule_revision"
    REVISIT_PREREQUISITES = "revisit_prerequisites"
    PAUSE_FOR_CONSOLIDATION = "pause_for_consolidation"


class RecommendationPriorityBand(StrEnum):
    """Instructional urgency band for a recommendation.

    Mapped from Educational Priority and adjusted by progress/diagnosis
    signals. Distinct from diagnosis severity and from UI ranking chrome.
    """

    NEGLIGIBLE = "negligible"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationReasonCode(StrEnum):
    """Stable reason codes attached to RecommendationReason entries."""

    DIAGNOSIS_TYPE = "diagnosis_type"
    PRIORITY_BAND = "priority_band"
    PRIORITY_PEAK_FACTOR = "priority_peak_factor"
    INTERVENTION_SIGNAL = "intervention_signal"
    MASTERY_TREND = "mastery_trend"
    CONFIDENCE_TREND = "confidence_trend"
    KNOWLEDGE_STABILITY = "knowledge_stability"
    REVISION_EFFECTIVENESS = "revision_effectiveness"
    LEARNING_VELOCITY = "learning_velocity"
    STRATEGY_COMPLEXITY = "strategy_complexity"
    MISSION_READY = "mission_ready"
    STUDY_PLAN_REVIEW = "study_plan_review"
    TWIN_CONFIDENCE = "twin_confidence"


class SupportingEvidenceCode(StrEnum):
    """Stable codes for SupportingEvidence cited by a Recommendation."""

    DIAGNOSIS = "diagnosis"
    PRIORITY = "priority"
    PROGRESS_INTERVENTION = "progress_intervention"
    PROGRESS_MASTERY = "progress_mastery"
    PROGRESS_CONFIDENCE = "progress_confidence"
    PROGRESS_STABILITY = "progress_stability"
    PROGRESS_REVISION = "progress_revision"
    PROGRESS_VELOCITY = "progress_velocity"
    STRATEGY = "strategy"
    MISSION = "mission"
    STUDY_PLAN = "study_plan"
    TWIN = "twin"
