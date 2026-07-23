"""Student-facing presentation helpers — projection only, no educational reasoning.

Maps existing Education OS primitives into human-readable readiness labels.
Never estimates mastery, generates recommendations, or forecasts exams.
"""

from __future__ import annotations

from application.education.mission_generation.enums import (
    MissionObjectiveCode,
    MissionType,
)
from application.education.mission_generation.models.mission import Mission
from application.student_experience.readiness.enums import (
    AssessmentConfidenceCategory,
    ConsistencyBand,
    EvidenceQualityBand,
    EvidenceQuantityBand,
    ReadinessCategory,
    ReadinessDirection,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.mastery_estimation.enums import LearningStabilityBand
from domain.education.recommendation_engine.enums import RecommendationCategory

_OBJECTIVE_LABELS: dict[MissionObjectiveCode, str] = {
    MissionObjectiveCode.COMPLETE_PRACTICE: "Complete practice",
    MissionObjectiveCode.REVIEW_TARGET: "Review",
    MissionObjectiveCode.STRENGTHEN_TARGET: "Strengthen",
    MissionObjectiveCode.ADDRESS_PREREQUISITE: "Address prerequisite",
    MissionObjectiveCode.CONSOLIDATE_TARGET: "Consolidate",
    MissionObjectiveCode.PREPARE_CHECKPOINT: "Prepare for checkpoint",
    MissionObjectiveCode.REVISE_TARGET: "Revise",
    MissionObjectiveCode.MIXED_COVERAGE: "Mixed practice",
    MissionObjectiveCode.RECOVER_CONFIDENCE: "Rebuild confidence",
    MissionObjectiveCode.MAINTAIN_TARGET: "Maintain",
}

_MISSION_TYPE_LABELS: dict[MissionType, str] = {
    MissionType.PRACTICE_QUESTIONS: "Practice questions",
    MissionType.REVIEW_CONCEPT: "Review concept",
    MissionType.STRENGTHEN_FOUNDATION: "Strengthen foundation",
    MissionType.REVISE_PREREQUISITE: "Revise prerequisite",
    MissionType.CONSOLIDATE_KNOWLEDGE: "Consolidate knowledge",
    MissionType.CHECKPOINT_PREPARATION: "Checkpoint preparation",
    MissionType.REVISION_SESSION: "Revision session",
    MissionType.MIXED_PRACTICE: "Mixed practice",
    MissionType.CONFIDENCE_RECOVERY: "Confidence recovery",
    MissionType.MAINTENANCE_REVIEW: "Maintenance review",
}

_RECOMMENDATION_GUIDANCE: dict[RecommendationCategory, str] = {
    RecommendationCategory.REVIEW_CONCEPT: "Review",
    RecommendationCategory.STUDY_PREREQUISITE: "Address prerequisite work for",
    RecommendationCategory.ATTEMPT_CHECKPOINT: "Prepare for checkpoint on",
    RecommendationCategory.STRENGTHEN_WEAK_AREA: "Strengthen",
    RecommendationCategory.DELAY_ADVANCED_TOPIC: "Consolidate foundations before",
    RecommendationCategory.CONTINUE_CURRENT_MISSION: "Continue current work on",
    RecommendationCategory.INCREASE_REVISION_FREQUENCY: "Increase revision for",
    RecommendationCategory.REDUCE_REVISION_FREQUENCY: "Ease revision load for",
    RecommendationCategory.REVISIT_FOUNDATION: "Revisit foundations for",
    RecommendationCategory.MAINTAIN_MASTERY: "Maintain mastery of",
    RecommendationCategory.FOCUS_COMPETENCY: "Complete next mission on",
    RecommendationCategory.PREPARE_ASSESSMENT: "Prepare assessment coverage for",
    RecommendationCategory.CONSOLIDATE_KNOWLEDGE: "Finish revision cycle for",
}

_CATEGORY_FROM_PERCENT: tuple[tuple[float, ReadinessCategory], ...] = (
    (25.0, ReadinessCategory.EARLY_STAGE),
    (50.0, ReadinessCategory.BUILDING),
    (75.0, ReadinessCategory.APPROACHING),
    (90.0, ReadinessCategory.STRONG),
)

_CATEGORY_LABELS: dict[ReadinessCategory, str] = {
    ReadinessCategory.UNAVAILABLE: "Readiness not available yet",
    ReadinessCategory.EARLY_STAGE: "Early stage",
    ReadinessCategory.BUILDING: "Building readiness",
    ReadinessCategory.APPROACHING: "Approaching readiness",
    ReadinessCategory.STRONG: "Strong readiness",
    ReadinessCategory.EXAM_READY: "Exam ready",
}

_DIRECTION_FROM_STABILITY: dict[LearningStabilityBand, ReadinessDirection] = {
    LearningStabilityBand.INSUFFICIENT_DATA: ReadinessDirection.UNKNOWN,
    LearningStabilityBand.VOLATILE: ReadinessDirection.DECLINING,
    LearningStabilityBand.MODERATE: ReadinessDirection.STABLE,
    LearningStabilityBand.STABLE: ReadinessDirection.IMPROVING,
}

_DIRECTION_MESSAGES: dict[ReadinessDirection, str] = {
    ReadinessDirection.UNKNOWN: (
        "Not enough study history to show a readiness direction yet."
    ),
    ReadinessDirection.IMPROVING: "Your readiness is improving.",
    ReadinessDirection.STABLE: "Your readiness is stable.",
    ReadinessDirection.DECLINING: "Your readiness signal is declining.",
}

_CONFIDENCE_FROM_LEVEL: dict[ConfidenceLevel, AssessmentConfidenceCategory] = {
    ConfidenceLevel.VERY_HIGH: AssessmentConfidenceCategory.VERY_HIGH,
    ConfidenceLevel.HIGH: AssessmentConfidenceCategory.HIGH,
    ConfidenceLevel.MEDIUM: AssessmentConfidenceCategory.MODERATE,
    ConfidenceLevel.LOW: AssessmentConfidenceCategory.LIMITED,
    ConfidenceLevel.VERY_LOW: AssessmentConfidenceCategory.LIMITED,
    ConfidenceLevel.UNKNOWN: AssessmentConfidenceCategory.UNKNOWN,
}

_CONFIDENCE_LABELS: dict[AssessmentConfidenceCategory, str] = {
    AssessmentConfidenceCategory.VERY_HIGH: "Very High",
    AssessmentConfidenceCategory.HIGH: "High",
    AssessmentConfidenceCategory.MODERATE: "Moderate",
    AssessmentConfidenceCategory.LIMITED: "Limited",
    AssessmentConfidenceCategory.UNKNOWN: "Unknown",
}

_CONFIDENCE_MESSAGES: dict[AssessmentConfidenceCategory, str] = {
    AssessmentConfidenceCategory.VERY_HIGH: (
        "Assessment confidence is very high based on available evidence."
    ),
    AssessmentConfidenceCategory.HIGH: (
        "Assessment confidence is high based on available evidence."
    ),
    AssessmentConfidenceCategory.MODERATE: (
        "Assessment confidence is moderate — more study evidence will sharpen it."
    ),
    AssessmentConfidenceCategory.LIMITED: (
        "Assessment confidence is limited — keep studying to strengthen the picture."
    ),
    AssessmentConfidenceCategory.UNKNOWN: (
        "Assessment confidence is not available yet."
    ),
}

_QUALITY_FROM_CONFIDENCE: dict[
    AssessmentConfidenceCategory, EvidenceQualityBand
] = {
    AssessmentConfidenceCategory.VERY_HIGH: EvidenceQualityBand.EXCELLENT,
    AssessmentConfidenceCategory.HIGH: EvidenceQualityBand.STRONG,
    AssessmentConfidenceCategory.MODERATE: EvidenceQualityBand.ADEQUATE,
    AssessmentConfidenceCategory.LIMITED: EvidenceQualityBand.LIMITED,
    AssessmentConfidenceCategory.UNKNOWN: EvidenceQualityBand.UNKNOWN,
}

_QUALITY_LABELS: dict[EvidenceQualityBand, str] = {
    EvidenceQualityBand.UNKNOWN: "Unknown",
    EvidenceQualityBand.LIMITED: "Limited",
    EvidenceQualityBand.ADEQUATE: "Adequate",
    EvidenceQualityBand.STRONG: "Strong",
    EvidenceQualityBand.EXCELLENT: "Excellent",
}

_QUANTITY_THRESHOLDS: tuple[tuple[int, EvidenceQuantityBand], ...] = (
    (1, EvidenceQuantityBand.SPARSE),
    (4, EvidenceQuantityBand.MODERATE),
    (8, EvidenceQuantityBand.SUBSTANTIAL),
)

_QUANTITY_LABELS: dict[EvidenceQuantityBand, str] = {
    EvidenceQuantityBand.UNKNOWN: "Unknown",
    EvidenceQuantityBand.SPARSE: "Sparse",
    EvidenceQuantityBand.MODERATE: "Moderate",
    EvidenceQuantityBand.SUBSTANTIAL: "Substantial",
    EvidenceQuantityBand.RICH: "Rich",
}

_CONSISTENCY_FROM_STABILITY: dict[LearningStabilityBand, ConsistencyBand] = {
    LearningStabilityBand.INSUFFICIENT_DATA: ConsistencyBand.UNKNOWN,
    LearningStabilityBand.VOLATILE: ConsistencyBand.UNEVEN,
    LearningStabilityBand.MODERATE: ConsistencyBand.MODERATE,
    LearningStabilityBand.STABLE: ConsistencyBand.CONSISTENT,
}

_CONSISTENCY_LABELS: dict[ConsistencyBand, str] = {
    ConsistencyBand.UNKNOWN: "Unknown",
    ConsistencyBand.UNEVEN: "Uneven",
    ConsistencyBand.MODERATE: "Moderate",
    ConsistencyBand.CONSISTENT: "Consistent",
}


def humanise_identifier(value: str | None) -> str:
    """Turn kebab/snake identifiers into Title Case labels."""
    if value is None:
        return ""
    cleaned = value.strip().replace("_", " ").replace("-", " ")
    if not cleaned:
        return ""
    return " ".join(part.capitalize() for part in cleaned.split())


def mission_title(mission: Mission) -> str:
    """Student-facing mission title from mission type + curriculum scope."""
    type_label = _MISSION_TYPE_LABELS.get(
        mission.mission_type, humanise_identifier(mission.mission_type.value)
    )
    scope = humanise_identifier(mission.competency_id) or humanise_identifier(
        mission.subject_id
    )
    if scope:
        return f"{type_label}: {scope}"
    return type_label


def study_objective_label(mission: Mission) -> str:
    """Student-facing study objective for a mission."""
    base = _OBJECTIVE_LABELS.get(
        mission.objective.code, humanise_identifier(mission.objective.code.value)
    )
    scope = humanise_identifier(mission.objective.competency_id) or humanise_identifier(
        mission.objective.subject_id
    )
    if scope:
        return f"{base} — {scope}"
    return base


def readiness_category_from_percent(percent: float | None) -> ReadinessCategory:
    """Project an existing readiness percent into a student-facing category."""
    if percent is None:
        return ReadinessCategory.UNAVAILABLE
    for threshold, category in _CATEGORY_FROM_PERCENT:
        if percent < threshold:
            return category
    return ReadinessCategory.EXAM_READY


def readiness_category_label(category: ReadinessCategory) -> str:
    return _CATEGORY_LABELS[category]


def readiness_direction_from_stability(
    band: LearningStabilityBand | str | None,
) -> ReadinessDirection:
    """Project existing stability into Improving / Stable / Declining."""
    if band is None:
        return ReadinessDirection.UNKNOWN
    if isinstance(band, str):
        try:
            band = LearningStabilityBand(band)
        except ValueError:
            return ReadinessDirection.UNKNOWN
    return _DIRECTION_FROM_STABILITY.get(band, ReadinessDirection.UNKNOWN)


def readiness_direction_message(direction: ReadinessDirection) -> str:
    return _DIRECTION_MESSAGES[direction]


def assessment_confidence_from_level(
    level: ConfidenceLevel | str | None,
) -> AssessmentConfidenceCategory:
    """Project existing confidence level into assessment-confidence language."""
    if level is None:
        return AssessmentConfidenceCategory.UNKNOWN
    if isinstance(level, str):
        try:
            level = ConfidenceLevel(level)
        except ValueError:
            return AssessmentConfidenceCategory.UNKNOWN
    return _CONFIDENCE_FROM_LEVEL.get(level, AssessmentConfidenceCategory.UNKNOWN)


def assessment_confidence_from_magnitude(
    magnitude: float | None,
) -> AssessmentConfidenceCategory:
    """Project an existing confidence magnitude via foundation ConfidenceLevel."""
    if magnitude is None:
        return AssessmentConfidenceCategory.UNKNOWN
    # Mirror ConfidenceScore band thresholds without inventing new scores.
    if magnitude < 0.20:
        level = ConfidenceLevel.VERY_LOW
    elif magnitude < 0.40:
        level = ConfidenceLevel.LOW
    elif magnitude < 0.60:
        level = ConfidenceLevel.MEDIUM
    elif magnitude < 0.80:
        level = ConfidenceLevel.HIGH
    else:
        level = ConfidenceLevel.VERY_HIGH
    return assessment_confidence_from_level(level)


def assessment_confidence_label(category: AssessmentConfidenceCategory) -> str:
    return _CONFIDENCE_LABELS[category]


def assessment_confidence_message(category: AssessmentConfidenceCategory) -> str:
    return _CONFIDENCE_MESSAGES[category]


def evidence_quality_from_confidence(
    category: AssessmentConfidenceCategory,
) -> EvidenceQualityBand:
    return _QUALITY_FROM_CONFIDENCE.get(category, EvidenceQualityBand.UNKNOWN)


def evidence_quality_label(band: EvidenceQualityBand) -> str:
    return _QUALITY_LABELS[band]


def evidence_quantity_from_count(count: int | None) -> EvidenceQuantityBand:
    if count is None or count < 0:
        return EvidenceQuantityBand.UNKNOWN
    if count == 0:
        return EvidenceQuantityBand.UNKNOWN
    for threshold, band in _QUANTITY_THRESHOLDS:
        if count < threshold:
            return band
    return EvidenceQuantityBand.RICH


def evidence_quantity_label(band: EvidenceQuantityBand) -> str:
    return _QUANTITY_LABELS[band]


def consistency_from_stability(
    band: LearningStabilityBand | str | None,
) -> ConsistencyBand:
    if band is None:
        return ConsistencyBand.UNKNOWN
    if isinstance(band, str):
        try:
            band = LearningStabilityBand(band)
        except ValueError:
            return ConsistencyBand.UNKNOWN
    return _CONSISTENCY_FROM_STABILITY.get(band, ConsistencyBand.UNKNOWN)


def consistency_label(band: ConsistencyBand) -> str:
    return _CONSISTENCY_LABELS[band]


def recommendation_guidance(
    category: RecommendationCategory | str,
    *,
    scope: str | None = None,
) -> str:
    """Compose deterministic guidance text from an existing recommendation."""
    if isinstance(category, str):
        try:
            category = RecommendationCategory(category)
        except ValueError:
            verb = humanise_identifier(category) or "Follow guidance for"
            if scope:
                return f"{verb} {scope}."
            return f"{verb}."
    verb = _RECOMMENDATION_GUIDANCE.get(
        category, humanise_identifier(category.value) or "Follow guidance for"
    )
    if scope:
        return f"{verb} {scope}."
    return f"{verb}."
