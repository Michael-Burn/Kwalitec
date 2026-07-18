"""Immutable audit trail for Mission Adapter invocations.

Every adapter call should produce an audit record. In-memory only —
never persists, never stores educational content, never stores PII
beyond stable internal identifiers.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType
from uuid import uuid4

from app.application.mission_adapter.dto.audit_record import AuditRecord
from app.application.mission_adapter.dto.routing_decision import (
    RoutingMode,
    SelectedEngine,
)
from app.application.mission_adapter.exceptions import AuditFailure


class AuditService:
    """Generate and retain immutable audit records (in-memory)."""

    def __init__(self, *, clock=None, id_factory=None) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:16])
        self._records: list[AuditRecord] = []

    @property
    def records(self) -> tuple[AuditRecord, ...]:
        """All audit records in insertion order."""
        return tuple(self._records)

    def clear(self) -> None:
        """Drop in-memory records (tests / process reset)."""
        self._records.clear()

    def record(
        self,
        *,
        operation: str,
        learner_id: str,
        routing_mode: RoutingMode,
        selected_engine: SelectedEngine,
        fallbacks: tuple[str, ...] = (),
        duration_ms: float = 0.0,
        comparison_executed: bool = False,
        comparison_id: str | None = None,
        engine_versions: dict[str, str] | MappingProxyType | None = None,
        success: bool = True,
        error_type: str | None = None,
        correlation_id: str | None = None,
        organisation_id: str | None = None,
        metadata: dict[str, str] | None = None,
        audit_id: str | None = None,
        timestamp: datetime | None = None,
    ) -> AuditRecord:
        """Create and store an immutable audit record.

        Raises:
            AuditFailure: When required fields are missing.
        """
        if not operation:
            raise AuditFailure("operation is required")
        if not learner_id:
            raise AuditFailure("learner_id is required")
        versions = engine_versions or {}
        try:
            record = AuditRecord(
                audit_id=audit_id or self._id_factory(),
                timestamp=timestamp or self._clock(),
                operation=operation,
                learner_id=learner_id,
                routing_mode=routing_mode,
                selected_engine=selected_engine,
                fallbacks=fallbacks,
                duration_ms=float(duration_ms),
                comparison_executed=comparison_executed,
                comparison_id=comparison_id,
                engine_versions=MappingProxyType(dict(versions)),
                success=success,
                error_type=error_type,
                correlation_id=correlation_id,
                organisation_id=organisation_id,
                metadata=MappingProxyType(dict(metadata or {})),
            )
        except Exception as exc:  # noqa: BLE001 — wrap construction errors
            raise AuditFailure(f"Failed to build audit record: {exc}") from exc
        self._records.append(record)
        return record

    def for_learner(self, learner_id: str) -> tuple[AuditRecord, ...]:
        """Filter records by stable learner id."""
        return tuple(r for r in self._records if r.learner_id == learner_id)

    def latest(self) -> AuditRecord | None:
        """Most recent audit record, if any."""
        return self._records[-1] if self._records else None
