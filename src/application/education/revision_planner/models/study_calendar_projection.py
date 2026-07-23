"""StudyCalendarProjection — flattened calendar view of a schedule."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.education.revision_planner.enums import DayKind
from application.education.revision_planner.errors import ScheduleInvariantViolation
from application.education.revision_planner.ids import DayId, SessionId


@dataclass(frozen=True, slots=True)
class CalendarDayProjection:
    """One projected calendar day for UI / downstream consumers."""

    day_id: DayId
    day_date: date
    kind: DayKind
    session_ids: tuple[SessionId, ...]
    allocated_minutes: int
    available_minutes: int

    def __post_init__(self) -> None:
        if not isinstance(self.day_id, DayId):
            raise ScheduleInvariantViolation(
                "day_id must be a DayId",
                invariant="CalendarDayProjection.day_id.type",
            )
        if not isinstance(self.day_date, date):
            raise ScheduleInvariantViolation(
                "day_date must be a date",
                invariant="CalendarDayProjection.day_date.type",
            )
        if not isinstance(self.kind, DayKind):
            raise ScheduleInvariantViolation(
                "kind must be a DayKind",
                invariant="CalendarDayProjection.kind.type",
            )
        object.__setattr__(self, "session_ids", tuple(self.session_ids))
        for session_id in self.session_ids:
            if not isinstance(session_id, SessionId):
                raise ScheduleInvariantViolation(
                    "session_ids must contain SessionId values",
                    invariant="CalendarDayProjection.session_ids.type",
                )
        for name, value in (
            ("allocated_minutes", self.allocated_minutes),
            ("available_minutes", self.available_minutes),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ScheduleInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"CalendarDayProjection.{name}.type",
                )
            if value < 0:
                raise ScheduleInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"CalendarDayProjection.{name}.non_negative",
                )


@dataclass(frozen=True, slots=True)
class StudyCalendarProjection:
    """Immutable calendar projection of a StudySchedule."""

    days: tuple[CalendarDayProjection, ...] = ()
    horizon_start: date | None = None
    horizon_end: date | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "days", tuple(self.days))
        for day in self.days:
            if not isinstance(day, CalendarDayProjection):
                raise ScheduleInvariantViolation(
                    "days must contain CalendarDayProjection values",
                    invariant="StudyCalendarProjection.days.type",
                )
        if self.horizon_start is not None and not isinstance(self.horizon_start, date):
            raise ScheduleInvariantViolation(
                "horizon_start must be a date when provided",
                invariant="StudyCalendarProjection.horizon_start.type",
            )
        if self.horizon_end is not None and not isinstance(self.horizon_end, date):
            raise ScheduleInvariantViolation(
                "horizon_end must be a date when provided",
                invariant="StudyCalendarProjection.horizon_end.type",
            )
        if (
            self.horizon_start is not None
            and self.horizon_end is not None
            and self.horizon_end < self.horizon_start
        ):
            raise ScheduleInvariantViolation(
                "horizon_end must be on or after horizon_start",
                invariant="StudyCalendarProjection.horizon.order",
            )

    def day_count(self) -> int:
        return len(self.days)

    def study_day_count(self) -> int:
        return sum(1 for d in self.days if d.kind is DayKind.STUDY)
