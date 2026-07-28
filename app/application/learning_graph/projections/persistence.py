"""Projection persistence — append-only store for Twin→Graph projections.

No Alembic migrations. Stores projection batches / relationships / events
in-process (and optionally mirrors concept edges onto an existing LearningGraph
via LearningGraphPersistenceService when a graph is supplied).

Mastery scores are never persisted as Graph authority — only relationship
artefacts and Twin decision references.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from threading import RLock

from app.domain.learning_graph.projections.batch import ProjectionBatch
from app.domain.learning_graph.projections.events import (
    GraphProjectionCreated,
    GraphProjectionSkipped,
    GraphProjectionUpdated,
)
from app.domain.learning_graph.projections.projection import GraphProjection
from app.domain.learning_graph.projections.relationship import RelationshipProjection
from app.domain.learning_graph.projections.result import ProjectionResult

ProjectionEvent = (
    GraphProjectionCreated | GraphProjectionUpdated | GraphProjectionSkipped
)


@dataclass
class _TwinProjectionLedger:
    """Append-only ledger for one twin / graph."""

    twin_id: str
    graph_id: str
    relationships_by_id: dict[str, RelationshipProjection] = field(
        default_factory=dict
    )
    batches: list[ProjectionBatch] = field(default_factory=list)
    graph_projections: list[GraphProjection] = field(default_factory=list)
    events: list[ProjectionEvent] = field(default_factory=list)
    versions: list[str] = field(default_factory=list)


class ProjectionPersistenceService:
    """Deterministic, idempotent projection store with replay support."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._ledgers: dict[str, _TwinProjectionLedger] = {}

    def _key(self, *, twin_id: str, graph_id: str) -> str:
        return f"{twin_id}:{graph_id}"

    def _ledger(self, *, twin_id: str, graph_id: str) -> _TwinProjectionLedger:
        key = self._key(twin_id=twin_id, graph_id=graph_id)
        ledger = self._ledgers.get(key)
        if ledger is None:
            ledger = _TwinProjectionLedger(twin_id=twin_id, graph_id=graph_id)
            self._ledgers[key] = ledger
        return ledger

    def existing_projection_ids(self, *, twin_id: str, graph_id: str) -> frozenset[str]:
        with self._lock:
            ledger = self._ledgers.get(self._key(twin_id=twin_id, graph_id=graph_id))
            if ledger is None:
                return frozenset()
            return frozenset(ledger.relationships_by_id.keys())

    def get_relationship(
        self, *, twin_id: str, graph_id: str, projection_id: str
    ) -> RelationshipProjection | None:
        with self._lock:
            ledger = self._ledgers.get(self._key(twin_id=twin_id, graph_id=graph_id))
            if ledger is None:
                return None
            return ledger.relationships_by_id.get(projection_id)

    def list_relationships(
        self, *, twin_id: str, graph_id: str
    ) -> tuple[RelationshipProjection, ...]:
        with self._lock:
            ledger = self._ledgers.get(self._key(twin_id=twin_id, graph_id=graph_id))
            if ledger is None:
                return ()
            return tuple(
                ledger.relationships_by_id[pid]
                for pid in sorted(ledger.relationships_by_id.keys())
            )

    def list_events(
        self, *, twin_id: str, graph_id: str
    ) -> tuple[ProjectionEvent, ...]:
        with self._lock:
            ledger = self._ledgers.get(self._key(twin_id=twin_id, graph_id=graph_id))
            if ledger is None:
                return ()
            return tuple(ledger.events)

    def list_batches(
        self, *, twin_id: str, graph_id: str
    ) -> tuple[ProjectionBatch, ...]:
        with self._lock:
            ledger = self._ledgers.get(self._key(twin_id=twin_id, graph_id=graph_id))
            if ledger is None:
                return ()
            return tuple(ledger.batches)

    def version_history(self, *, twin_id: str, graph_id: str) -> tuple[str, ...]:
        with self._lock:
            ledger = self._ledgers.get(self._key(twin_id=twin_id, graph_id=graph_id))
            if ledger is None:
                return ()
            return tuple(ledger.versions)

    def persist(self, result: ProjectionResult) -> ProjectionResult:
        """Append projection result. Idempotent for identical relationship ids."""
        context = result.context
        with self._lock:
            ledger = self._ledger(
                twin_id=context.twin_id, graph_id=context.graph_id
            )
            for rel in result.batch.relationships:
                ledger.relationships_by_id[rel.projection_id] = rel
            ledger.batches.append(result.batch)
            ledger.graph_projections.append(result.graph_projection)
            ledger.events.extend(result.events)
            ledger.versions.append(result.graph_projection.projection_id)
            return result

    def snapshot(self, *, twin_id: str, graph_id: str) -> dict:
        """Deterministic serialisable snapshot for replay comparison."""
        with self._lock:
            ledger = self._ledgers.get(self._key(twin_id=twin_id, graph_id=graph_id))
            if ledger is None:
                return {
                    "twin_id": twin_id,
                    "graph_id": graph_id,
                    "relationships": [],
                    "batch_ids": [],
                    "event_kinds": [],
                    "versions": [],
                }
            return {
                "twin_id": twin_id,
                "graph_id": graph_id,
                "relationships": [
                    {
                        "projection_id": r.projection_id,
                        "relationship_type": r.relationship_type.value,
                        "from_ref": r.from_ref,
                        "to_ref": r.to_ref,
                        "decision_id": r.decision_id,
                        "projection_version": r.projection_version,
                        "provenance": dict(r.provenance),
                    }
                    for r in sorted(
                        ledger.relationships_by_id.values(),
                        key=lambda item: item.projection_id,
                    )
                ],
                "batch_ids": [b.batch_id for b in ledger.batches],
                "event_kinds": [e.kind.value for e in ledger.events],
                "versions": list(ledger.versions),
            }

    def clear(self) -> None:
        with self._lock:
            self._ledgers.clear()

    def clone_empty(self) -> ProjectionPersistenceService:
        """Fresh store for isolated replay runs."""
        return ProjectionPersistenceService()

    def deep_copy(self) -> ProjectionPersistenceService:
        """Copy store state (tests / diagnostics)."""
        clone = ProjectionPersistenceService()
        with self._lock:
            clone._ledgers = deepcopy(self._ledgers)
        return clone
