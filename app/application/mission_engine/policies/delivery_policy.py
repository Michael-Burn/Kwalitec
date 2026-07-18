"""Stateless delivery rules for Mission Engine 2.0.

Maps mission + optional runtime phase to a delivery action tag.
No UI rendering. No educational reasoning.
"""

from __future__ import annotations

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.mission_state import DeliveryAction, MissionState


class DeliveryPolicy:
    """Deterministic delivery action selection (stateless)."""

    @staticmethod
    def decide(
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
    ) -> DeliveryAction:
        """Select the delivery action for a mission.

        Priority (deterministic):
        1. Terminal / archived → NONE
        2. Revision slot / flag → REVISION
        3. Resume flag or paused runtime → RESUME
        4. IN_PROGRESS or active runtime → CONTINUE
        5. Completed session review posture → REVIEW
        6. Otherwise TODAY
        """
        if mission.state in {
            MissionState.SKIPPED,
            MissionState.ARCHIVED,
        }:
            return DeliveryAction.NONE

        if mission.state == MissionState.COMPLETED:
            return DeliveryAction.REVIEW

        if mission.is_revision or mission.slot.value == "revision":
            return DeliveryAction.REVISION

        phase = (runtime_phase or "").lower()
        if mission.is_resume or phase == "paused":
            return DeliveryAction.RESUME

        if mission.state == MissionState.IN_PROGRESS or phase == "active":
            return DeliveryAction.CONTINUE

        if phase == "completed":
            return DeliveryAction.REVIEW

        return DeliveryAction.TODAY

    @staticmethod
    def is_deliverable(mission: DailyMission) -> bool:
        """True when a non-NONE delivery payload should be produced."""
        return DeliveryPolicy.decide(mission) != DeliveryAction.NONE
