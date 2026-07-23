"""StudentAvailability — caller-supplied calendar availability windows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time

from application.education.revision_planner.enums import Weekday
from application.education.revision_planner.errors import ScheduleInvariantViolation


@dataclass(frozen=True, slots=True)
class AvailabilityWindow:
    """One contiguous availability window on a calendar day."""

    day: date
    start_time: time
    end_time: time
    available_minutes: int

    def __post_init__(self) -> None:
        if not isinstance(self.day, date):
            raise ScheduleInvariantViolation(
                "day must be a date",
                invariant="AvailabilityWindow.day.type",
            )
        if not isinstance(self.start_time, time):
            raise ScheduleInvariantViolation(
                "start_time must be a time",
                invariant="AvailabilityWindow.start_time.type",
            )
        if not isinstance(self.end_time, time):
            raise ScheduleInvariantViolation(
                "end_time must be a time",
                invariant="AvailabilityWindow.end_time.type",
            )
        if self.start_time >= self.end_time:
            raise ScheduleInvariantViolation(
                "start_time must be before end_time",
                invariant="AvailabilityWindow.time.order",
            )
        if isinstance(self.available_minutes, bool) or not isinstance(
            self.available_minutes, int
        ):
            raise ScheduleInvariantViolation(
                "available_minutes must be an integer",
                invariant="AvailabilityWindow.available_minutes.type",
            )
        if self.available_minutes < 1:
            raise ScheduleInvariantViolation(
                "available_minutes must be >= 1",
                invariant="AvailabilityWindow.available_minutes.positive",
            )


@dataclass(frozen=True, slots=True)
class StudentAvailability:
    """Immutable student availability supplied by the caller.

    When ``windows`` is empty, the planner synthesises default daily windows
    from PlanningConstraints and the planning horizon.
    """

    student_id: str
    windows: tuple[AvailabilityWindow, ...] = ()
    unavailable_dates: tuple[date, ...] = ()
    preferred_weekdays: tuple[Weekday, ...] = ()

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ScheduleInvariantViolation(
                "student_id must be a non-empty string",
                invariant="StudentAvailability.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        object.__setattr__(self, "windows", tuple(self.windows))
        for window in self.windows:
            if not isinstance(window, AvailabilityWindow):
                raise ScheduleInvariantViolation(
                    "windows must contain AvailabilityWindow values",
                    invariant="StudentAvailability.windows.type",
                )
        unavailable = tuple(sorted(set(self.unavailable_dates)))
        for day in unavailable:
            if not isinstance(day, date):
                raise ScheduleInvariantViolation(
                    "unavailable_dates must contain date values",
                    invariant="StudentAvailability.unavailable_dates.type",
                )
        object.__setattr__(self, "unavailable_dates", unavailable)
        preferred = tuple(self.preferred_weekdays)
        for weekday in preferred:
            if not isinstance(weekday, Weekday):
                raise ScheduleInvariantViolation(
                    "preferred_weekdays must contain Weekday values",
                    invariant="StudentAvailability.preferred_weekdays.type",
                )
        object.__setattr__(self, "preferred_weekdays", preferred)

    def is_unavailable(self, day: date) -> bool:
        return day in self.unavailable_dates

    def windows_for(self, day: date) -> tuple[AvailabilityWindow, ...]:
        return tuple(w for w in self.windows if w.day == day)

    def total_available_minutes(self) -> int:
        return sum(w.available_minutes for w in self.windows)
