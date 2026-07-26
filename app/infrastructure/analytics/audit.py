"""Audit metadata attached to analytics emits (PRD-001 §9)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class AuditMetadata:
    """Emit-path audit fields (not educational payload).

    Attributes:
        source: Emitting subsystem label (e.g. ``dispatcher``, ``outbox``).
        emitted_at: Wall clock when the dispatcher accepted the event.
        flag_enabled: Whether ``ANALYTICS_EVENTS_V1`` was on at emit time.
        sink: Sink name used (``null``, ``memory_outbox``, ``sql_outbox``).
        notes: Optional short operational note (never free-text learner content).
    """

    source: str = "analytics"
    emitted_at: datetime | None = None
    flag_enabled: bool = False
    sink: str = "null"
    notes: str = ""

    def with_emit(
        self,
        *,
        flag_enabled: bool,
        sink: str,
        source: str | None = None,
        notes: str | None = None,
    ) -> AuditMetadata:
        """Return a copy stamped for a successful dispatch path."""
        return AuditMetadata(
            source=(source if source is not None else self.source),
            emitted_at=datetime.now(tz=UTC),
            flag_enabled=flag_enabled,
            sink=sink,
            notes=(notes if notes is not None else self.notes),
        )

    def to_dict(self) -> dict[str, str | bool | None]:
        """Plain dict suitable for JSON serialization."""
        return {
            "source": self.source,
            "emitted_at": self.emitted_at.isoformat() if self.emitted_at else None,
            "flag_enabled": self.flag_enabled,
            "sink": self.sink,
            "notes": self.notes,
        }
