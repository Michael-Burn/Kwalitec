"""Produce immutable mission payloads for dashboard / notifications / APIs.

No UI rendering. No educational reasoning.
"""

from __future__ import annotations

from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.dto.mission_card import MissionCard
from app.application.mission_engine_v2.dto.mission_execution import MissionExecution
from app.application.mission_engine_v2.exceptions import DispatchError
from app.application.mission_engine_v2.lifecycle import DispatchAction
from app.application.mission_engine_v2.policies.dispatch_policy import DispatchPolicy


class MissionDispatcher:
    """Build MissionExecution payloads from missions / cards."""

    def dispatch(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
        action: DispatchAction | None = None,
        extra: dict[str, str] | None = None,
    ) -> MissionExecution:
        """Produce an execution payload for ``mission``."""
        resolved = action or DispatchPolicy.decide(
            mission,
            runtime_phase=runtime_phase,
        )
        if resolved == DispatchAction.NONE:
            raise DispatchError(
                f"Mission {mission.mission_id} is not dispatchable "
                f"(state={mission.state.value}, slot={mission.slot.value})"
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
            "sequence_index": str(mission.sequence_index),
        }
        if mission.objective_id:
            payload["objective_id"] = mission.objective_id
        if mission.is_resume:
            payload["is_resume"] = "true"
        if mission.is_revision:
            payload["is_revision"] = "true"
        if mission.explanation_keys:
            payload["explanation_keys"] = ",".join(mission.explanation_keys)
        if extra:
            payload.update({k: str(v) for k, v in extra.items()})
        return MissionExecution(
            mission_id=mission.mission_id,
            action=resolved,
            learner_id=mission.learner_id,
            journey_id=mission.journey_id,
            session_id=mission.session_id,
            topic_id=mission.topic_id,
            title=mission.title,
            scheduled_date=mission.scheduled_date,
            payload=MissionExecution.freeze_payload(payload),
        )

    def dispatch_card(
        self,
        card: MissionCard,
        *,
        extra: dict[str, str] | None = None,
    ) -> MissionExecution:
        """Produce an execution payload from a MissionCard."""
        if card.dispatch_action == DispatchAction.NONE:
            raise DispatchError(f"Card {card.mission_id} is not dispatchable")
        payload = {
            "mission_id": card.mission_id,
            "journey_id": card.journey_id,
            "session_id": card.session_id,
            "topic_id": card.topic_id,
            "slot": card.slot.value,
            "state": card.state.value,
            "action": card.dispatch_action.value,
            "effort": card.effort,
            "sequence_index": str(card.sequence_index),
        }
        if card.objective_id:
            payload["objective_id"] = card.objective_id
        if extra:
            payload.update({k: str(v) for k, v in extra.items()})
        return MissionExecution(
            mission_id=card.mission_id,
            action=card.dispatch_action,
            learner_id=card.learner_id,
            journey_id=card.journey_id,
            session_id=card.session_id,
            topic_id=card.topic_id,
            title=card.title,
            scheduled_date=card.scheduled_date,
            payload=MissionExecution.freeze_payload(payload),
        )

    def dispatch_today(
        self,
        mission: DailyMission,
        *,
        runtime_phase: str | None = None,
    ) -> MissionExecution:
        """Convenience: force TODAY action when lawful."""
        action = DispatchPolicy.decide(mission, runtime_phase=runtime_phase)
        if action == DispatchAction.NONE:
            raise DispatchError("Mission is not dispatchable as today's mission")
        if action not in {
            DispatchAction.TODAY,
            DispatchAction.RESUME,
            DispatchAction.CONTINUE,
        }:
            action = DispatchAction.TODAY
        return self.dispatch(mission, runtime_phase=runtime_phase, action=action)

    def dispatch_resume(self, mission: DailyMission) -> MissionExecution:
        return self.dispatch(mission, action=DispatchAction.RESUME)

    def dispatch_continue(self, mission: DailyMission) -> MissionExecution:
        return self.dispatch(mission, action=DispatchAction.CONTINUE)

    def dispatch_review(self, mission: DailyMission) -> MissionExecution:
        return self.dispatch(mission, action=DispatchAction.REVIEW)

    def dispatch_revision(self, mission: DailyMission) -> MissionExecution:
        return self.dispatch(mission, action=DispatchAction.REVISION)
