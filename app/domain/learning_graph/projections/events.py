"""Factual Learning Graph projection events (AP-002D4).

No orchestration. No Mission / Tutor notifications.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class ProjectionEventKind(StrEnum):
    """Kinds of factual projection events."""

    CREATED = "graph_projection_created"
    UPDATED = "graph_projection_updated"
    SKIPPED = "graph_projection_skipped"


@dataclass(frozen=True, slots=True)
class GraphProjectionCreated:
    """A new relationship projection was accepted into the Graph."""

    event_id: str
    projection_id: str
    graph_id: str
    twin_id: str
    decision_id: str
    relationship_type: str
    occurred_at: datetime
    projection_version: str
    kind: ProjectionEventKind = ProjectionEventKind.CREATED

    def __post_init__(self) -> None:
        _require_nonblank(self, "event_id", "projection_id", "graph_id", "twin_id")
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


@dataclass(frozen=True, slots=True)
class GraphProjectionUpdated:
    """An existing relationship projection was refreshed (same identity)."""

    event_id: str
    projection_id: str
    graph_id: str
    twin_id: str
    decision_id: str
    relationship_type: str
    occurred_at: datetime
    projection_version: str
    kind: ProjectionEventKind = ProjectionEventKind.UPDATED

    def __post_init__(self) -> None:
        _require_nonblank(self, "event_id", "projection_id", "graph_id", "twin_id")
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


@dataclass(frozen=True, slots=True)
class GraphProjectionSkipped:
    """A decision produced no new graph relationship (idempotent / non-projectable)."""

    event_id: str
    graph_id: str
    twin_id: str
    decision_id: str
    reason_code: str
    occurred_at: datetime
    projection_version: str
    projection_id: str = ""
    kind: ProjectionEventKind = ProjectionEventKind.SKIPPED

    def __post_init__(self) -> None:
        _require_nonblank(
            self, "event_id", "graph_id", "twin_id", "decision_id", "reason_code"
        )
        when = self.occurred_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "occurred_at", when.astimezone(UTC).replace(tzinfo=None)
            )


def _require_nonblank(obj: object, *fields: str) -> None:
    for field_name in fields:
        if not (getattr(obj, field_name) or "").strip():
            raise ValueError(f"{field_name} is required")
