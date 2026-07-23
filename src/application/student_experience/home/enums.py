"""Student Home Experience enumerations.

Presentation vocabulary only — never mastery bands, recommendation
categories, or educational reasoning codes exposed as domain types.
"""

from __future__ import annotations

from enum import StrEnum


class FocusActionKind(StrEnum):
    """Primary action the student can take from Today's Focus.

    Labels continue the student's current learning state — never generic
    navigation. PX-002 continuous journey vocabulary.
    """

    START_MISSION = "start_mission"
    RESUME_MISSION = "resume_mission"
    RESUME_SESSION = "resume_session"
    CONTINUE_MISSION = "continue_mission"
    REVIEW_REFLECTION = "review_reflection"
    PREPARE_CHECKPOINT = "prepare_checkpoint"
    VIEW_SCHEDULE = "view_schedule"
    NONE = "none"


class QuickActionKind(StrEnum):
    """Deterministic quick-action kinds on the home surface."""

    START_TODAYS_MISSION = "start_todays_mission"
    RESUME_PAUSED_MISSION = "resume_paused_mission"
    RESUME_SESSION = "resume_session"
    CONTINUE_MISSION = "continue_mission"
    REVIEW_REFLECTION = "review_reflection"
    PREPARE_CHECKPOINT = "prepare_checkpoint"
    REVIEW_YESTERDAY = "review_yesterday"
    VIEW_SCHEDULE = "view_schedule"
    CONTINUE_REVISION = "continue_revision"


class InsightKind(StrEnum):
    """Deterministic learning-insight categories."""

    MOST_IMPROVED_SUBJECT = "most_improved_subject"
    WEAKEST_COMPETENCY = "weakest_competency"
    BIGGEST_OPPORTUNITY = "biggest_opportunity"
    MISSION_COMPLETION_QUALITY = "mission_completion_quality"
    UPCOMING_PREREQUISITE = "upcoming_prerequisite"


class ReadinessTrend(StrEnum):
    """Projected readiness trend language — never a new estimate."""

    UNKNOWN = "unknown"
    IMPROVING = "improving"
    STEADY = "steady"
    NEEDS_ATTENTION = "needs_attention"


class MasteryTrendLabel(StrEnum):
    """Student-facing mastery trend labels projected from existing bands."""

    NOT_YET_ASSESSED = "not_yet_assessed"
    JUST_GETTING_STARTED = "just_getting_started"
    DEVELOPING = "developing"
    STEADY_PROGRESS = "steady_progress"
    STRONG = "strong"


class MilestoneKind(StrEnum):
    """Upcoming milestone kinds on the home surface."""

    STUDY_SESSION = "study_session"
    EXAM = "exam"
    CHECKPOINT = "checkpoint"
    REVISION = "revision"
