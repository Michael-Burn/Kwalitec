"""Immutable MissionDelivery — delivery payload for adapters (not UI)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from types import MappingProxyType

from app.application.mission_engine.mission_state import DeliveryAction


@dataclass(frozen=True)
class MissionDelivery:
    """Delivery payload describing how a mission should be presented.

    No UI. Consumers (dashboard assemblers, V1 adapters) interpret ``action``.

    Attributes:
        mission_id: Mission identity.
        action: Delivery action tag.
        learner_id: Owning learner.
        journey_id: Parent journey.
        session_id: Bound session.
        topic_id: Curriculum topic.
        title: Structural title.
        scheduled_date: Commitment date.
        payload: Read-only string map for adapter fields.
    """

    mission_id: str
    action: DeliveryAction
    learner_id: str
    journey_id: str
    session_id: str
    topic_id: str
    title: str
    scheduled_date: date
    payload: MappingProxyType

    @staticmethod
    def freeze_payload(data: dict[str, str] | None = None) -> MappingProxyType:
        """Freeze a string map into an immutable payload."""
        return MappingProxyType(dict(data or {}))
