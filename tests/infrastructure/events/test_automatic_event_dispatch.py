"""Tests for automatic domain event dispatch via UnitOfWork (INF-008)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock

from infrastructure.events.dispatcher import EventDispatcher
from infrastructure.events.publisher import DomainEventPublisher
from infrastructure.persistence.sqlalchemy.repositories.digital_twin_repository import (
    SqlAlchemyDigitalTwinRepository,
)
from infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork


@dataclass(frozen=True)
class _FakeEvent:
    name: str


class _FakeAggregate:
    """Minimal aggregate satisfying EventSource."""

    def __init__(self, events: list[_FakeEvent] | None = None) -> None:
        self._pending: list[_FakeEvent] = list(events or [])

    def pull_events(self) -> list[_FakeEvent]:
        out = list(self._pending)
        self._pending.clear()
        return out

    def add_event(self, event: _FakeEvent) -> None:
        self._pending.append(event)


def _make_uow_and_receiver() -> tuple[SqlAlchemyUnitOfWork, list[Any]]:
    """Build a UoW with a real EventDispatcher backed by a capturing publisher."""
    publisher = DomainEventPublisher()
    received: list[Any] = []
    publisher.subscribe(lambda e: received.append(e))
    dispatcher = EventDispatcher(publisher)

    session = MagicMock()
    session.begin = MagicMock()
    session.commit = MagicMock()
    session.rollback = MagicMock()
    session.close = MagicMock()
    session.merge = MagicMock()

    uow = SqlAlchemyUnitOfWork(lambda: session, event_dispatcher=dispatcher)
    return uow, received


class TestCommitPublishesEventsAutomatically:
    def test_commit_publishes_tracked_aggregate_events(self) -> None:
        uow, received = _make_uow_and_receiver()
        agg = _FakeAggregate([_FakeEvent("auto")])

        with uow:
            uow._track_aggregate(agg)
            uow.commit()

        assert [e.name for e in received] == ["auto"]

    def test_multiple_aggregates_published_in_order(self) -> None:
        uow, received = _make_uow_and_receiver()
        a = _FakeAggregate([_FakeEvent("a1")])
        b = _FakeAggregate([_FakeEvent("b1")])

        with uow:
            uow._track_aggregate(a)
            uow._track_aggregate(b)
            uow.commit()

        assert [e.name for e in received] == ["a1", "b1"]


class TestRollbackSuppressesEvents:
    def test_explicit_rollback_discards_events(self) -> None:
        uow, received = _make_uow_and_receiver()
        agg = _FakeAggregate([_FakeEvent("lost")])

        with uow:
            uow._track_aggregate(agg)
            uow.rollback()

        assert received == []

    def test_implicit_rollback_on_exception_discards_events(self) -> None:
        uow, received = _make_uow_and_receiver()
        agg = _FakeAggregate([_FakeEvent("lost")])

        try:
            with uow:
                uow._track_aggregate(agg)
                raise ValueError("boom")
        except ValueError:
            pass

        assert received == []

    def test_commit_failure_discards_events(self) -> None:
        publisher = DomainEventPublisher()
        received: list[Any] = []
        publisher.subscribe(lambda e: received.append(e))
        dispatcher = EventDispatcher(publisher)

        session = MagicMock()
        session.begin = MagicMock()
        session.commit = MagicMock(side_effect=RuntimeError("db failure"))
        session.rollback = MagicMock()
        session.close = MagicMock()

        uow = SqlAlchemyUnitOfWork(lambda: session, event_dispatcher=dispatcher)
        agg = _FakeAggregate([_FakeEvent("never")])

        try:
            with uow:
                uow._track_aggregate(agg)
                uow.commit()
        except RuntimeError:
            pass

        assert received == []


class TestDuplicatePublicationImpossible:
    def test_second_commit_does_not_republish(self) -> None:
        uow, received = _make_uow_and_receiver()
        agg = _FakeAggregate([_FakeEvent("once")])

        with uow:
            uow._track_aggregate(agg)
            uow.commit()

        assert len(received) == 1


class TestNoManualPullEventsInServices:
    def test_application_services_contain_no_pull_events(self) -> None:
        """Structural check: no pull_events() in application service source."""
        import importlib
        import inspect

        from application.services import (
            AssessmentApplicationService,
            LearningApplicationService,
            PlanningApplicationService,
            TwinApplicationService,
        )

        for cls in (
            LearningApplicationService,
            TwinApplicationService,
            AssessmentApplicationService,
            PlanningApplicationService,
        ):
            source = inspect.getsource(importlib.import_module(cls.__module__))
            assert "pull_events" not in source, (
                f"{cls.__name__} still contains pull_events()"
            )


class TestRepositoryTracking:
    """Verify that repository save() calls trigger aggregate tracking."""

    def test_save_invokes_on_save_callback(self) -> None:
        """The on_save callback fires with the aggregate before mapping."""
        tracked: list[Any] = []
        session = MagicMock()
        session.merge = MagicMock()

        def capture_and_abort(aggregate: Any) -> None:
            tracked.append(aggregate)
            raise _TrackingProbeError()

        repo = SqlAlchemyDigitalTwinRepository(
            session, on_save=capture_and_abort
        )

        agg = _FakeAggregate([_FakeEvent("x")])
        try:
            repo.save(agg)  # type: ignore[arg-type]
        except _TrackingProbeError:
            pass

        assert len(tracked) == 1
        assert tracked[0] is agg


class _TrackingProbeError(Exception):
    """Sentinel to abort save() after the callback fires."""


class TestUoWWithoutDispatcher:
    """Backward compatibility: UoW works without an event dispatcher."""

    def test_commit_succeeds_without_dispatcher(self) -> None:
        session = MagicMock()
        session.begin = MagicMock()
        session.commit = MagicMock()
        session.close = MagicMock()

        uow = SqlAlchemyUnitOfWork(lambda: session)
        with uow:
            uow.commit()

    def test_rollback_succeeds_without_dispatcher(self) -> None:
        session = MagicMock()
        session.begin = MagicMock()
        session.rollback = MagicMock()
        session.close = MagicMock()

        uow = SqlAlchemyUnitOfWork(lambda: session)
        with uow:
            uow.rollback()
