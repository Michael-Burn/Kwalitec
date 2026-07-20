"""StudyCalendar — ordered relative-day projection of a StudyPlan.

Architecture Source
    SESSION_ASSEMBLY_MODEL.md
Concept
    Study Calendar

Relative day indices only. No external calendar APIs.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.study_planning.enums import PlanningHorizonBand
from domain.study_planning.study_day import StudyDay
from domain.study_planning.study_session import StudySession


@dataclass(frozen=True, slots=True)
class StudyCalendar(EducationalValueObject):
    """Immutable ordered set of StudyDays spanning the plan horizon."""

    days: tuple[StudyDay, ...]

    def _validate(self) -> None:
        if not isinstance(self.days, tuple) or not self.days:
            raise EducationalInvariantViolation(
                "days must be a non-empty tuple",
                invariant="StudyCalendar.days.min_one",
            )
        seen: set[int] = set()
        previous = -1
        for day in self.days:
            if not isinstance(day, StudyDay):
                raise EducationalInvariantViolation(
                    "days must contain StudyDay values",
                    invariant="StudyCalendar.days.item_type",
                )
            if day.day_index in seen:
                raise EducationalInvariantViolation(
                    "calendar days must declare unique day indices",
                    invariant="StudyCalendar.days.unique",
                )
            if day.day_index < previous:
                raise EducationalInvariantViolation(
                    "calendar days must be ordered by ascending day_index",
                    invariant="StudyCalendar.days.order",
                )
            seen.add(day.day_index)
            previous = day.day_index

    @classmethod
    def of(cls, *days: StudyDay) -> StudyCalendar:
        ordered = tuple(sorted(days, key=lambda d: d.day_index))
        return cls(days=ordered)

    def day_count(self) -> int:
        return len(self.days)

    def active_day_count(self) -> int:
        return sum(1 for day in self.days if not day.is_empty())

    def day_at(self, day_index: int) -> StudyDay | None:
        for day in self.days:
            if day.day_index == day_index:
                return day
        return None

    def all_sessions(self) -> tuple[StudySession, ...]:
        sessions: list[StudySession] = []
        for day in self.days:
            sessions.extend(day.sessions)
        return tuple(sessions)

    def horizon_band(self) -> PlanningHorizonBand:
        active = self.active_day_count()
        if active <= 3:
            return PlanningHorizonBand.COMPACT
        if active <= 7:
            return PlanningHorizonBand.STANDARD
        return PlanningHorizonBand.EXTENDED

    def last_session_day_index(self) -> int:
        last = -1
        for day in self.days:
            if not day.is_empty():
                last = day.day_index
        if last < 0:
            raise EducationalInvariantViolation(
                "calendar has no scheduled sessions",
                invariant="StudyCalendar.last_session.empty",
            )
        return last
