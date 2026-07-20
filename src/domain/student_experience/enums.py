"""Student Experience enumerations.

Vocabulary for deterministic presentation projections. These labels describe
engagement and recognition chrome — never educational decisions, mastery
claims, or recommendation mutations.
"""

from __future__ import annotations

from enum import StrEnum


class AchievementKind(StrEnum):
    """Catalogue of presentation achievements recognised from Educational OS outputs."""

    FIRST_MISSION = "first_mission"
    STREAK_THREE = "streak_three"
    STREAK_SEVEN = "streak_seven"
    MISSIONS_FIVE = "missions_five"
    IMPROVING_MASTERY = "improving_mastery"
    STABLE_KNOWLEDGE = "stable_knowledge"
    EFFECTIVE_REVISION = "effective_revision"
    PLAN_PROGRESS = "plan_progress"


class CelebrationKind(StrEnum):
    """Kinds of progress celebration presentation events."""

    ACHIEVEMENT = "achievement"
    STREAK = "streak"
    PROGRESS = "progress"
    MILESTONE = "milestone"


class MotivationTone(StrEnum):
    """Deterministic motivational messaging tone bands."""

    ENCOURAGING = "encouraging"
    STEADY = "steady"
    RECOVERING = "recovering"
    CELEBRATORY = "celebratory"


class ReminderKind(StrEnum):
    """Kinds of presentation reminders derived from plans and recommendations."""

    REVIEW_WINDOW = "review_window"
    REVISION_FOCUS = "revision_focus"
    NEXT_SESSION = "next_session"
    CONTINUE_MISSION = "continue_mission"


class StreakBand(StrEnum):
    """Qualitative band for LearningStreak length."""

    NONE = "none"
    STARTING = "starting"  # 1–2 days
    BUILDING = "building"  # 3–6 days
    STRONG = "strong"  # 7+ days


class MilestoneKind(StrEnum):
    """Presentation milestone recognition categories."""

    FIRST_COMPLETION = "first_completion"
    STREAK_THRESHOLD = "streak_threshold"
    MISSION_COUNT = "mission_count"
    PROGRESS_SIGNAL = "progress_signal"
    PLAN_SIGNAL = "plan_signal"
