"""WorkloadBalancer — balances daily allocated minutes across the horizon."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from application.education.revision_planner.errors import ScheduleInvariantViolation
from application.education.revision_planner.models.study_day import StudyDay
from application.education.revision_planner.models.study_session import StudySession
from application.education.revision_planner.planning_constraints import (
    PlanningConstraints,
)


@dataclass(frozen=True, slots=True)
class DayCapacity:
    """Mutable planning view of remaining capacity for one day."""

    day_date: date
    available_minutes: int
    allocated_minutes: int = 0

    def remaining(self) -> int:
        return max(0, self.available_minutes - self.allocated_minutes)

    def can_fit(self, minutes: int) -> bool:
        return minutes <= self.remaining()

    def with_allocation(self, minutes: int) -> DayCapacity:
        return DayCapacity(
            day_date=self.day_date,
            available_minutes=self.available_minutes,
            allocated_minutes=self.allocated_minutes + minutes,
        )


class WorkloadBalancer:
    """Deterministic daily capacity tracking and selection.

    Prefers under-utilised study days while respecting daily caps and
    weekly workload limits when provided.
    """

    @staticmethod
    def capacities_from_days(days: Sequence[StudyDay]) -> tuple[DayCapacity, ...]:
        return tuple(
            DayCapacity(
                day_date=day.day_date,
                available_minutes=day.available_minutes,
                allocated_minutes=day.active_allocated_minutes(),
            )
            for day in days
            if day.available_minutes > 0 and not day.is_rest_day()
        )

    @staticmethod
    def select_day(
        capacities: Sequence[DayCapacity],
        *,
        minutes: int,
        preferred_date: date | None = None,
        constraints: PlanningConstraints | None = None,
    ) -> DayCapacity | None:
        """Select the best day that can fit ``minutes``.

        Preference order:
        1. preferred_date when it can fit
        2. earliest day with lowest utilisation that can fit
        """
        if minutes < 1:
            raise ScheduleInvariantViolation(
                "minutes must be >= 1",
                invariant="WorkloadBalancer.select_day.minutes",
            )
        eligible = [c for c in capacities if c.can_fit(minutes)]
        if not eligible:
            return None

        if preferred_date is not None:
            for capacity in eligible:
                if capacity.day_date == preferred_date:
                    return capacity

        # Prefer earliest under-filled days for consistency / low overload.
        def sort_key(capacity: DayCapacity) -> tuple:
            utilisation = (
                capacity.allocated_minutes / capacity.available_minutes
                if capacity.available_minutes
                else 1.0
            )
            return (utilisation, capacity.day_date)

        return sorted(eligible, key=sort_key)[0]

    @staticmethod
    def apply_allocation(
        capacities: Sequence[DayCapacity],
        day_date: date,
        minutes: int,
    ) -> tuple[DayCapacity, ...]:
        updated: list[DayCapacity] = []
        for capacity in capacities:
            if capacity.day_date == day_date:
                updated.append(capacity.with_allocation(minutes))
            else:
                updated.append(capacity)
        return tuple(updated)

    @staticmethod
    def weekly_total(
        capacities: Sequence[DayCapacity],
        *,
        week_start: date,
    ) -> int:
        end = date.fromordinal(week_start.toordinal() + 6)
        return sum(
            c.allocated_minutes
            for c in capacities
            if week_start <= c.day_date <= end
        )

    @staticmethod
    def respects_weekly_cap(
        capacities: Sequence[DayCapacity],
        *,
        day_date: date,
        additional_minutes: int,
        constraints: PlanningConstraints,
    ) -> bool:
        weekly_cap = constraints.weekly_workload_minutes
        if weekly_cap is None:
            return True
        # ISO week Monday.
        week_start = date.fromordinal(
            day_date.toordinal() - (day_date.isoweekday() - 1)
        )
        current = WorkloadBalancer.weekly_total(capacities, week_start=week_start)
        return current + additional_minutes <= weekly_cap

    @staticmethod
    def rebalance_session_order(
        sessions: Sequence[StudySession],
    ) -> tuple[StudySession, ...]:
        """Re-index sessions by date/time for contiguous sequence_index."""
        from application.education.revision_planner.enums import SessionStatus

        inactive = {SessionStatus.CANCELLED, SessionStatus.RESCHEDULED}
        active = [s for s in sessions if s.status not in inactive]
        terminal = [s for s in sessions if s.status in inactive]
        ordered = sorted(
            active,
            key=lambda s: (s.session_date, s.start_time, s.session_id.value),
        )
        reindexed = tuple(
            session.with_timing(sequence_index=index)
            for index, session in enumerate(ordered, start=1)
        )
        # Keep terminal sessions after active ones with high sequence indices.
        terminal_indexed = tuple(
            session.with_timing(sequence_index=len(reindexed) + index)
            for index, session in enumerate(terminal, start=1)
        )
        return reindexed + terminal_indexed
