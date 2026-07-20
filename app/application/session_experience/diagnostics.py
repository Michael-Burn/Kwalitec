"""Diagnostics — immutable Learning Session Experience diagnostic reports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType

from app.application.session_experience._registry import SessionExperienceRegistry
from app.application.session_experience.ports import PORT_NAMES
from app.domain.session_experience.session_workspace import CANONICAL_SURFACES

SESSION_EXPERIENCE_VERSION = "0.1.0-session"


@dataclass(frozen=True)
class DiagnosticReport:
    """Immutable diagnostic snapshot of Learning Session Experience."""

    experience_version: str
    generated_at: str
    workspace_count: int
    session_count: int
    registered_ports: tuple[str, ...]
    missing_ports: tuple[str, ...]
    port_availability: MappingProxyType
    canonical_surfaces: tuple[str, ...]
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "registered_ports", tuple(self.registered_ports)
        )
        object.__setattr__(self, "missing_ports", tuple(self.missing_ports))
        object.__setattr__(
            self, "canonical_surfaces", tuple(self.canonical_surfaces)
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
    """Build immutable diagnostic reports (no mutation of session state)."""

    def __init__(
        self,
        *,
        registry: SessionExperienceRegistry,
        ports: dict | None = None,
        experience_version: str = SESSION_EXPERIENCE_VERSION,
        clock=None,
    ) -> None:
        self._registry = registry
        self._ports = dict(ports or {})
        self._experience_version = experience_version
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
            experience_version=self._experience_version,
            generated_at=str(self._clock()),
            workspace_count=self._registry.workspace_count,
            session_count=self._registry.session_count,
            registered_ports=tuple(registered),
            missing_ports=tuple(missing),
            port_availability=MappingProxyType(availability),
            canonical_surfaces=tuple(s.value for s in CANONICAL_SURFACES),
            metadata=MappingProxyType(
                {
                    "foundation": True,
                    "ui": True,
                    "owns_educational_law": False,
                    "linear_flow": True,
                }
            ),
        )
