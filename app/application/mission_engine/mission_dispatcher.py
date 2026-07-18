"""Produce mission delivery payloads for adapters (not UI).

Examples: today's mission, resume, continue, review, revision.
"""

from __future__ import annotations

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.dto.mission_delivery import MissionDelivery
from app.application.mission_engine.dto.mission_summary import MissionSummary
from app.application.mission_engine.exceptions import DeliveryError
from app.application.mission_engine.mission_state import DeliveryAction
from app.application.mission_engine.policies.delivery_policy import DeliveryPolicy


class MissionDispatcher:
    """Build MissionDelivery payloads from missions / summaries."""

    def dispatch(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
        action: DeliveryAction | None = None,
        extra: dict[str, str] | None = None,
    ) -> MissionDelivery:
        """Produce a delivery payload for ``mission``."""
        resolved = action or DeliveryPolicy.decide(
            mission,
            runtime_phase=runtime_phase,
        )
        if resolved == DeliveryAction.NONE:
            raise DeliveryError(
                f"Mission {mission.mission_id} is not deliverable "
                f"(state={mission.state.value})"
            )
        payload = {
            "mission_id": mission.mission_id,
            "journey_id": mission.journey_id,
            "session_id": mission.session_id,
            "topic_id": mission.topic_id,
            "slot": mission.slot.value,
            "state": mission.state.value,
            "action": resolved.value,
            "effort": mission.effort,
        }
        if mission.objective_id:
            payload["objective_id"] = mission.objective_id
        if mission.is_resume:
            payload["is_resume"] = "true"
        if mission.is_revision:
            payload["is_revision"] = "true"
        if extra:
            payload.update({k: str(v) for k, v in extra.items()})
        return MissionDelivery(
            mission_id=mission.mission_id,
            action=resolved,
            learner_id=mission.learner_id,
            journey_id=mission.journey_id,
            session_id=mission.session_id,
            topic_id=mission.topic_id,
            title=mission.title,
            scheduled_date=mission.scheduled_date,
            payload=MissionDelivery.freeze_payload(payload),
        )

    def dispatch_summary(
        self,
        summary: MissionSummary,
        *,
        extra: dict[str, str] | None = None,
    ) -> MissionDelivery:
        """Produce a delivery payload from a MissionSummary."""
        if summary.delivery_action == DeliveryAction.NONE:
            raise DeliveryError(
                f"Summary {summary.mission_id} is not deliverable"
            )
        payload = {
            "mission_id": summary.mission_id,
            "journey_id": summary.journey_id,
            "session_id": summary.session_id,
            "topic_id": summary.topic_id,
            "slot": summary.slot.value,
            "state": summary.state.value,
            "action": summary.delivery_action.value,
            "effort": summary.effort,
        }
        if summary.objective_id:
            payload["objective_id"] = summary.objective_id
        if extra:
            payload.update({k: str(v) for k, v in extra.items()})
        return MissionDelivery(
            mission_id=summary.mission_id,
            action=summary.delivery_action,
            learner_id=summary.learner_id,
            journey_id=summary.journey_id,
            session_id=summary.session_id,
            topic_id=summary.topic_id,
            title=summary.title,
            scheduled_date=summary.scheduled_date,
            payload=MissionDelivery.freeze_payload(payload),
        )

    def dispatch_today(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
    ) -> MissionDelivery:
        """Convenience: force TODAY action when lawful."""
        action = DeliveryPolicy.decide(mission, runtime_phase=runtime_phase)
        if action == DeliveryAction.NONE:
            raise DeliveryError("Mission is not deliverable as today's mission")
        if action not in {
            DeliveryAction.TODAY,
            DeliveryAction.RESUME,
            DeliveryAction.CONTINUE,
        }:
            action = DeliveryAction.TODAY
        return self.dispatch(mission, runtime_phase=runtime_phase, action=action)

    def dispatch_resume(self, mission: DailyMission) -> MissionDelivery:
        """Convenience: resume delivery."""
        return self.dispatch(mission, action=DeliveryAction.RESUME)

    def dispatch_continue(self, mission: DailyMission) -> MissionDelivery:
        """Convenience: continue delivery."""
        return self.dispatch(mission, action=DeliveryAction.CONTINUE)

    def dispatch_review(self, mission: DailyMission) -> MissionDelivery:
        """Convenience: review delivery."""
        return self.dispatch(mission, action=DeliveryAction.REVIEW)

    def dispatch_revision(self, mission: DailyMission) -> MissionDelivery:
        """Convenience: revision delivery."""
        return self.dispatch(mission, action=DeliveryAction.REVISION)
