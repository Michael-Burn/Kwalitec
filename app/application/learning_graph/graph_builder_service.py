"""Build / sync Learning Graph structure from Twin + curriculum evidence.

Curriculum relationships come from CurriculumEvidenceBundle (CIP-003 retrieval),
never from direct VectorStore / Knowledge Graph access.
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import UTC, datetime

from app.domain.educational_reasoning.reasoning_context import CurriculumEvidenceBundle
from app.domain.learning_graph.graph_edge import GraphEdge
from app.domain.learning_graph.graph_node import GraphNode, PrerequisiteStatus
from app.domain.learning_graph.graph_snapshot import GraphSnapshot
from app.domain.learning_graph.graph_update import GraphUpdate, GraphUpdateKind
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.learning_graph.mastery_link import MasteryLink
from app.domain.learning_graph.relationship import RelationshipType
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.observation import Observation
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


class LearningGraphBuilderService:
    """Synchronise Learning Graph nodes/edges from Twin state + evidence."""

    def sync_from_twin_and_evidence(
        self,
        graph: LearningGraph,
        *,
        twin: StudentDigitalTwin,
        evidence: CurriculumEvidenceBundle | None = None,
        computed_at: datetime | None = None,
        record_snapshot: bool = True,
    ) -> LearningGraph:
        """Upsert nodes from Twin mastery/observations and edges from evidence."""
        now = computed_at or datetime.now(UTC).replace(tzinfo=None)
        evidence = evidence or CurriculumEvidenceBundle.empty()

        nodes, links = self._build_nodes(graph, twin=twin, now=now)
        edges = self._build_edges(
            graph,
            twin=twin,
            nodes=nodes,
            evidence=evidence,
            now=now,
        )

        interim = LearningGraph(
            graph_id=graph.graph_id,
            twin_id=graph.twin_id,
            student_id=graph.student_id,
            nodes=nodes,
            edges=edges,
            mastery_links=links,
            update_history=graph.update_history,
            snapshots=graph.snapshots,
            created_at=graph.created_at,
            updated_at=now,
            version=graph.version,
        )
        interim = interim.recompute_prerequisite_statuses()

        update = GraphUpdate(
            update_id=f"lgu-{uuid.uuid4().hex[:16]}",
            graph_id=graph.graph_id,
            twin_id=graph.twin_id,
            kind=GraphUpdateKind.SYNC_FROM_TWIN,
            summary=(
                f"Synced graph: nodes={interim.node_count} edges={interim.edge_count}"
            ),
            created_at=now,
            payload=(
                ("node_count", str(interim.node_count)),
                ("edge_count", str(interim.edge_count)),
            ),
        )
        snapshot = None
        if record_snapshot:
            snapshot = GraphSnapshot(
                snapshot_id=f"lgs-{uuid.uuid4().hex[:16]}",
                graph_id=graph.graph_id,
                twin_id=graph.twin_id,
                node_count=interim.node_count,
                edge_count=interim.edge_count,
                created_at=now,
                reason="sync_from_twin_and_evidence",
                node_concept_ids=tuple(sorted(n.concept_id for n in interim.nodes)),
                edge_ids=tuple(sorted(e.edge_id for e in interim.edges)),
            )

        return interim.with_structure(
            nodes=interim.nodes,
            edges=interim.edges,
            mastery_links=interim.mastery_links,
            update=update,
            snapshot=snapshot,
            updated_at=now,
        )

    def _build_nodes(
        self,
        graph: LearningGraph,
        *,
        twin: StudentDigitalTwin,
        now: datetime,
    ) -> tuple[tuple[GraphNode, ...], tuple[MasteryLink, ...]]:
        concept_meta: dict[str, dict] = {}

        for record in twin.mastery.records:
            concept_meta[record.concept_id] = {
                "title": record.concept_title or "",
                "mastery_id": record.mastery_id,
                "mastery_score": record.mastery_score,
                "confidence": record.confidence,
                "evidence_count": record.evidence_count,
                "trend": record.trend.value
                if hasattr(record.trend, "value")
                else str(record.trend),
                "last_interaction": record.last_updated,
            }

        for obs in twin.observations:
            cid = (obs.curriculum_entity_id or "").strip()
            if not cid:
                continue
            meta = concept_meta.setdefault(
                cid,
                {
                    "title": str(obs.metadata.get("concept_title") or ""),
                    "mastery_id": "",
                    "mastery_score": 0.0,
                    "confidence": 0.0,
                    "evidence_count": 0,
                    "trend": "unknown",
                    "last_interaction": obs.recorded_at,
                },
            )
            if obs.recorded_at and (
                meta["last_interaction"] is None
                or obs.recorded_at > meta["last_interaction"]
            ):
                meta["last_interaction"] = obs.recorded_at
            title = str(obs.metadata.get("concept_title") or "")
            if title and not meta["title"]:
                meta["title"] = title

        existing = {n.concept_id: n for n in graph.nodes}
        nodes: list[GraphNode] = []
        links: list[MasteryLink] = []

        for concept_id in sorted(concept_meta.keys()):
            meta = concept_meta[concept_id]
            prior = existing.get(concept_id)
            node_id = prior.node_id if prior else _node_id(graph.graph_id, concept_id)
            mastery_id = meta["mastery_id"] or (
                prior.mastery_link_id if prior else ""
            )
            link_id = mastery_id or ""
            node = GraphNode(
                node_id=node_id,
                graph_id=graph.graph_id,
                concept_id=concept_id,
                concept_title=meta["title"],
                mastery_link_id=link_id,
                mastery_score=float(meta["mastery_score"]),
                confidence=float(meta["confidence"]),
                evidence_count=int(meta["evidence_count"]),
                last_interaction=meta["last_interaction"] or now,
                trend=str(meta["trend"]),
                prerequisite_status=(
                    prior.prerequisite_status
                    if prior
                    else PrerequisiteStatus.UNKNOWN
                ),
            )
            nodes.append(node)
            if link_id:
                links.append(
                    MasteryLink(
                        link_id=link_id,
                        graph_id=graph.graph_id,
                        concept_id=concept_id,
                        mastery_id=link_id,
                        twin_id=twin.twin_id,
                    )
                )

        return tuple(nodes), tuple(links)

    def _build_edges(
        self,
        graph: LearningGraph,
        *,
        twin: StudentDigitalTwin,
        nodes: tuple[GraphNode, ...],
        evidence: CurriculumEvidenceBundle,
        now: datetime,
    ) -> tuple[GraphEdge, ...]:
        """Derive edges from retrieval evidence; keep prior non-conflicting edges."""
        known_concepts = {n.concept_id for n in nodes}
        edge_map: dict[tuple[str, str, str], GraphEdge] = {}

        # Preserve existing edges whose endpoints still exist (or will be added).
        for edge in graph.edges:
            key = (
                edge.from_concept_id,
                edge.to_concept_id,
                edge.relationship_type.value,
            )
            edge_map[key] = edge

        for concept_id, result in sorted(evidence.by_concept.items()):
            if result is None or not result.results:
                continue
            top = result.results[0]
            evidence_ids = [
                e.evidence_id for e in top.evidence if e.evidence_id
            ]
            evidence_ids.append(f"ranked:{top.entity_id}")
            if result.retrieval_log_id:
                evidence_ids.append(f"retrieval:{result.retrieval_log_id}")
            evidence_tuple = tuple(dict.fromkeys(evidence_ids))

            # Ensure prerequisite concepts exist as nodes (structure-only stubs).
            prereqs = tuple(top.prerequisites) or tuple(result.prerequisite_ids)
            for prereq_id in prereqs:
                if not prereq_id:
                    continue
                known_concepts.add(prereq_id)
                key = (
                    concept_id,
                    prereq_id,
                    RelationshipType.PREREQUISITE.value,
                )
                edge_map[key] = GraphEdge(
                    edge_id=_edge_id(
                        graph.graph_id,
                        concept_id,
                        prereq_id,
                        RelationshipType.PREREQUISITE,
                    ),
                    graph_id=graph.graph_id,
                    from_concept_id=concept_id,
                    to_concept_id=prereq_id,
                    relationship_type=RelationshipType.PREREQUISITE,
                    strength=round(min(1.0, top.confidence), 4),
                    confidence=round(top.confidence, 4),
                    provenance="curriculum_retrieval",
                    supporting_evidence=evidence_tuple,
                )

            for related_id in top.related_concepts:
                if not related_id or related_id == concept_id:
                    continue
                known_concepts.add(related_id)
                key = (
                    concept_id,
                    related_id,
                    RelationshipType.RELATED_CONCEPT.value,
                )
                edge_map[key] = GraphEdge(
                    edge_id=_edge_id(
                        graph.graph_id,
                        concept_id,
                        related_id,
                        RelationshipType.RELATED_CONCEPT,
                    ),
                    graph_id=graph.graph_id,
                    from_concept_id=concept_id,
                    to_concept_id=related_id,
                    relationship_type=RelationshipType.RELATED_CONCEPT,
                    strength=round(min(1.0, top.rank_score), 4),
                    confidence=round(top.confidence * 0.8, 4),
                    provenance="curriculum_retrieval",
                    supporting_evidence=evidence_tuple,
                )

        # Materialise stub nodes for referenced concepts missing from Twin mastery.
        # Caller re-merges via nodes list — stubs added here as edges only;
        # LearningGraphService ensures stub nodes before persist.
        _ = known_concepts  # used by ensure_stub_nodes
        _ = twin
        _ = now
        return tuple(
            edge_map[k]
            for k in sorted(edge_map.keys(), key=lambda t: (t[0], t[1], t[2]))
        )

    def ensure_stub_nodes(
        self,
        graph: LearningGraph,
        *,
        computed_at: datetime | None = None,
    ) -> LearningGraph:
        """Add structure-only stub nodes for edge endpoints lacking nodes."""
        now = computed_at or datetime.now(UTC).replace(tzinfo=None)
        by_concept = dict(graph.nodes_by_concept())
        needed: set[str] = set()
        for edge in graph.edges:
            needed.add(edge.from_concept_id)
            needed.add(edge.to_concept_id)
        added = False
        for concept_id in sorted(needed):
            if concept_id in by_concept:
                continue
            by_concept[concept_id] = GraphNode(
                node_id=_node_id(graph.graph_id, concept_id),
                graph_id=graph.graph_id,
                concept_id=concept_id,
                concept_title="",
                mastery_link_id="",
                mastery_score=0.0,
                confidence=0.0,
                evidence_count=0,
                last_interaction=now,
                trend="unknown",
                prerequisite_status=PrerequisiteStatus.UNKNOWN,
            )
            added = True
        if not added:
            return graph
        nodes = tuple(by_concept[c] for c in sorted(by_concept.keys()))
        return graph.with_structure(nodes=nodes, updated_at=now)


def project_mastery_onto_graph(
    graph: LearningGraph,
    mastery: MasteryMap,
    *,
    observations: tuple[Observation, ...] = (),
    computed_at: datetime | None = None,
) -> LearningGraph:
    """Refresh node mastery projections from Twin mastery without altering edges."""
    now = computed_at or datetime.now(UTC).replace(tzinfo=None)
    last_by_concept: dict[str, datetime] = {}
    for obs in observations:
        cid = (obs.curriculum_entity_id or "").strip()
        if not cid:
            continue
        prior = last_by_concept.get(cid)
        if prior is None or obs.recorded_at > prior:
            last_by_concept[cid] = obs.recorded_at

    updated: list[GraphNode] = []
    for node in graph.nodes:
        record = mastery.get(node.concept_id)
        if record is None:
            updated.append(node)
            continue
        updated.append(
            GraphNode(
                node_id=node.node_id,
                graph_id=node.graph_id,
                concept_id=node.concept_id,
                concept_title=record.concept_title or node.concept_title,
                mastery_link_id=record.mastery_id,
                mastery_score=record.mastery_score,
                confidence=record.confidence,
                evidence_count=record.evidence_count,
                last_interaction=last_by_concept.get(
                    node.concept_id, record.last_updated or now
                ),
                trend=(
                    record.trend.value
                    if hasattr(record.trend, "value")
                    else str(record.trend)
                ),
                prerequisite_status=node.prerequisite_status,
            )
        )
    interim = graph.with_structure(nodes=tuple(updated), updated_at=now)
    return interim.recompute_prerequisite_statuses()


def _node_id(graph_id: str, concept_id: str) -> str:
    digest = hashlib.sha256(f"node:{graph_id}:{concept_id}".encode()).hexdigest()[:16]
    return f"lgn-{digest}"


def _edge_id(
    graph_id: str,
    from_id: str,
    to_id: str,
    rel: RelationshipType,
) -> str:
    digest = hashlib.sha256(
        f"edge:{graph_id}:{from_id}:{to_id}:{rel.value}".encode()
    ).hexdigest()[:16]
    return f"lge-{digest}"
