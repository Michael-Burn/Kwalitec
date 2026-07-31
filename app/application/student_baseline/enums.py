"""SB-001A closed declaration vocabulary — self-assessment only."""

from __future__ import annotations

from enum import StrEnum


class BaselineStatus(StrEnum):
    """Lifecycle of a Baseline row."""

    DRAFT = "draft"
    COMPLETE = "complete"
    SUPERSEDED = "superseded"


class PreviousExperience(StrEnum):
    """Have you studied this subject before?"""

    BRAND_NEW = "brand_new"
    STARTED = "started"
    ABOUT_HALFWAY = "about_halfway"
    MOSTLY_COMPLETED = "mostly_completed"
    REVISION_PHASE = "revision_phase"


class PositionMode(StrEnum):
    """Curriculum position choice."""

    START_BEGINNING = "start_beginning"
    CONTINUE_TOPIC = "continue_topic"


class ExamHistory(StrEnum):
    """Previous exam attempt posture."""

    FIRST_SITTING = "first_sitting"
    PREVIOUSLY_ATTEMPTED = "previously_attempted"


class LearningObjective(StrEnum):
    """What should Kwalitec do?"""

    CONTINUE = "continue"
    RESTART = "restart"
    RECOMMEND = "recommend"


class ConfidenceBand(StrEnum):
    """Self-assessed confidence — never a diagnostic."""

    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


EXPERIENCE_LABELS: dict[PreviousExperience, str] = {
    PreviousExperience.BRAND_NEW: "Brand new",
    PreviousExperience.STARTED: "Started",
    PreviousExperience.ABOUT_HALFWAY: "About halfway",
    PreviousExperience.MOSTLY_COMPLETED: "Mostly completed",
    PreviousExperience.REVISION_PHASE: "Revision phase",
}

OBJECTIVE_LABELS: dict[LearningObjective, str] = {
    LearningObjective.CONTINUE: "Continue where I stopped",
    LearningObjective.RESTART: "Restart from the beginning",
    LearningObjective.RECOMMEND: "Recommend the best starting point",
}

CONFIDENCE_LABELS: dict[ConfidenceBand, str] = {
    ConfidenceBand.VERY_LOW: "Very low",
    ConfidenceBand.LOW: "Low",
    ConfidenceBand.MODERATE: "Moderate",
    ConfidenceBand.HIGH: "High",
    ConfidenceBand.VERY_HIGH: "Very high",
}

EXAM_HISTORY_LABELS: dict[ExamHistory, str] = {
    ExamHistory.FIRST_SITTING: "First sitting",
    ExamHistory.PREVIOUSLY_ATTEMPTED: "Previously attempted",
}

POSITION_MODE_LABELS: dict[PositionMode, str] = {
    PositionMode.START_BEGINNING: "Start from the beginning",
    PositionMode.CONTINUE_TOPIC: "Continue from a completed chapter/topic",
}
