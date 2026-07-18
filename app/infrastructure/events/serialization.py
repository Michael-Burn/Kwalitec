"""Event serialization for durable storage and transport."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.versioning import (
    EventVersionPolicy,
    default_version_policy,
)

REQUIRED_KEYS = (
    "event_id",
    "event_type",
    "occurred_at",
    "event_version",
    "source",
    "payload",
    "correlation_id",
    "causation_id",
)


class EventSerializer:
    """Serialize / deserialize IntegrationEvent envelopes."""

    def __init__(self, version_policy: EventVersionPolicy | None = None) -> None:
        self._policy = version_policy or default_version_policy()

    @property
    def version_policy(self) -> EventVersionPolicy:
        """Active version policy used on deserialize (upcast)."""
        return self._policy

    def to_dict(self, event: IntegrationEvent) -> dict[str, Any]:
        """Convert an event to a plain dict (ISO timestamps)."""
        return {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "occurred_at": event.occurred_at.isoformat(),
            "event_version": event.event_version,
            "source": event.source,
            "payload": dict(event.payload),
            "correlation_id": event.correlation_id,
            "causation_id": event.causation_id,
        }

    def to_json(self, event: IntegrationEvent) -> str:
        """Serialize an event to a JSON string."""
        return json.dumps(
            self.to_dict(event), separators=(",", ":"), sort_keys=True
        )

    def from_dict(
        self,
        data: dict[str, Any],
        *,
        upcast: bool = True,
    ) -> IntegrationEvent:
        """Deserialize a dict into an IntegrationEvent.

        When ``upcast`` is True, applies the version policy so consumers
        always see the current schema without rewriting storage.
        """
        missing = [k for k in REQUIRED_KEYS if k not in data]
        if missing:
            raise ValueError(f"event dict missing keys: {missing}")
        occurred = data["occurred_at"]
        if isinstance(occurred, str):
            occurred_at = datetime.fromisoformat(occurred)
        elif isinstance(occurred, datetime):
            occurred_at = occurred
        else:
            raise ValueError("occurred_at must be str or datetime")
        event = IntegrationEvent.create(
            str(data["event_type"]),
            dict(data["payload"] or {}),
            event_id=str(data["event_id"]),
            occurred_at=occurred_at,
            event_version=int(data["event_version"]),
            source=str(data["source"]),
            correlation_id=str(data.get("correlation_id") or ""),
            causation_id=str(data.get("causation_id") or ""),
        )
        self._policy.assert_compatible(event)
        if upcast:
            return self._policy.upcast(event)
        return event

    def from_json(self, raw: str, *, upcast: bool = True) -> IntegrationEvent:
        """Deserialize a JSON string into an IntegrationEvent."""
        return self.from_dict(json.loads(raw), upcast=upcast)
