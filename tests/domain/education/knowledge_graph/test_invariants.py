"""Cross-cutting invariant tests for Knowledge Dependency Graph."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph import RelationshipType
from tests.domain.education.knowledge_graph.conftest import (
    NODE_BAYES_THEOREM,
    NODE_CONDITIONAL_PROBABILITY,
    NODE_CREDIBILITY_THEORY,
    NODE_PROBABILITY,
    make_graph,
    make_node,
    make_probability_chain_graph,
)


def test_node_identifiers_are_unique() -> None:
    graph = make_graph()
    graph.add_node(make_node(node_id=NODE_PROBABILITY))
    with pytest.raises(EducationalInvariantViolation):
        graph.add_node(make_node(node_id=NODE_PROBABILITY, label="Duplicate"))


def test_relationships_are_unique_per_source_target_type() -> None:
    graph = make_graph()
    graph.add_node(make_node(node_id=NODE_PROBABILITY))
    graph.add_node(make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional"))
    graph.connect(
        NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
    )
    with pytest.raises(EducationalInvariantViolation):
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )


def test_no_duplicate_edges_across_disconnect_and_reconnect() -> None:
    graph = make_probability_chain_graph()
    graph.disconnect(
        NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
    )
    graph.connect(
        NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
    )
    with pytest.raises(EducationalInvariantViolation):
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )


def test_no_self_dependencies_for_any_relationship_type() -> None:
    graph = make_graph()
    graph.add_node(make_node(node_id=NODE_PROBABILITY))
    for relationship_type in RelationshipType:
        with pytest.raises(EducationalInvariantViolation):
            graph.connect(NODE_PROBABILITY, NODE_PROBABILITY, relationship_type)


def test_cycles_prohibited_for_every_structural_relationship_type() -> None:
    structural_types = (
        RelationshipType.PREREQUISITE,
        RelationshipType.REQUIRES,
        RelationshipType.FOUNDATIONAL,
        RelationshipType.DERIVED_FROM,
    )
    for relationship_type in structural_types:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.connect(NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, relationship_type)
        with pytest.raises(EducationalInvariantViolation):
            graph.connect(
                NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY, relationship_type
            )


def test_cycles_permitted_for_every_advisory_relationship_type() -> None:
    advisory_types = (
        RelationshipType.SUPPORTS,
        RelationshipType.REINFORCES,
        RelationshipType.OPTIONAL,
        RelationshipType.RELATED,
    )
    for relationship_type in advisory_types:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.connect(NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, relationship_type)
        graph.connect(NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY, relationship_type)
        assert graph.edge_count() == 2


def test_graph_remains_consistent_after_many_mutations() -> None:
    from domain.education.knowledge_graph import KnowledgeGraphConsistencySpecification

    graph = make_probability_chain_graph()
    spec = KnowledgeGraphConsistencySpecification()
    assert spec.is_satisfied_by(graph)

    graph.disconnect(
        NODE_BAYES_THEOREM, NODE_CONDITIONAL_PROBABILITY, RelationshipType.PREREQUISITE
    )
    assert spec.is_satisfied_by(graph)

    graph.connect(NODE_BAYES_THEOREM, NODE_PROBABILITY, RelationshipType.SUPPORTS)
    assert spec.is_satisfied_by(graph)

    graph.remove_node(NODE_CONDITIONAL_PROBABILITY)
    assert spec.is_satisfied_by(graph)


def test_nodes_property_returns_defensive_copy() -> None:
    from domain.education.knowledge_graph import KnowledgeNodeId

    graph = make_probability_chain_graph()
    snapshot_tuple = graph.nodes
    graph.add_node(make_node(node_id=KnowledgeNodeId("new-node"), label="Newly added"))
    assert len(snapshot_tuple) == 4
    assert len(graph.nodes) == 5


def test_edges_property_returns_defensive_copy() -> None:
    graph = make_probability_chain_graph()
    edges_before = graph.edges
    graph.disconnect(
        NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
    )
    assert len(edges_before) == 3
    assert len(graph.edges) == 2


def test_transitive_reasoning_excludes_the_origin_node() -> None:
    graph = make_probability_chain_graph()
    prerequisites = graph.find_prerequisites(NODE_CREDIBILITY_THEORY, transitive=True)
    assert NODE_CREDIBILITY_THEORY not in prerequisites
    dependents = graph.find_dependents(NODE_PROBABILITY, transitive=True)
    assert NODE_PROBABILITY not in dependents
