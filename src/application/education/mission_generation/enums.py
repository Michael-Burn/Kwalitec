"""Adaptive Mission Generator enumerations.

Mission vocabulary expresses executable learning work derived from
educational recommendations. Categories here are mission types — never
mastery bands, recommendation intent, or UI packaging.
"""

from __future__ import annotations

from enum import StrEnum


class MissionType(StrEnum):
    """Executable educational mission kinds produced by the generator."""

    PRACTICE_QUESTIONS = "practice_questions"
    REVIEW_CONCEPT = "review_concept"
    STRENGTHEN_FOUNDATION = "strengthen_foundation"
    REVISE_PREREQUISITE = "revise_prerequisite"
    CONSOLIDATE_KNOWLEDGE = "consolidate_knowledge"
    CHECKPOINT_PREPARATION = "checkpoint_preparation"
    REVISION_SESSION = "revision_session"
    MIXED_PRACTICE = "mixed_practice"
    CONFIDENCE_RECOVERY = "confidence_recovery"
    MAINTENANCE_REVIEW = "maintenance_review"


class MissionDurationBand(StrEnum):
    """Estimated sitting duration band for a generated mission."""

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


class MissionPriorityBand(StrEnum):
    """Qualitative priority band derived from a priority magnitude."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MissionConstraintKind(StrEnum):
    """Kind of executable constraint attached to a mission or plan."""

    REQUIRE_PREREQUISITE_FIRST = "require_prerequisite_first"
    LIMIT_DAILY_WORKLOAD = "limit_daily_workload"
    RESPECT_AVAILABLE_TIME = "respect_available_time"
    PRESERVE_COVERAGE = "preserve_coverage"
    INCREASE_RECURRENCE = "increase_recurrence"
    DECREASE_RECURRENCE = "decrease_recurrence"
    PREFER_MISSION_TYPE = "prefer_mission_type"
    TARGET_EXAMINATION = "target_examination"
    BLOCK_ADVANCEMENT = "block_advancement"


class MissionStepAction(StrEnum):
    """Structured action code for one mission step."""

    PRACTICE = "practice"
    REVIEW = "review"
    REVISE = "revise"
    CONSOLIDATE = "consolidate"
    PREPARE = "prepare"
    MAINTAIN = "maintain"
    RECOVER = "recover"
    MIX = "mix"


class MissionObjectiveCode(StrEnum):
    """Structured objective code — never free-form natural language."""

    COMPLETE_PRACTICE = "complete_practice"
    REVIEW_TARGET = "review_target"
    STRENGTHEN_TARGET = "strengthen_target"
    ADDRESS_PREREQUISITE = "address_prerequisite"
    CONSOLIDATE_TARGET = "consolidate_target"
    PREPARE_CHECKPOINT = "prepare_checkpoint"
    REVISE_TARGET = "revise_target"
    MIXED_COVERAGE = "mixed_coverage"
    RECOVER_CONFIDENCE = "recover_confidence"
    MAINTAIN_TARGET = "maintain_target"


class MissionRecurrenceBand(StrEnum):
    """How often a mission should recur — independent of mission size."""

    REDUCED = "reduced"
    NORMAL = "normal"
    INCREASED = "increased"


class LearningPace(StrEnum):
    """Caller-supplied learning pace preference (application input)."""

    SLOW = "slow"
    NORMAL = "normal"
    FAST = "fast"
