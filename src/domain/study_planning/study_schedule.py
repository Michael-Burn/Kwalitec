"""StudySchedule — globally ordered StudySessions for a plan.

Architecture Source
    SESSION_ASSEMBLY_MODEL.md
Concept
    Study Schedule
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.study_planning.enums import SessionKind
from domain.study_planning.ids import StudySessionId
from domain.study_planning.study_session import StudySession


@dataclass(frozen=True, slots=True)
class StudySchedule(EducationalValueObject):
    """Immutable global ordering of StudySessions across the plan.

    Ordering is educational law: sequence_index must be contiguous from 1.
    Day indices must be non-decreasing along the schedule.
    """

    sessions: tuple[StudySession, ...]

    def _validate(self) -> None:
        if not isinstance(self.sessions, tuple) or not self.sessions:
            raise EducationalInvariantViolation(
                "sessions must be a non-empty tuple",
                invariant="StudySchedule.sessions.min_one",
            )
        seen_ids: set[str] = set()
        previous_day = -1
        for expected_index, session in enumerate(self.sessions, start=1):
            if not isinstance(session, StudySession):
                raise EducationalInvariantViolation(
                    "sessions must contain StudySession values",
                    invariant="StudySchedule.sessions.item_type",
                )
            if session.sequence_index != expected_index:
                raise EducationalInvariantViolation(
                    "sessions must be ordered with contiguous sequence_index "
                    f"starting at 1 (expected {expected_index}, got "
                    f"{session.sequence_index})",
                    invariant="StudySchedule.sessions.sequence_order",
                )
            if session.session_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "schedule must not contain duplicate session identities",
                    invariant="StudySchedule.sessions.unique",
                )
            if session.day_index < previous_day:
                raise EducationalInvariantViolation(
                    "schedule day_index must be non-decreasing",
                    invariant="StudySchedule.sessions.day_order",
                )
            seen_ids.add(session.session_id.value)
            previous_day = session.day_index
        if not any(session.is_work() for session in self.sessions):
            raise EducationalInvariantViolation(
                "schedule must contain at least one work session",
                invariant="StudySchedule.work.min_one",
            )

    @classmethod
    def of(cls, *sessions: StudySession) -> StudySchedule:
        return cls(sessions=tuple(sessions))

    @property
    def length(self) -> int:
        return len(self.sessions)

    def ordered_sessions(self) -> tuple[StudySession, ...]:
        return self.sessions

    def work_sessions(self) -> tuple[StudySession, ...]:
        return tuple(s for s in self.sessions if s.kind is SessionKind.WORK)

    def review_sessions(self) -> tuple[StudySession, ...]:
        return tuple(s for s in self.sessions if s.kind is SessionKind.REVIEW)

    def recovery_sessions(self) -> tuple[StudySession, ...]:
        return tuple(s for s in self.sessions if s.kind is SessionKind.RECOVERY)

    def total_minutes(self) -> int:
        return sum(s.allocated_minutes for s in self.sessions)

    def total_work_minutes(self) -> int:
        return sum(s.allocated_minutes for s in self.work_sessions())

    def total_review_minutes(self) -> int:
        return sum(s.allocated_minutes for s in self.review_sessions())

    def total_recovery_minutes(self) -> int:
        return sum(s.allocated_minutes for s in self.recovery_sessions())

    def session_ids(self) -> tuple[StudySessionId, ...]:
        return tuple(s.session_id for s in self.sessions)

    def index_of(self, session_id: StudySessionId) -> int:
        for session in self.sessions:
            if session.session_id == session_id:
                return session.sequence_index
        raise EducationalInvariantViolation(
            "session is not part of this schedule",
            invariant="StudySchedule.session.not_found",
        )
