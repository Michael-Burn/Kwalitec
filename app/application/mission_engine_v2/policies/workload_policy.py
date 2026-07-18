"""Stateless workload limits for Mission Engine 2.0.

Caps concurrent open missions using structural signals only.
Never encodes educational prioritisation or mastery.
"""

from __future__ import annotations

from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.lifecycle import (
    MissionState,
    is_active_mission_state,
    is_open_mission_state,
)


class WorkloadPolicy:
    """Deterministic workload caps (stateless)."""

    MAX_ACTIVE_MISSIONS = 1
    MAX_OPEN_MISSIONS_PER_LEARNER = 20
    MAX_DEFERRED_MISSIONS = 10
    MAX_MISSED_MISSIONS = 10
    MAX_REVISION_MISSIONS = 5
    MAX_FUTURE_MISSIONS = 14
    MAX_OUTSTANDING_REFLECTIONS = 5
    MAX_REVISION_DEBT = 8

    @staticmethod
    def open_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        return tuple(m for m in missions if is_open_mission_state(m.state))

    @staticmethod
    def active_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        return tuple(m for m in missions if is_active_mission_state(m.state))

    @staticmethod
    def deferred_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        from app.application.mission_engine_v2.lifecycle import MissionSlot

        return tuple(
            m
            for m in missions
            if m.slot == MissionSlot.DEFERRED and is_open_mission_state(m.state)
        )

    @staticmethod
    def missed_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        from app.application.mission_engine_v2.lifecycle import MissionSlot

        return tuple(
            m
            for m in missions
            if m.slot == MissionSlot.MISSED and is_open_mission_state(m.state)
        )

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
    def future_missions(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> tuple[DailyMission, ...]:
        from app.application.mission_engine_v2.lifecycle import MissionSlot

        return tuple(
            m
            for m in missions
            if m.slot == MissionSlot.FUTURE and is_open_mission_state(m.state)
        )

    @staticmethod
    def can_activate(
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        excluding_mission_id: str | None = None,
    ) -> bool:
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

    @staticmethod
    def can_add_future(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> bool:
        return (
            len(WorkloadPolicy.future_missions(missions))
            < WorkloadPolicy.MAX_FUTURE_MISSIONS
        )

    @staticmethod
    def effort_weight(effort: str) -> int:
        """Structural effort band weight (never mastery)."""
        weights = {
            "minimal": 1,
            "light": 1,
            "low": 1,
            "medium": 2,
            "moderate": 2,
            "heavy": 3,
            "high": 3,
            "intensive": 4,
        }
        return weights.get(effort.lower().strip(), 2)

    @staticmethod
    def total_outstanding_reflections(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> int:
        return sum(
            max(0, m.outstanding_reflections)
            for m in missions
            if is_open_mission_state(m.state)
        )

    @staticmethod
    def total_revision_debt(
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> int:
        return sum(
            max(0, m.revision_debt)
            for m in missions
            if is_open_mission_state(m.state)
        )

    @staticmethod
    def has_journey_continuity(
        missions: list[DailyMission] | tuple[DailyMission, ...],
        journey_id: str,
    ) -> bool:
        """True when an open mission already continues ``journey_id``."""
        return any(
            m.journey_id == journey_id and is_open_mission_state(m.state)
            for m in missions
        )

    @staticmethod
    def is_paused(mission: DailyMission) -> bool:
        return mission.state == MissionState.PAUSED
