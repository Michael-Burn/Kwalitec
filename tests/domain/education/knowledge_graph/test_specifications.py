"""Specification tests for Knowledge Dependency Graph."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph import (
    AcyclicPrerequisiteSpecification,
    KnowledgeGraphConsistencySpecification,
    KnowledgeRelationshipId,
    RelationshipType,
    RelationshipValiditySpecification,
)
from domain.education.knowledge_graph.value_objects.knowledge_edge import (
    KnowledgeEdge,
)
from domain.education.knowledge_graph.value_objects.knowledge_relationship import (
    KnowledgeRelationship,
)
from tests.domain.education.knowledge_graph.conftest import (
    NODE_BAYES_THEOREM,
    NODE_CONDITIONAL_PROBABILITY,
    NODE_CREDIBILITY_THEORY,
    NODE_PROBABILITY,
    make_graph,
    make_node,
    make_probability_chain_graph,
)


class TestKnowledgeGraphConsistencySpecification:
    def test_satisfied_by_empty_graph(self) -> None:
        graph = make_graph()
        assert KnowledgeGraphConsistencySpecification().is_satisfied_by(graph)

    def test_satisfied_by_probability_chain(self) -> None:
        graph = make_probability_chain_graph()
        assert KnowledgeGraphConsistencySpecification().is_satisfied_by(graph)

    def test_assert_satisfied_by_passes_silently(self) -> None:
        graph = make_probability_chain_graph()
        KnowledgeGraphConsistencySpecification().assert_satisfied_by(graph)

    def test_unsatisfied_when_edge_endpoint_missing(self) -> None:
        graph = make_probability_chain_graph()
        # Corrupt internal state directly to simulate drift.
        graph._nodes.pop(NODE_PROBABILITY.value)  # type: ignore[attr-defined]
        assert not KnowledgeGraphConsistencySpecification().is_satisfied_by(graph)

    def test_assert_satisfied_by_raises_when_unsatisfied(self) -> None:
        graph = make_probability_chain_graph()
        graph._nodes.pop(NODE_PROBABILITY.value)  # type: ignore[attr-defined]
        with pytest.raises(EducationalInvariantViolation) as excinfo:
            KnowledgeGraphConsistencySpecification().assert_satisfied_by(graph)
        assert (
            excinfo.value.invariant
            == "KnowledgeGraphConsistencySpecification.unsatisfied"
        )

    def test_unsatisfied_when_duplicate_node_ids(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        # Alias a second dict key to the same node object, simulating storage
        # drift where two keys resolve to nodes sharing one node_id.
        graph._nodes[NODE_CONDITIONAL_PROBABILITY.value] = graph._nodes[  # type: ignore[attr-defined]
            NODE_PROBABILITY.value
        ]
        node_ids = [node.node_id.value for node in graph.nodes]
        assert len(node_ids) != len(set(node_ids))
        assert not KnowledgeGraphConsistencySpecification().is_satisfied_by(graph)

    def test_unsatisfied_when_duplicate_edges_present(self) -> None:
        graph = make_probability_chain_graph()
        graph._edges.append(graph._edges[0])  # type: ignore[attr-defined]
        assert not KnowledgeGraphConsistencySpecification().is_satisfied_by(graph)

    def test_unsatisfied_when_edge_source_missing(self) -> None:
        graph = make_probability_chain_graph()
        # credibility-theory is only ever an edge *source*, never a target.
        graph._nodes.pop(NODE_CREDIBILITY_THEORY.value)  # type: ignore[attr-defined]
        assert not KnowledgeGraphConsistencySpecification().is_satisfied_by(graph)

    def test_unsatisfied_when_self_loop_edge_injected(self) -> None:
        graph = make_probability_chain_graph()
        self_edge = KnowledgeEdge(
            relationship_id=KnowledgeRelationshipId.for_edge(
                NODE_BAYES_THEOREM, NODE_BAYES_THEOREM, RelationshipType.RELATED
            ),
            source_node_id=NODE_BAYES_THEOREM,
            relationship=KnowledgeRelationship.of(
                NODE_BAYES_THEOREM, RelationshipType.RELATED
            ),
        )
        graph._edges.append(self_edge)  # type: ignore[attr-defined]
        assert not KnowledgeGraphConsistencySpecification().is_satisfied_by(graph)

    def test_unsatisfied_when_structural_cycle_present(self) -> None:
        graph = make_probability_chain_graph()
        edge = graph.edges[0]
        # Inject a reverse structural edge directly to simulate corrupted state.
        reverse = KnowledgeEdge(
            relationship_id=KnowledgeRelationshipId.for_edge(
                NODE_PROBABILITY,
                NODE_CREDIBILITY_THEORY,
                RelationshipType.PREREQUISITE,
            ),
            source_node_id=NODE_PROBABILITY,
            relationship=KnowledgeRelationship.of(
                NODE_CREDIBILITY_THEORY, RelationshipType.PREREQUISITE
            ),
        )
        graph._edges.append(reverse)  # type: ignore[attr-defined]
        assert not KnowledgeGraphConsistencySpecification().is_satisfied_by(graph)
        assert edge in graph.edges


class TestAcyclicPrerequisiteSpecification:
    def test_satisfied_by_acyclic_chain(self) -> None:
        graph = make_probability_chain_graph()
        assert AcyclicPrerequisiteSpecification().is_satisfied_by(graph)

    def test_ignores_advisory_relationships(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(make_node(node_id=NODE_CONDITIONAL_PROBABILITY))
        graph.connect(
            NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY, RelationshipType.SUPPORTS
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.SUPPORTS
        )
        assert AcyclicPrerequisiteSpecification().is_satisfied_by(graph)

    def test_assert_satisfied_by_passes(self) -> None:
        graph = make_probability_chain_graph()
        AcyclicPrerequisiteSpecification().assert_satisfied_by(graph)

    def test_unsatisfied_when_structural_cycle_injected(self) -> None:
        graph = make_probability_chain_graph()
        reverse = KnowledgeEdge(
            relationship_id=KnowledgeRelationshipId.for_edge(
                NODE_PROBABILITY, NODE_CREDIBILITY_THEORY, RelationshipType.REQUIRES
            ),
            source_node_id=NODE_PROBABILITY,
            relationship=KnowledgeRelationship.of(
                NODE_CREDIBILITY_THEORY, RelationshipType.REQUIRES
            ),
        )
        graph._edges.append(reverse)  # type: ignore[attr-defined]
        assert not AcyclicPrerequisiteSpecification().is_satisfied_by(graph)
        with pytest.raises(EducationalInvariantViolation) as excinfo:
            AcyclicPrerequisiteSpecification().assert_satisfied_by(graph)
        assert (
            excinfo.value.invariant == "AcyclicPrerequisiteSpecification.cycle_detected"
        )


class TestRelationshipValiditySpecification:
    def test_satisfied_by_probability_chain(self) -> None:
        graph = make_probability_chain_graph()
        assert RelationshipValiditySpecification().is_satisfied_by(graph)

    def test_assert_satisfied_by_passes(self) -> None:
        graph = make_probability_chain_graph()
        RelationshipValiditySpecification().assert_satisfied_by(graph)

    def test_unsatisfied_when_relationship_type_corrupted(self) -> None:
        graph = make_probability_chain_graph()
        edge = graph.edges[0]
        object.__setattr__(edge.relationship, "relationship_type", "not-a-type")
        assert not RelationshipValiditySpecification().is_satisfied_by(graph)

    def test_unsatisfied_when_strength_corrupted(self) -> None:
        graph = make_probability_chain_graph()
        edge = graph.edges[0]
        object.__setattr__(edge.relationship, "strength", "not-a-strength")
        assert not RelationshipValiditySpecification().is_satisfied_by(graph)

    def test_unsatisfied_when_metadata_corrupted(self) -> None:
        graph = make_probability_chain_graph()
        edge = graph.edges[0]
        object.__setattr__(edge.relationship, "metadata", "not-metadata")
        assert not RelationshipValiditySpecification().is_satisfied_by(graph)

    def test_unsatisfied_when_self_relationship_injected(self) -> None:
        graph = make_probability_chain_graph()
        # Bypass relationship self-check by constructing the KnowledgeRelationship
        # first (valid), then hand-assembling an edge whose source equals target.
        relationship = KnowledgeRelationship.of(
            NODE_BAYES_THEOREM, RelationshipType.RELATED
        )
        self_edge = KnowledgeEdge(
            relationship_id=KnowledgeRelationshipId.for_edge(
                NODE_BAYES_THEOREM, NODE_BAYES_THEOREM, RelationshipType.RELATED
            ),
            source_node_id=NODE_BAYES_THEOREM,
            relationship=relationship,
        )
        # KnowledgeEdge itself does not re-check self-relationships (that is
        # RelationshipPolicy's job at connect() time) — simulate a drifted
        # edge added directly to internal storage, bypassing connect().
        graph._edges.append(self_edge)  # type: ignore[attr-defined]
        assert not RelationshipValiditySpecification().is_satisfied_by(graph)
        with pytest.raises(EducationalInvariantViolation):
            RelationshipValiditySpecification().assert_satisfied_by(graph)
