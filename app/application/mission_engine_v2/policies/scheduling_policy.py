"""Stateless scheduling rules for Mission Engine 2.0.

Deterministic only. No optimisation heuristics. No educational reasoning.
"""

from __future__ import annotations

from datetime import date, timedelta

from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.lifecycle import (
    MissionSlot,
    MissionState,
    is_open_mission_state,
)


class SchedulingPolicy:
    """Deterministic schedule slot assignment and ordering."""

    SLOT_PRIORITY: tuple[MissionSlot, ...] = (
        MissionSlot.TODAY,
        MissionSlot.MISSED,
        MissionSlot.DEFERRED,
        MissionSlot.REVISION,
        MissionSlot.FUTURE,
    )

    @staticmethod
    def slot_for_date(
        scheduled_date: date,
        *,
        as_of_date: date,
        is_revision: bool = False,
        is_deferred: bool = False,
        is_missed: bool = False,
    ) -> MissionSlot:
        """Resolve a schedule slot from calendar position and flags."""
        if is_revision:
            return MissionSlot.REVISION
        if is_deferred:
            return MissionSlot.DEFERRED
        if is_missed or scheduled_date < as_of_date:
            return MissionSlot.MISSED
        if scheduled_date == as_of_date:
            return MissionSlot.TODAY
        return MissionSlot.FUTURE

    @staticmethod
    def future_date(as_of_date: date, *, days_ahead: int = 1) -> date:
        """Return a future calendar date relative to ``as_of_date``."""
        return as_of_date + timedelta(days=max(1, days_ahead))

    @staticmethod
    def should_mark_missed(
        mission: DailyMission,
        *,
        as_of_date: date,
    ) -> bool:
        """True when an open mission is past due and not already missed."""
        if not is_open_mission_state(mission.state):
            return False
        if mission.slot == MissionSlot.MISSED:
            return False
        if mission.slot == MissionSlot.REVISION:
            return False
        if mission.state in {MissionState.ACTIVE, MissionState.PAUSED}:
            # Active/paused today missions are not auto-missed.
            if mission.scheduled_date >= as_of_date:
                return False
        return mission.scheduled_date < as_of_date

    @staticmethod
    def order(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        """Deterministic ordering: slot priority → date → state → mission id."""
        slot_rank = {
            slot: idx for idx, slot in enumerate(SchedulingPolicy.SLOT_PRIORITY)
        }
        state_rank = {
            MissionState.ACTIVE: 0,
            MissionState.PAUSED: 1,
            MissionState.READY: 2,
            MissionState.PLANNED: 3,
            MissionState.COMPLETED: 4,
            MissionState.ARCHIVED: 5,
        }

        def key(m: DailyMission) -> tuple:
            return (
                slot_rank.get(m.slot, 99),
                m.scheduled_date.toordinal(),
                state_rank.get(m.state, 99),
                m.mission_id,
            )

        return tuple(sorted(missions, key=key))

    @staticmethod
    def pick_today(
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
    ) -> DailyMission | None:
        """Pick the primary today mission (prefer ACTIVE/PAUSED, then READY)."""
        candidates = [
            m
            for m in missions
            if m.slot == MissionSlot.TODAY
            and m.scheduled_date == as_of_date
            and is_open_mission_state(m.state)
            and not m.is_revision
        ]
        if not candidates:
            return None
        ordered = SchedulingPolicy.order(candidates)
        for preferred in (
            MissionState.ACTIVE,
            MissionState.PAUSED,
            MissionState.READY,
            MissionState.PLANNED,
        ):
            for mission in ordered:
                if mission.state == preferred:
                    return mission
        return ordered[0]

    @staticmethod
    def filter_slot(
        missions: list[DailyMission] | tuple[DailyMission, ...],
        slot: MissionSlot,
    ) -> tuple[DailyMission, ...]:
        """Return open missions in ``slot`` (or revision-flagged for REVISION)."""
        result: list[DailyMission] = []
        for mission in missions:
            if not is_open_mission_state(mission.state):
                continue
            if slot == MissionSlot.REVISION:
                if mission.slot == MissionSlot.REVISION or mission.is_revision:
                    result.append(mission)
            elif mission.slot == slot:
                result.append(mission)
        return SchedulingPolicy.order(result)
