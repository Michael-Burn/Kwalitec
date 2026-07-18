"""Stateless dispatch rules for Mission Engine 2.0.

Produces action tags for dashboard / notification / API payloads.
No UI rendering. No educational reasoning.
"""

from __future__ import annotations

from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.lifecycle import (
    DispatchAction,
    MissionSlot,
    MissionState,
)


class DispatchPolicy:
    """Decide dispatch action from mission posture and optional runtime phase."""

    @staticmethod
    def decide(
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
    ) -> DispatchAction:
        """Resolve a dispatch action for ``mission``."""
        if mission.state == MissionState.ARCHIVED:
            return DispatchAction.NONE
        if mission.state == MissionState.COMPLETED:
            return DispatchAction.REVIEW
        if mission.is_revision or mission.slot == MissionSlot.REVISION:
            return DispatchAction.REVISION
        if mission.slot == MissionSlot.DEFERRED:
            return DispatchAction.DEFERRED
        if mission.slot == MissionSlot.MISSED:
            return DispatchAction.TODAY
        phase = (runtime_phase or "").lower().strip()
        if mission.state == MissionState.PAUSED or phase == "paused":
            return DispatchAction.RESUME
        if mission.is_resume:
            return DispatchAction.RESUME
        if mission.state == MissionState.ACTIVE or phase == "active":
            return DispatchAction.CONTINUE
        if mission.slot == MissionSlot.TODAY:
            return DispatchAction.TODAY
        if mission.slot == MissionSlot.FUTURE:
            return DispatchAction.NONE
        if mission.state in {MissionState.PLANNED, MissionState.READY}:
            return DispatchAction.TODAY
        return DispatchAction.NONE

    @staticmethod
    def is_deliverable(action: DispatchAction) -> bool:
        return action != DispatchAction.NONE
