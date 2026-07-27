"""Persistence for Learning Graph structure (SDT-003).

Does not store Twin mastery/gap/recommendation rows — those remain in SDT-001.
Projected mastery fields on nodes are caches for traversal/diagnostics only.
"""

from __future__ import annotations

import json
from typing import Any

from app.domain.learning_graph.graph_edge import GraphEdge
from app.domain.learning_graph.graph_node import GraphNode, PrerequisiteStatus
from app.domain.learning_graph.graph_snapshot import GraphSnapshot
from app.domain.learning_graph.graph_update import GraphUpdate, GraphUpdateKind
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.learning_graph.mastery_link import MasteryLink
from app.domain.learning_graph.relationship import RelationshipType
from app.extensions import db
from app.models.learning_graph import (
    LgGraphEdge,
    LgGraphNode,
    LgGraphSnapshot,
    LgGraphUpdateHistory,
    LgLearningGraph,
)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    return json.loads(raw)


class LearningGraphPersistenceService:
    """Load and replace Learning Graph structure for a Twin."""

    def save_graph_root(self, graph: LearningGraph) -> LgLearningGraph:
        row = LgLearningGraph.query.filter_by(graph_id=graph.graph_id).first()
        if row is None:
            row = LgLearningGraph(
                graph_id=graph.graph_id,
                twin_id=graph.twin_id,
                student_id=graph.student_id,
                version=graph.version,
                created_at=graph.created_at,
                updated_at=graph.updated_at,
            )
            db.session.add(row)
        else:
            row.student_id = graph.student_id
            row.version = graph.version
            row.updated_at = graph.updated_at
        return row

    def replace_structure(self, graph: LearningGraph) -> None:
        """Replace nodes/edges for a graph; append snapshots and updates."""
        self.save_graph_root(graph)

        LgGraphNode.query.filter_by(graph_id=graph.graph_id).delete()
        LgGraphEdge.query.filter_by(graph_id=graph.graph_id).delete()

        for node in graph.nodes:
            db.session.add(
                LgGraphNode(
                    node_id=node.node_id,
                    graph_id=graph.graph_id,
                    concept_id=node.concept_id,
                    concept_title=node.concept_title or "",
                    mastery_link_id=node.mastery_link_id or "",
                    projected_mastery=node.mastery_score,
                    projected_confidence=node.confidence,
                    projected_evidence_count=node.evidence_count,
                    projected_trend=node.trend or "unknown",
                    last_interaction=node.last_interaction,
                    prerequisite_status=node.prerequisite_status.value,
                    updated_at=graph.updated_at,
                )
            )

        for edge in graph.edges:
            db.session.add(
                LgGraphEdge(
                    edge_id=edge.edge_id,
                    graph_id=graph.graph_id,
                    from_concept_id=edge.from_concept_id,
                    to_concept_id=edge.to_concept_id,
                    relationship_type=edge.relationship_type.value,
                    strength=edge.strength,
                    confidence=edge.confidence,
                    provenance=edge.provenance or "",
                    supporting_evidence_json=_dumps(list(edge.supporting_evidence)),
                    created_at=graph.updated_at or graph.created_at,
                )
            )

        # Append new history / snapshots only (match by id).
        existing_updates = {
            r.update_id
            for r in LgGraphUpdateHistory.query.filter_by(
                graph_id=graph.graph_id
            ).all()
        }
        for update in graph.update_history:
            if update.update_id in existing_updates:
                continue
            db.session.add(
                LgGraphUpdateHistory(
                    update_id=update.update_id,
                    graph_id=graph.graph_id,
                    twin_id=graph.twin_id,
                    kind=update.kind.value,
                    summary=update.summary,
                    payload_json=_dumps(update.payload_dict()),
                    created_at=update.created_at,
                )
            )

        existing_snaps = {
            r.snapshot_id
            for r in LgGraphSnapshot.query.filter_by(graph_id=graph.graph_id).all()
        }
        for snap in graph.snapshots:
            if snap.snapshot_id in existing_snaps:
                continue
            db.session.add(
                LgGraphSnapshot(
                    snapshot_id=snap.snapshot_id,
                    graph_id=graph.graph_id,
                    twin_id=graph.twin_id,
                    node_count=snap.node_count,
                    edge_count=snap.edge_count,
                    reason=snap.reason or "",
                    node_concept_ids_json=_dumps(list(snap.node_concept_ids)),
                    edge_ids_json=_dumps(list(snap.edge_ids)),
                    created_at=snap.created_at,
                )
            )

        db.session.flush()

    def load_graph(self, graph_id: str) -> LearningGraph | None:
        row = LgLearningGraph.query.filter_by(graph_id=graph_id).first()
        if row is None:
            return None
        return self._hydrate(row)

    def load_graph_for_twin(self, twin_id: str) -> LearningGraph | None:
        row = LgLearningGraph.query.filter_by(twin_id=twin_id).first()
        if row is None:
            return None
        return self._hydrate(row)

    def _hydrate(self, row: LgLearningGraph) -> LearningGraph:
        node_rows = LgGraphNode.query.filter_by(graph_id=row.graph_id).all()
        edge_rows = LgGraphEdge.query.filter_by(graph_id=row.graph_id).all()
        update_rows = (
            LgGraphUpdateHistory.query.filter_by(graph_id=row.graph_id)
            .order_by(LgGraphUpdateHistory.created_at.asc())
            .all()
        )
        snap_rows = (
            LgGraphSnapshot.query.filter_by(graph_id=row.graph_id)
            .order_by(LgGraphSnapshot.created_at.asc())
            .all()
        )

        nodes = tuple(
            GraphNode(
                node_id=n.node_id,
                graph_id=n.graph_id,
                concept_id=n.concept_id,
                concept_title=n.concept_title or "",
                mastery_link_id=n.mastery_link_id or "",
                mastery_score=n.projected_mastery,
                confidence=n.projected_confidence,
                evidence_count=n.projected_evidence_count,
                last_interaction=n.last_interaction,
                trend=n.projected_trend or "unknown",
                prerequisite_status=PrerequisiteStatus(
                    n.prerequisite_status or "unknown"
                ),
            )
            for n in sorted(node_rows, key=lambda r: r.concept_id)
        )
        edges = tuple(
            GraphEdge(
                edge_id=e.edge_id,
                graph_id=e.graph_id,
                from_concept_id=e.from_concept_id,
                to_concept_id=e.to_concept_id,
                relationship_type=RelationshipType(e.relationship_type),
                strength=e.strength,
                confidence=e.confidence,
                provenance=e.provenance or "",
                supporting_evidence=tuple(
                    _loads(e.supporting_evidence_json, [])
                ),
            )
            for e in sorted(
                edge_rows,
                key=lambda r: (
                    r.from_concept_id,
                    r.to_concept_id,
                    r.relationship_type,
                ),
            )
        )
        mastery_links = tuple(
            MasteryLink(
                link_id=n.mastery_link_id,
                graph_id=row.graph_id,
                concept_id=n.concept_id,
                mastery_id=n.mastery_link_id,
                twin_id=row.twin_id,
            )
            for n in nodes
            if n.mastery_link_id
        )
        updates = tuple(
            GraphUpdate(
                update_id=u.update_id,
                graph_id=u.graph_id,
                twin_id=u.twin_id,
                kind=GraphUpdateKind(u.kind),
                summary=u.summary or "",
                created_at=u.created_at,
                payload=tuple(sorted(_loads(u.payload_json, {}).items())),
            )
            for u in update_rows
        )
        snapshots = tuple(
            GraphSnapshot(
                snapshot_id=s.snapshot_id,
                graph_id=s.graph_id,
                twin_id=s.twin_id,
                node_count=s.node_count,
                edge_count=s.edge_count,
                created_at=s.created_at,
                reason=s.reason or "",
                node_concept_ids=tuple(_loads(s.node_concept_ids_json, [])),
                edge_ids=tuple(_loads(s.edge_ids_json, [])),
            )
            for s in snap_rows
        )
        return LearningGraph(
            graph_id=row.graph_id,
            twin_id=row.twin_id,
            student_id=row.student_id,
            nodes=nodes,
            edges=edges,
            mastery_links=mastery_links,
            update_history=updates,
            snapshots=snapshots,
            created_at=row.created_at,
            updated_at=row.updated_at,
            version=row.version,
        )

    @staticmethod
    def graph_as_dict(graph: LearningGraph) -> dict[str, Any]:
        return {
            "graph_id": graph.graph_id,
            "twin_id": graph.twin_id,
            "student_id": graph.student_id,
            "version": graph.version,
            "node_count": graph.node_count,
            "edge_count": graph.edge_count,
            "nodes": [
                {
                    "node_id": n.node_id,
                    "concept_id": n.concept_id,
                    "concept_title": n.concept_title,
                    "mastery_link_id": n.mastery_link_id,
                    "mastery_score": n.mastery_score,
                    "confidence": n.confidence,
                    "evidence_count": n.evidence_count,
                    "trend": n.trend,
                    "prerequisite_status": n.prerequisite_status.value,
                    "last_interaction": (
                        n.last_interaction.isoformat() if n.last_interaction else None
                    ),
                }
                for n in graph.nodes
            ],
            "edges": [
                {
                    "edge_id": e.edge_id,
                    "from_concept_id": e.from_concept_id,
                    "to_concept_id": e.to_concept_id,
                    "relationship_type": e.relationship_type.value,
                    "strength": e.strength,
                    "confidence": e.confidence,
                    "provenance": e.provenance,
                    "supporting_evidence": list(e.supporting_evidence),
                }
                for e in graph.edges
            ],
            "created_at": (
                graph.created_at.isoformat() if graph.created_at else None
            ),
            "updated_at": (
                graph.updated_at.isoformat() if graph.updated_at else None
            ),
        }
