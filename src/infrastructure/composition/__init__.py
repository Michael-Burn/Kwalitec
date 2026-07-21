"""Composition-root API for the Education OS runtime."""

from __future__ import annotations

from typing import Any

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
    "ProductServices",
    "SynchronousApplicationEventPublisher",
    "SystemClock",
    "SystemUUIDGenerator",
    "build_application_services",
    "build_container",
    "build_product_services",
    "build_product_unit_of_work",
    "build_session_factory",
    "build_unit_of_work",
    "create_container",
]


def __getattr__(name: str) -> Any:
    """Lazy-load product composition symbols to avoid import cycles."""
    if name in {
        "ProductServices",
        "build_product_services",
        "build_product_unit_of_work",
    }:
        from infrastructure.composition import product_factories

        return getattr(product_factories, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
