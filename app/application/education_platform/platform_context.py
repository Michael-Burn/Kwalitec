"""Platform context — immutable composition snapshot for a platform instance."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
)


@dataclass(frozen=True)
class PlatformContext:
    """Read-only view of composed platform identity and registrations.

    Holds no educational state. Used by health, diagnostics, and validators.
    """

    platform_version: str
    registered_ports: tuple[str, ...]
    missing_ports: tuple[str, ...]
    component_versions: MappingProxyType
    dependency_graph: tuple[tuple[str, str], ...]

    @staticmethod
    def from_registry(
        registry: DependencyRegistry,
        *,
        platform_version: str,
    ) -> PlatformContext:
        """Build an immutable context from the current registry state."""
        versions: dict[str, str] = {}
        for name in registry.registered_names():
            port = registry.get(name)
            version = getattr(port, "component_version", "unknown")
            versions[name] = str(version)
        # Edges follow the canonical chain among registered neighbours.
        registered = set(registry.registered_names())
        edges: list[tuple[str, str]] = []
        ordered = [n for n in DEPENDENCY_CHAIN if n in registered]
        for i in range(len(ordered) - 1):
            edges.append((ordered[i], ordered[i + 1]))
        return PlatformContext(
            platform_version=platform_version,
            registered_ports=registry.registered_names(),
            missing_ports=registry.missing_names(),
            component_versions=MappingProxyType(versions),
            dependency_graph=tuple(edges),
        )
