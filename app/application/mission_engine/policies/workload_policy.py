"""Stateless workload limits for Mission Engine 2.0.

Caps concurrent open missions. Never encodes educational prioritisation.
"""

from __future__ import annotations

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.mission_state import (
    MissionState,
    is_open_mission_state,
)


class WorkloadPolicy:
    """Deterministic workload caps (stateless)."""

    MAX_ACTIVE_MISSIONS = 1
    MAX_IN_PROGRESS_MISSIONS = 1
    MAX_OPEN_MISSIONS_PER_LEARNER = 20
    MAX_DEFERRED_MISSIONS = 10
    MAX_MISSED_MISSIONS = 10
    MAX_REVISION_MISSIONS = 5

    ACTIVE_STATES = frozenset(
        {
            MissionState.ACTIVE,
            MissionState.IN_PROGRESS,
        }
    )

    @staticmethod
    def open_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        """Return open (non-terminal) missions."""
        return tuple(m for m in missions if is_open_mission_state(m.state))

    @staticmethod
    def active_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        """Return ACTIVE or IN_PROGRESS missions."""
        return tuple(m for m in missions if m.state in WorkloadPolicy.ACTIVE_STATES)

    @staticmethod
    def deferred_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        return tuple(m for m in missions if m.state == MissionState.DEFERRED)

    @staticmethod
    def missed_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        return tuple(m for m in missions if m.state == MissionState.MISSED)

    @staticmethod
    def revision_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        return tuple(
            m
            for m in missions
            if m.is_revision and is_open_mission_state(m.state)
        )

    @staticmethod
    def can_activate(
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        excluding_mission_id: str | None = None,
    ) -> bool:
        """True when activating another mission would not exceed active cap."""
        actives = [
            m
            for m in WorkloadPolicy.active_missions(missions)
            if m.mission_id != excluding_mission_id
        ]
        return len(actives) < WorkloadPolicy.MAX_ACTIVE_MISSIONS

    @staticmethod
    def can_add_open(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> bool:
        """True when another open mission may be added for the learner."""
        return (
            len(WorkloadPolicy.open_missions(missions))
            < WorkloadPolicy.MAX_OPEN_MISSIONS_PER_LEARNER
        )

    @staticmethod
    def can_defer(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> bool:
        return (
            len(WorkloadPolicy.deferred_missions(missions))
            < WorkloadPolicy.MAX_DEFERRED_MISSIONS
        )

    @staticmethod
    def can_mark_missed(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> bool:
        return (
            len(WorkloadPolicy.missed_missions(missions))
            < WorkloadPolicy.MAX_MISSED_MISSIONS
        )

    @staticmethod
    def can_add_revision(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> bool:
        return (
            len(WorkloadPolicy.revision_missions(missions))
            < WorkloadPolicy.MAX_REVISION_MISSIONS
        )
