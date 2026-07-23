"""ScheduleSnapshot — immutable point-in-time capture of a StudySchedule."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from application.education.mission_generation.ids import MissionPlanId
from application.education.revision_planner.errors import ScheduleInvariantViolation
from application.education.revision_planner.ids import ScheduleId
from application.education.revision_planner.models.schedule_metrics import (
    ScheduleMetrics,
    WorkloadDistribution,
)
from application.education.revision_planner.models.schedule_summary import (
    ScheduleSummary,
)
from application.education.revision_planner.models.scheduled_mission import (
    ScheduledMission,
)
from application.education.revision_planner.models.study_calendar_projection import (
    StudyCalendarProjection,
)
from application.education.revision_planner.models.study_day import StudyDay
from application.education.revision_planner.models.study_session import StudySession
from application.education.revision_planner.planning_constraints import (
    PlanningConstraints,
)


@dataclass(frozen=True, slots=True)
class ScheduleSnapshot:
    """Immutable snapshot of schedule state at a caller-supplied instant."""

    schedule_id: ScheduleId
    student_id: str
    source_plan_id: MissionPlanId
    captured_at: datetime
    start_date: date
    end_date: date
    days: tuple[StudyDay, ...]
    sessions: tuple[StudySession, ...]
    scheduled_missions: tuple[ScheduledMission, ...]
    constraints: PlanningConstraints
    metrics: ScheduleMetrics
    workload: WorkloadDistribution
    summary: ScheduleSummary
    calendar: StudyCalendarProjection

    def __post_init__(self) -> None:
        if not isinstance(self.schedule_id, ScheduleId):
            raise ScheduleInvariantViolation(
                "schedule_id must be a ScheduleId",
                invariant="ScheduleSnapshot.schedule_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ScheduleInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ScheduleSnapshot.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.source_plan_id, MissionPlanId):
            raise ScheduleInvariantViolation(
                "source_plan_id must be a MissionPlanId",
                invariant="ScheduleSnapshot.source_plan_id.type",
            )
        if not isinstance(self.captured_at, datetime):
            raise ScheduleInvariantViolation(
                "captured_at must be a datetime",
                invariant="ScheduleSnapshot.captured_at.type",
            )
        if not isinstance(self.start_date, date) or not isinstance(self.end_date, date):
            raise ScheduleInvariantViolation(
                "start_date and end_date must be dates",
                invariant="ScheduleSnapshot.dates.type",
            )
        object.__setattr__(self, "days", tuple(self.days))
        object.__setattr__(self, "sessions", tuple(self.sessions))
        object.__setattr__(self, "scheduled_missions", tuple(self.scheduled_missions))
        if not isinstance(self.constraints, PlanningConstraints):
            raise ScheduleInvariantViolation(
                "constraints must be a PlanningConstraints",
                invariant="ScheduleSnapshot.constraints.type",
            )
        if not isinstance(self.metrics, ScheduleMetrics):
            raise ScheduleInvariantViolation(
                "metrics must be a ScheduleMetrics",
                invariant="ScheduleSnapshot.metrics.type",
            )
        if not isinstance(self.workload, WorkloadDistribution):
            raise ScheduleInvariantViolation(
                "workload must be a WorkloadDistribution",
                invariant="ScheduleSnapshot.workload.type",
            )
        if not isinstance(self.summary, ScheduleSummary):
            raise ScheduleInvariantViolation(
                "summary must be a ScheduleSummary",
                invariant="ScheduleSnapshot.summary.type",
            )
        if not isinstance(self.calendar, StudyCalendarProjection):
            raise ScheduleInvariantViolation(
                "calendar must be a StudyCalendarProjection",
                invariant="ScheduleSnapshot.calendar.type",
            )
