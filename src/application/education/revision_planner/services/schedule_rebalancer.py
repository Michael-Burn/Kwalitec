"""ScheduleRebalancer — rebalance and local mutation helpers for schedules."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date, datetime, time, timedelta

from application.education.mission_generation.ids import MissionId
from application.education.mission_generation.models.mission import Mission
from application.education.revision_planner.enums import (
    DayKind,
    ScheduledMissionStatus,
    SessionStatus,
)
from application.education.revision_planner.errors import RevisionPlanningError
from application.education.revision_planner.ids import DayId, SessionId
from application.education.revision_planner.models.completion_metrics import (
    CompletionMetrics,
)
from application.education.revision_planner.models.scheduled_mission import (
    ScheduledMission,
)
from application.education.revision_planner.models.study_day import StudyDay
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.education.revision_planner.models.study_session import StudySession
from application.education.revision_planner.planning_constraints import (
    PlanningConstraints,
)
from application.education.revision_planner.services.session_allocator import (
    SessionAllocator,
)
from application.education.revision_planner.services.workload_balancer import (
    DayCapacity,
    WorkloadBalancer,
)


class ScheduleRebalancer:
    """Local schedule mutations that avoid full rebuilds when possible."""

    @staticmethod
    def rebuild_days(
        *,
        schedule_id_value: str,
        start_date: date,
        end_date: date,
        sessions: Sequence[StudySession],
        capacities: Sequence[DayCapacity],
        rest_dates: frozenset[date],
        holiday_dates: frozenset[date],
        exam_date: date | None,
    ) -> tuple[StudyDay, ...]:
        capacity_map = {c.day_date: c for c in capacities}
        sessions_by_day: dict[date, list[StudySession]] = {}
        for session in sessions:
            if session.status in (SessionStatus.CANCELLED, SessionStatus.RESCHEDULED):
                # Still attach cancelled sessions to their original day for audit.
                sessions_by_day.setdefault(session.session_date, []).append(session)
                continue
            sessions_by_day.setdefault(session.session_date, []).append(session)

        days: list[StudyDay] = []
        cursor = start_date
        index = 1
        while cursor <= end_date:
            if cursor == exam_date:
                kind = DayKind.EXAM
                available = 0
            elif cursor in holiday_dates:
                kind = DayKind.HOLIDAY
                available = 0
            elif cursor in rest_dates:
                kind = DayKind.REST
                available = 0
            elif cursor in capacity_map:
                kind = DayKind.STUDY
                available = capacity_map[cursor].available_minutes
            else:
                kind = DayKind.UNAVAILABLE
                available = 0
            day_sessions = tuple(
                sorted(
                    sessions_by_day.get(cursor, []),
                    key=lambda s: (s.start_time, s.session_id.value),
                )
            )
            days.append(
                StudyDay(
                    day_id=DayId(f"{schedule_id_value}:d{index:04d}"),
                    day_date=cursor,
                    sessions=day_sessions,
                    available_minutes=available,
                    kind=kind,
                )
            )
            cursor = date.fromordinal(cursor.toordinal() + 1)
            index += 1
        return tuple(days)

    @staticmethod
    def complete_session(
        schedule: StudySchedule,
        session_id: SessionId,
        *,
        completion_metrics: CompletionMetrics,
        at: datetime,
    ) -> StudySchedule:
        session = schedule.session_by_id(session_id)
        if session is None:
            raise RevisionPlanningError(
                f"session not found: {session_id.value}",
                code="session_not_found",
            )
        if session.status is SessionStatus.COMPLETED:
            raise RevisionPlanningError(
                f"session already completed: {session_id.value}",
                code="session_already_completed",
            )
        if session.status is SessionStatus.CANCELLED:
            raise RevisionPlanningError(
                f"cannot complete cancelled session: {session_id.value}",
                code="session_cancelled",
            )

        updated_sessions = tuple(
            (
                s.with_status(
                    SessionStatus.COMPLETED, completion_metrics=completion_metrics
                )
                if s.session_id == session_id
                else s
            )
            for s in schedule.sessions
        )
        completed_ids = frozenset(session.scheduled_mission_ids)
        updated_missions = tuple(
            (
                m.with_status(ScheduledMissionStatus.COMPLETED)
                if m.mission_id in completed_ids
                else m
            )
            for m in schedule.scheduled_missions
        )
        days = ScheduleRebalancer._refresh_day_sessions(
            schedule.days, updated_sessions
        )
        return schedule.replace_sessions(
            WorkloadBalancer.rebalance_session_order(updated_sessions),
            days=days,
            scheduled_missions=updated_missions,
            generated_at=at,
        )

    @staticmethod
    def cancel_session(
        schedule: StudySchedule,
        session_id: SessionId,
        *,
        at: datetime,
    ) -> StudySchedule:
        session = schedule.session_by_id(session_id)
        if session is None:
            raise RevisionPlanningError(
                f"session not found: {session_id.value}",
                code="session_not_found",
            )
        if session.status is SessionStatus.CANCELLED:
            return schedule

        updated_sessions = tuple(
            (
                s.with_status(SessionStatus.CANCELLED)
                if s.session_id == session_id
                else s
            )
            for s in schedule.sessions
        )
        cancelled_ids = frozenset(session.scheduled_mission_ids)
        updated_missions = tuple(
            (
                m.with_status(ScheduledMissionStatus.CANCELLED)
                if m.mission_id in cancelled_ids
                else m
            )
            for m in schedule.scheduled_missions
        )
        reindexed = WorkloadBalancer.rebalance_session_order(updated_sessions)
        days = ScheduleRebalancer._refresh_day_sessions(schedule.days, reindexed)
        return schedule.replace_sessions(
            reindexed,
            days=days,
            scheduled_missions=updated_missions,
            generated_at=at,
        )

    @staticmethod
    def reschedule_session(
        schedule: StudySchedule,
        session_id: SessionId,
        *,
        new_date: date,
        new_start_time: time,
        at: datetime,
        constraints: PlanningConstraints | None = None,
    ) -> StudySchedule:
        session = schedule.session_by_id(session_id)
        if session is None:
            raise RevisionPlanningError(
                f"session not found: {session_id.value}",
                code="session_not_found",
            )
        if session.status in (SessionStatus.COMPLETED, SessionStatus.CANCELLED):
            raise RevisionPlanningError(
                f"cannot reschedule terminal session: {session_id.value}",
                code="session_terminal",
            )
        if new_date < schedule.start_date or new_date > schedule.end_date:
            raise RevisionPlanningError(
                "new_date is outside schedule horizon",
                code="date_out_of_horizon",
            )

        end_dt = datetime.combine(new_date, new_start_time) + timedelta(
            minutes=session.estimated_duration_minutes
        )
        moved = session.with_timing(
            session_date=new_date,
            start_time=new_start_time,
            end_time=end_dt.time().replace(microsecond=0),
        ).with_status(SessionStatus.PLANNED)

        # Mark original placement as RESCHEDULED identity retained; replace in place.
        updated_sessions = tuple(
            moved if s.session_id == session_id else s for s in schedule.sessions
        )
        reindexed = WorkloadBalancer.rebalance_session_order(updated_sessions)

        updated_missions: list[ScheduledMission] = []
        for mission in schedule.scheduled_missions:
            if session_id in mission.session_ids:
                updated_missions.append(
                    ScheduledMission(
                        mission_id=mission.mission_id,
                        mission_type=mission.mission_type,
                        scheduled_date=new_date,
                        session_ids=mission.session_ids,
                        allocated_minutes=mission.allocated_minutes,
                        remaining_minutes=mission.remaining_minutes,
                        priority_magnitude=mission.priority_magnitude,
                        status=mission.status,
                        chunk_index=mission.chunk_index,
                        chunk_count=mission.chunk_count,
                        subject_id=mission.subject_id,
                        competency_id=mission.competency_id,
                        is_maintenance=mission.is_maintenance,
                        is_prerequisite=mission.is_prerequisite,
                    )
                )
            else:
                updated_missions.append(mission)

        # Rebuild day available minutes from existing days where possible.
        capacities = tuple(
            DayCapacity(
                day_date=day.day_date,
                available_minutes=day.available_minutes,
                allocated_minutes=0,
            )
            for day in schedule.days
            if day.kind is DayKind.STUDY
        )
        # Recompute allocations from reindexed sessions.
        capacity_list = list(capacities)
        for s in reindexed:
            if s.status in (SessionStatus.CANCELLED, SessionStatus.RESCHEDULED):
                continue
            capacity_list = list(
                WorkloadBalancer.apply_allocation(
                    capacity_list, s.session_date, s.estimated_duration_minutes
                )
            )

        rest_dates = frozenset(
            d.day_date for d in schedule.days if d.kind is DayKind.REST
        )
        holiday_dates = frozenset(
            d.day_date for d in schedule.days if d.kind is DayKind.HOLIDAY
        )
        exam_date = schedule.exam_target.exam_date if schedule.exam_target else None
        days = ScheduleRebalancer.rebuild_days(
            schedule_id_value=schedule.schedule_id.value,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            sessions=reindexed,
            capacities=capacity_list,
            rest_dates=rest_dates,
            holiday_dates=holiday_dates,
            exam_date=exam_date,
        )
        _ = constraints  # reserved for future capacity checks
        return schedule.replace_sessions(
            reindexed,
            days=days,
            scheduled_missions=tuple(updated_missions),
            generated_at=at,
        )

    @staticmethod
    def insert_mission(
        schedule: StudySchedule,
        mission: Mission,
        *,
        at: datetime,
    ) -> StudySchedule:
        if schedule.contains_mission(mission.mission_id):
            raise RevisionPlanningError(
                f"mission already scheduled: {mission.mission_id.value}",
                code="mission_already_scheduled",
            )
        constraints = schedule.constraints or PlanningConstraints()
        capacities = WorkloadBalancer.capacities_from_days(schedule.days)
        # Zero allocated so insert uses remaining true capacity.
        fresh = tuple(
            DayCapacity(
                day_date=c.day_date,
                available_minutes=c.available_minutes,
                allocated_minutes=0,
            )
            for c in capacities
        )
        # Seed with existing active allocations.
        seeded = list(fresh)
        for session in schedule.active_sessions():
            seeded = list(
                WorkloadBalancer.apply_allocation(
                    seeded,
                    session.session_date,
                    session.estimated_duration_minutes,
                )
            )

        result = SessionAllocator.insert_mission(
            mission,
            schedule_id=schedule.schedule_id,
            existing_sessions=schedule.sessions,
            capacities=seeded,
            constraints=constraints,
        )
        if not result.scheduled_missions:
            raise RevisionPlanningError(
                "insufficient capacity to insert mission",
                code="insufficient_capacity",
            )

        rest_dates = frozenset(
            d.day_date for d in schedule.days if d.kind is DayKind.REST
        )
        holiday_dates = frozenset(
            d.day_date for d in schedule.days if d.kind is DayKind.HOLIDAY
        )
        exam_date = schedule.exam_target.exam_date if schedule.exam_target else None
        days = ScheduleRebalancer.rebuild_days(
            schedule_id_value=schedule.schedule_id.value,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            sessions=result.sessions,
            capacities=result.capacities,
            rest_dates=rest_dates,
            holiday_dates=holiday_dates,
            exam_date=exam_date,
        )
        return schedule.replace_sessions(
            result.sessions,
            days=days,
            scheduled_missions=schedule.scheduled_missions + result.scheduled_missions,
            generated_at=at,
        )

    @staticmethod
    def remove_completed_missions(
        schedule: StudySchedule,
        completed_mission_ids: frozenset[MissionId],
        *,
        at: datetime,
    ) -> StudySchedule:
        """Drop future sessions that only reference completed missions."""
        if not completed_mission_ids:
            return schedule

        kept_sessions: list[StudySession] = []
        for session in schedule.sessions:
            if session.status is SessionStatus.COMPLETED:
                kept_sessions.append(session)
                continue
            remaining_ids = tuple(
                mid
                for mid in session.scheduled_mission_ids
                if mid not in completed_mission_ids
            )
            if not remaining_ids:
                # Drop entire future session for completed-only work.
                if session.status is SessionStatus.PLANNED:
                    continue
                kept_sessions.append(session)
                continue
            if remaining_ids != session.scheduled_mission_ids:
                kept_sessions.append(
                    StudySession(
                        session_id=session.session_id,
                        session_date=session.session_date,
                        start_time=session.start_time,
                        end_time=session.end_time,
                        estimated_duration_minutes=session.estimated_duration_minutes,
                        scheduled_mission_ids=remaining_ids,
                        objectives=session.objectives,
                        priority=session.priority,
                        status=session.status,
                        completion_metrics=session.completion_metrics,
                        sequence_index=session.sequence_index,
                    )
                )
            else:
                kept_sessions.append(session)

        updated_missions = tuple(
            m.with_status(ScheduledMissionStatus.COMPLETED)
            if m.mission_id in completed_mission_ids
            else m
            for m in schedule.scheduled_missions
        )

        reindexed = WorkloadBalancer.rebalance_session_order(kept_sessions)
        days = ScheduleRebalancer._refresh_day_sessions(schedule.days, reindexed)
        return schedule.replace_sessions(
            reindexed,
            days=days,
            scheduled_missions=updated_missions,
            generated_at=at,
        )

    @staticmethod
    def rebalance(schedule: StudySchedule, *, at: datetime) -> StudySchedule:
        """Re-index sessions and rebuild day groupings without changing times."""
        reindexed = WorkloadBalancer.rebalance_session_order(schedule.sessions)
        capacities = tuple(
            DayCapacity(
                day_date=day.day_date,
                available_minutes=day.available_minutes,
                allocated_minutes=0,
            )
            for day in schedule.days
            if day.kind is DayKind.STUDY
        )
        rest_dates = frozenset(
            d.day_date for d in schedule.days if d.kind is DayKind.REST
        )
        holiday_dates = frozenset(
            d.day_date for d in schedule.days if d.kind is DayKind.HOLIDAY
        )
        exam_date = schedule.exam_target.exam_date if schedule.exam_target else None
        days = ScheduleRebalancer.rebuild_days(
            schedule_id_value=schedule.schedule_id.value,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            sessions=reindexed,
            capacities=capacities,
            rest_dates=rest_dates,
            holiday_dates=holiday_dates,
            exam_date=exam_date,
        )
        return schedule.replace_sessions(
            reindexed, days=days, generated_at=at
        )

    @staticmethod
    def _refresh_day_sessions(
        days: Sequence[StudyDay],
        sessions: Sequence[StudySession],
    ) -> tuple[StudyDay, ...]:
        by_date: dict[date, list[StudySession]] = {}
        for session in sessions:
            by_date.setdefault(session.session_date, []).append(session)
        return tuple(
            day.with_sessions(
                tuple(
                    sorted(
                        by_date.get(day.day_date, []),
                        key=lambda s: (s.start_time, s.session_id.value),
                    )
                )
            )
            for day in days
        )
