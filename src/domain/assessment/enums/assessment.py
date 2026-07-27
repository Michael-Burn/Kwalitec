"""Assessment type, purpose, and session status enumerations.

Architecture Source
    knowledge/product/AP-002/EDUCATIONAL_MODEL.md
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md
"""

from __future__ import annotations

from enum import StrEnum


class AssessmentType(StrEnum):
    """Delivery form of an assessment instrument.

    A type describes *how* evidence is collected; purpose describes *why*.
    """

    SINGLE_ITEM = "single_item"
    QUIZ_BUNDLE = "quiz_bundle"
    REFLECTION_SET = "reflection_set"
    MIXED = "mixed"


class AssessmentPurpose(StrEnum):
    """Educational intent for collecting evidence (Assessment intents)."""

    DIAGNOSTIC = "diagnostic"
    FORMATIVE_CHECKPOINT = "formative_checkpoint"
    ADAPTIVE_PROBE = "adaptive_probe"
    RECOVERY_CHECK = "recovery_check"
    MASTERY_VERIFICATION = "mastery_verification"
    REVISION_STABILITY = "revision_stability"
    REFLECTION = "reflection"


class AssessmentStatus(StrEnum):
    """Lifecycle status of an AssessmentSession.

    Conceptual machine from ASSESSMENT_LIFECYCLE.md §3.
    """

    DRAFT = "draft"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    SUBMITTED = "submitted"
    OBSERVED = "observed"
    REASONED = "reasoned"
    CLOSED = "closed"
    ABANDONED = "abandoned"
    INVALIDATED = "invalidated"
