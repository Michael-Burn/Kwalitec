"""EI-002B — Tutor context constrained to certified curriculum nodes."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.application.curriculum_intelligence.learner_knowledge_graph_service import (
    LearnerKnowledgeGraphBuilder,
    assert_certified_package,
)
from app.domain.curriculum_intelligence.certified_learning import (
    CertifiedTutorContext,
    LearnerKnowledgeGraph,
)


class CertifiedTutorContextService:
    """Assemble Tutor context that references certified nodes only.

    Foreign (non-certified) concept ids are rejected and reported; excerpts
    and related ids are filtered to the certified learner graph.
    """

    def __init__(
        self, graph_builder: LearnerKnowledgeGraphBuilder | None = None
    ) -> None:
        self._graph = graph_builder or LearnerKnowledgeGraphBuilder()

    def build(
        self,
        package: dict[str, Any],
        *,
        primary_node_id: str,
        candidate_node_ids: tuple[str, ...] | list[str] = (),
        excerpts: tuple[tuple[str, str], ...] | list[tuple[str, str]] = (),
        context_id: str | None = None,
    ) -> CertifiedTutorContext:
        provenance = assert_certified_package(package)
        graph = self._graph.build(package)
        allowed = {n.node_id for n in graph.nodes}
        primary = (primary_node_id or "").strip()
        if primary and primary not in allowed:
            raise ValueError(
                f"Tutor primary node {primary!r} is not a certified curriculum node"
            )
        if not primary:
            # Default to first LO or topic.
            objs = graph.objectives()
            topics = graph.topics()
            primary = (
                objs[0].node_id
                if objs
                else (topics[0].node_id if topics else "")
            )
        if not primary:
            raise ValueError("certified curriculum has no nodes for Tutor context")

        rejected: list[str] = []
        kept: list[str] = [primary]
        for cid in candidate_node_ids:
            nid = str(cid).strip()
            if not nid or nid == primary:
                continue
            if nid in allowed:
                kept.append(nid)
            else:
                rejected.append(nid)

        filtered_excerpts: list[tuple[str, str]] = []
        for node_id, text in excerpts:
            nid = str(node_id).strip()
            body = str(text or "").strip()
            if not nid or not body:
                continue
            if nid in allowed:
                filtered_excerpts.append((nid, body))
            else:
                rejected.append(nid)

        # Auto-fill excerpts from node titles when none supplied.
        if not filtered_excerpts:
            node = graph.node(primary)
            if node is not None and node.title:
                filtered_excerpts.append((primary, node.title))

        prereqs = _certified_prerequisites(graph, primary)
        related = _certified_related(graph, primary, limit=8)

        return CertifiedTutorContext(
            context_id=(context_id or "").strip() or f"ctc_{uuid4().hex[:12]}",
            curriculum_identity=graph.curriculum_identity,
            primary_node_id=primary,
            allowed_node_ids=tuple(dict.fromkeys(kept + list(prereqs) + list(related))),
            excerpts=tuple(filtered_excerpts),
            prerequisite_ids=prereqs,
            related_node_ids=related,
            provenance=provenance,
            rejected_foreign_ids=tuple(dict.fromkeys(rejected)),
        )


def _certified_prerequisites(
    graph: LearnerKnowledgeGraph, node_id: str
) -> tuple[str, ...]:
    node = graph.node(node_id)
    if node is None:
        return ()
    # Topic prerequisites + parent walk.
    ids: list[str] = list(graph.prerequisites(node_id))
    if node.parent_node_id:
        ids.append(node.parent_node_id)
        ids.extend(graph.prerequisites(node.parent_node_id))
    return tuple(dict.fromkeys(x for x in ids if x and x != node_id))


def _certified_related(
    graph: LearnerKnowledgeGraph, node_id: str, *, limit: int
) -> tuple[str, ...]:
    node = graph.node(node_id)
    if node is None:
        return ()
    related: list[str] = []
    # Sibling objectives under same topic.
    parent = node.parent_node_id
    if parent:
        for child in graph.children(parent):
            if child != node_id:
                related.append(child)
    # Parent topic's other children when primary is a topic.
    for child in graph.children(node_id):
        related.append(child)
    return tuple(dict.fromkeys(related))[:limit]
