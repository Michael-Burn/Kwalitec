"""SessionAllocator — places missions into timed StudySessions."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

from application.education.mission_generation.enums import (
    MissionPriorityBand,
    MissionType,
)
from application.education.mission_generation.models.mission import Mission
from application.education.revision_planner.enums import (
    ScheduledMissionStatus,
    SessionPriority,
    SessionStatus,
)
from application.education.revision_planner.errors import RevisionPlanningError
from application.education.revision_planner.ids import ScheduleId, SessionId
from application.education.revision_planner.models.scheduled_mission import (
    ScheduledMission,
)
from application.education.revision_planner.models.study_session import StudySession
from application.education.revision_planner.planning_constraints import (
    PlanningConstraints,
)
from application.education.revision_planner.services.dependency_resolver import (
    DependencyResolver,
)
from application.education.revision_planner.services.spacing_strategy import (
    SpacingStrategy,
)
from application.education.revision_planner.services.workload_balancer import (
    DayCapacity,
    WorkloadBalancer,
)

_PRIORITY_MAP: dict[MissionPriorityBand, SessionPriority] = {
    MissionPriorityBand.LOW: SessionPriority.LOW,
    MissionPriorityBand.MEDIUM: SessionPriority.MEDIUM,
    MissionPriorityBand.HIGH: SessionPriority.HIGH,
    MissionPriorityBand.CRITICAL: SessionPriority.CRITICAL,
}

DEFAULT_WINDOW_START = time(9, 0)
DEFAULT_WINDOW_END = time(21, 0)


@dataclass(frozen=True, slots=True)
class AllocationResult:
    """Result of allocating missions across day capacities."""

    sessions: tuple[StudySession, ...]
    scheduled_missions: tuple[ScheduledMission, ...]
    capacities: tuple[DayCapacity, ...]


class SessionAllocator:
    """Deterministically allocate Mission work into StudySessions.

    Long missions are split across multiple sessions. High-priority work
    is placed as early as practical. Maintenance missions are spaced.
    """

    @staticmethod
    def allocate(
        missions: Sequence[Mission],
        *,
        schedule_id: ScheduleId,
        capacities: Sequence[DayCapacity],
        constraints: PlanningConstraints,
        session_ordinal_start: int = 1,
    ) -> AllocationResult:
        if not capacities:
            raise RevisionPlanningError(
                "no day capacity available for allocation",
                code="no_capacity",
            )

        ordered = DependencyResolver.resolve(
            missions, honour_dependencies=constraints.honour_mission_dependencies
        )
        primary, maintenance = SessionAllocator._partition(ordered)
        study_dates = tuple(c.day_date for c in capacities)

        maintenance_targets = SpacingStrategy.target_dates(
            maintenance,
            study_dates=study_dates,
            policy=constraints.spacing_policy,
        )
        preferred_by_id = {
            mission.mission_id.value: maintenance_targets[index]
            for index, mission in enumerate(maintenance)
            if index < len(maintenance_targets)
        }

        working_capacities = list(capacities)
        sessions: list[StudySession] = []
        scheduled: list[ScheduledMission] = []
        ordinal = session_ordinal_start
        last_maintenance_date: date | None = None

        queue = list(primary) + list(maintenance)
        for mission in queue:
            preferred = preferred_by_id.get(mission.mission_id.value)
            if mission.is_lightweight() and preferred is None:
                preferred = SpacingStrategy.next_spaced_date(
                    last_maintenance_date,
                    candidates=study_dates,
                    policy=constraints.spacing_policy,
                )

            chunks = SessionAllocator._split_duration(
                mission.estimate.duration_minutes,
                maximum_session_minutes=constraints.maximum_session_minutes,
                preferred_session_minutes=constraints.preferred_session_minutes,
            )
            session_ids: list[SessionId] = []
            first_date: date | None = None
            allocated_total = 0

            for chunk_index, chunk_minutes in enumerate(chunks, start=1):
                placed = SessionAllocator._place_chunk(
                    mission,
                    chunk_minutes=chunk_minutes,
                    chunk_index=chunk_index,
                    chunk_count=len(chunks),
                    schedule_id=schedule_id,
                    ordinal=ordinal,
                    capacities=working_capacities,
                    preferred_date=preferred,
                    constraints=constraints,
                )
                if placed is None:
                    # Soft-fail: leave remaining unscheduled rather than raise,
                    # so partial schedules remain valid under tight horizons.
                    break
                session, working_capacities = placed
                sessions.append(session)
                session_ids.append(session.session_id)
                ordinal += 1
                allocated_total += chunk_minutes
                if first_date is None:
                    first_date = session.session_date
                if mission.is_lightweight():
                    last_maintenance_date = session.session_date

            if not session_ids or first_date is None:
                continue

            remaining = max(0, mission.estimate.duration_minutes - allocated_total)
            status = (
                ScheduledMissionStatus.PARTIAL
                if remaining > 0
                else ScheduledMissionStatus.SCHEDULED
            )
            scheduled.append(
                ScheduledMission(
                    mission_id=mission.mission_id,
                    mission_type=mission.mission_type,
                    scheduled_date=first_date,
                    session_ids=tuple(session_ids),
                    allocated_minutes=allocated_total,
                    remaining_minutes=remaining,
                    priority_magnitude=mission.ordering.priority_magnitude,
                    status=status,
                    chunk_index=1,
                    chunk_count=len(chunks),
                    subject_id=mission.subject_id,
                    competency_id=mission.competency_id,
                    is_maintenance=mission.is_lightweight(),
                    is_prerequisite=DependencyResolver.is_prerequisite(mission),
                )
            )

        reindexed = WorkloadBalancer.rebalance_session_order(sessions)
        return AllocationResult(
            sessions=reindexed,
            scheduled_missions=tuple(scheduled),
            capacities=tuple(working_capacities),
        )

    @staticmethod
    def _partition(
        missions: Sequence[Mission],
    ) -> tuple[tuple[Mission, ...], tuple[Mission, ...]]:
        primary: list[Mission] = []
        maintenance: list[Mission] = []
        for mission in missions:
            if (
                mission.is_lightweight()
                or mission.mission_type is MissionType.MAINTENANCE_REVIEW
            ):
                maintenance.append(mission)
            else:
                primary.append(mission)
        return tuple(primary), tuple(maintenance)

    @staticmethod
    def _split_duration(
        total_minutes: int,
        *,
        maximum_session_minutes: int,
        preferred_session_minutes: int,
    ) -> tuple[int, ...]:
        if total_minutes <= maximum_session_minutes:
            return (total_minutes,)
        chunk_size = min(preferred_session_minutes, maximum_session_minutes)
        chunks: list[int] = []
        remaining = total_minutes
        while remaining > 0:
            take = min(chunk_size, remaining, maximum_session_minutes)
            # Avoid tiny leftover fragments when possible.
            if remaining - take > 0 and remaining - take < max(5, chunk_size // 3):
                take = remaining
            chunks.append(take)
            remaining -= take
        return tuple(chunks)

    @staticmethod
    def _place_chunk(
        mission: Mission,
        *,
        chunk_minutes: int,
        chunk_index: int,
        chunk_count: int,
        schedule_id: ScheduleId,
        ordinal: int,
        capacities: list[DayCapacity],
        preferred_date: date | None,
        constraints: PlanningConstraints,
    ) -> tuple[StudySession, list[DayCapacity]] | None:
        del chunk_index, chunk_count  # reserved for future chunk labelling
        # Try preferred, then scan earliest-fit while honouring weekly caps.
        attempt_dates: list[date | None] = [preferred_date]
        # Fall back without preferred.
        attempt_dates.append(None)

        for preferred in attempt_dates:
            capacity = WorkloadBalancer.select_day(
                capacities,
                minutes=chunk_minutes,
                preferred_date=preferred,
                constraints=constraints,
            )
            if capacity is None:
                continue
            if not WorkloadBalancer.respects_weekly_cap(
                capacities,
                day_date=capacity.day_date,
                additional_minutes=chunk_minutes,
                constraints=constraints,
            ):
                # Try other days that respect the weekly cap.
                alternatives = [
                    c
                    for c in capacities
                    if c.can_fit(chunk_minutes)
                    and WorkloadBalancer.respects_weekly_cap(
                        capacities,
                        day_date=c.day_date,
                        additional_minutes=chunk_minutes,
                        constraints=constraints,
                    )
                ]
                if not alternatives:
                    continue
                capacity = sorted(
                    alternatives,
                    key=lambda c: (
                        c.allocated_minutes / c.available_minutes
                        if c.available_minutes
                        else 1.0,
                        c.day_date,
                    ),
                )[0]

            start_time, end_time = SessionAllocator._session_window(
                capacity,
                chunk_minutes=chunk_minutes,
                constraints=constraints,
            )
            session_id = SessionId(f"{schedule_id.value}:s{ordinal:04d}")
            session = StudySession(
                session_id=session_id,
                session_date=capacity.day_date,
                start_time=start_time,
                end_time=end_time,
                estimated_duration_minutes=chunk_minutes,
                scheduled_mission_ids=(mission.mission_id,),
                objectives=(mission.objective.code,),
                priority=_PRIORITY_MAP.get(
                    mission.ordering.priority_band, SessionPriority.MEDIUM
                ),
                status=SessionStatus.PLANNED,
                sequence_index=ordinal,
            )
            updated = list(
                WorkloadBalancer.apply_allocation(
                    capacities, capacity.day_date, chunk_minutes
                )
            )
            return session, updated
        return None

    @staticmethod
    def _session_window(
        capacity: DayCapacity,
        *,
        chunk_minutes: int,
        constraints: PlanningConstraints,
    ) -> tuple[time, time]:
        window_start = constraints.preferred_window_start or DEFAULT_WINDOW_START
        window_end = constraints.preferred_window_end or DEFAULT_WINDOW_END

        # Offset start by already allocated minutes + recovery gaps.
        offset = capacity.allocated_minutes
        if capacity.allocated_minutes > 0:
            offset += constraints.minimum_recovery_minutes_between_sessions

        start_dt = datetime.combine(capacity.day_date, window_start) + timedelta(
            minutes=offset
        )
        end_dt = start_dt + timedelta(minutes=chunk_minutes)
        latest = datetime.combine(capacity.day_date, window_end)
        if end_dt > latest:
            # Clamp backward within the window when possible.
            start_dt = latest - timedelta(minutes=chunk_minutes)
            end_dt = latest
            earliest = datetime.combine(capacity.day_date, window_start)
            if start_dt < earliest:
                start_dt = earliest
                end_dt = earliest + timedelta(minutes=chunk_minutes)

        return start_dt.time().replace(microsecond=0), end_dt.time().replace(
            microsecond=0
        )

    @staticmethod
    def insert_mission(
        mission: Mission,
        *,
        schedule_id: ScheduleId,
        existing_sessions: Sequence[StudySession],
        capacities: Sequence[DayCapacity],
        constraints: PlanningConstraints,
    ) -> AllocationResult:
        """Allocate a single new mission without rebuilding prior sessions."""
        next_ordinal = len(existing_sessions) + 1
        result = SessionAllocator.allocate(
            (mission,),
            schedule_id=schedule_id,
            capacities=capacities,
            constraints=constraints,
            session_ordinal_start=next_ordinal,
        )
        combined = WorkloadBalancer.rebalance_session_order(
            tuple(existing_sessions) + result.sessions
        )
        return AllocationResult(
            sessions=combined,
            scheduled_missions=result.scheduled_missions,
            capacities=result.capacities,
        )
