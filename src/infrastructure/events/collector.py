"""Collect pending domain events from aggregates."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class EventSource(Protocol):
    """Any aggregate that exposes a ``pull_events`` drain."""

    def pull_events(self) -> list[Any]: ...


class EventCollector:
    """Drain pending domain events from registered aggregates.

    After collection the aggregates' internal buffers are cleared
    (``pull_events`` is destructive by convention).
    """

    def __init__(self) -> None:
        self._sources: list[EventSource] = []

    def track(self, source: EventSource) -> None:
        """Register an aggregate whose events should be collected on commit."""
        if source not in self._sources:
            self._sources.append(source)

    def collect(self) -> list[Any]:
        """Pull events from all tracked sources, preserving registration order."""
        events: list[Any] = []
        for source in self._sources:
            events.extend(source.pull_events())
        return events

    def clear(self) -> None:
        """Forget all tracked sources without pulling their events."""
        self._sources.clear()
