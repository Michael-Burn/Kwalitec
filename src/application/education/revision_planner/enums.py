"""Adaptive Revision Planner enumerations.

Scheduling vocabulary for organising MissionPlan work into a StudySchedule.
Categories here describe calendar organisation — never mastery bands,
recommendation intent, or mission generation.
"""

from __future__ import annotations

from enum import StrEnum


class SessionStatus(StrEnum):
    """Lifecycle status of a StudySession."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


class SessionPriority(StrEnum):
    """Qualitative priority band for a study session."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ScheduledMissionStatus(StrEnum):
    """Placement status of a mission inside a schedule."""

    PENDING = "pending"
    PARTIAL = "partial"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ABANDONED = "abandoned"


class DayKind(StrEnum):
    """Classification of a calendar day within a study schedule."""

    STUDY = "study"
    REST = "rest"
    EXAM = "exam"
    HOLIDAY = "holiday"
    UNAVAILABLE = "unavailable"


class WorkloadBand(StrEnum):
    """Qualitative daily workload intensity."""

    LIGHT = "light"
    MODERATE = "moderate"
    HEAVY = "heavy"
    OVERLOADED = "overloaded"


class SpacingPolicy(StrEnum):
    """How maintenance / review missions are spaced across the schedule."""

    COMPACT = "compact"
    BALANCED = "balanced"
    DISTRIBUTED = "distributed"


class AbandonmentPolicy(StrEnum):
    """How abandoned missions are treated when replanning."""

    RESCHEDULE_EARLY = "reschedule_early"
    RESCHEDULE_NEXT_AVAILABLE = "reschedule_next_available"
    DEFER_TO_END = "defer_to_end"
    DROP = "drop"


class Weekday(StrEnum):
    """ISO weekday (Monday=1 … Sunday=7) as a stable enum."""

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    @classmethod
    def from_iso(cls, iso_weekday: int) -> Weekday:
        mapping = {
            1: cls.MONDAY,
            2: cls.TUESDAY,
            3: cls.WEDNESDAY,
            4: cls.THURSDAY,
            5: cls.FRIDAY,
            6: cls.SATURDAY,
            7: cls.SUNDAY,
        }
        if iso_weekday not in mapping:
            raise ValueError(f"iso_weekday must be 1..7, got {iso_weekday}")
        return mapping[iso_weekday]

    def to_iso(self) -> int:
        return {
            Weekday.MONDAY: 1,
            Weekday.TUESDAY: 2,
            Weekday.WEDNESDAY: 3,
            Weekday.THURSDAY: 4,
            Weekday.FRIDAY: 5,
            Weekday.SATURDAY: 6,
            Weekday.SUNDAY: 7,
        }[self]
