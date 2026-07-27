"""Graph snapshot — point-in-time structural audit of a Learning Graph."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class GraphSnapshot:
    """Point-in-time structural snapshot of a Learning Graph (for audit)."""

    snapshot_id: str
    graph_id: str
    twin_id: str
    node_count: int
    edge_count: int
    created_at: datetime
    reason: str = ""
    node_concept_ids: tuple[str, ...] = ()
    edge_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (self.snapshot_id or "").strip():
            raise ValueError("snapshot_id is required")
        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(
            self, "node_concept_ids", tuple(self.node_concept_ids or ())
        )
        object.__setattr__(self, "edge_ids", tuple(self.edge_ids or ()))
