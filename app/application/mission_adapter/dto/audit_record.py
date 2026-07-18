"""Immutable AuditRecord — append-only adapter invocation trail."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType

from app.application.mission_adapter.dto.routing_decision import (
    RoutingMode,
    SelectedEngine,
)


@dataclass(frozen=True)
class AuditRecord:
    """Immutable record of one Mission Adapter invocation.

    Captures routing and operational metadata. Uses stable internal
    identifiers only — no student-identifying PII beyond learner_id /
    organisation_id keys already treated as internal ids.
    """

    audit_id: str
    timestamp: datetime
    operation: str
    learner_id: str
    routing_mode: RoutingMode
    selected_engine: SelectedEngine
    fallbacks: tuple[str, ...]
    duration_ms: float
    comparison_executed: bool
    comparison_id: str | None
    engine_versions: MappingProxyType
    success: bool
    error_type: str | None = None
    correlation_id: str | None = None
    organisation_id: str | None = None
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.engine_versions, MappingProxyType):
            object.__setattr__(
                self,
                "engine_versions",
                MappingProxyType(dict(self.engine_versions)),
            )
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )
