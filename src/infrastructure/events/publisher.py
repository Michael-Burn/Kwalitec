"""Publish domain events to registered handlers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DomainEventHandler = Callable[[Any], None]


class DomainEventPublisher:
    """Fan-out domain events to synchronous handlers.

    Handlers are called in registration order. Each event is delivered to
    every handler exactly once per ``publish`` invocation (duplicate
    protection is handled by the dispatcher, not here).
    """

    def __init__(self) -> None:
        self._handlers: list[DomainEventHandler] = []

    def subscribe(self, handler: DomainEventHandler) -> None:
        """Add a handler that will receive all published domain events."""
        self._handlers.append(handler)

    def publish(self, events: list[Any]) -> None:
        """Deliver *events* to every registered handler, preserving order."""
        for event in events:
            for handler in self._handlers:
                handler(event)
