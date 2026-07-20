"""StudyDay — one relative planning day with allocated sessions.

Architecture Source
    SESSION_ASSEMBLY_MODEL.md (capacity honesty)
Concept
    Study Day
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.study_planning.study_session import StudySession


@dataclass(frozen=True, slots=True)
class StudyDay(EducationalValueObject):
    """Immutable daily container for scheduled StudySessions.

    Capacity honesty: allocated session minutes must not exceed available
    minutes for the day.
    """

    day_index: int
    available_minutes: int
    sessions: tuple[StudySession, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.day_index, int) or isinstance(self.day_index, bool):
            raise EducationalInvariantViolation(
                "day_index must be an integer",
                invariant="StudyDay.day_index.type",
            )
        if self.day_index < 0:
            raise EducationalInvariantViolation(
                "day_index must be non-negative",
                invariant="StudyDay.day_index.non_negative",
            )
        if not isinstance(self.available_minutes, int) or isinstance(
            self.available_minutes, bool
        ):
            raise EducationalInvariantViolation(
                "available_minutes must be an integer",
                invariant="StudyDay.available_minutes.type",
            )
        if self.available_minutes <= 0:
            raise EducationalInvariantViolation(
                "available_minutes must be positive",
                invariant="StudyDay.available_minutes.positive",
            )
        if not isinstance(self.sessions, tuple):
            raise EducationalInvariantViolation(
                "sessions must be a tuple of StudySession",
                invariant="StudyDay.sessions.type",
            )
        previous_sequence = 0
        for session in self.sessions:
            if not isinstance(session, StudySession):
                raise EducationalInvariantViolation(
                    "sessions must contain StudySession values",
                    invariant="StudyDay.sessions.item_type",
                )
            if session.day_index != self.day_index:
                raise EducationalInvariantViolation(
                    "session day_index must match StudyDay.day_index",
                    invariant="StudyDay.sessions.day_match",
                )
            if session.sequence_index <= previous_sequence:
                raise EducationalInvariantViolation(
                    "sessions on a day must appear in ascending sequence_index",
                    invariant="StudyDay.sessions.sequence_order",
                )
            previous_sequence = session.sequence_index
        if self.allocated_minutes() > self.available_minutes:
            raise EducationalInvariantViolation(
                "allocated session minutes must not exceed available minutes",
                invariant="StudyDay.capacity.honesty",
            )

    def allocated_minutes(self) -> int:
        return sum(session.allocated_minutes for session in self.sessions)

    def remaining_minutes(self) -> int:
        return self.available_minutes - self.allocated_minutes()

    def session_count(self) -> int:
        return len(self.sessions)

    def is_empty(self) -> bool:
        return not self.sessions
