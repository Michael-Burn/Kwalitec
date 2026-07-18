"""In-process event catalogue and publish bus."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.types import EVENT_TYPES

Handler = Callable[[IntegrationEvent], None]


class EventRegistry:
    """Catalogue of known event types plus optional in-process handlers."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = {t: [] for t in EVENT_TYPES}
        self._published: list[IntegrationEvent] = []

    @property
    def known_types(self) -> tuple[str, ...]:
        """Return the known Version 2 event type catalogue."""
        return EVENT_TYPES

    def is_known(self, event_type: str) -> bool:
        """True when ``event_type`` is in the catalogue."""
        return event_type in self._handlers

    def subscribe(self, event_type: str, handler: Handler) -> None:
        """Register an in-process handler for ``event_type``."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: IntegrationEvent) -> None:
        """Publish an event to subscribers (append-only local log)."""
        self._published.append(event)
        for handler in self._handlers.get(event.event_type, ()):
            handler(event)

    def published(self) -> tuple[IntegrationEvent, ...]:
        """Return published events in order (test / diagnostics aid)."""
        return tuple(self._published)

    def clear(self) -> None:
        """Clear the local publish log (does not remove subscriptions)."""
        self._published.clear()

    def diagnostics(self) -> dict[str, Any]:
        """Operational diagnostics for the registry."""
        return {
            "known_types": list(EVENT_TYPES),
            "published_count": len(self._published),
            "handler_counts": {k: len(v) for k, v in self._handlers.items()},
        }
