"""SpacingStrategy — distributes maintenance / review work across days."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date, timedelta

from application.education.mission_generation.models.mission import Mission
from application.education.revision_planner.enums import SpacingPolicy


class SpacingStrategy:
    """Deterministic spacing of maintenance missions across the horizon.

    Compact packs maintenance early; Balanced spreads evenly; Distributed
    maximises gaps between maintenance placements.
    """

    @staticmethod
    def target_dates(
        maintenance_missions: Sequence[Mission],
        *,
        study_dates: Sequence[date],
        policy: SpacingPolicy,
    ) -> tuple[date, ...]:
        """Return one preferred study date per maintenance mission."""
        dates = list(study_dates)
        missions = list(maintenance_missions)
        if not missions:
            return ()
        if not dates:
            return ()

        if policy is SpacingPolicy.COMPACT:
            return SpacingStrategy._compact(missions, dates)
        if policy is SpacingPolicy.DISTRIBUTED:
            return SpacingStrategy._distributed(missions, dates)
        return SpacingStrategy._balanced(missions, dates)

    @staticmethod
    def _compact(
        missions: Sequence[Mission], dates: Sequence[date]
    ) -> tuple[date, ...]:
        assigned: list[date] = []
        for index, _mission in enumerate(missions):
            assigned.append(dates[min(index, len(dates) - 1)])
        return tuple(assigned)

    @staticmethod
    def _balanced(
        missions: Sequence[Mission], dates: Sequence[date]
    ) -> tuple[date, ...]:
        count = len(missions)
        span = len(dates)
        assigned: list[date] = []
        for index in range(count):
            # Evenly spaced indices across the horizon.
            if count == 1:
                position = 0
            else:
                position = round(index * (span - 1) / (count - 1))
            assigned.append(dates[position])
        return tuple(assigned)

    @staticmethod
    def _distributed(
        missions: Sequence[Mission], dates: Sequence[date]
    ) -> tuple[date, ...]:
        count = len(missions)
        span = len(dates)
        if count == 1:
            return (dates[span // 2],)
        # Prefer larger gaps: place at floors of equal partitions, skipping
        # first day when possible to leave room for high-priority work.
        gap = max(1, span // count)
        assigned: list[date] = []
        cursor = min(gap - 1, span - 1) if gap > 1 else 0
        for _ in range(count):
            assigned.append(dates[min(cursor, span - 1)])
            cursor += gap
            if cursor >= span:
                cursor = span - 1
        return tuple(assigned)

    @staticmethod
    def minimum_gap_days(policy: SpacingPolicy) -> int:
        if policy is SpacingPolicy.COMPACT:
            return 0
        if policy is SpacingPolicy.DISTRIBUTED:
            return 2
        return 1

    @staticmethod
    def next_spaced_date(
        last_date: date | None,
        *,
        candidates: Sequence[date],
        policy: SpacingPolicy,
    ) -> date | None:
        """Pick the earliest candidate respecting the policy gap."""
        if not candidates:
            return None
        gap = SpacingStrategy.minimum_gap_days(policy)
        if last_date is None:
            return candidates[0]
        earliest = last_date + timedelta(days=gap)
        for candidate in candidates:
            if candidate >= earliest:
                return candidate
        return candidates[-1]
