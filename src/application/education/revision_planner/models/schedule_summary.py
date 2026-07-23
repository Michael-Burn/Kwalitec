"""ScheduleSummary — compact overview of a StudySchedule."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.education.revision_planner.errors import ScheduleInvariantViolation
from application.education.revision_planner.ids import ScheduleId


@dataclass(frozen=True, slots=True)
class ScheduleSummary:
    """Immutable summary derived from a StudySchedule."""

    schedule_id: ScheduleId
    student_id: str
    start_date: date
    end_date: date
    study_day_count: int
    session_count: int
    mission_count: int
    total_allocated_minutes: int
    average_daily_minutes: float
    utilises_exam_deadline: bool = False
    utilises_target_completion: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.schedule_id, ScheduleId):
            raise ScheduleInvariantViolation(
                "schedule_id must be a ScheduleId",
                invariant="ScheduleSummary.schedule_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ScheduleInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ScheduleSummary.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.start_date, date):
            raise ScheduleInvariantViolation(
                "start_date must be a date",
                invariant="ScheduleSummary.start_date.type",
            )
        if not isinstance(self.end_date, date):
            raise ScheduleInvariantViolation(
                "end_date must be a date",
                invariant="ScheduleSummary.end_date.type",
            )
        if self.end_date < self.start_date:
            raise ScheduleInvariantViolation(
                "end_date must be on or after start_date",
                invariant="ScheduleSummary.date_order",
            )
        for name in (
            "study_day_count",
            "session_count",
            "mission_count",
            "total_allocated_minutes",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ScheduleInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"ScheduleSummary.{name}.type",
                )
            if value < 0:
                raise ScheduleInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ScheduleSummary.{name}.non_negative",
                )
        if isinstance(self.average_daily_minutes, bool) or not isinstance(
            self.average_daily_minutes, int | float
        ):
            raise ScheduleInvariantViolation(
                "average_daily_minutes must be a real number",
                invariant="ScheduleSummary.average_daily_minutes.type",
            )
        object.__setattr__(
            self, "average_daily_minutes", round(float(self.average_daily_minutes), 4)
        )
