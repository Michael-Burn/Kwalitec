"""Event schema versioning policy.

Historical events are never rewritten. Consumers upcast on read so that
future schema evolution never incorrectly replays older payloads.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.infrastructure.events.base import IntegrationEvent

Upcaster = Callable[[IntegrationEvent], IntegrationEvent]


class EventVersionPolicy:
    """Register per-type upcasters from stored version → current version."""

    def __init__(self) -> None:
        self._current: dict[str, int] = {}
        self._upcasters: dict[tuple[str, int], Upcaster] = {}

    def register_current(self, event_type: str, version: int) -> None:
        """Declare the current schema version for ``event_type``."""
        if version < 1:
            raise ValueError("version must be >= 1")
        self._current[event_type] = version

    def register_upcaster(
        self,
        event_type: str,
        from_version: int,
        upcaster: Upcaster,
    ) -> None:
        """Register a single-step upcaster ``from_version`` → ``from_version+1``."""
        if from_version < 1:
            raise ValueError("from_version must be >= 1")
        self._upcasters[(event_type, from_version)] = upcaster

    def current_version(self, event_type: str) -> int:
        """Return the declared current version (default 1)."""
        return self._current.get(event_type, 1)

    def upcast(self, event: IntegrationEvent) -> IntegrationEvent:
        """Upcast ``event`` to the current schema version for its type.

        Never mutates the stored historical event; returns a new instance.
        Unknown older versions without upcasters raise ``ValueError`` so that
        incorrect replay is refused rather than silently misinterpreted.
        """
        target = self.current_version(event.event_type)
        current = event
        while current.event_version < target:
            key = (current.event_type, current.event_version)
            upcaster = self._upcasters.get(key)
            if upcaster is None:
                raise ValueError(
                    f"missing upcaster for {current.event_type} "
                    f"v{current.event_version} → v{current.event_version + 1}"
                )
            nxt = upcaster(current)
            if nxt.event_version != current.event_version + 1:
                raise ValueError(
                    "upcaster must increment event_version by exactly 1"
                )
            if nxt.event_type != current.event_type:
                raise ValueError("upcaster must preserve event_type")
            if nxt.event_id != current.event_id:
                raise ValueError("upcaster must preserve event_id")
            current = nxt
        return current

    def assert_compatible(self, event: IntegrationEvent) -> None:
        """Refuse future/unknown versions that would corrupt replay."""
        current = self.current_version(event.event_type)
        if event.event_version > current:
            raise ValueError(
                f"event version {event.event_version} is newer than "
                f"supported {current} for {event.event_type}"
            )


def default_version_policy() -> EventVersionPolicy:
    """Build the Version 2 default event version policy (all types at v1)."""
    from app.infrastructure.events.types import EVENT_TYPES

    policy = EventVersionPolicy()
    for etype in EVENT_TYPES:
        policy.register_current(etype, 1)
    return policy


def identity_payload_rename(
    old_key: str,
    new_key: str,
) -> Upcaster:
    """Factory: rename a payload key during an upcast step."""

    def _upcast(event: IntegrationEvent) -> IntegrationEvent:
        payload: dict[str, Any] = dict(event.payload)
        if old_key in payload and new_key not in payload:
            payload[new_key] = payload.pop(old_key)
        return IntegrationEvent(
            event_type=event.event_type,
            payload=payload,
            event_id=event.event_id,
            occurred_at=event.occurred_at,
            event_version=event.event_version + 1,
            source=event.source,
            correlation_id=event.correlation_id,
            causation_id=event.causation_id,
        )

    return _upcast
