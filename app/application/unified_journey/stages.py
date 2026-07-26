"""Canonical Unified Student Journey stages (P2-MS001).

Immutable identifiers for Experience Layer orchestration.
Stages organise Programme I capabilities into one end-to-end student
journey. They do not encode educational law.
"""

from __future__ import annotations

from enum import StrEnum


class JourneyStage(StrEnum):
    """Canonical student journey stages.

    Identifiers are immutable product vocabulary for Experience navigation
    and coordination. Educational decisions remain in Programme I engines.
    """

    ONBOARDING = "onboarding"
    PLANNING = "planning"
    DAILY_MISSION = "daily_mission"
    STUDY_SESSION = "study_session"
    SESSION_REFLECTION = "session_reflection"
    WEEKLY_REVIEW = "weekly_review"
    REVISION_MODE = "revision_mode"
    EXAM_READINESS = "exam_readiness"
    LEARNING_ARCHIVE = "learning_archive"


# Stable canonical order for progress / chrome (not a state machine).
CANONICAL_JOURNEY_STAGES: tuple[JourneyStage, ...] = (
    JourneyStage.ONBOARDING,
    JourneyStage.PLANNING,
    JourneyStage.DAILY_MISSION,
    JourneyStage.STUDY_SESSION,
    JourneyStage.SESSION_REFLECTION,
    JourneyStage.WEEKLY_REVIEW,
    JourneyStage.REVISION_MODE,
    JourneyStage.EXAM_READINESS,
    JourneyStage.LEARNING_ARCHIVE,
)

STAGE_LABELS: dict[JourneyStage, str] = {
    JourneyStage.ONBOARDING: "Onboarding",
    JourneyStage.PLANNING: "Planning",
    JourneyStage.DAILY_MISSION: "Today",
    JourneyStage.STUDY_SESSION: "Study Session",
    JourneyStage.SESSION_REFLECTION: "Reflection",
    JourneyStage.WEEKLY_REVIEW: "Weekly Review",
    JourneyStage.REVISION_MODE: "Revision",
    JourneyStage.EXAM_READINESS: "Exam Readiness",
    JourneyStage.LEARNING_ARCHIVE: "Archive",
}

# Stages shown in primary Experience chrome when unified journey is enabled.
# Flow-only stages (Study Session, Session Reflection) stay out of primary nav.
# Weekly Review shares History until a dedicated surface exists — omitted from
# chrome so Archive remains the single History destination.
PRIMARY_NAV_STAGES: tuple[JourneyStage, ...] = (
    JourneyStage.DAILY_MISSION,
    JourneyStage.PLANNING,
    JourneyStage.EXAM_READINESS,
    JourneyStage.REVISION_MODE,
    JourneyStage.LEARNING_ARCHIVE,
    JourneyStage.ONBOARDING,
)


def resolve_journey_stage(value: JourneyStage | str) -> JourneyStage:
    """Resolve a stage identifier; raises ``ValueError`` when unknown."""
    if isinstance(value, JourneyStage):
        return value
    key = str(value).strip().lower()
    try:
        return JourneyStage(key)
    except ValueError as exc:
        raise ValueError(f"unknown journey stage: {value!r}") from exc


def is_canonical_stage(value: JourneyStage | str) -> bool:
    """True when ``value`` is a known canonical journey stage."""
    try:
        resolve_journey_stage(value)
        return True
    except ValueError:
        return False


def stage_label(value: JourneyStage | str) -> str:
    """Human label for a journey stage (Experience chrome only)."""
    return STAGE_LABELS[resolve_journey_stage(value)]
