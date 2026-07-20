"""Orchestrate collect → commit → publish, suppressing on rollback."""

from __future__ import annotations

from typing import Any

from infrastructure.events.collector import EventCollector, EventSource
from infrastructure.events.publisher import DomainEventPublisher


class EventDispatcher:
    """Coordinate domain-event collection and post-commit publication.

    Typical usage::

        dispatcher = EventDispatcher(publisher)
        dispatcher.track(aggregate)
        ...
        # On successful commit:
        dispatcher.dispatch_after_commit()

        # On rollback:
        dispatcher.discard()

    Duplicate-publication is prevented: once ``dispatch_after_commit`` has
    been called, calling it again without new ``track`` registrations is a
    no-op (the collected list is empty because ``pull_events`` is
    destructive and ``discard`` clears sources).
    """

    def __init__(self, publisher: DomainEventPublisher) -> None:
        self._publisher = publisher
        self._collector = EventCollector()
        self._staged: list[Any] = []

    def track(self, source: EventSource) -> None:
        """Register an aggregate for event collection."""
        self._collector.track(source)

    def stage(self) -> None:
        """Collect events from tracked aggregates into an internal buffer.

        Call this *before* commit so that events are captured while
        aggregates are still attached to the session.
        """
        self._staged.extend(self._collector.collect())

    def dispatch_after_commit(self) -> None:
        """Publish staged events and reset internal state.

        Must be called only after a successful commit. Safe to call
        multiple times — the second call is a no-op because staged
        events are cleared after publication.
        """
        events = self._staged
        self._staged = []
        self._collector.clear()
        self._publisher.publish(events)

    def discard(self) -> None:
        """Suppress all pending events (call on rollback)."""
        self._staged.clear()
        self._collector.clear()
