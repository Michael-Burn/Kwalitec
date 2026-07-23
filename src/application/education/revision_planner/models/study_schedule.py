"""StudySchedule — immutable adaptive revision schedule.

Architecture Source
    PRD-002 Adaptive Revision Planner

Organises MissionPlan work into StudyDays and StudySessions.
Never creates educational work. Never estimates mastery.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from application.education.mission_generation.ids import MissionId, MissionPlanId
from application.education.revision_planner.enums import DayKind, SessionStatus
from application.education.revision_planner.errors import ScheduleInvariantViolation
from application.education.revision_planner.exam_target import ExamTarget
from application.education.revision_planner.ids import ScheduleId, SessionId
from application.education.revision_planner.models.schedule_metrics import (
    DayWorkload,
    ScheduleMetrics,
    WorkloadDistribution,
)
from application.education.revision_planner.models.schedule_snapshot import (
    ScheduleSnapshot,
)
from application.education.revision_planner.models.schedule_summary import (
    ScheduleSummary,
)
from application.education.revision_planner.models.scheduled_mission import (
    ScheduledMission,
)
from application.education.revision_planner.models.study_calendar_projection import (
    CalendarDayProjection,
    StudyCalendarProjection,
)
from application.education.revision_planner.models.study_day import StudyDay
from application.education.revision_planner.models.study_session import StudySession
from application.education.revision_planner.planning_constraints import (
    PlanningConstraints,
)

_INACTIVE = frozenset({SessionStatus.CANCELLED, SessionStatus.RESCHEDULED})


@dataclass(frozen=True, slots=True)
class StudySchedule:
    """Immutable schedule organising MissionPlan work across calendar days.

    StudySchedule is the Adaptive Revision Planner's product: deterministic
    calendar organisation derived from a MissionPlan at one caller-supplied
    planning horizon. It never mutates the MissionPlan, never persists,
    never estimates mastery, and never generates missions.
    """

    schedule_id: ScheduleId
    student_id: str
    source_plan_id: MissionPlanId
    generated_at: datetime
    start_date: date
    end_date: date
    days: tuple[StudyDay, ...] = ()
    sessions: tuple[StudySession, ...] = ()
    scheduled_missions: tuple[ScheduledMission, ...] = ()
    constraints: PlanningConstraints | None = None
    exam_target: ExamTarget | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.schedule_id, ScheduleId):
            raise ScheduleInvariantViolation(
                "schedule_id must be a ScheduleId",
                invariant="StudySchedule.schedule_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ScheduleInvariantViolation(
                "student_id must be a non-empty string",
                invariant="StudySchedule.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.source_plan_id, MissionPlanId):
            raise ScheduleInvariantViolation(
                "source_plan_id must be a MissionPlanId",
                invariant="StudySchedule.source_plan_id.type",
            )
        if not isinstance(self.generated_at, datetime):
            raise ScheduleInvariantViolation(
                "generated_at must be a datetime",
                invariant="StudySchedule.generated_at.type",
            )
        if not isinstance(self.start_date, date) or not isinstance(self.end_date, date):
            raise ScheduleInvariantViolation(
                "start_date and end_date must be dates",
                invariant="StudySchedule.dates.type",
            )
        if self.end_date < self.start_date:
            raise ScheduleInvariantViolation(
                "end_date must be on or after start_date",
                invariant="StudySchedule.dates.order",
            )
        object.__setattr__(self, "days", tuple(self.days))
        for day in self.days:
            if not isinstance(day, StudyDay):
                raise ScheduleInvariantViolation(
                    "days must contain StudyDay values",
                    invariant="StudySchedule.days.type",
                )
        object.__setattr__(self, "sessions", tuple(self.sessions))
        for session in self.sessions:
            if not isinstance(session, StudySession):
                raise ScheduleInvariantViolation(
                    "sessions must contain StudySession values",
                    invariant="StudySchedule.sessions.type",
                )
        object.__setattr__(self, "scheduled_missions", tuple(self.scheduled_missions))
        for scheduled in self.scheduled_missions:
            if not isinstance(scheduled, ScheduledMission):
                raise ScheduleInvariantViolation(
                    "scheduled_missions must contain ScheduledMission values",
                    invariant="StudySchedule.scheduled_missions.type",
                )
        if self.constraints is None:
            object.__setattr__(self, "constraints", PlanningConstraints())
        elif not isinstance(self.constraints, PlanningConstraints):
            raise ScheduleInvariantViolation(
                "constraints must be a PlanningConstraints",
                invariant="StudySchedule.constraints.type",
            )
        if self.exam_target is not None and not isinstance(
            self.exam_target, ExamTarget
        ):
            raise ScheduleInvariantViolation(
                "exam_target must be an ExamTarget when provided",
                invariant="StudySchedule.exam_target.type",
            )
        self._assert_session_identity_unique()
        self._assert_session_sequence()

    def _assert_session_identity_unique(self) -> None:
        seen: set[str] = set()
        for session in self.sessions:
            if session.session_id.value in seen:
                raise ScheduleInvariantViolation(
                    "schedule must not contain duplicate session identities",
                    invariant="StudySchedule.sessions.unique",
                )
            seen.add(session.session_id.value)

    def _assert_session_sequence(self) -> None:
        active = [s for s in self.sessions if s.status not in _INACTIVE]
        ordered = sorted(
            active,
            key=lambda s: (s.session_date, s.start_time, s.session_id.value),
        )
        for expected, session in enumerate(ordered, start=1):
            if session.sequence_index != expected:
                raise ScheduleInvariantViolation(
                    "active sessions must have contiguous sequence_index "
                    f"starting at 1 (expected {expected}, got "
                    f"{session.sequence_index})",
                    invariant="StudySchedule.sessions.sequence_order",
                )

    def day_count(self) -> int:
        return len(self.days)

    def study_days(self) -> tuple[StudyDay, ...]:
        return tuple(d for d in self.days if d.kind is DayKind.STUDY)

    def rest_days(self) -> tuple[StudyDay, ...]:
        return tuple(d for d in self.days if d.kind is DayKind.REST)

    def active_sessions(self) -> tuple[StudySession, ...]:
        return tuple(s for s in self.sessions if s.status not in _INACTIVE)

    def session_by_id(self, session_id: SessionId) -> StudySession | None:
        for session in self.sessions:
            if session.session_id == session_id:
                return session
        return None

    def day_for(self, day: date) -> StudyDay | None:
        for study_day in self.days:
            if study_day.day_date == day:
                return study_day
        return None

    def sessions_on(self, day: date) -> tuple[StudySession, ...]:
        return tuple(s for s in self.sessions if s.session_date == day)

    def missions_pending(self) -> tuple[ScheduledMission, ...]:
        from application.education.revision_planner.enums import ScheduledMissionStatus

        return tuple(
            m
            for m in self.scheduled_missions
            if m.status
            in (
                ScheduledMissionStatus.PENDING,
                ScheduledMissionStatus.PARTIAL,
                ScheduledMissionStatus.SCHEDULED,
            )
        )

    def contains_mission(self, mission_id: MissionId) -> bool:
        return any(m.mission_id == mission_id for m in self.scheduled_missions)

    def total_allocated_minutes(self) -> int:
        return sum(s.estimated_duration_minutes for s in self.active_sessions())

    def total_available_minutes(self) -> int:
        return sum(d.available_minutes for d in self.study_days())

    def produce_metrics(self) -> ScheduleMetrics:
        study = self.study_days()
        rest = self.rest_days()
        active = self.active_sessions()
        completed = sum(1 for s in self.sessions if s.status is SessionStatus.COMPLETED)
        cancelled = sum(1 for s in self.sessions if s.status is SessionStatus.CANCELLED)
        from application.education.revision_planner.enums import ScheduledMissionStatus

        completed_missions = sum(
            1
            for m in self.scheduled_missions
            if m.status is ScheduledMissionStatus.COMPLETED
        )
        daily_minutes = [d.active_allocated_minutes() for d in study]
        avg = (
            round(sum(daily_minutes) / len(daily_minutes), 4) if daily_minutes else 0.0
        )
        peak = max(daily_minutes) if daily_minutes else 0
        return ScheduleMetrics(
            total_days=len(self.days),
            study_days=len(study),
            rest_days=len(rest),
            total_sessions=len(self.sessions),
            active_sessions=len(active),
            completed_sessions=completed,
            cancelled_sessions=cancelled,
            total_allocated_minutes=self.total_allocated_minutes(),
            total_available_minutes=self.total_available_minutes(),
            scheduled_mission_count=len(self.scheduled_missions),
            completed_mission_count=completed_missions,
            average_daily_minutes=avg,
            peak_daily_minutes=peak,
        )

    def produce_workload(self) -> WorkloadDistribution:
        daily: list[DayWorkload] = []
        for day in self.days:
            daily.append(
                DayWorkload(
                    day_iso=day.day_date.isoformat(),
                    allocated_minutes=day.active_allocated_minutes(),
                    available_minutes=day.available_minutes,
                )
            )
        allocated = [d.allocated_minutes for d in daily if d.available_minutes > 0]
        weekly: list[int] = []
        running = 0
        for index, day in enumerate(self.days, start=1):
            running += day.active_allocated_minutes()
            if index % 7 == 0 or index == len(self.days):
                weekly.append(running)
                running = 0
        if not allocated:
            return WorkloadDistribution(
                daily=tuple(daily),
                weekly_totals=tuple(weekly),
                max_day_minutes=0,
                min_day_minutes=0,
                variance=0.0,
            )
        mean = sum(allocated) / len(allocated)
        variance = sum((value - mean) ** 2 for value in allocated) / len(allocated)
        return WorkloadDistribution(
            daily=tuple(daily),
            weekly_totals=tuple(weekly),
            max_day_minutes=max(allocated),
            min_day_minutes=min(allocated),
            variance=variance,
        )

    def produce_summary(self) -> ScheduleSummary:
        metrics = self.produce_metrics()
        constraints = self.constraints or PlanningConstraints()
        return ScheduleSummary(
            schedule_id=self.schedule_id,
            student_id=self.student_id,
            start_date=self.start_date,
            end_date=self.end_date,
            study_day_count=metrics.study_days,
            session_count=metrics.active_sessions,
            mission_count=len(self.missions_pending())
            + metrics.completed_mission_count,
            total_allocated_minutes=metrics.total_allocated_minutes,
            average_daily_minutes=metrics.average_daily_minutes,
            utilises_exam_deadline=self.exam_target is not None,
            utilises_target_completion=constraints.target_completion_date is not None,
        )

    def produce_calendar(self) -> StudyCalendarProjection:
        projections = tuple(
            CalendarDayProjection(
                day_id=day.day_id,
                day_date=day.day_date,
                kind=day.kind,
                session_ids=tuple(s.session_id for s in day.sessions),
                allocated_minutes=day.active_allocated_minutes(),
                available_minutes=day.available_minutes,
            )
            for day in self.days
        )
        return StudyCalendarProjection(
            days=projections,
            horizon_start=self.start_date,
            horizon_end=self.end_date,
        )

    def produce_snapshot(
        self, *, captured_at: datetime | None = None
    ) -> ScheduleSnapshot:
        at = captured_at if captured_at is not None else self.generated_at
        return ScheduleSnapshot(
            schedule_id=self.schedule_id,
            student_id=self.student_id,
            source_plan_id=self.source_plan_id,
            captured_at=at,
            start_date=self.start_date,
            end_date=self.end_date,
            days=self.days,
            sessions=self.sessions,
            scheduled_missions=self.scheduled_missions,
            constraints=self.constraints or PlanningConstraints(),
            metrics=self.produce_metrics(),
            workload=self.produce_workload(),
            summary=self.produce_summary(),
            calendar=self.produce_calendar(),
        )

    def replace_sessions(
        self,
        sessions: tuple[StudySession, ...],
        *,
        days: tuple[StudyDay, ...] | None = None,
        scheduled_missions: tuple[ScheduledMission, ...] | None = None,
        generated_at: datetime | None = None,
    ) -> StudySchedule:
        """Return a new schedule with replaced session/day/mission placements."""
        return StudySchedule(
            schedule_id=self.schedule_id,
            student_id=self.student_id,
            source_plan_id=self.source_plan_id,
            generated_at=(
                generated_at if generated_at is not None else self.generated_at
            ),
            start_date=self.start_date,
            end_date=self.end_date,
            days=days if days is not None else self.days,
            sessions=sessions,
            scheduled_missions=(
                scheduled_missions
                if scheduled_missions is not None
                else self.scheduled_missions
            ),
            constraints=self.constraints,
            exam_target=self.exam_target,
        )
