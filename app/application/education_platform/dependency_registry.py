"""Dependency registry — port registration only.

Never instantiates concrete Educational Core services. Callers inject
implementations; the registry stores references and supports replacement.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Any

from app.application.education_platform.exceptions import DependencyError
from app.application.education_platform.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
)
from app.application.education_platform.policies.validation_policy import (
    ValidationPolicy,
)


class DependencyRegistry:
    """Registers Educational Core ports by stable name.

    Supports replace for test doubles and alternate implementations.
    Does not construct curriculum, blueprint, journey, session, activity,
    or mission engines.
    """

    def __init__(self) -> None:
        self._ports: dict[str, Any] = {}

    def register(self, name: str, port: object) -> None:
        """Register ``port`` under ``name``.

        Raises:
            DependencyError: Unknown name, duplicate, or ``port`` is None.
        """
        try:
            ValidationPolicy.assert_port_name(name)
            ValidationPolicy.assert_no_duplicate(
                name, registered=set(self._ports), allow_replace=False
            )
        except Exception as exc:
            raise DependencyError(str(exc)) from exc
        if port is None:
            raise DependencyError(f"Cannot register None for port {name!r}")
        self._ports[name] = port

    def replace(self, name: str, port: object) -> object | None:
        """Replace an existing registration; return the previous port.

        Raises:
            DependencyError: Unknown name, missing prior registration, or None.
        """
        try:
            ValidationPolicy.assert_port_name(name)
        except Exception as exc:
            raise DependencyError(str(exc)) from exc
        if name not in self._ports:
            raise DependencyError(
                f"Cannot replace unregistered port: {name!r}"
            )
        if port is None:
            raise DependencyError(f"Cannot replace with None for port {name!r}")
        previous = self._ports[name]
        self._ports[name] = port
        return previous

    def get(self, name: str) -> Any:
        """Return the registered port for ``name``.

        Raises:
            DependencyError: When the port is not registered.
        """
        try:
            return self._ports[name]
        except KeyError as exc:
            raise DependencyError(f"Port not registered: {name!r}") from exc

    def has(self, name: str) -> bool:
        """True when ``name`` is registered."""
        return name in self._ports

    def unregister(self, name: str) -> object:
        """Remove and return the port for ``name``.

        Raises:
            DependencyError: When the port is not registered.
        """
        if name not in self._ports:
            raise DependencyError(f"Port not registered: {name!r}")
        return self._ports.pop(name)

    def clear(self) -> None:
        """Remove all registrations (tests / process reset)."""
        self._ports.clear()

    def registered_names(self) -> tuple[str, ...]:
        """Return registered port names in canonical dependency order."""
        return tuple(n for n in DEPENDENCY_CHAIN if n in self._ports)

    def missing_names(self) -> tuple[str, ...]:
        """Return required ports not yet registered (canonical order)."""
        return ValidationPolicy.missing_ports(set(self._ports))

    def as_mapping(self) -> MappingProxyType:
        """Read-only view of name → port."""
        return MappingProxyType(dict(self._ports))

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and name in self._ports

    def __len__(self) -> int:
        return len(self._ports)
