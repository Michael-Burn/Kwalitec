"""Shared factories for Knowledge Dependency Graph domain tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.knowledge_graph import (
    ConceptCluster,
    DependencyStrength,
    KnowledgeEdge,
    KnowledgeGraph,
    KnowledgeGraphId,
    KnowledgeNode,
    KnowledgeNodeId,
    KnowledgeNodeKind,
    KnowledgePath,
    KnowledgeRelationship,
    KnowledgeRelationshipId,
    RelationshipMetadata,
    RelationshipType,
)

GRAPH_001 = KnowledgeGraphId("graph-001")
NODE_PROBABILITY = KnowledgeNodeId("probability")
NODE_CONDITIONAL_PROBABILITY = KnowledgeNodeId("conditional-probability")
NODE_BAYES_THEOREM = KnowledgeNodeId("bayes-theorem")
NODE_CREDIBILITY_THEORY = KnowledgeNodeId("credibility-theory")


@pytest.fixture
def graph_id() -> KnowledgeGraphId:
    return KnowledgeGraphId("graph-001")


@pytest.fixture
def as_of() -> datetime:
    return datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)


def make_node_id(value: str) -> KnowledgeNodeId:
    return KnowledgeNodeId(value)


def make_node(
    *,
    node_id: KnowledgeNodeId | str = NODE_PROBABILITY,
    label: str = "Probability",
    kind: KnowledgeNodeKind = KnowledgeNodeKind.CONCEPT,
    description: str | None = None,
) -> KnowledgeNode:
    if isinstance(node_id, str):
        node_id = KnowledgeNodeId(node_id)
    return KnowledgeNode(
        node_id=node_id, label=label, kind=kind, description=description
    )


def make_strength(
    band: str = "helpful", *, weight: float | None = None
) -> DependencyStrength:
    factories = {
        "optional": DependencyStrength.optional,
        "helpful": DependencyStrength.helpful,
        "important": DependencyStrength.important,
        "critical": DependencyStrength.critical,
    }
    return factories[band](weight=weight)


def make_metadata(
    *, description: str | None = None, tags: tuple[str, ...] = ()
) -> RelationshipMetadata:
    return RelationshipMetadata(description=description, tags=tags)


def make_relationship(
    *,
    target_node_id: KnowledgeNodeId | str = NODE_PROBABILITY,
    relationship_type: RelationshipType = RelationshipType.PREREQUISITE,
    strength: DependencyStrength | None = None,
    metadata: RelationshipMetadata | None = None,
) -> KnowledgeRelationship:
    if isinstance(target_node_id, str):
        target_node_id = KnowledgeNodeId(target_node_id)
    return KnowledgeRelationship.of(
        target_node_id, relationship_type, strength=strength, metadata=metadata
    )


def make_edge(
    *,
    source_node_id: KnowledgeNodeId | str = NODE_CONDITIONAL_PROBABILITY,
    target_node_id: KnowledgeNodeId | str = NODE_PROBABILITY,
    relationship_type: RelationshipType = RelationshipType.PREREQUISITE,
    strength: DependencyStrength | None = None,
    metadata: RelationshipMetadata | None = None,
) -> KnowledgeEdge:
    if isinstance(source_node_id, str):
        source_node_id = KnowledgeNodeId(source_node_id)
    relationship = make_relationship(
        target_node_id=target_node_id,
        relationship_type=relationship_type,
        strength=strength,
        metadata=metadata,
    )
    return KnowledgeEdge(
        relationship_id=KnowledgeRelationshipId.for_edge(
            source_node_id, relationship.target_node_id, relationship_type
        ),
        source_node_id=source_node_id,
        relationship=relationship,
    )


def make_path(*node_ids: KnowledgeNodeId | str) -> KnowledgePath:
    coerced = tuple(KnowledgeNodeId(n) if isinstance(n, str) else n for n in node_ids)
    return KnowledgePath(coerced)


def make_cluster(
    *, cluster_id: str = "cluster-1", node_ids: tuple[KnowledgeNodeId, ...] = ()
) -> ConceptCluster:
    return ConceptCluster(cluster_id=cluster_id, node_ids=node_ids)


def make_graph(*, graph_id: KnowledgeGraphId | str = GRAPH_001) -> KnowledgeGraph:
    if isinstance(graph_id, str):
        graph_id = KnowledgeGraphId(graph_id)
    return KnowledgeGraph.create(graph_id)


def make_probability_chain_graph() -> KnowledgeGraph:
    """Probability -> Conditional Probability -> Bayes' Theorem -> Credibility."""
    graph = make_graph()
    graph.add_node(make_node(node_id=NODE_PROBABILITY, label="Probability"))
    graph.add_node(
        make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional Probability")
    )
    graph.add_node(make_node(node_id=NODE_BAYES_THEOREM, label="Bayes' Theorem"))
    graph.add_node(
        make_node(node_id=NODE_CREDIBILITY_THEORY, label="Credibility Theory")
    )
    graph.connect(
        NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
    )
    graph.connect(
        NODE_BAYES_THEOREM,
        NODE_CONDITIONAL_PROBABILITY,
        RelationshipType.PREREQUISITE,
    )
    graph.connect(
        NODE_CREDIBILITY_THEORY, NODE_BAYES_THEOREM, RelationshipType.PREREQUISITE
    )
    return graph
