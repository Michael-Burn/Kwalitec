"""Student-facing presentation helpers — projection only, no educational reasoning.

Maps existing Education OS primitives into human-readable labels. Never
estimates mastery, generates recommendations, or invents missions.
"""

from __future__ import annotations

from application.education.mission_generation.enums import (
    MissionObjectiveCode,
    MissionType,
)
from application.education.mission_generation.models.mission import Mission
from application.student_experience.home.enums import (
    MasteryTrendLabel,
    ReadinessTrend,
)
from domain.education.mastery_estimation.enums import (
    LearningStabilityBand,
    MasteryBand,
)

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

_MASTERY_TREND: dict[MasteryBand, MasteryTrendLabel] = {
    MasteryBand.NOT_ASSESSED: MasteryTrendLabel.NOT_YET_ASSESSED,
    MasteryBand.NOT_STARTED: MasteryTrendLabel.JUST_GETTING_STARTED,
    MasteryBand.DEVELOPING: MasteryTrendLabel.DEVELOPING,
    MasteryBand.SECURE: MasteryTrendLabel.STEADY_PROGRESS,
    MasteryBand.MASTERED: MasteryTrendLabel.STRONG,
}

_MASTERY_MESSAGES: dict[MasteryTrendLabel, str] = {
    MasteryTrendLabel.NOT_YET_ASSESSED: (
        "Your progress will appear once you start studying."
    ),
    MasteryTrendLabel.JUST_GETTING_STARTED: "You're just getting started — keep going.",
    MasteryTrendLabel.DEVELOPING: "You're building foundations.",
    MasteryTrendLabel.STEADY_PROGRESS: "You're making steady progress.",
    MasteryTrendLabel.STRONG: "Your mastery is looking strong.",
}

_READINESS_TREND: dict[LearningStabilityBand, ReadinessTrend] = {
    LearningStabilityBand.INSUFFICIENT_DATA: ReadinessTrend.UNKNOWN,
    LearningStabilityBand.VOLATILE: ReadinessTrend.NEEDS_ATTENTION,
    LearningStabilityBand.MODERATE: ReadinessTrend.STEADY,
    LearningStabilityBand.STABLE: ReadinessTrend.IMPROVING,
}

_READINESS_MESSAGES: dict[ReadinessTrend, str] = {
    ReadinessTrend.UNKNOWN: (
        "Not enough study history to show a readiness trend yet."
    ),
    ReadinessTrend.NEEDS_ATTENTION: (
        "Your readiness signal is uneven — consistent study will help."
    ),
    ReadinessTrend.STEADY: "Your readiness is holding steady.",
    ReadinessTrend.IMPROVING: "Your readiness trend looks encouraging.",
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


def mastery_trend_from_band(band: MasteryBand | str | None) -> MasteryTrendLabel:
    """Project an existing mastery band into a student-facing trend label."""
    if band is None:
        return MasteryTrendLabel.NOT_YET_ASSESSED
    if isinstance(band, str):
        try:
            band = MasteryBand(band)
        except ValueError:
            return MasteryTrendLabel.NOT_YET_ASSESSED
    return _MASTERY_TREND.get(band, MasteryTrendLabel.NOT_YET_ASSESSED)


def mastery_message_for(trend: MasteryTrendLabel) -> str:
    return _MASTERY_MESSAGES[trend]


def readiness_trend_from_stability(
    band: LearningStabilityBand | str | None,
) -> ReadinessTrend:
    """Project existing stability into a readiness trend — never re-estimate."""
    if band is None:
        return ReadinessTrend.UNKNOWN
    if isinstance(band, str):
        try:
            band = LearningStabilityBand(band)
        except ValueError:
            return ReadinessTrend.UNKNOWN
    return _READINESS_TREND.get(band, ReadinessTrend.UNKNOWN)


def readiness_message_for(trend: ReadinessTrend) -> str:
    return _READINESS_MESSAGES[trend]


def readiness_label_from_percent(percent: float | None) -> str:
    if percent is None:
        return "Readiness not available yet"
    if percent < 25.0:
        return "Early stage"
    if percent < 50.0:
        return "Building readiness"
    if percent < 75.0:
        return "Approaching readiness"
    if percent < 90.0:
        return "Strong readiness"
    return "Exam ready"
