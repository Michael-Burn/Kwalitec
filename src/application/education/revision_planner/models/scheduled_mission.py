"""ScheduledMission — placement of one Mission inside a StudySchedule."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.education.mission_generation.enums import MissionType
from application.education.mission_generation.ids import MissionId
from application.education.revision_planner.enums import ScheduledMissionStatus
from application.education.revision_planner.errors import ScheduleInvariantViolation
from application.education.revision_planner.ids import SessionId


@dataclass(frozen=True, slots=True)
class ScheduledMission:
    """Immutable placement of mission work across one or more sessions.

    The planner never creates educational work — it only organises existing
    Mission identities from a MissionPlan into calendar slots.
    """

    mission_id: MissionId
    mission_type: MissionType
    scheduled_date: date
    session_ids: tuple[SessionId, ...]
    allocated_minutes: int
    remaining_minutes: int
    priority_magnitude: float
    status: ScheduledMissionStatus = ScheduledMissionStatus.SCHEDULED
    chunk_index: int = 1
    chunk_count: int = 1
    subject_id: str | None = None
    competency_id: str | None = None
    is_maintenance: bool = False
    is_prerequisite: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.mission_id, MissionId):
            raise ScheduleInvariantViolation(
                "mission_id must be a MissionId",
                invariant="ScheduledMission.mission_id.type",
            )
        if not isinstance(self.mission_type, MissionType):
            raise ScheduleInvariantViolation(
                "mission_type must be a MissionType",
                invariant="ScheduledMission.mission_type.type",
            )
        if not isinstance(self.scheduled_date, date):
            raise ScheduleInvariantViolation(
                "scheduled_date must be a date",
                invariant="ScheduledMission.scheduled_date.type",
            )
        object.__setattr__(self, "session_ids", tuple(self.session_ids))
        for session_id in self.session_ids:
            if not isinstance(session_id, SessionId):
                raise ScheduleInvariantViolation(
                    "session_ids must contain SessionId values",
                    invariant="ScheduledMission.session_ids.type",
                )
        for name, value in (
            ("allocated_minutes", self.allocated_minutes),
            ("remaining_minutes", self.remaining_minutes),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ScheduleInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"ScheduledMission.{name}.type",
                )
            if value < 0:
                raise ScheduleInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ScheduledMission.{name}.non_negative",
                )
        if isinstance(self.priority_magnitude, bool) or not isinstance(
            self.priority_magnitude, int | float
        ):
            raise ScheduleInvariantViolation(
                "priority_magnitude must be a real number",
                invariant="ScheduledMission.priority_magnitude.type",
            )
        magnitude = float(self.priority_magnitude)
        if magnitude < 0.0 or magnitude > 1.0:
            raise ScheduleInvariantViolation(
                "priority_magnitude must be between 0.0 and 1.0 inclusive",
                invariant="ScheduledMission.priority_magnitude.range",
            )
        object.__setattr__(self, "priority_magnitude", round(magnitude, 4))
        if not isinstance(self.status, ScheduledMissionStatus):
            raise ScheduleInvariantViolation(
                "status must be a ScheduledMissionStatus",
                invariant="ScheduledMission.status.type",
            )
        if isinstance(self.chunk_index, bool) or not isinstance(self.chunk_index, int):
            raise ScheduleInvariantViolation(
                "chunk_index must be an integer",
                invariant="ScheduledMission.chunk_index.type",
            )
        if self.chunk_index < 1:
            raise ScheduleInvariantViolation(
                "chunk_index must be >= 1",
                invariant="ScheduledMission.chunk_index.positive",
            )
        if isinstance(self.chunk_count, bool) or not isinstance(self.chunk_count, int):
            raise ScheduleInvariantViolation(
                "chunk_count must be an integer",
                invariant="ScheduledMission.chunk_count.type",
            )
        if self.chunk_count < 1:
            raise ScheduleInvariantViolation(
                "chunk_count must be >= 1",
                invariant="ScheduledMission.chunk_count.positive",
            )
        if self.chunk_index > self.chunk_count:
            raise ScheduleInvariantViolation(
                "chunk_index must be <= chunk_count",
                invariant="ScheduledMission.chunk_index.range",
            )
        subject_id = (self.subject_id or "").strip() or None
        object.__setattr__(self, "subject_id", subject_id)
        competency_id = (self.competency_id or "").strip() or None
        object.__setattr__(self, "competency_id", competency_id)

    def with_status(self, status: ScheduledMissionStatus) -> ScheduledMission:
        return ScheduledMission(
            mission_id=self.mission_id,
            mission_type=self.mission_type,
            scheduled_date=self.scheduled_date,
            session_ids=self.session_ids,
            allocated_minutes=self.allocated_minutes,
            remaining_minutes=self.remaining_minutes,
            priority_magnitude=self.priority_magnitude,
            status=status,
            chunk_index=self.chunk_index,
            chunk_count=self.chunk_count,
            subject_id=self.subject_id,
            competency_id=self.competency_id,
            is_maintenance=self.is_maintenance,
            is_prerequisite=self.is_prerequisite,
        )
