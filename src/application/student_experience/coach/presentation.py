"""Student-facing presentation helpers — projection only, no educational reasoning.

Maps existing Education OS and Student Experience primitives into coaching
labels. Never estimates mastery, generates recommendations, generates
missions, or calls an LLM.
"""

from __future__ import annotations

from application.education.mission_generation.enums import (
    MissionObjectiveCode,
    MissionType,
)
from application.education.mission_generation.models.mission import Mission

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

_REVISION_TYPES = frozenset(
    {
        MissionType.REVISION_SESSION,
        MissionType.REVISE_PREREQUISITE,
        MissionType.MAINTENANCE_REVIEW,
        MissionType.CONSOLIDATE_KNOWLEDGE,
    }
)


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


def is_revision_mission(mission: Mission | None) -> bool:
    if mission is None:
        return False
    return mission.mission_type in _REVISION_TYPES
