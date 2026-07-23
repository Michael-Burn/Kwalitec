"""Policy tests for Knowledge Dependency Graph."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph import (
    CycleDetectionPolicy,
    GraphValidationPolicy,
    KnowledgeGraphId,
    KnowledgeRelationship,
    LearningPathPolicy,
    RelationshipPolicy,
    RelationshipType,
)
from tests.domain.education.knowledge_graph.conftest import (
    NODE_BAYES_THEOREM,
    NODE_CONDITIONAL_PROBABILITY,
    NODE_CREDIBILITY_THEORY,
    NODE_PROBABILITY,
    make_edge,
    make_node,
    make_path,
)


class TestRelationshipPolicyClassification:
    @pytest.mark.parametrize(
        "relationship_type",
        [
            RelationshipType.PREREQUISITE,
            RelationshipType.REQUIRES,
            RelationshipType.FOUNDATIONAL,
            RelationshipType.DERIVED_FROM,
        ],
    )
    def test_structural_types(self, relationship_type: RelationshipType) -> None:
        assert RelationshipPolicy.is_structural(relationship_type)
        assert not RelationshipPolicy.is_advisory(relationship_type)

    @pytest.mark.parametrize(
        "relationship_type",
        [
            RelationshipType.SUPPORTS,
            RelationshipType.REINFORCES,
            RelationshipType.OPTIONAL,
            RelationshipType.RELATED,
        ],
    )
    def test_advisory_types(self, relationship_type: RelationshipType) -> None:
        assert RelationshipPolicy.is_advisory(relationship_type)
        assert not RelationshipPolicy.is_structural(relationship_type)

    def test_structural_and_advisory_sets_partition_all_types(self) -> None:
        structural = RelationshipPolicy.structural_types()
        advisory = RelationshipPolicy.advisory_types()
        assert structural.isdisjoint(advisory)
        assert structural | advisory == set(RelationshipType)


class TestRelationshipPolicyValidation:
    def test_assert_valid_type_accepts(self) -> None:
        RelationshipPolicy.assert_valid_type(RelationshipType.PREREQUISITE)

    def test_assert_valid_type_rejects(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            RelationshipPolicy.assert_valid_type("prerequisite")  # type: ignore[arg-type]

    def test_assert_no_self_relationship_accepts(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        RelationshipPolicy.assert_no_self_relationship(
            NODE_CONDITIONAL_PROBABILITY, relationship
        )

    def test_assert_no_self_relationship_rejects(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        with pytest.raises(EducationalInvariantViolation):
            RelationshipPolicy.assert_no_self_relationship(
                NODE_PROBABILITY, relationship
            )

    def test_assert_not_duplicate_accepts_when_absent(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        RelationshipPolicy.assert_not_duplicate(
            (), NODE_CONDITIONAL_PROBABILITY, relationship
        )

    def test_assert_not_duplicate_rejects_when_present(self) -> None:
        existing_edge = make_edge()
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        with pytest.raises(EducationalInvariantViolation):
            RelationshipPolicy.assert_not_duplicate(
                (existing_edge,), NODE_CONDITIONAL_PROBABILITY, relationship
            )

    def test_assert_not_duplicate_allows_different_source(self) -> None:
        existing_edge = make_edge(source_node_id=NODE_CONDITIONAL_PROBABILITY)
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        RelationshipPolicy.assert_not_duplicate(
            (existing_edge,), NODE_BAYES_THEOREM, relationship
        )

    def test_assert_can_connect_runs_all_checks(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        RelationshipPolicy.assert_can_connect(
            (), NODE_CONDITIONAL_PROBABILITY, relationship
        )

    def test_assert_can_connect_rejects_self(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        with pytest.raises(EducationalInvariantViolation):
            RelationshipPolicy.assert_can_connect((), NODE_PROBABILITY, relationship)


class TestCycleDetectionPolicy:
    def test_no_cycle_in_chain(self) -> None:
        edges = [
            (NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY),
            (NODE_BAYES_THEOREM, NODE_CONDITIONAL_PROBABILITY),
        ]
        assert CycleDetectionPolicy.find_cycle(edges) is None

    def test_no_cycle_when_no_edges(self) -> None:
        assert CycleDetectionPolicy.find_cycle([]) is None

    def test_direct_cycle_detected(self) -> None:
        edges = [
            (NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY),
            (NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY),
        ]
        cycle = CycleDetectionPolicy.find_cycle(edges)
        assert cycle is not None
        assert cycle[0] == cycle[-1]

    def test_transitive_cycle_detected(self) -> None:
        edges = [
            (NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY),
            (NODE_CONDITIONAL_PROBABILITY, NODE_BAYES_THEOREM),
            (NODE_BAYES_THEOREM, NODE_CREDIBILITY_THEORY),
            (NODE_CREDIBILITY_THEORY, NODE_PROBABILITY),
        ]
        cycle = CycleDetectionPolicy.find_cycle(edges)
        assert cycle is not None

    def test_self_loop_detected(self) -> None:
        edges = [(NODE_PROBABILITY, NODE_PROBABILITY)]
        cycle = CycleDetectionPolicy.find_cycle(edges)
        assert cycle == (NODE_PROBABILITY, NODE_PROBABILITY)

    def test_disconnected_acyclic_components(self) -> None:
        edges = [
            (NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY),
            (NODE_CREDIBILITY_THEORY, NODE_BAYES_THEOREM),
        ]
        assert CycleDetectionPolicy.find_cycle(edges) is None

    def test_assert_acyclic_passes(self) -> None:
        CycleDetectionPolicy.assert_acyclic(
            [(NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY)]
        )

    def test_assert_acyclic_raises(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as excinfo:
            CycleDetectionPolicy.assert_acyclic(
                [
                    (NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY),
                    (NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY),
                ]
            )
        assert excinfo.value.invariant == "CycleDetectionPolicy.cycle_detected"


class TestGraphValidationPolicy:
    def test_assert_identity_accepts(self) -> None:
        graph_id = KnowledgeGraphId("graph-001")
        assert GraphValidationPolicy.assert_identity(graph_id) is graph_id

    def test_assert_identity_rejects(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            GraphValidationPolicy.assert_identity("graph-001")  # type: ignore[arg-type]

    def test_assert_nodes_accepts_unique(self) -> None:
        nodes = GraphValidationPolicy.assert_nodes(
            (make_node(node_id=NODE_PROBABILITY), make_node(node_id=NODE_BAYES_THEOREM))
        )
        assert len(nodes) == 2

    def test_assert_nodes_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            GraphValidationPolicy.assert_nodes(("not-a-node",))  # type: ignore[arg-type]

    def test_assert_nodes_rejects_duplicates(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            GraphValidationPolicy.assert_nodes(
                (
                    make_node(node_id=NODE_PROBABILITY),
                    make_node(node_id=NODE_PROBABILITY),
                )
            )

    def test_assert_edges_accepts_valid(self) -> None:
        nodes_by_id = {
            NODE_CONDITIONAL_PROBABILITY.value: make_node(
                node_id=NODE_CONDITIONAL_PROBABILITY
            ),
            NODE_PROBABILITY.value: make_node(node_id=NODE_PROBABILITY),
        }
        edges = GraphValidationPolicy.assert_edges((make_edge(),), nodes_by_id)
        assert len(edges) == 1

    def test_assert_edges_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            GraphValidationPolicy.assert_edges(("not-an-edge",), {})  # type: ignore[arg-type]

    def test_assert_edges_rejects_unregistered_source(self) -> None:
        nodes_by_id = {NODE_PROBABILITY.value: make_node(node_id=NODE_PROBABILITY)}
        with pytest.raises(EducationalInvariantViolation):
            GraphValidationPolicy.assert_edges((make_edge(),), nodes_by_id)

    def test_assert_edges_rejects_unregistered_target(self) -> None:
        nodes_by_id = {
            NODE_CONDITIONAL_PROBABILITY.value: make_node(
                node_id=NODE_CONDITIONAL_PROBABILITY
            )
        }
        with pytest.raises(EducationalInvariantViolation):
            GraphValidationPolicy.assert_edges((make_edge(),), nodes_by_id)

    def test_assert_edges_rejects_duplicates(self) -> None:
        nodes_by_id = {
            NODE_CONDITIONAL_PROBABILITY.value: make_node(
                node_id=NODE_CONDITIONAL_PROBABILITY
            ),
            NODE_PROBABILITY.value: make_node(node_id=NODE_PROBABILITY),
        }
        with pytest.raises(EducationalInvariantViolation):
            GraphValidationPolicy.assert_edges((make_edge(), make_edge()), nodes_by_id)

    def test_assert_edges_rejects_structural_cycle(self) -> None:
        nodes_by_id = {
            NODE_PROBABILITY.value: make_node(node_id=NODE_PROBABILITY),
            NODE_CONDITIONAL_PROBABILITY.value: make_node(
                node_id=NODE_CONDITIONAL_PROBABILITY
            ),
        }
        forward = make_edge(
            source_node_id=NODE_CONDITIONAL_PROBABILITY, target_node_id=NODE_PROBABILITY
        )
        backward = make_edge(
            source_node_id=NODE_PROBABILITY, target_node_id=NODE_CONDITIONAL_PROBABILITY
        )
        with pytest.raises(EducationalInvariantViolation):
            GraphValidationPolicy.assert_edges((forward, backward), nodes_by_id)


class TestLearningPathPolicy:
    def test_assert_nonempty_path_accepts(self) -> None:
        path = make_path(NODE_PROBABILITY)
        assert LearningPathPolicy.assert_nonempty_path(path) is path

    def test_assert_nonempty_path_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningPathPolicy.assert_nonempty_path("not-a-path")  # type: ignore[arg-type]

    def test_assert_reachable_returns_path(self) -> None:
        path = make_path(NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY)
        result = LearningPathPolicy.assert_reachable(
            path, start=NODE_PROBABILITY, target=NODE_CONDITIONAL_PROBABILITY
        )
        assert result is path

    def test_assert_reachable_raises_when_none(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as excinfo:
            LearningPathPolicy.assert_reachable(
                None, start=NODE_PROBABILITY, target=NODE_CREDIBILITY_THEORY
            )
        assert excinfo.value.invariant == "LearningPathPolicy.unreachable"
