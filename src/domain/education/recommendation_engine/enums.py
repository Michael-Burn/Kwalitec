"""Recommendation Engine domain enumerations.

Architecture Source
    PROJECT_CONTEXT.md
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
    STUDENT_DIGITAL_TWIN.md
Concept
    Recommendation Category / Priority Band / Impact Band /
    Reason Code / Constraint Kind

Every band and category here is always *computed* deterministically by the
Recommendation Engine from educational state, mastery assessment, evidence,
and knowledge graph structure. Categories express educational intent —
never UI actions, mission tasks, or product packaging.
"""

from __future__ import annotations

from enum import StrEnum


class RecommendationCategory(StrEnum):
    """Educational recommendation intent produced by the engine.

    Categories describe *what educational action is warranted*, not how a
    UI should render it or how a mission should be composed.
    """

    REVIEW_CONCEPT = "review_concept"
    STUDY_PREREQUISITE = "study_prerequisite"
    ATTEMPT_CHECKPOINT = "attempt_checkpoint"
    STRENGTHEN_WEAK_AREA = "strengthen_weak_area"
    DELAY_ADVANCED_TOPIC = "delay_advanced_topic"
    CONTINUE_CURRENT_MISSION = "continue_current_mission"
    INCREASE_REVISION_FREQUENCY = "increase_revision_frequency"
    REDUCE_REVISION_FREQUENCY = "reduce_revision_frequency"
    REVISIT_FOUNDATION = "revisit_foundation"
    MAINTAIN_MASTERY = "maintain_mastery"
    FOCUS_COMPETENCY = "focus_competency"
    PREPARE_ASSESSMENT = "prepare_assessment"
    CONSOLIDATE_KNOWLEDGE = "consolidate_knowledge"


class RecommendationPriorityBand(StrEnum):
    """Qualitative priority band derived from a priority magnitude."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationImpactBand(StrEnum):
    """Qualitative educational impact band derived from an impact magnitude."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecommendationReasonCode(StrEnum):
    """Structured, machine-readable reason attached to a recommendation.

    Reason codes are structured domain information describing *why* a
    recommendation was produced — never natural language explanation text.
    """

    WEAK_PREREQUISITE = "weak_prerequisite"
    LOW_MASTERY_HIGH_CONFIDENCE = "low_mastery_high_confidence"
    LOW_MASTERY_LOW_CONFIDENCE = "low_mastery_low_confidence"
    STABLE_HIGH_MASTERY = "stable_high_mastery"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"
    ACTIVE_MISSION = "active_mission"
    ACTIVE_CHECKPOINT = "active_checkpoint"
    VOLATILE_MASTERY = "volatile_mastery"
    DEVELOPING_MASTERY = "developing_mastery"
    ADVANCED_WITHOUT_FOUNDATION = "advanced_without_foundation"
    SECURE_READY_FOR_CHECKPOINT = "secure_ready_for_checkpoint"
    STABLE_REVISION_LOAD = "stable_revision_load"
    DIRECT_KNOWLEDGE_GAP = "direct_knowledge_gap"


class RecommendationConstraintKind(StrEnum):
    """Kind of educational constraint attached to a recommendation or set."""

    BLOCK_ADVANCEMENT = "block_advancement"
    REQUIRE_PREREQUISITE = "require_prerequisite"
    DEFER_CHECKPOINT = "defer_checkpoint"
    LIMIT_SCOPE = "limit_scope"
    PRESERVE_MISSION = "preserve_mission"
