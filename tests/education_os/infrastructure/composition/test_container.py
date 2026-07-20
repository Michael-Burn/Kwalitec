"""Composition-root construction and dependency-injection tests (INF-005)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from application.events.base import ApplicationEvent
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.uuid_generator import UUIDGenerator
from application.services import (
    AssessmentApplicationService,
    DashboardApplicationService,
    LearningApplicationService,
    PlanningApplicationService,
    TwinApplicationService,
)
from infrastructure.composition import (
    SynchronousApplicationEventPublisher,
    SystemClock,
    SystemUUIDGenerator,
    build_container,
    create_container,
)
from infrastructure.persistence.sqlalchemy import SqlAlchemyUnitOfWork
from tests.education_os.application.fakes import (
    FixedClock,
    InMemoryEventPublisher,
    SequenceUUIDGenerator,
)


def make_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=create_engine("sqlite+pysqlite:///:memory:"))


def test_default_container_wires_complete_dependency_graph() -> None:
    session_factory = make_session_factory()

    container = build_container(session_factory)

    assert container.session_factory is session_factory
    assert isinstance(container.unit_of_work, SqlAlchemyUnitOfWork)
    assert isinstance(container.clock, SystemClock)
    assert isinstance(container.uuid_generator, SystemUUIDGenerator)
    assert isinstance(
        container.event_publisher,
        SynchronousApplicationEventPublisher,
    )
    assert isinstance(container.services.learning, LearningApplicationService)
    assert isinstance(container.services.twin, TwinApplicationService)
    assert isinstance(container.services.assessment, AssessmentApplicationService)
    assert isinstance(container.services.planning, PlanningApplicationService)
    assert isinstance(container.services.dashboard, DashboardApplicationService)


def test_container_uses_injected_port_implementations() -> None:
    clock = FixedClock()
    uuids = SequenceUUIDGenerator()
    events = InMemoryEventPublisher()

    container = build_container(
        make_session_factory(),
        clock=clock,
        uuid_generator=uuids,
        event_publisher=events,
    )

    assert container.clock is clock
    assert container.uuid_generator is uuids
    assert container.event_publisher is events
    for service in (
        container.services.learning,
        container.services.twin,
        container.services.assessment,
        container.services.planning,
    ):
        assert service._uow is container.unit_of_work
        assert service._clock is clock
        assert service._events is events
    assert container.services.dashboard._twin is container.services.twin
    assert container.services.dashboard._planning is container.services.planning
    assert container.services.dashboard._clock is clock


def test_create_container_constructs_session_factory_from_bind() -> None:
    container = create_container("sqlite+pysqlite:///:memory:")

    with container.unit_of_work:
        assert container.unit_of_work.is_active


def test_default_providers_satisfy_application_ports() -> None:
    clock = SystemClock()
    uuids = SystemUUIDGenerator()
    events = SynchronousApplicationEventPublisher()

    assert isinstance(clock, Clock)
    assert isinstance(uuids, UUIDGenerator)
    assert isinstance(events, ApplicationEventPublisher)
    assert clock.now().tzinfo is UTC
    assert str(UUID(uuids.new_id()))


def test_event_publisher_notifies_injected_handlers_in_order() -> None:
    published: list[tuple[str, ApplicationEvent]] = []
    event = ApplicationEvent(occurred_at=datetime(2026, 7, 20, tzinfo=UTC))
    container = build_container(
        make_session_factory(),
        event_handlers=(
            lambda value: published.append(("first", value)),
            lambda value: published.append(("second", value)),
        ),
    )

    container.event_publisher.publish(event)

    assert published == [("first", event), ("second", event)]


def test_event_handlers_and_publisher_are_mutually_exclusive() -> None:
    with pytest.raises(ValueError, match="not both"):
        build_container(
            make_session_factory(),
            event_publisher=InMemoryEventPublisher(),
            event_handlers=(lambda event: None,),
        )
