"""Educational Feedback Loop enumerations (ILE-005).

Review and reflection vocabulary for educational calibration of Study
Sensei guidance. Never engagement, ranking, Twin, or selection labels.
"""

from __future__ import annotations

from enum import StrEnum


class RecommendationReviewState(StrEnum):
    """Terminal-facing review posture for one significant recommendation.

    History is never rewritten. Reviews append educational assessment only.
    """

    SUPPORTED = "supported_by_later_evidence"
    PARTIALLY_SUPPORTED = "partially_supported"
    INCONCLUSIVE = "inconclusive"
    EVIDENCE_INSUFFICIENT = "evidence_insufficient"
    REQUIRES_FUTURE_OBSERVATION = "requires_future_observation"


class EvidenceQualityBand(StrEnum):
    """Quality of educational evidence available for calibration.

    Measures usefulness of evidence for professional judgement — not
    click volume, streak length, or screen time.
    """

    INSUFFICIENT = "insufficient"
    LIMITED = "limited"
    ADEQUATE = "adequate"
    STRONG = "strong"


class StudentReflectionPromptId(StrEnum):
    """Optional brief reflective questions for learners."""

    HELPED = "helped"
    TIMING = "timing"
    UNDERSTOOD_WHY = "understood_why"
    SAME_DECISION = "same_decision"


class ReflectionAnswer(StrEnum):
    """Optional ordinal answers — never scored for engagement."""

    YES = "yes"
    MOSTLY = "mostly"
    NO = "no"
    SKIPPED = "skipped"


class SenseiAssessmentFocus(StrEnum):
    """Internal Sensei self-reflection focus areas."""

    EDUCATIONAL_USEFULNESS = "educational_usefulness"
    TIMING_APPROPRIATENESS = "timing_appropriateness"
    EXPLAINABILITY_CLARITY = "explainability_clarity"
    DECISION_QUALITY = "decision_quality"
    EVIDENCE_QUALITY = "evidence_quality"


# Student-safe labels (never expose engine vocabulary).
REVIEW_STATE_LABELS: dict[str, str] = {
    RecommendationReviewState.SUPPORTED: "Supported by later evidence",
    RecommendationReviewState.PARTIALLY_SUPPORTED: "Partially supported",
    RecommendationReviewState.INCONCLUSIVE: "Inconclusive",
    RecommendationReviewState.EVIDENCE_INSUFFICIENT: "Evidence insufficient",
    RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION: (
        "Requires future observation"
    ),
}

EVIDENCE_QUALITY_LABELS: dict[str, str] = {
    EvidenceQualityBand.INSUFFICIENT: "Evidence insufficient",
    EvidenceQualityBand.LIMITED: "Limited evidence",
    EvidenceQualityBand.ADEQUATE: "Adequate evidence",
    EvidenceQualityBand.STRONG: "Strong evidence",
}

REFLECTION_PROMPT_TEXT: dict[str, str] = {
    StudentReflectionPromptId.HELPED: "Did this recommendation help?",
    StudentReflectionPromptId.TIMING: "Was the timing appropriate?",
    StudentReflectionPromptId.UNDERSTOOD_WHY: (
        "Did you understand why it was recommended?"
    ),
    StudentReflectionPromptId.SAME_DECISION: (
        "Would you make the same decision again?"
    ),
}

REFLECTION_ANSWER_LABELS: dict[str, str] = {
    ReflectionAnswer.YES: "Yes",
    ReflectionAnswer.MOSTLY: "Mostly",
    ReflectionAnswer.NO: "No",
    ReflectionAnswer.SKIPPED: "Prefer not to say",
}

# Forbidden optimisation language — engagement theatre.
FORBIDDEN_CALIBRATION_TERMS: tuple[str, ...] = (
    "engagement",
    "screen time",
    "streak",
    "retention metric",
    "daily active",
    "gamification",
    "click-through",
    "conversion",
)
