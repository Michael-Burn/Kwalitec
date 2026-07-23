"""Learning Journey Experience enumerations.

Presentation vocabulary only — never mastery bands, recommendation
categories, or educational reasoning codes exposed as domain types.
"""

from __future__ import annotations

from enum import StrEnum


class TimelineEventKind(StrEnum):
    """Descriptive timeline event kinds — never explanatory reasoning."""

    MISSION_COMPLETED = "mission_completed"
    MISSION_SCHEDULED = "mission_scheduled"
    MASTERY_IMPROVED = "mastery_improved"
    RECOMMENDATION_CHANGED = "recommendation_changed"
    CHECKPOINT_COMPLETED = "checkpoint_completed"
    COMPETENCY_STRENGTHENED = "competency_strengthened"
    EVALUATION_RECORDED = "evaluation_recorded"
    MILESTONE_REACHED = "milestone_reached"


class TrendDirection(StrEnum):
    """Historical trend direction — never a forecast."""

    UNKNOWN = "unknown"
    IMPROVING = "improving"
    STEADY = "steady"
    DECLINING = "declining"


class TrajectoryLabel(StrEnum):
    """Student-facing trajectory language projected from history."""

    UNKNOWN = "unknown"
    JUST_STARTING = "just_starting"
    BUILDING = "building"
    STEADY = "steady"
    ACCELERATING = "accelerating"


class StudyTimeBand(StrEnum):
    """Preferred study-time band projected from session start hours."""

    UNKNOWN = "unknown"
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class JourneyMilestoneKind(StrEnum):
    """Educational milestone kinds projected for the journey surface."""

    FIRST_MISSION = "first_mission"
    FIRST_REVISION_CYCLE = "first_revision_cycle"
    COMPETENCY_MASTERED = "competency_mastered"
    SUBJECT_FINISHED = "subject_finished"
    READINESS_TARGET = "readiness_target"
    STREAK = "streak"
    CUSTOM = "custom"


class WeekdayLabel(StrEnum):
    """Student-facing weekday labels."""

    UNKNOWN = "unknown"
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
