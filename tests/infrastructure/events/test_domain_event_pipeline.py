"""Tests for the domain-event pipeline (INF-007)."""

from __future__ import annotations

from dataclasses import dataclass

from infrastructure.events.collector import EventCollector, EventSource
from infrastructure.events.dispatcher import EventDispatcher
from infrastructure.events.publisher import DomainEventPublisher

# ── Helpers ──────────────────────────────────────────────────


@dataclass(frozen=True)
class _FakeEvent:
    name: str


class _FakeAggregate:
    """Minimal aggregate that satisfies the EventSource protocol."""

    def __init__(self, events: list[_FakeEvent] | None = None) -> None:
        self._pending: list[_FakeEvent] = list(events or [])

    def pull_events(self) -> list[_FakeEvent]:
        out = list(self._pending)
        self._pending.clear()
        return out

    def add_event(self, event: _FakeEvent) -> None:
        self._pending.append(event)


# ── EventCollector ───────────────────────────────────────────


class TestEventCollector:
    def test_collect_returns_events_in_registration_order(self) -> None:
        a = _FakeAggregate([_FakeEvent("a1"), _FakeEvent("a2")])
        b = _FakeAggregate([_FakeEvent("b1")])
        collector = EventCollector()
        collector.track(a)
        collector.track(b)
        events = collector.collect()
        assert [e.name for e in events] == ["a1", "a2", "b1"]

    def test_collect_drains_pending_events(self) -> None:
        agg = _FakeAggregate([_FakeEvent("x")])
        collector = EventCollector()
        collector.track(agg)
        collector.collect()
        assert collector.collect() == []

    def test_duplicate_track_ignored(self) -> None:
        agg = _FakeAggregate([_FakeEvent("x")])
        collector = EventCollector()
        collector.track(agg)
        collector.track(agg)
        events = collector.collect()
        assert len(events) == 1

    def test_clear_forgets_sources(self) -> None:
        agg = _FakeAggregate([_FakeEvent("x")])
        collector = EventCollector()
        collector.track(agg)
        collector.clear()
        assert collector.collect() == []

    def test_protocol_satisfied(self) -> None:
        assert isinstance(_FakeAggregate(), EventSource)


# ── DomainEventPublisher ─────────────────────────────────────


class TestDomainEventPublisher:
    def test_publish_delivers_to_all_handlers(self) -> None:
        seen_a: list[str] = []
        seen_b: list[str] = []
        pub = DomainEventPublisher()
        pub.subscribe(lambda e: seen_a.append(e.name))
        pub.subscribe(lambda e: seen_b.append(e.name))
        pub.publish([_FakeEvent("e1"), _FakeEvent("e2")])
        assert seen_a == ["e1", "e2"]
        assert seen_b == ["e1", "e2"]

    def test_publish_preserves_order(self) -> None:
        seen: list[str] = []
        pub = DomainEventPublisher()
        pub.subscribe(lambda e: seen.append(e.name))
        pub.publish([_FakeEvent("first"), _FakeEvent("second"), _FakeEvent("third")])
        assert seen == ["first", "second", "third"]

    def test_publish_empty_list_is_noop(self) -> None:
        called = []
        pub = DomainEventPublisher()
        pub.subscribe(lambda e: called.append(e))
        pub.publish([])
        assert called == []


# ── EventDispatcher ──────────────────────────────────────────


class TestEventDispatcher:
    def _make_dispatcher(self) -> tuple[EventDispatcher, list[_FakeEvent]]:
        pub = DomainEventPublisher()
        received: list[_FakeEvent] = []
        pub.subscribe(lambda e: received.append(e))
        return EventDispatcher(pub), received

    def test_commit_publishes_events(self) -> None:
        dispatcher, received = self._make_dispatcher()
        agg = _FakeAggregate([_FakeEvent("committed")])
        dispatcher.track(agg)
        dispatcher.stage()
        dispatcher.dispatch_after_commit()
        assert [e.name for e in received] == ["committed"]

    def test_rollback_suppresses_events(self) -> None:
        dispatcher, received = self._make_dispatcher()
        agg = _FakeAggregate([_FakeEvent("lost")])
        dispatcher.track(agg)
        dispatcher.stage()
        dispatcher.discard()
        assert received == []

    def test_ordering_preserved(self) -> None:
        dispatcher, received = self._make_dispatcher()
        a = _FakeAggregate([_FakeEvent("a")])
        b = _FakeAggregate([_FakeEvent("b")])
        dispatcher.track(a)
        dispatcher.track(b)
        dispatcher.stage()
        dispatcher.dispatch_after_commit()
        assert [e.name for e in received] == ["a", "b"]

    def test_duplicate_publication_prevented(self) -> None:
        dispatcher, received = self._make_dispatcher()
        agg = _FakeAggregate([_FakeEvent("once")])
        dispatcher.track(agg)
        dispatcher.stage()
        dispatcher.dispatch_after_commit()
        dispatcher.dispatch_after_commit()
        assert len(received) == 1

    def test_discard_then_dispatch_is_empty(self) -> None:
        dispatcher, received = self._make_dispatcher()
        agg = _FakeAggregate([_FakeEvent("gone")])
        dispatcher.track(agg)
        dispatcher.stage()
        dispatcher.discard()
        dispatcher.dispatch_after_commit()
        assert received == []

    def test_new_events_after_dispatch(self) -> None:
        dispatcher, received = self._make_dispatcher()
        agg = _FakeAggregate([_FakeEvent("first")])
        dispatcher.track(agg)
        dispatcher.stage()
        dispatcher.dispatch_after_commit()

        agg.add_event(_FakeEvent("second"))
        dispatcher.track(agg)
        dispatcher.stage()
        dispatcher.dispatch_after_commit()
        assert [e.name for e in received] == ["first", "second"]
