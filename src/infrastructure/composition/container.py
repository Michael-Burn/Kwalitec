"""Application composition root for the Education OS runtime."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Engine

from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from application.ports.uuid_generator import UUIDGenerator
from infrastructure.composition.factories import (
    ApplicationServices,
    build_application_services,
    build_session_factory,
    build_unit_of_work,
)
from infrastructure.composition.providers import (
    ApplicationEventHandler,
    SynchronousApplicationEventPublisher,
    SystemClock,
    SystemUUIDGenerator,
)
from infrastructure.events.dispatcher import EventDispatcher
from infrastructure.events.publisher import DomainEventPublisher
from infrastructure.persistence.sqlalchemy.unit_of_work import SessionFactory


@dataclass(frozen=True, slots=True)
class ApplicationContainer:
    """Explicit dependency graph assembled for one application scope."""

    session_factory: SessionFactory
    unit_of_work: UnitOfWork
    clock: Clock
    uuid_generator: UUIDGenerator
    event_publisher: ApplicationEventPublisher
    services: ApplicationServices


def build_container(
    session_factory: SessionFactory,
    *,
    clock: Clock | None = None,
    uuid_generator: UUIDGenerator | None = None,
    event_publisher: ApplicationEventPublisher | None = None,
    event_handlers: Iterable[ApplicationEventHandler] = (),
) -> ApplicationContainer:
    """Wire infrastructure and application services with explicit dependencies."""
    resolved_event_handlers = tuple(event_handlers)
    if event_publisher is not None and resolved_event_handlers:
        raise ValueError("provide event_publisher or event_handlers, not both")

    resolved_clock = clock or SystemClock()
    resolved_uuid_generator = uuid_generator or SystemUUIDGenerator()
    resolved_event_publisher = event_publisher or SynchronousApplicationEventPublisher(
        resolved_event_handlers
    )
    domain_publisher = DomainEventPublisher()
    domain_dispatcher = EventDispatcher(domain_publisher)
    unit_of_work = build_unit_of_work(
        session_factory, event_dispatcher=domain_dispatcher
    )
    services = build_application_services(
        uow=unit_of_work,
        events=resolved_event_publisher,
        clock=resolved_clock,
    )
    return ApplicationContainer(
        session_factory=session_factory,
        unit_of_work=unit_of_work,
        clock=resolved_clock,
        uuid_generator=resolved_uuid_generator,
        event_publisher=resolved_event_publisher,
        services=services,
    )


def create_container(
    bind: Engine | str,
    *,
    clock: Clock | None = None,
    uuid_generator: UUIDGenerator | None = None,
    event_publisher: ApplicationEventPublisher | None = None,
    event_handlers: Iterable[ApplicationEventHandler] = (),
    **engine_kwargs: Any,
) -> ApplicationContainer:
    """Construct a session factory and assemble the complete dependency graph."""
    session_factory = build_session_factory(bind, **engine_kwargs)
    return build_container(
        session_factory,
        clock=clock,
        uuid_generator=uuid_generator,
        event_publisher=event_publisher,
        event_handlers=event_handlers,
    )
