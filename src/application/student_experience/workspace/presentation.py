"""Student-facing presentation helpers — projection only, no educational reasoning.

Maps existing Education OS primitives into workspace labels. Never estimates
mastery, generates recommendations, generates missions, or invents timers.
"""

from __future__ import annotations

from application.education.mission_execution.enums import (
    ConfidenceTrend,
    ExecutionStatus,
)
from application.education.mission_generation.enums import (
    MissionObjectiveCode,
    MissionPriorityBand,
    MissionStepAction,
    MissionType,
)
from application.education.mission_generation.models.mission import Mission
from application.education.revision_planner.enums import SessionStatus
from application.student_experience.workspace.enums import (
    PriorityLabel,
    TimerDisplayState,
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

_MISSION_PURPOSE: dict[MissionType, str] = {
    MissionType.PRACTICE_QUESTIONS: "Build skill through focused practice.",
    MissionType.REVIEW_CONCEPT: "Revisit the concept so it stays clear.",
    MissionType.STRENGTHEN_FOUNDATION: "Strengthen the foundations you need next.",
    MissionType.REVISE_PREREQUISITE: "Cover prerequisite material first.",
    MissionType.CONSOLIDATE_KNOWLEDGE: "Consolidate what you have already studied.",
    MissionType.CHECKPOINT_PREPARATION: "Prepare for an upcoming checkpoint.",
    MissionType.REVISION_SESSION: "Revise material for lasting recall.",
    MissionType.MIXED_PRACTICE: "Mix practice across related topics.",
    MissionType.CONFIDENCE_RECOVERY: "Rebuild confidence with guided work.",
    MissionType.MAINTENANCE_REVIEW: "Maintain what you already know.",
}

_STEP_ACTION_LABELS: dict[MissionStepAction, str] = {
    MissionStepAction.PRACTICE: "Practice",
    MissionStepAction.REVIEW: "Review",
    MissionStepAction.REVISE: "Revise",
    MissionStepAction.CONSOLIDATE: "Consolidate",
    MissionStepAction.PREPARE: "Prepare",
    MissionStepAction.MAINTAIN: "Maintain",
    MissionStepAction.RECOVER: "Recover",
    MissionStepAction.MIX: "Mixed practice",
}

_PRIORITY_FROM_BAND: dict[MissionPriorityBand, PriorityLabel] = {
    MissionPriorityBand.LOW: PriorityLabel.LOW,
    MissionPriorityBand.MEDIUM: PriorityLabel.MEDIUM,
    MissionPriorityBand.HIGH: PriorityLabel.HIGH,
    MissionPriorityBand.CRITICAL: PriorityLabel.CRITICAL,
}

_PRIORITY_LABELS: dict[PriorityLabel, str] = {
    PriorityLabel.LOW: "Low",
    PriorityLabel.MEDIUM: "Medium",
    PriorityLabel.HIGH: "High",
    PriorityLabel.CRITICAL: "Critical",
    PriorityLabel.UNKNOWN: "Unknown",
}

_CONFIDENCE_TREND_LABELS: dict[ConfidenceTrend, str] = {
    ConfidenceTrend.NONE: "No confidence trend yet",
    ConfidenceTrend.STABLE: "Confidence is steady",
    ConfidenceTrend.RISING: "Confidence is rising",
    ConfidenceTrend.FALLING: "Confidence is falling",
    ConfidenceTrend.MIXED: "Confidence signals are mixed",
}

_TIMER_FROM_EXECUTION: dict[ExecutionStatus, TimerDisplayState] = {
    ExecutionStatus.PLANNED: TimerDisplayState.IDLE,
    ExecutionStatus.STARTED: TimerDisplayState.ACTIVE,
    ExecutionStatus.RESUMED: TimerDisplayState.ACTIVE,
    ExecutionStatus.PAUSED: TimerDisplayState.PAUSED,
    ExecutionStatus.COMPLETED: TimerDisplayState.COMPLETE,
    ExecutionStatus.ABANDONED: TimerDisplayState.COMPLETE,
    ExecutionStatus.EXPIRED: TimerDisplayState.COMPLETE,
}

_TIMER_FROM_SESSION: dict[SessionStatus, TimerDisplayState] = {
    SessionStatus.PLANNED: TimerDisplayState.IDLE,
    SessionStatus.IN_PROGRESS: TimerDisplayState.ACTIVE,
    SessionStatus.COMPLETED: TimerDisplayState.COMPLETE,
    SessionStatus.CANCELLED: TimerDisplayState.COMPLETE,
    SessionStatus.RESCHEDULED: TimerDisplayState.UNAVAILABLE,
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


def mission_purpose(mission: Mission) -> str:
    """Student-facing purpose statement projected from mission type."""
    return _MISSION_PURPOSE.get(
        mission.mission_type,
        "Complete the scheduled study work for this session.",
    )


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


def objective_code_label(code: MissionObjectiveCode) -> str:
    return _OBJECTIVE_LABELS.get(code, humanise_identifier(code.value))


def step_action_label(action: MissionStepAction) -> str:
    return _STEP_ACTION_LABELS.get(action, humanise_identifier(action.value))


def priority_from_band(band: MissionPriorityBand | None) -> PriorityLabel:
    if band is None:
        return PriorityLabel.UNKNOWN
    return _PRIORITY_FROM_BAND.get(band, PriorityLabel.UNKNOWN)


def priority_label(label: PriorityLabel) -> str:
    return _PRIORITY_LABELS[label]


def confidence_trend_label(trend: ConfidenceTrend) -> str:
    return _CONFIDENCE_TREND_LABELS.get(trend, "Confidence trend unavailable")


def timer_state_from_execution(status: ExecutionStatus | None) -> TimerDisplayState:
    if status is None:
        return TimerDisplayState.UNAVAILABLE
    return _TIMER_FROM_EXECUTION.get(status, TimerDisplayState.UNAVAILABLE)


def timer_state_from_session(status: SessionStatus | None) -> TimerDisplayState:
    if status is None:
        return TimerDisplayState.UNAVAILABLE
    return _TIMER_FROM_SESSION.get(status, TimerDisplayState.UNAVAILABLE)


def format_minutes(minutes: int | float | None) -> str:
    """Format a minute count for student-facing display."""
    if minutes is None:
        return "—"
    value = max(0, int(round(float(minutes))))
    if value == 1:
        return "1 minute"
    return f"{value} minutes"


def format_seconds_as_minutes(seconds: float | None) -> str:
    if seconds is None:
        return "—"
    return format_minutes(float(seconds) / 60.0)


def is_checkpoint_mission(mission: Mission | None) -> bool:
    if mission is None:
        return False
    return (
        mission.mission_type is MissionType.CHECKPOINT_PREPARATION
        or mission.objective.code is MissionObjectiveCode.PREPARE_CHECKPOINT
    )
