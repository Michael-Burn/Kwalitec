"""Schedule and reschedule missions deterministically.

Produces today's, deferred, revision, missed, and future mission queues.
No optimisation heuristics. No educational reasoning.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date

from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.dto.mission_timeline import MissionTimeline
from app.application.mission_engine_v2.exceptions import (
    SchedulingError,
    WorkloadExceeded,
)
from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState
from app.application.mission_engine_v2.policies.scheduling_policy import (
    SchedulingPolicy,
)
from app.application.mission_engine_v2.policies.workload_policy import WorkloadPolicy


class MissionScheduler:
    """Deterministic mission scheduling operations."""

    def build_timeline(
        self,
        learner_id: str,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        as_of_date: date,
    ) -> MissionTimeline:
        """Assemble a MissionTimeline snapshot for ``as_of_date``."""
        scoped = [m for m in missions if m.learner_id == learner_id]
        ordered = SchedulingPolicy.order(scoped)
        today = SchedulingPolicy.pick_today(ordered, as_of_date=as_of_date)
        deferred = SchedulingPolicy.filter_slot(ordered, MissionSlot.DEFERRED)
        revision = SchedulingPolicy.filter_slot(ordered, MissionSlot.REVISION)
        missed = SchedulingPolicy.filter_slot(ordered, MissionSlot.MISSED)
        future = SchedulingPolicy.filter_slot(ordered, MissionSlot.FUTURE)
        return MissionTimeline(
            learner_id=learner_id,
            as_of_date=as_of_date,
            today=today,
            deferred=deferred,
            revision=revision,
            missed=missed,
            future=future,
            ordered=ordered,
        )

    def schedule_today(
        self,
        mission: DailyMission,
        *,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
    ) -> DailyMission:
        """Place ``mission`` on today's READY/ACTIVE-eligible slot."""
        if not WorkloadPolicy.can_activate(
            existing,
            excluding_mission_id=mission.mission_id,
        ):
            # READY is allowed even when another is active? No — one active
            # means we still can have READY but not activate. Today slot uses READY.
            pass
        if not WorkloadPolicy.can_add_open(
            [m for m in existing if m.mission_id != mission.mission_id]
        ):
            raise WorkloadExceeded("Cannot schedule today: open mission capacity")
        return replace(
            mission,
            scheduled_date=as_of_date,
            slot=MissionSlot.TODAY,
            state=MissionState.READY,
            is_revision=False,
        )

    def schedule_deferred(
        self,
        mission: DailyMission,
        *,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
        target_date: date | None = None,
    ) -> DailyMission:
        """Move an incomplete mission into the deferred queue."""
        if not WorkloadPolicy.can_defer(existing):
            raise WorkloadExceeded("Deferred mission capacity exceeded")
        if mission.state in {MissionState.COMPLETED, MissionState.ARCHIVED}:
            raise SchedulingError(
                f"Cannot defer mission in state {mission.state.value}"
            )
        state = mission.state
        if state == MissionState.ACTIVE:
            state = MissionState.PAUSED
        elif state not in {
            MissionState.PLANNED,
            MissionState.READY,
            MissionState.PAUSED,
        }:
            state = MissionState.PLANNED
        return replace(
            mission,
            state=state,
            slot=MissionSlot.DEFERRED,
            scheduled_date=target_date or mission.scheduled_date,
        )

    def schedule_revision(
        self,
        mission: DailyMission,
        *,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
    ) -> DailyMission:
        """Place ``mission`` in the revision queue (does not claim ACTIVE)."""
        if not WorkloadPolicy.can_add_revision(existing):
            raise WorkloadExceeded("Revision mission capacity exceeded")
        return replace(
            mission,
            scheduled_date=as_of_date,
            slot=MissionSlot.REVISION,
            state=MissionState.PLANNED,
            is_revision=True,
            revision_debt=max(1, mission.revision_debt),
        )

    def schedule_future(
        self,
        mission: DailyMission,
        *,
        as_of_date: date,
        days_ahead: int = 1,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
    ) -> DailyMission:
        """Place ``mission`` on the future queue."""
        if not WorkloadPolicy.can_add_future(existing):
            raise WorkloadExceeded("Future mission capacity exceeded")
        future_date = SchedulingPolicy.future_date(
            as_of_date,
            days_ahead=days_ahead,
        )
        return replace(
            mission,
            scheduled_date=future_date,
            slot=MissionSlot.FUTURE,
            state=MissionState.PLANNED,
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
        return replace(
            mission,
            slot=MissionSlot.MISSED,
            state=(
                MissionState.PLANNED
                if mission.state
                not in {MissionState.READY, MissionState.PAUSED}
                else mission.state
            ),
        )

    def reschedule(
        self,
        mission: DailyMission,
        *,
        new_date: date,
        as_of_date: date,
        existing: list[DailyMission] | tuple[DailyMission, ...] = (),
        is_revision: bool = False,
        is_deferred: bool = False,
    ) -> DailyMission:
        """Reschedule an incomplete / missed / deferred mission."""
        if mission.state in {MissionState.COMPLETED, MissionState.ARCHIVED}:
            raise SchedulingError(
                f"Cannot reschedule mission in state {mission.state.value}"
            )
        slot = SchedulingPolicy.slot_for_date(
            new_date,
            as_of_date=as_of_date,
            is_revision=is_revision or mission.is_revision,
            is_deferred=is_deferred,
        )
        state = MissionState.PLANNED
        if slot == MissionSlot.TODAY:
            state = MissionState.READY
        return replace(
            mission,
            scheduled_date=new_date,
            slot=slot,
            state=state,
            is_revision=is_revision or mission.is_revision,
        )

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
                    marked = self.mark_missed(
                        mission,
                        as_of_date=as_of_date,
                        existing=working,
                    )
                    updated.append(marked)
                    working = [
                        marked if m.mission_id == mission.mission_id else m
                        for m in working
                    ]
                except (SchedulingError, WorkloadExceeded):
                    updated.append(mission)
            else:
                updated.append(mission)
        return tuple(updated)
