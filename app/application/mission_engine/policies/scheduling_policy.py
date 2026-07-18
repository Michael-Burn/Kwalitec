"""Stateless scheduling rules for Mission Engine 2.0.

Deterministic only — no optimisation heuristics, no educational reasoning.
"""

from __future__ import annotations

from datetime import date, timedelta

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.mission_state import (
    MissionSlot,
    MissionState,
    is_open_mission_state,
)


class SchedulingPolicy:
    """Deterministic mission scheduling rules (stateless)."""

    SLOT_ORDER: tuple[MissionSlot, ...] = (
        MissionSlot.TODAY,
        MissionSlot.MISSED,
        MissionSlot.DEFERRED,
        MissionSlot.REVISION,
        MissionSlot.TOMORROW,
    )

    STATE_PRIORITY: dict[MissionState, int] = {
        MissionState.IN_PROGRESS: 0,
        MissionState.ACTIVE: 1,
        MissionState.SCHEDULED: 2,
        MissionState.MISSED: 3,
        MissionState.DEFERRED: 4,
        MissionState.SKIPPED: 5,
        MissionState.COMPLETED: 6,
        MissionState.ARCHIVED: 7,
    }

    @staticmethod
    def slot_for_date(
        scheduled_date: date,
        *,
        as_of_date: date,
        is_revision: bool = False,
    ) -> MissionSlot:
        """Derive the schedule slot for a date relative to ``as_of_date``."""
        if is_revision:
            return MissionSlot.REVISION
        if scheduled_date == as_of_date:
            return MissionSlot.TODAY
        if scheduled_date == as_of_date + timedelta(days=1):
            return MissionSlot.TOMORROW
        if scheduled_date < as_of_date:
            return MissionSlot.MISSED
        return MissionSlot.DEFERRED

    @staticmethod
    def tomorrow_date(as_of_date: date) -> date:
        """Calendar date for tomorrow relative to ``as_of_date``."""
        return as_of_date + timedelta(days=1)

    @staticmethod
    def should_mark_missed(
        mission: DailyMission,
        *,
        as_of_date: date,
    ) -> bool:
        """True when an open past-dated mission should become MISSED."""
        if not is_open_mission_state(mission.state):
            return False
        if mission.state in {MissionState.MISSED, MissionState.DEFERRED}:
            return False
        return mission.scheduled_date < as_of_date

    @staticmethod
    def should_activate_today(
        mission: DailyMission,
        *,
        as_of_date: date,
    ) -> bool:
        """True when a scheduled mission belongs on today's active slot."""
        return (
            mission.state == MissionState.SCHEDULED
            and mission.scheduled_date == as_of_date
            and mission.slot == MissionSlot.TODAY
        )

    @staticmethod
    def sort_key(mission: DailyMission) -> tuple[int, date, int, str]:
        """Deterministic ordering key: slot → date → state → id."""
        try:
            slot_rank = SchedulingPolicy.SLOT_ORDER.index(mission.slot)
        except ValueError:
            slot_rank = len(SchedulingPolicy.SLOT_ORDER)
        state_rank = SchedulingPolicy.STATE_PRIORITY.get(mission.state, 99)
        return (slot_rank, mission.scheduled_date, state_rank, mission.mission_id)

    @staticmethod
    def order(missions: list[DailyMission] | tuple[DailyMission, ...]) -> tuple[
        DailyMission, ...
    ]:
        """Return missions in deterministic schedule order."""
        return tuple(sorted(missions, key=SchedulingPolicy.sort_key))

    @staticmethod
    def pick_today(
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
    ) -> DailyMission | None:
        """Select today's primary mission (prefer IN_PROGRESS → ACTIVE)."""
        candidates = [
            m
            for m in missions
            if m.scheduled_date == as_of_date
            and m.state
            in {
                MissionState.IN_PROGRESS,
                MissionState.ACTIVE,
                MissionState.SCHEDULED,
            }
            and m.slot in {MissionSlot.TODAY, MissionSlot.REVISION}
        ]
        ordered = SchedulingPolicy.order(candidates)
        return ordered[0] if ordered else None

    @staticmethod
    def pick_tomorrow(
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
    ) -> DailyMission | None:
        """Select tomorrow's scheduled mission, if any."""
        target = SchedulingPolicy.tomorrow_date(as_of_date)
        candidates = [
            m
            for m in missions
            if m.scheduled_date == target
            and m.state == MissionState.SCHEDULED
            and m.slot == MissionSlot.TOMORROW
        ]
        ordered = SchedulingPolicy.order(candidates)
        return ordered[0] if ordered else None
