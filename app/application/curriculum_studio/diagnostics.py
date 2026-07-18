"""Diagnostics — immutable Curriculum Studio diagnostic reports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType

from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio.ports import PORT_NAMES
from app.domain.curriculum_studio.workflow_stage import CANONICAL_WORKFLOW

STUDIO_VERSION = "0.2.0-application"


@dataclass(frozen=True)
class DiagnosticReport:
    """Immutable diagnostic snapshot of Curriculum Studio."""

    studio_version: str
    generated_at: str
    workspace_count: int
    version_count: int
    registered_ports: tuple[str, ...]
    missing_ports: tuple[str, ...]
    port_availability: MappingProxyType
    canonical_workflow: tuple[str, ...]
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "registered_ports", tuple(self.registered_ports)
        )
        object.__setattr__(self, "missing_ports", tuple(self.missing_ports))
        object.__setattr__(
            self, "canonical_workflow", tuple(self.canonical_workflow)
        )
        if not isinstance(self.port_availability, MappingProxyType):
            object.__setattr__(
                self,
                "port_availability",
                MappingProxyType(dict(self.port_availability)),
            )
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self, "metadata", MappingProxyType(dict(self.metadata))
            )


class Diagnostics:
    """Build immutable diagnostic reports (no mutation of Studio state)."""

    def __init__(
        self,
        *,
        registry: StudioRegistry,
        ports: dict | None = None,
        studio_version: str = STUDIO_VERSION,
        clock=None,
    ) -> None:
        self._registry = registry
        self._ports = dict(ports or {})
        self._studio_version = studio_version
        self._clock = clock or (lambda: datetime.now(UTC).isoformat())

    def report(self) -> DiagnosticReport:
        """Generate a diagnostic report."""
        availability: dict[str, bool] = {}
        registered: list[str] = []
        missing: list[str] = []
        for name in PORT_NAMES:
            port = self._ports.get(name)
            if port is None:
                missing.append(name)
                availability[name] = False
            else:
                registered.append(name)
                try:
                    availability[name] = bool(port.is_available())
                except Exception:  # noqa: BLE001 — diagnostics must not raise
                    availability[name] = False
        return DiagnosticReport(
            studio_version=self._studio_version,
            generated_at=str(self._clock()),
            workspace_count=self._registry.workspace_count,
            version_count=self._registry.version_count,
            registered_ports=tuple(registered),
            missing_ports=tuple(missing),
            port_availability=MappingProxyType(availability),
            canonical_workflow=tuple(s.value for s in CANONICAL_WORKFLOW),
            metadata=MappingProxyType({"foundation": False, "application": True}),
        )
