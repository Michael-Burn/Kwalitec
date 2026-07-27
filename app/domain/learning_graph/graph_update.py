"""Graph update history value objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class GraphUpdateKind(StrEnum):
    """Kinds of Learning Graph structural updates."""

    CREATE = "create"
    NODE_UPSERT = "node_upsert"
    EDGE_UPSERT = "edge_upsert"
    SYNC_FROM_TWIN = "sync_from_twin"
    SYNC_FROM_EVIDENCE = "sync_from_evidence"
    SNAPSHOT = "snapshot"


@dataclass(frozen=True)
class GraphUpdate:
    """One recorded structural change to a Learning Graph."""

    update_id: str
    graph_id: str
    twin_id: str
    kind: GraphUpdateKind
    summary: str
    created_at: datetime
    payload: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not (self.update_id or "").strip():
            raise ValueError("update_id is required")
        kind = self.kind
        if not isinstance(kind, GraphUpdateKind):
            object.__setattr__(self, "kind", GraphUpdateKind(str(kind)))
        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "payload", tuple(self.payload or ()))

    def payload_dict(self) -> dict[str, str]:
        return dict(self.payload)
