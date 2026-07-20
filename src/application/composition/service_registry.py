"""Service registry — explicit dependency catalogue for one composition scope.

Holds references assembled by the composition root. Supports replacement for
tests and alternate providers. Does not construct collaborators and must not
be used as a runtime service locator from business code.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Any

# Canonical registration order for the Educational Operating System graph.
SERVICE_NAMES: tuple[str, ...] = (
    "session_factory",
    "unit_of_work",
    "clock",
    "uuid_generator",
    "event_publisher",
    "learning",
    "twin",
    "assessment",
    "planning",
    "dashboard",
    "mission_generator",
    "recommendation_generator",
    "study_planner",
    "progress_evaluator",
    "explanation_builder",
    "experience_generator",
    "ai_provider",
    "mission_enricher",
    "recommendation_enricher",
    "educational_pipeline",
)

_KNOWN_NAMES = frozenset(SERVICE_NAMES)


class CompositionError(Exception):
    """Raised when composition registration or resolution fails."""


class ServiceRegistry:
    """Registers assembled collaborators by stable name.

    Instances are scoped to one assembled application graph. There is no
    process-global registry.
    """

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: object) -> None:
        """Register ``service`` under ``name``.

        Raises:
            CompositionError: Unknown name, duplicate, or ``service`` is None.
        """
        if name not in _KNOWN_NAMES:
            raise CompositionError(f"Unknown service name: {name!r}")
        if name in self._services:
            raise CompositionError(f"Service already registered: {name!r}")
        if service is None:
            raise CompositionError(f"Cannot register None for service {name!r}")
        self._services[name] = service

    def replace(self, name: str, service: object) -> object:
        """Replace an existing registration; return the previous service.

        Raises:
            CompositionError: Unknown name, missing prior registration, or None.
        """
        if name not in _KNOWN_NAMES:
            raise CompositionError(f"Unknown service name: {name!r}")
        if name not in self._services:
            raise CompositionError(
                f"Cannot replace unregistered service: {name!r}"
            )
        if service is None:
            raise CompositionError(f"Cannot replace with None for service {name!r}")
        previous = self._services[name]
        self._services[name] = service
        return previous

    def get(self, name: str) -> Any:
        """Return the registered service for ``name``.

        Raises:
            CompositionError: When the service is not registered.
        """
        try:
            return self._services[name]
        except KeyError as exc:
            raise CompositionError(f"Service not registered: {name!r}") from exc

    def has(self, name: str) -> bool:
        """True when ``name`` is registered."""
        return name in self._services

    def registered_names(self) -> tuple[str, ...]:
        """Return registered names in canonical order."""
        return tuple(name for name in SERVICE_NAMES if name in self._services)

    def missing_names(self) -> tuple[str, ...]:
        """Return known names not yet registered (canonical order)."""
        return tuple(name for name in SERVICE_NAMES if name not in self._services)

    def as_mapping(self) -> MappingProxyType[str, Any]:
        """Read-only view of name → service."""
        return MappingProxyType(dict(self._services))

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and name in self._services

    def __len__(self) -> int:
        return len(self._services)
