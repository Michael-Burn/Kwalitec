"""AdaptiveRevisionPlanner — MissionPlan → StudySchedule.

Architecture Source
    PRD-002 Adaptive Revision Planner

Transforms an immutable MissionPlan into an adaptive StudySchedule.
Organises educational work. Never creates educational work.

Must not:
    - estimate mastery
    - generate recommendations
    - generate missions
    - modify MissionPlan
    - modify StudentEducationalState
    - persist, call Flask/SQLAlchemy, invoke AI, or use randomness
    - read wall-clock time via now()/utcnow()

Every method is a pure function of its explicit, caller-supplied inputs —
the same inputs always produce the same output.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date, datetime, time

from application.education.mission_generation.enums import MissionType
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.revision_planner.enums import (
    AbandonmentPolicy,
    Weekday,
)
from application.education.revision_planner.errors import RevisionPlanningError
from application.education.revision_planner.exam_target import ExamTarget
from application.education.revision_planner.execution_history import ExecutionHistory
from application.education.revision_planner.ids import ScheduleId, SessionId
from application.education.revision_planner.models.completion_metrics import (
    CompletionMetrics,
)
from application.education.revision_planner.models.schedule_snapshot import (
    ScheduleSnapshot,
)
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.education.revision_planner.models.study_session import StudySession
from application.education.revision_planner.planning_constraints import (
    PlanningConstraints,
)
from application.education.revision_planner.services.dependency_resolver import (
    DependencyResolver,
)
from application.education.revision_planner.services.schedule_rebalancer import (
    ScheduleRebalancer,
)
from application.education.revision_planner.services.schedule_validator import (
    ScheduleValidator,
)
from application.education.revision_planner.services.session_allocator import (
    SessionAllocator,
)
from application.education.revision_planner.services.workload_balancer import (
    DayCapacity,
)
from application.education.revision_planner.student_availability import (
    StudentAvailability,
)

DEFAULT_HORIZON_DAYS = 14
DEFAULT_WINDOW_START = time(9, 0)
DEFAULT_WINDOW_END = time(12, 0)


class AdaptiveRevisionPlanner:
    """Deterministic planner producing StudySchedule from MissionPlan.

    Pure application composition. Mission generation remains the sole
    producer of educational work; this planner only organises that work
    onto a calendar.
    """

    # --- top-level planning -------------------------------------------------

    @staticmethod
    def create_schedule(
        mission_plan: MissionPlan,
        *,
        schedule_id: ScheduleId,
        start_date: date,
        generated_at: datetime,
        availability: StudentAvailability | None = None,
        planning_constraints: PlanningConstraints | None = None,
        execution_history: ExecutionHistory | None = None,
        exam_target: ExamTarget | None = None,
        holiday_dates: Sequence[date] = (),
        horizon_days: int | None = None,
    ) -> StudySchedule:
        """Create a full StudySchedule from a MissionPlan.

        Pipeline (deterministic):
        1. Filter completed missions from history
        2. Apply abandonment policy to abandoned missions
        3. Resolve prerequisite dependencies
        4. Build day capacities from availability + constraints
        5. Allocate sessions (split long missions, space maintenance)
        6. Assemble StudyDays / StudySchedule
        7. Validate
        """
        AdaptiveRevisionPlanner._assert_create_inputs(
            mission_plan,
            schedule_id=schedule_id,
            start_date=start_date,
            generated_at=generated_at,
        )
        constraints = planning_constraints or PlanningConstraints()
        history = execution_history or ExecutionHistory()
        student_availability = availability or StudentAvailability(
            student_id=mission_plan.student_id
        )
        holidays = frozenset(holiday_dates)

        end_date = AdaptiveRevisionPlanner._resolve_end_date(
            start_date=start_date,
            constraints=constraints,
            exam_target=exam_target,
            horizon_days=horizon_days,
        )
        missions = AdaptiveRevisionPlanner._missions_to_schedule(
            mission_plan.missions,
            history=history,
            constraints=constraints,
        )
        capacities, rest_dates = AdaptiveRevisionPlanner._build_capacities(
            start_date=start_date,
            end_date=end_date,
            availability=student_availability,
            constraints=constraints,
            holiday_dates=holidays,
            exam_date=exam_target.exam_date if exam_target else None,
        )

        if not missions:
            days = ScheduleRebalancer.rebuild_days(
                schedule_id_value=schedule_id.value,
                start_date=start_date,
                end_date=end_date,
                sessions=(),
                capacities=capacities,
                rest_dates=rest_dates,
                holiday_dates=holidays,
                exam_date=exam_target.exam_date if exam_target else None,
            )
            schedule = StudySchedule(
                schedule_id=schedule_id,
                student_id=mission_plan.student_id,
                source_plan_id=mission_plan.plan_id,
                generated_at=generated_at,
                start_date=start_date,
                end_date=end_date,
                days=days,
                sessions=(),
                scheduled_missions=(),
                constraints=constraints,
                exam_target=exam_target,
            )
            ScheduleValidator.validate(schedule)
            return schedule

        if not capacities:
            raise RevisionPlanningError(
                "no study capacity in planning horizon",
                code="no_capacity",
            )

        allocation = SessionAllocator.allocate(
            missions,
            schedule_id=schedule_id,
            capacities=capacities,
            constraints=constraints,
        )
        days = ScheduleRebalancer.rebuild_days(
            schedule_id_value=schedule_id.value,
            start_date=start_date,
            end_date=end_date,
            sessions=allocation.sessions,
            capacities=allocation.capacities,
            rest_dates=rest_dates,
            holiday_dates=holidays,
            exam_date=exam_target.exam_date if exam_target else None,
        )
        schedule = StudySchedule(
            schedule_id=schedule_id,
            student_id=mission_plan.student_id,
            source_plan_id=mission_plan.plan_id,
            generated_at=generated_at,
            start_date=start_date,
            end_date=end_date,
            days=days,
            sessions=allocation.sessions,
            scheduled_missions=allocation.scheduled_missions,
            constraints=constraints,
            exam_target=exam_target,
        )
        ScheduleValidator.validate(schedule)
        return schedule

    @staticmethod
    def replan_schedule(
        schedule: StudySchedule,
        mission_plan: MissionPlan,
        *,
        generated_at: datetime,
        availability: StudentAvailability | None = None,
        planning_constraints: PlanningConstraints | None = None,
        execution_history: ExecutionHistory | None = None,
        holiday_dates: Sequence[date] = (),
    ) -> StudySchedule:
        """Rebuild a schedule from the current MissionPlan and history."""
        return AdaptiveRevisionPlanner.create_schedule(
            mission_plan,
            schedule_id=schedule.schedule_id,
            start_date=schedule.start_date,
            generated_at=generated_at,
            availability=availability,
            planning_constraints=planning_constraints or schedule.constraints,
            execution_history=execution_history,
            exam_target=schedule.exam_target,
            holiday_dates=holiday_dates,
            horizon_days=(schedule.end_date - schedule.start_date).days + 1,
        )

    @staticmethod
    def schedule_day(
        mission_plan: MissionPlan,
        *,
        schedule_id: ScheduleId,
        day: date,
        generated_at: datetime,
        availability: StudentAvailability | None = None,
        planning_constraints: PlanningConstraints | None = None,
        execution_history: ExecutionHistory | None = None,
        exam_target: ExamTarget | None = None,
        holiday_dates: Sequence[date] = (),
    ) -> StudySchedule:
        """Produce a single-day schedule."""
        return AdaptiveRevisionPlanner.create_schedule(
            mission_plan,
            schedule_id=schedule_id,
            start_date=day,
            generated_at=generated_at,
            availability=availability,
            planning_constraints=planning_constraints,
            execution_history=execution_history,
            exam_target=exam_target,
            holiday_dates=holiday_dates,
            horizon_days=1,
        )

    @staticmethod
    def schedule_week(
        mission_plan: MissionPlan,
        *,
        schedule_id: ScheduleId,
        week_start: date,
        generated_at: datetime,
        availability: StudentAvailability | None = None,
        planning_constraints: PlanningConstraints | None = None,
        execution_history: ExecutionHistory | None = None,
        exam_target: ExamTarget | None = None,
        holiday_dates: Sequence[date] = (),
    ) -> StudySchedule:
        """Produce a seven-day schedule starting at ``week_start``."""
        return AdaptiveRevisionPlanner.create_schedule(
            mission_plan,
            schedule_id=schedule_id,
            start_date=week_start,
            generated_at=generated_at,
            availability=availability,
            planning_constraints=planning_constraints,
            execution_history=execution_history,
            exam_target=exam_target,
            holiday_dates=holiday_dates,
            horizon_days=7,
        )

    # --- local mutations ----------------------------------------------------

    @staticmethod
    def insert_new_mission(
        schedule: StudySchedule,
        mission: Mission,
        *,
        at: datetime,
    ) -> StudySchedule:
        """Insert one mission without rebuilding the entire schedule."""
        return ScheduleRebalancer.insert_mission(schedule, mission, at=at)

    @staticmethod
    def complete_session(
        schedule: StudySchedule,
        session_id: SessionId,
        *,
        completion_metrics: CompletionMetrics,
        at: datetime,
    ) -> StudySchedule:
        """Mark a session completed and update scheduled mission status."""
        return ScheduleRebalancer.complete_session(
            schedule,
            session_id,
            completion_metrics=completion_metrics,
            at=at,
        )

    @staticmethod
    def cancel_session(
        schedule: StudySchedule,
        session_id: SessionId,
        *,
        at: datetime,
    ) -> StudySchedule:
        """Cancel a session and mark associated missions cancelled."""
        return ScheduleRebalancer.cancel_session(schedule, session_id, at=at)

    @staticmethod
    def reschedule(
        schedule: StudySchedule,
        session_id: SessionId,
        *,
        new_date: date,
        new_start_time: time,
        at: datetime,
    ) -> StudySchedule:
        """Move a session to a new date/time within the horizon."""
        return ScheduleRebalancer.reschedule_session(
            schedule,
            session_id,
            new_date=new_date,
            new_start_time=new_start_time,
            at=at,
            constraints=schedule.constraints,
        )

    @staticmethod
    def rebalance(schedule: StudySchedule, *, at: datetime) -> StudySchedule:
        """Re-index sessions and rebuild day groupings."""
        return ScheduleRebalancer.rebalance(schedule, at=at)

    @staticmethod
    def produce_snapshot(
        schedule: StudySchedule,
        *,
        captured_at: datetime | None = None,
    ) -> ScheduleSnapshot:
        """Produce an immutable snapshot of a schedule."""
        return schedule.produce_snapshot(captured_at=captured_at)

    # --- helpers ------------------------------------------------------------

    @staticmethod
    def _assert_create_inputs(
        mission_plan: MissionPlan,
        *,
        schedule_id: ScheduleId,
        start_date: date,
        generated_at: datetime,
    ) -> None:
        if not isinstance(mission_plan, MissionPlan):
            raise RevisionPlanningError(
                "mission_plan must be a MissionPlan",
                code="invalid_mission_plan",
            )
        if not isinstance(schedule_id, ScheduleId):
            raise RevisionPlanningError(
                "schedule_id must be a ScheduleId",
                code="invalid_schedule_id",
            )
        if not isinstance(start_date, date):
            raise RevisionPlanningError(
                "start_date must be a date",
                code="invalid_start_date",
            )
        if not isinstance(generated_at, datetime):
            raise RevisionPlanningError(
                "generated_at must be a datetime",
                code="invalid_generated_at",
            )

    @staticmethod
    def _resolve_end_date(
        *,
        start_date: date,
        constraints: PlanningConstraints,
        exam_target: ExamTarget | None,
        horizon_days: int | None,
    ) -> date:
        candidates: list[date] = []
        if horizon_days is not None:
            if horizon_days < 1:
                raise RevisionPlanningError(
                    "horizon_days must be >= 1",
                    code="invalid_horizon",
                )
            candidates.append(
                date.fromordinal(start_date.toordinal() + horizon_days - 1)
            )
        if constraints.target_completion_date is not None:
            candidates.append(constraints.target_completion_date)
        if exam_target is not None:
            # Schedule ends the day before the exam when possible.
            if exam_target.exam_date > start_date:
                candidates.append(
                    date.fromordinal(exam_target.exam_date.toordinal() - 1)
                )
            else:
                candidates.append(exam_target.exam_date)
        if not candidates:
            candidates.append(
                date.fromordinal(start_date.toordinal() + DEFAULT_HORIZON_DAYS - 1)
            )
        end_date = min(candidates)
        if end_date < start_date:
            raise RevisionPlanningError(
                "resolved end_date precedes start_date",
                code="invalid_horizon",
            )
        return end_date

    @staticmethod
    def _missions_to_schedule(
        missions: Sequence[Mission],
        *,
        history: ExecutionHistory,
        constraints: PlanningConstraints,
    ) -> tuple[Mission, ...]:
        excluded = history.exclude_from_future()
        remaining: list[Mission] = []
        abandoned: list[Mission] = []

        for mission in missions:
            if mission.mission_id in excluded:
                continue
            if history.is_abandoned(mission.mission_id):
                if constraints.abandonment_policy is AbandonmentPolicy.DROP:
                    continue
                abandoned.append(mission)
                continue
            remaining.append(mission)

        ordered = DependencyResolver.resolve(
            remaining, honour_dependencies=constraints.honour_mission_dependencies
        )
        if not abandoned:
            return ordered

        abandoned_ordered = DependencyResolver.resolve(
            abandoned, honour_dependencies=constraints.honour_mission_dependencies
        )
        policy = constraints.abandonment_policy
        if policy is AbandonmentPolicy.RESCHEDULE_EARLY:
            return abandoned_ordered + ordered
        if policy is AbandonmentPolicy.DEFER_TO_END:
            return ordered + abandoned_ordered
        # RESCHEDULE_NEXT_AVAILABLE — append after in-progress priority work
        # but before maintenance when practical.
        primary = [
            m
            for m in ordered
            if not m.is_lightweight()
            and m.mission_type is not MissionType.MAINTENANCE_REVIEW
        ]
        maintenance = [
            m
            for m in ordered
            if m.is_lightweight() or m.mission_type is MissionType.MAINTENANCE_REVIEW
        ]
        return tuple(primary) + abandoned_ordered + tuple(maintenance)

    @staticmethod
    def _build_capacities(
        *,
        start_date: date,
        end_date: date,
        availability: StudentAvailability,
        constraints: PlanningConstraints,
        holiday_dates: frozenset[date],
        exam_date: date | None,
    ) -> tuple[tuple[DayCapacity, ...], frozenset[date]]:
        rest_dates: set[date] = set()
        capacities: list[DayCapacity] = []
        daily_cap = constraints.effective_daily_cap_minutes()
        window_start = constraints.preferred_window_start or DEFAULT_WINDOW_START
        window_end = constraints.preferred_window_end or DEFAULT_WINDOW_END

        cursor = start_date
        while cursor <= end_date:
            if cursor == exam_date or cursor in holiday_dates:
                cursor = date.fromordinal(cursor.toordinal() + 1)
                continue
            if constraints.is_rest_weekday(cursor) or availability.is_unavailable(
                cursor
            ):
                rest_dates.add(cursor)
                cursor = date.fromordinal(cursor.toordinal() + 1)
                continue

            windows = availability.windows_for(cursor)
            if windows:
                available = min(sum(w.available_minutes for w in windows), daily_cap)
            else:
                # Synthesise a default window when caller supplied none.
                available = AdaptiveRevisionPlanner._default_available_minutes(
                    cursor,
                    availability=availability,
                    daily_cap=daily_cap,
                    window_start=window_start,
                    window_end=window_end,
                )
            if available > 0:
                capacities.append(
                    DayCapacity(
                        day_date=cursor,
                        available_minutes=available,
                        allocated_minutes=0,
                    )
                )
            cursor = date.fromordinal(cursor.toordinal() + 1)

        return tuple(capacities), frozenset(rest_dates)

    @staticmethod
    def _default_available_minutes(
        day: date,
        *,
        availability: StudentAvailability,
        daily_cap: int,
        window_start: time,
        window_end: time,
    ) -> int:
        if availability.preferred_weekdays:
            weekday = Weekday.from_iso(day.isoweekday())
            if weekday not in availability.preferred_weekdays:
                return 0
        start_minutes = window_start.hour * 60 + window_start.minute
        end_minutes = window_end.hour * 60 + window_end.minute
        window_minutes = max(0, end_minutes - start_minutes)
        return min(daily_cap, window_minutes) if window_minutes else daily_cap

    @staticmethod
    def sessions_for_day(
        schedule: StudySchedule, day: date
    ) -> tuple[StudySession, ...]:
        return schedule.sessions_on(day)

    @staticmethod
    def filter_incomplete_missions(
        missions: Sequence[Mission],
        history: ExecutionHistory,
    ) -> tuple[Mission, ...]:
        excluded = history.exclude_from_future()
        return tuple(m for m in missions if m.mission_id not in excluded)
