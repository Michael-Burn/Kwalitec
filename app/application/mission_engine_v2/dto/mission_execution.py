"""Immutable MissionExecution — dispatch payload for adapters / APIs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from types import MappingProxyType

from app.application.mission_engine_v2.lifecycle import DispatchAction


@dataclass(frozen=True)
class MissionExecution:
    """Immutable execution / delivery payload (not UI).

    Suitable for dashboard assemblers, notifications, and future APIs.
    """

    mission_id: str
    action: DispatchAction
    learner_id: str
    journey_id: str
    session_id: str
    topic_id: str
    title: str
    scheduled_date: date
    payload: MappingProxyType

    @staticmethod
    def freeze_payload(data: dict[str, str]) -> MappingProxyType:
        """Freeze a string-keyed payload mapping."""
        return MappingProxyType(dict(data))
