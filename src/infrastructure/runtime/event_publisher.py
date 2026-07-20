"""Event publisher adapter for production runtime (INF-006)."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from application.events.base import ApplicationEvent
from application.ports.event_publisher import ApplicationEventPublisher

ApplicationEventHandler = Callable[[ApplicationEvent], None]


class SynchronousApplicationEventPublisher(ApplicationEventPublisher):
    """Publish application events to injected handlers (no queues)."""

    def __init__(
        self,
        handlers: Iterable[ApplicationEventHandler] = (),
    ) -> None:
        self._handlers = tuple(handlers)

    def publish(self, event: ApplicationEvent) -> None:
        for handler in self._handlers:
            handler(event)

