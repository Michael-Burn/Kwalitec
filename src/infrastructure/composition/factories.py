"""Typed factories for composition-root dependency construction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from application.services import (
    AssessmentApplicationService,
    DashboardApplicationService,
    LearningApplicationService,
    PlanningApplicationService,
    TwinApplicationService,
)
from infrastructure.events.dispatcher import EventDispatcher
from infrastructure.persistence.sqlalchemy.session import create_session_factory
from infrastructure.persistence.sqlalchemy.unit_of_work import (
    SessionFactory,
    SqlAlchemyUnitOfWork,
)


@dataclass(frozen=True, slots=True)
class ApplicationServices:
    """Explicitly expose the application services assembled for one scope."""

    learning: LearningApplicationService
    twin: TwinApplicationService
    assessment: AssessmentApplicationService
    planning: PlanningApplicationService
    dashboard: DashboardApplicationService


def build_session_factory(
    bind: Engine | str,
    **engine_kwargs: Any,
) -> sessionmaker[Session]:
    """Construct the Education OS SQLAlchemy session factory."""
    return create_session_factory(bind, **engine_kwargs)


def build_unit_of_work(
    session_factory: SessionFactory,
    event_dispatcher: EventDispatcher | None = None,
) -> SqlAlchemyUnitOfWork:
    """Construct a UnitOfWork whose repositories share one scoped session."""
    return SqlAlchemyUnitOfWork(session_factory, event_dispatcher=event_dispatcher)


def build_application_services(
    *,
    uow: UnitOfWork,
    events: ApplicationEventPublisher,
    clock: Clock,
) -> ApplicationServices:
    """Construct application services through constructor injection."""
    twin = TwinApplicationService(uow=uow, events=events, clock=clock)
    planning = PlanningApplicationService(
        uow=uow,
        events=events,
        clock=clock,
    )
    return ApplicationServices(
        learning=LearningApplicationService(uow=uow, events=events, clock=clock),
        twin=twin,
        assessment=AssessmentApplicationService(
            uow=uow,
            events=events,
            clock=clock,
        ),
        planning=planning,
        dashboard=DashboardApplicationService(
            twin=twin,
            planning=planning,
            clock=clock,
        ),
    )
