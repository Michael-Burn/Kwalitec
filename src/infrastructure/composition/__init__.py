"""Composition-root API for the Education OS runtime."""

from __future__ import annotations

from infrastructure.composition.container import (
    ApplicationContainer,
    build_container,
    create_container,
)
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

__all__ = [
    "ApplicationContainer",
    "ApplicationEventHandler",
    "ApplicationServices",
    "SynchronousApplicationEventPublisher",
    "SystemClock",
    "SystemUUIDGenerator",
    "build_application_services",
    "build_container",
    "build_session_factory",
    "build_unit_of_work",
    "create_container",
]
