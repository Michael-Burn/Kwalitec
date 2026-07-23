"""StudyDay — one calendar day of scheduled study sessions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.education.revision_planner.enums import (
    DayKind,
    SessionStatus,
    WorkloadBand,
)
from application.education.revision_planner.errors import ScheduleInvariantViolation
from application.education.revision_planner.ids import DayId
from application.education.revision_planner.models.study_session import StudySession

_WORKLOAD_THRESHOLDS: tuple[tuple[float, WorkloadBand], ...] = (
    (0.40, WorkloadBand.LIGHT),
    (0.75, WorkloadBand.MODERATE),
    (1.00, WorkloadBand.HEAVY),
)

_INACTIVE = frozenset({SessionStatus.CANCELLED, SessionStatus.RESCHEDULED})


@dataclass(frozen=True, slots=True)
class StudyDay:
    """Immutable calendar day aggregating StudySessions."""

    day_id: DayId
    day_date: date
    sessions: tuple[StudySession, ...] = ()
    available_minutes: int = 0
    kind: DayKind = DayKind.STUDY

    def __post_init__(self) -> None:
        if not isinstance(self.day_id, DayId):
            raise ScheduleInvariantViolation(
                "day_id must be a DayId",
                invariant="StudyDay.day_id.type",
            )
        if not isinstance(self.day_date, date):
            raise ScheduleInvariantViolation(
                "day_date must be a date",
                invariant="StudyDay.day_date.type",
            )
        object.__setattr__(self, "sessions", tuple(self.sessions))
        for session in self.sessions:
            if not isinstance(session, StudySession):
                raise ScheduleInvariantViolation(
                    "sessions must contain StudySession values",
                    invariant="StudyDay.sessions.type",
                )
            if session.session_date != self.day_date:
                raise ScheduleInvariantViolation(
                    "session dates must match StudyDay.day_date",
                    invariant="StudyDay.sessions.date_match",
                )
        if isinstance(self.available_minutes, bool) or not isinstance(
            self.available_minutes, int
        ):
            raise ScheduleInvariantViolation(
                "available_minutes must be an integer",
                invariant="StudyDay.available_minutes.type",
            )
        if self.available_minutes < 0:
            raise ScheduleInvariantViolation(
                "available_minutes must be >= 0",
                invariant="StudyDay.available_minutes.non_negative",
            )
        if not isinstance(self.kind, DayKind):
            raise ScheduleInvariantViolation(
                "kind must be a DayKind",
                invariant="StudyDay.kind.type",
            )

    def active_allocated_minutes(self) -> int:
        return sum(
            s.estimated_duration_minutes
            for s in self.sessions
            if s.status not in _INACTIVE
        )

    @property
    def allocated_minutes(self) -> int:
        return self.active_allocated_minutes()

    def remaining_minutes(self) -> int:
        return max(0, self.available_minutes - self.active_allocated_minutes())

    def is_rest_day(self) -> bool:
        return self.kind is DayKind.REST

    def workload_band(self) -> WorkloadBand:
        if self.available_minutes <= 0:
            if self.active_allocated_minutes() > 0:
                return WorkloadBand.OVERLOADED
            return WorkloadBand.LIGHT
        ratio = self.active_allocated_minutes() / self.available_minutes
        for threshold, band in _WORKLOAD_THRESHOLDS:
            if ratio <= threshold:
                return band
        return WorkloadBand.OVERLOADED

    def with_sessions(self, sessions: tuple[StudySession, ...]) -> StudyDay:
        return StudyDay(
            day_id=self.day_id,
            day_date=self.day_date,
            sessions=sessions,
            available_minutes=self.available_minutes,
            kind=self.kind,
        )
