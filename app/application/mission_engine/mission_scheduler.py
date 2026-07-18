"""Schedule and reschedule missions deterministically.

Responsible for today's, tomorrow's, deferred, missed, and revision slots.
No optimisation heuristics. No educational reasoning.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.dto.mission_schedule import MissionSchedule
from app.application.mission_engine.exceptions import (
    SchedulingError,
    WorkloadExceeded,
)
from app.application.mission_engine.mission_state import (
    MissionSlot,
    MissionState,
    MissionTransitionEvent,
    next_mission_state,
)
from app.application.mission_engine.policies.scheduling_policy import SchedulingPolicy
from app.application.mission_engine.policies.workload_policy import WorkloadPolicy


class MissionScheduler:
    """Deterministic mission scheduling operations."""

    def build_schedule(
        self,
        learner_id: str,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
    ) -> MissionSchedule:
        """Assemble a MissionSchedule snapshot for ``as_of_date``."""
        scoped = [m for m in missions if m.learner_id == learner_id]
        ordered = SchedulingPolicy.order(scoped)
        today = SchedulingPolicy.pick_today(ordered, as_of_date=as_of_date)
        tomorrow = SchedulingPolicy.pick_tomorrow(ordered, as_of_date=as_of_date)
        deferred = tuple(
            m
            for m in ordered
            if m.slot == MissionSlot.DEFERRED or m.state == MissionState.DEFERRED
        )
        missed = tuple(
            m
            for m in ordered
            if m.slot == MissionSlot.MISSED or m.state == MissionState.MISSED
        )
        revision = tuple(
            m for m in ordered if m.slot == MissionSlot.REVISION or m.is_revision
        )
        return MissionSchedule(
            learner_id=learner_id,
            as_of_date=as_of_date,
            today=today,
            tomorrow=tomorrow,
            deferred=deferred,
            missed=missed,
            revision=revision,
            ordered=ordered,
        )

    def schedule_today(
        self,
        mission: DailyMission,
        *,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
    ) -> DailyMission:
        """Place ``mission`` on today's ACTIVE slot."""
        if not WorkloadPolicy.can_activate(
            existing,
            excluding_mission_id=mission.mission_id,
        ):
            raise WorkloadExceeded("Cannot schedule today: active mission exists")
        return replace(
            mission,
            scheduled_date=as_of_date,
            slot=MissionSlot.TODAY,
            state=MissionState.ACTIVE,
            is_revision=False,
        )

    def schedule_tomorrow(
        self,
        mission: DailyMission,
        *,
        as_of_date: date,
    ) -> DailyMission:
        """Place ``mission`` on tomorrow's SCHEDULED slot."""
        return replace(
            mission,
            scheduled_date=SchedulingPolicy.tomorrow_date(as_of_date),
            slot=MissionSlot.TOMORROW,
            state=MissionState.SCHEDULED,
        )

    def defer(
        self,
        mission: DailyMission,
        *,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
        target_date: date | None = None,
    ) -> DailyMission:
        """Defer an incomplete mission."""
        if not WorkloadPolicy.can_defer(existing):
            raise WorkloadExceeded("Deferred mission capacity exceeded")
        nxt = next_mission_state(mission.state, MissionTransitionEvent.DEFER)
        if nxt is None:
            raise SchedulingError(
                f"Cannot defer mission in state {mission.state.value}"
            )
        return replace(
            mission,
            state=nxt,
            slot=MissionSlot.DEFERRED,
            scheduled_date=target_date or mission.scheduled_date,
        )

    def mark_missed(
        self,
        mission: DailyMission,
        *,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
    ) -> DailyMission:
        """Mark a past incomplete mission as MISSED."""
        if not SchedulingPolicy.should_mark_missed(mission, as_of_date=as_of_date):
            raise SchedulingError(
                f"Mission {mission.mission_id} is not eligible to be marked missed"
            )
        if not WorkloadPolicy.can_mark_missed(existing):
            raise WorkloadExceeded("Missed mission capacity exceeded")
        nxt = next_mission_state(mission.state, MissionTransitionEvent.MISS)
        if nxt is None and mission.state != MissionState.SCHEDULED:
            # ACTIVE / IN_PROGRESS also map via MISS when lawful.
            nxt = next_mission_state(mission.state, MissionTransitionEvent.MISS)
        if nxt is None:
            raise SchedulingError(
                f"Cannot mark missed from state {mission.state.value}"
            )
        return replace(
            mission,
            state=MissionState.MISSED,
            slot=MissionSlot.MISSED,
        )

    def reschedule(
        self,
        mission: DailyMission,
        *,
        new_date: date,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
        is_revision: bool = False,
    ) -> DailyMission:
        """Reschedule an incomplete / missed / deferred mission."""
        if mission.state in {
            MissionState.COMPLETED,
            MissionState.ARCHIVED,
            MissionState.SKIPPED,
        }:
            raise SchedulingError(
                f"Cannot reschedule mission in state {mission.state.value}"
            )
        slot = SchedulingPolicy.slot_for_date(
            new_date,
            as_of_date=as_of_date,
            is_revision=is_revision or mission.is_revision,
        )
        state = MissionState.SCHEDULED
        if slot == MissionSlot.TODAY:
            if not WorkloadPolicy.can_activate(
                existing,
                excluding_mission_id=mission.mission_id,
            ):
                raise WorkloadExceeded(
                    "Cannot reschedule to today: active mission exists"
                )
            state = MissionState.ACTIVE
        return replace(
            mission,
            scheduled_date=new_date,
            slot=slot,
            state=state,
            is_revision=is_revision or mission.is_revision,
        )

    def skip(self, mission: DailyMission) -> DailyMission:
        """Skip a mission without completing its session."""
        nxt = next_mission_state(mission.state, MissionTransitionEvent.SKIP)
        if nxt is None:
            raise SchedulingError(
                f"Cannot skip mission in state {mission.state.value}"
            )
        return replace(mission, state=nxt)

    def start(self, mission: DailyMission) -> DailyMission:
        """Mark an ACTIVE mission as IN_PROGRESS (session started)."""
        nxt = next_mission_state(mission.state, MissionTransitionEvent.START)
        if nxt is None:
            raise SchedulingError(
                f"Cannot start mission in state {mission.state.value}"
            )
        return replace(mission, state=nxt)

    def refresh_missed(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
    ) -> tuple[DailyMission, ...]:
        """Deterministically mark past open missions as missed where lawful."""
        updated: list[DailyMission] = []
        working = list(missions)
        for mission in missions:
            if SchedulingPolicy.should_mark_missed(mission, as_of_date=as_of_date):
                try:
                    updated.append(
                        self.mark_missed(
                            mission,
                            as_of_date=as_of_date,
                            existing=working,
                        )
                    )
                    # Reflect change in working set for capacity checks.
                    working = [
                        updated[-1] if m.mission_id == mission.mission_id else m
                        for m in working
                    ]
                except (SchedulingError, WorkloadExceeded):
                    updated.append(mission)
            else:
                updated.append(mission)
        return tuple(updated)
