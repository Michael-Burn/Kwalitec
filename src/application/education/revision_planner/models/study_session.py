"""StudySession — one timed block of scheduled mission work."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time

from application.education.mission_generation.enums import MissionObjectiveCode
from application.education.mission_generation.ids import MissionId
from application.education.revision_planner.enums import SessionPriority, SessionStatus
from application.education.revision_planner.errors import ScheduleInvariantViolation
from application.education.revision_planner.ids import SessionId
from application.education.revision_planner.models.completion_metrics import (
    CompletionMetrics,
)


@dataclass(frozen=True, slots=True)
class StudySession:
    """Immutable timed study session containing scheduled mission references.

    Sessions organise existing mission work. They never invent missions.
    """

    session_id: SessionId
    session_date: date
    start_time: time
    end_time: time
    estimated_duration_minutes: int
    scheduled_mission_ids: tuple[MissionId, ...]
    objectives: tuple[MissionObjectiveCode, ...] = ()
    priority: SessionPriority = SessionPriority.MEDIUM
    status: SessionStatus = SessionStatus.PLANNED
    completion_metrics: CompletionMetrics | None = None
    sequence_index: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.session_id, SessionId):
            raise ScheduleInvariantViolation(
                "session_id must be a SessionId",
                invariant="StudySession.session_id.type",
            )
        if not isinstance(self.session_date, date):
            raise ScheduleInvariantViolation(
                "session_date must be a date",
                invariant="StudySession.session_date.type",
            )
        if not isinstance(self.start_time, time):
            raise ScheduleInvariantViolation(
                "start_time must be a time",
                invariant="StudySession.start_time.type",
            )
        if not isinstance(self.end_time, time):
            raise ScheduleInvariantViolation(
                "end_time must be a time",
                invariant="StudySession.end_time.type",
            )
        if self.start_time >= self.end_time:
            raise ScheduleInvariantViolation(
                "start_time must be before end_time",
                invariant="StudySession.time.order",
            )
        if isinstance(self.estimated_duration_minutes, bool) or not isinstance(
            self.estimated_duration_minutes, int
        ):
            raise ScheduleInvariantViolation(
                "estimated_duration_minutes must be an integer",
                invariant="StudySession.estimated_duration_minutes.type",
            )
        if self.estimated_duration_minutes < 1:
            raise ScheduleInvariantViolation(
                "estimated_duration_minutes must be >= 1",
                invariant="StudySession.estimated_duration_minutes.positive",
            )
        object.__setattr__(
            self, "scheduled_mission_ids", tuple(self.scheduled_mission_ids)
        )
        if not self.scheduled_mission_ids:
            raise ScheduleInvariantViolation(
                "scheduled_mission_ids must not be empty",
                invariant="StudySession.scheduled_mission_ids.min_one",
            )
        for mission_id in self.scheduled_mission_ids:
            if not isinstance(mission_id, MissionId):
                raise ScheduleInvariantViolation(
                    "scheduled_mission_ids must contain MissionId values",
                    invariant="StudySession.scheduled_mission_ids.type",
                )
        object.__setattr__(self, "objectives", tuple(self.objectives))
        for objective in self.objectives:
            if not isinstance(objective, MissionObjectiveCode):
                raise ScheduleInvariantViolation(
                    "objectives must contain MissionObjectiveCode values",
                    invariant="StudySession.objectives.type",
                )
        if not isinstance(self.priority, SessionPriority):
            raise ScheduleInvariantViolation(
                "priority must be a SessionPriority",
                invariant="StudySession.priority.type",
            )
        if not isinstance(self.status, SessionStatus):
            raise ScheduleInvariantViolation(
                "status must be a SessionStatus",
                invariant="StudySession.status.type",
            )
        if self.completion_metrics is not None and not isinstance(
            self.completion_metrics, CompletionMetrics
        ):
            raise ScheduleInvariantViolation(
                "completion_metrics must be a CompletionMetrics when provided",
                invariant="StudySession.completion_metrics.type",
            )
        if isinstance(self.sequence_index, bool) or not isinstance(
            self.sequence_index, int
        ):
            raise ScheduleInvariantViolation(
                "sequence_index must be an integer",
                invariant="StudySession.sequence_index.type",
            )
        if self.sequence_index < 1:
            raise ScheduleInvariantViolation(
                "sequence_index must be >= 1",
                invariant="StudySession.sequence_index.positive",
            )

    def with_status(
        self,
        status: SessionStatus,
        *,
        completion_metrics: CompletionMetrics | None = None,
    ) -> StudySession:
        return StudySession(
            session_id=self.session_id,
            session_date=self.session_date,
            start_time=self.start_time,
            end_time=self.end_time,
            estimated_duration_minutes=self.estimated_duration_minutes,
            scheduled_mission_ids=self.scheduled_mission_ids,
            objectives=self.objectives,
            priority=self.priority,
            status=status,
            completion_metrics=(
                completion_metrics
                if completion_metrics is not None
                else self.completion_metrics
            ),
            sequence_index=self.sequence_index,
        )

    def with_timing(
        self,
        *,
        session_date: date | None = None,
        start_time: time | None = None,
        end_time: time | None = None,
        sequence_index: int | None = None,
    ) -> StudySession:
        return StudySession(
            session_id=self.session_id,
            session_date=(
                session_date if session_date is not None else self.session_date
            ),
            start_time=start_time if start_time is not None else self.start_time,
            end_time=end_time if end_time is not None else self.end_time,
            estimated_duration_minutes=self.estimated_duration_minutes,
            scheduled_mission_ids=self.scheduled_mission_ids,
            objectives=self.objectives,
            priority=self.priority,
            status=self.status,
            completion_metrics=self.completion_metrics,
            sequence_index=(
                sequence_index if sequence_index is not None else self.sequence_index
            ),
        )

    def is_active(self) -> bool:
        return self.status in (SessionStatus.PLANNED, SessionStatus.IN_PROGRESS)

    def is_terminal(self) -> bool:
        return self.status in (
            SessionStatus.COMPLETED,
            SessionStatus.CANCELLED,
            SessionStatus.RESCHEDULED,
        )
