"""Stateless lifecycle transition helpers for Mission Engine 2.0."""

from __future__ import annotations

from app.application.mission_engine_v2.exceptions import InvalidMissionState
from app.application.mission_engine_v2.lifecycle import (
    MissionState,
    MissionTransitionEvent,
    is_terminal_mission_state,
    next_mission_state,
)


class LifecyclePolicy:
    """Validate and resolve mission wrapper transitions."""

    @staticmethod
    def resolve(
        current: MissionState,
        event: MissionTransitionEvent,
    ) -> MissionState:
        """Return the next state or raise InvalidMissionState."""
        nxt = next_mission_state(current, event)
        if nxt is None:
            raise InvalidMissionState(
                f"Cannot apply {event.value} to mission in state {current.value}"
            )
        return nxt

    @staticmethod
    def can_transition(
        current: MissionState,
        event: MissionTransitionEvent,
    ) -> bool:
        return next_mission_state(current, event) is not None

    @staticmethod
    def assert_not_terminal(state: MissionState) -> None:
        if is_terminal_mission_state(state):
            raise InvalidMissionState(
                f"Mission is terminal in state {state.value}"
            )

    @staticmethod
    def assert_completable(state: MissionState) -> None:
        if state not in {MissionState.ACTIVE, MissionState.PAUSED}:
            raise InvalidMissionState(
                f"Cannot complete mission in state {state.value}"
            )

    @staticmethod
    def assert_archivable(state: MissionState) -> None:
        if state != MissionState.COMPLETED:
            raise InvalidMissionState(
                f"Cannot archive mission in state {state.value}"
            )
