"""Aggregate behaviour tests for KnowledgeGraph."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph import (
    DependencyStrength,
    KnowledgeEdge,
    KnowledgeGraph,
    KnowledgeGraphId,
    KnowledgeNode,
    KnowledgeNodeId,
    KnowledgeNodeKind,
    KnowledgeRelationship,
    KnowledgeRelationshipId,
    RelationshipMetadata,
    RelationshipType,
)
from tests.domain.education.knowledge_graph.conftest import (
    GRAPH_001,
    NODE_BAYES_THEOREM,
    NODE_CONDITIONAL_PROBABILITY,
    NODE_CREDIBILITY_THEORY,
    NODE_PROBABILITY,
    make_graph,
    make_node,
    make_probability_chain_graph,
)


class TestConstruction:
    def test_create_factory_is_empty(self) -> None:
        graph = KnowledgeGraph.create(GRAPH_001)
        assert graph.graph_id == GRAPH_001
        assert graph.node_count() == 0
        assert graph.edge_count() == 0

    def test_rejects_wrong_identity_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGraph("graph-001")  # type: ignore[arg-type]

    def test_construct_with_nodes_and_edges(self) -> None:
        node_a = make_node(node_id=NODE_PROBABILITY)
        node_b = make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        edge = KnowledgeGraph(GRAPH_001, nodes=(node_a, node_b)).connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        graph = KnowledgeGraph(GRAPH_001, nodes=(node_a, node_b), edges=(edge,))
        assert graph.node_count() == 2
        assert graph.edge_count() == 1

    def test_construct_rejects_duplicate_nodes(self) -> None:
        node = make_node(node_id=NODE_PROBABILITY)
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGraph(GRAPH_001, nodes=(node, node))

    def test_construct_rejects_edge_with_unregistered_endpoint(self) -> None:
        node = make_node(node_id=NODE_PROBABILITY)
        relationship_edge = make_probability_chain_graph().edges[0]
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGraph(GRAPH_001, nodes=(node,), edges=(relationship_edge,))

    def test_construct_with_advisory_edge_skips_cycle_participation(self) -> None:
        node_a = make_node(node_id=NODE_PROBABILITY)
        node_b = make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        scratch = KnowledgeGraph(GRAPH_001, nodes=(node_a, node_b))
        advisory_edge = scratch.connect(
            NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.SUPPORTS
        )
        graph = KnowledgeGraph(
            GRAPH_001, nodes=(node_a, node_b), edges=(advisory_edge,)
        )
        assert graph.edge_count() == 1

    def test_construct_rejects_structural_cycle(self) -> None:
        node_a = make_node(node_id=NODE_PROBABILITY)
        node_b = make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        scratch = KnowledgeGraph(GRAPH_001, nodes=(node_a, node_b))
        forward = scratch.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        backward = KnowledgeEdge(
            relationship_id=KnowledgeRelationshipId.for_edge(
                NODE_PROBABILITY,
                NODE_CONDITIONAL_PROBABILITY,
                RelationshipType.REQUIRES,
            ),
            source_node_id=NODE_PROBABILITY,
            relationship=KnowledgeRelationship.of(
                NODE_CONDITIONAL_PROBABILITY, RelationshipType.REQUIRES
            ),
        )
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGraph(GRAPH_001, nodes=(node_a, node_b), edges=(forward, backward))


class TestNodeQueries:
    def test_has_node(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        assert graph.has_node(NODE_PROBABILITY)
        assert not graph.has_node(NODE_BAYES_THEOREM)

    def test_node_for_returns_node(self) -> None:
        graph = make_graph()
        node = make_node(node_id=NODE_PROBABILITY)
        graph.add_node(node)
        assert graph.node_for(NODE_PROBABILITY) == node

    def test_node_for_returns_none_when_absent(self) -> None:
        graph = make_graph()
        assert graph.node_for(NODE_PROBABILITY) is None

    def test_nodes_returns_tuple(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        assert isinstance(graph.nodes, tuple)
        assert len(graph.nodes) == 1


class TestAddNode:
    def test_add_node_registers(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        assert graph.node_count() == 1

    def test_add_node_rejects_wrong_type(self) -> None:
        graph = make_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.add_node("not-a-node")  # type: ignore[arg-type]

    def test_add_node_rejects_duplicate(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        with pytest.raises(EducationalInvariantViolation):
            graph.add_node(make_node(node_id=NODE_PROBABILITY, label="Other"))


class TestRemoveNode:
    def test_remove_node_removes_registration(self) -> None:
        graph = make_probability_chain_graph()
        graph.remove_node(NODE_PROBABILITY)
        assert not graph.has_node(NODE_PROBABILITY)

    def test_remove_node_cascades_edges(self) -> None:
        graph = make_probability_chain_graph()
        edges_before = graph.edge_count()
        assert edges_before == 3
        graph.remove_node(NODE_PROBABILITY)
        for edge in graph.edges:
            assert edge.source_node_id != NODE_PROBABILITY
            assert edge.target_node_id != NODE_PROBABILITY
        assert graph.edge_count() == 2

    def test_remove_node_rejects_unregistered(self) -> None:
        graph = make_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.remove_node(NODE_PROBABILITY)

    def test_remove_middle_node_breaks_chain(self) -> None:
        graph = make_probability_chain_graph()
        graph.remove_node(NODE_CONDITIONAL_PROBABILITY)
        assert graph.find_prerequisites(NODE_BAYES_THEOREM) == ()


class TestConnect:
    def test_connect_creates_edge(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        edge = graph.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        assert graph.has_edge(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        assert edge.source_node_id == NODE_CONDITIONAL_PROBABILITY
        assert edge.target_node_id == NODE_PROBABILITY

    def test_connect_with_custom_strength_and_metadata(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        edge = graph.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
            strength=DependencyStrength.critical(),
            metadata=RelationshipMetadata(description="required foundation"),
        )
        assert edge.strength == DependencyStrength.critical()
        assert edge.metadata.description == "required foundation"

    def test_connect_rejects_unregistered_source(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        with pytest.raises(EducationalInvariantViolation):
            graph.connect(
                NODE_CONDITIONAL_PROBABILITY,
                NODE_PROBABILITY,
                RelationshipType.PREREQUISITE,
            )

    def test_connect_rejects_unregistered_target(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_CONDITIONAL_PROBABILITY))
        with pytest.raises(EducationalInvariantViolation):
            graph.connect(
                NODE_CONDITIONAL_PROBABILITY,
                NODE_PROBABILITY,
                RelationshipType.PREREQUISITE,
            )

    def test_connect_rejects_self_relationship(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        with pytest.raises(EducationalInvariantViolation):
            graph.connect(
                NODE_PROBABILITY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
            )

    def test_connect_rejects_duplicate_edge(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        with pytest.raises(EducationalInvariantViolation):
            graph.connect(
                NODE_CONDITIONAL_PROBABILITY,
                NODE_PROBABILITY,
                RelationshipType.PREREQUISITE,
            )

    def test_connect_allows_multiple_relationship_types_between_same_pair(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.RELATED
        )
        assert graph.edge_count() == 2

    def test_connect_rejects_structural_cycle(self) -> None:
        graph = make_probability_chain_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.connect(
                NODE_PROBABILITY, NODE_CREDIBILITY_THEORY, RelationshipType.PREREQUISITE
            )

    def test_connect_allows_advisory_cycle(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.connect(
            NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY, RelationshipType.SUPPORTS
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.SUPPORTS
        )
        assert graph.edge_count() == 2


class TestDisconnect:
    def test_disconnect_removes_edge(self) -> None:
        graph = make_probability_chain_graph()
        graph.disconnect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        assert not graph.has_edge(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        assert graph.edge_count() == 2

    def test_disconnect_missing_edge_raises(self) -> None:
        graph = make_probability_chain_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.disconnect(
                NODE_PROBABILITY, NODE_CREDIBILITY_THEORY, RelationshipType.PREREQUISITE
            )

    def test_disconnect_then_reconnect(self) -> None:
        graph = make_probability_chain_graph()
        graph.disconnect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        assert graph.edge_count() == 3


class TestFindPrerequisites:
    def test_direct_prerequisites(self) -> None:
        graph = make_probability_chain_graph()
        assert graph.find_prerequisites(NODE_BAYES_THEOREM) == (
            NODE_CONDITIONAL_PROBABILITY,
        )

    def test_transitive_prerequisites(self) -> None:
        graph = make_probability_chain_graph()
        result = graph.find_prerequisites(NODE_BAYES_THEOREM, transitive=True)
        assert set(result) == {NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY}

    def test_no_prerequisites_for_foundation(self) -> None:
        graph = make_probability_chain_graph()
        assert graph.find_prerequisites(NODE_PROBABILITY) == ()

    def test_ignores_advisory_relationships(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.SUPPORTS
        )
        assert graph.find_prerequisites(NODE_CONDITIONAL_PROBABILITY) == ()

    def test_rejects_unregistered_node(self) -> None:
        graph = make_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.find_prerequisites(NODE_PROBABILITY)


class TestFindDependents:
    def test_direct_dependents(self) -> None:
        graph = make_probability_chain_graph()
        assert graph.find_dependents(NODE_PROBABILITY) == (
            NODE_CONDITIONAL_PROBABILITY,
        )

    def test_transitive_dependents(self) -> None:
        graph = make_probability_chain_graph()
        result = graph.find_dependents(NODE_PROBABILITY, transitive=True)
        assert set(result) == {
            NODE_CONDITIONAL_PROBABILITY,
            NODE_BAYES_THEOREM,
            NODE_CREDIBILITY_THEORY,
        }

    def test_no_dependents_for_leaf(self) -> None:
        graph = make_probability_chain_graph()
        assert graph.find_dependents(NODE_CREDIBILITY_THEORY) == ()

    def test_rejects_unregistered_node(self) -> None:
        graph = make_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.find_dependents(NODE_PROBABILITY)


class TestFindFoundations:
    def test_foundation_of_deep_node(self) -> None:
        graph = make_probability_chain_graph()
        assert graph.find_foundations(NODE_CREDIBILITY_THEORY) == (NODE_PROBABILITY,)

    def test_node_with_no_prerequisites_is_its_own_foundation(self) -> None:
        graph = make_probability_chain_graph()
        assert graph.find_foundations(NODE_PROBABILITY) == (NODE_PROBABILITY,)

    def test_multiple_foundations(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(make_node(node_id=NODE_BAYES_THEOREM, label="Bayes"))
        graph.add_node(make_node(node_id=NODE_CREDIBILITY_THEORY, label="Credibility"))
        graph.connect(
            NODE_CREDIBILITY_THEORY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        graph.connect(
            NODE_CREDIBILITY_THEORY, NODE_BAYES_THEOREM, RelationshipType.PREREQUISITE
        )
        foundations = graph.find_foundations(NODE_CREDIBILITY_THEORY)
        assert set(foundations) == {NODE_PROBABILITY, NODE_BAYES_THEOREM}

    def test_rejects_unregistered_node(self) -> None:
        graph = make_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.find_foundations(NODE_PROBABILITY)

    def test_falls_back_to_self_when_state_is_corrupted(self) -> None:
        """A node whose only structural edge is a corrupted self-loop still
        yields a defined (self) foundation rather than an empty result."""
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        self_edge = KnowledgeEdge(
            relationship_id=KnowledgeRelationshipId.for_edge(
                NODE_PROBABILITY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
            ),
            source_node_id=NODE_PROBABILITY,
            relationship=KnowledgeRelationship.of(
                NODE_PROBABILITY, RelationshipType.PREREQUISITE
            ),
        )
        graph._edges.append(self_edge)  # type: ignore[attr-defined]
        assert graph.find_foundations(NODE_PROBABILITY) == (NODE_PROBABILITY,)


class TestFindLearningPath:
    def test_full_chain_path(self) -> None:
        graph = make_probability_chain_graph()
        path = graph.find_learning_path(NODE_PROBABILITY, NODE_CREDIBILITY_THEORY)
        assert list(path) == [
            NODE_PROBABILITY,
            NODE_CONDITIONAL_PROBABILITY,
            NODE_BAYES_THEOREM,
            NODE_CREDIBILITY_THEORY,
        ]

    def test_partial_chain_path(self) -> None:
        graph = make_probability_chain_graph()
        path = graph.find_learning_path(
            NODE_CONDITIONAL_PROBABILITY, NODE_CREDIBILITY_THEORY
        )
        assert list(path) == [
            NODE_CONDITIONAL_PROBABILITY,
            NODE_BAYES_THEOREM,
            NODE_CREDIBILITY_THEORY,
        ]

    def test_trivial_path_when_start_equals_target(self) -> None:
        graph = make_probability_chain_graph()
        path = graph.find_learning_path(NODE_PROBABILITY, NODE_PROBABILITY)
        assert list(path) == [NODE_PROBABILITY]

    def test_raises_when_unreachable(self) -> None:
        graph = make_probability_chain_graph()
        with pytest.raises(EducationalInvariantViolation) as excinfo:
            graph.find_learning_path(NODE_CREDIBILITY_THEORY, NODE_PROBABILITY)
        assert excinfo.value.invariant == "LearningPathPolicy.unreachable"

    def test_rejects_unregistered_start(self) -> None:
        graph = make_probability_chain_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.find_learning_path(KnowledgeNodeId("unknown"), NODE_PROBABILITY)

    def test_rejects_unregistered_target(self) -> None:
        graph = make_probability_chain_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.find_learning_path(NODE_PROBABILITY, KnowledgeNodeId("unknown"))

    def test_shortest_path_chosen_when_multiple_exist(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.add_node(make_node(node_id=NODE_BAYES_THEOREM, label="Bayes"))
        graph.add_node(make_node(node_id=NODE_CREDIBILITY_THEORY, label="Credibility"))
        # Direct edge plus a longer detour; shortest path should use the direct hop.
        graph.connect(
            NODE_CREDIBILITY_THEORY, NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        graph.connect(
            NODE_CREDIBILITY_THEORY, NODE_BAYES_THEOREM, RelationshipType.PREREQUISITE
        )
        graph.connect(
            NODE_BAYES_THEOREM,
            NODE_CONDITIONAL_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        path = graph.find_learning_path(NODE_PROBABILITY, NODE_CREDIBILITY_THEORY)
        assert path.step_count == 1
        assert list(path) == [NODE_PROBABILITY, NODE_CREDIBILITY_THEORY]

    def test_private_shortest_path_helper_handles_equal_endpoints(self) -> None:
        """The internal helper is defensively self-contained even though the
        public find_learning_path already short-circuits equal endpoints
        before delegating to it."""
        graph = make_probability_chain_graph()
        path = graph._shortest_structural_path(  # type: ignore[attr-defined]
            NODE_PROBABILITY, NODE_PROBABILITY
        )
        assert path is not None
        assert list(path) == [NODE_PROBABILITY]


class TestDiamondDependencyGraph:
    """Diamond-shaped dependency graph: T -> A -> M -> F and T -> B -> M.

    Exercises BFS traversal branches where a node is reached through more
    than one path and must be skipped the second time it is discovered.
    """

    NODE_T = KnowledgeNodeId("diamond-t")
    NODE_A = KnowledgeNodeId("diamond-a")
    NODE_B = KnowledgeNodeId("diamond-b")
    NODE_M = KnowledgeNodeId("diamond-m")
    NODE_F = KnowledgeNodeId("diamond-f")

    def _build(self) -> KnowledgeGraph:
        graph = make_graph()
        for node_id in (
            self.NODE_T,
            self.NODE_A,
            self.NODE_B,
            self.NODE_M,
            self.NODE_F,
        ):
            graph.add_node(make_node(node_id=node_id, label=node_id.value))
        graph.connect(self.NODE_T, self.NODE_A, RelationshipType.PREREQUISITE)
        graph.connect(self.NODE_T, self.NODE_B, RelationshipType.PREREQUISITE)
        graph.connect(self.NODE_A, self.NODE_M, RelationshipType.PREREQUISITE)
        graph.connect(self.NODE_B, self.NODE_M, RelationshipType.PREREQUISITE)
        graph.connect(self.NODE_M, self.NODE_F, RelationshipType.PREREQUISITE)
        return graph

    def test_transitive_prerequisites_visit_shared_node_once(self) -> None:
        graph = self._build()
        prerequisites = graph.find_prerequisites(self.NODE_T, transitive=True)
        assert set(prerequisites) == {
            self.NODE_A,
            self.NODE_B,
            self.NODE_M,
            self.NODE_F,
        }
        assert len(prerequisites) == 4

    def test_transitive_dependents_visit_shared_node_once(self) -> None:
        graph = self._build()
        dependents = graph.find_dependents(self.NODE_M, transitive=True)
        assert set(dependents) == {self.NODE_A, self.NODE_B, self.NODE_T}
        assert len(dependents) == 3

    def test_learning_path_through_converging_branches(self) -> None:
        graph = self._build()
        path = graph.find_learning_path(self.NODE_F, self.NODE_T)
        assert path.start == self.NODE_F
        assert path.end == self.NODE_T
        assert path.contains(self.NODE_M)


class TestFindConceptClusters:
    def test_no_clusters_without_advisory_edges(self) -> None:
        graph = make_probability_chain_graph()
        assert graph.find_concept_clusters() == ()

    def test_single_cluster_from_supports(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.add_node(make_node(node_id=NODE_BAYES_THEOREM, label="Bayes"))
        graph.connect(
            NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY, RelationshipType.SUPPORTS
        )
        graph.connect(
            NODE_CONDITIONAL_PROBABILITY, NODE_BAYES_THEOREM, RelationshipType.RELATED
        )
        clusters = graph.find_concept_clusters()
        assert len(clusters) == 1
        assert set(clusters[0].node_ids) == {
            NODE_PROBABILITY,
            NODE_CONDITIONAL_PROBABILITY,
            NODE_BAYES_THEOREM,
        }

    def test_isolated_node_not_in_any_cluster(self) -> None:
        graph = make_graph()
        graph.add_node(make_node(node_id=NODE_PROBABILITY))
        graph.add_node(
            make_node(node_id=NODE_CONDITIONAL_PROBABILITY, label="Conditional")
        )
        graph.add_node(make_node(node_id=NODE_BAYES_THEOREM, label="Bayes"))
        graph.connect(
            NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY, RelationshipType.SUPPORTS
        )
        clusters = graph.find_concept_clusters()
        assert len(clusters) == 1
        assert NODE_BAYES_THEOREM not in clusters[0].node_ids

    def test_multiple_disjoint_clusters(self) -> None:
        graph = make_graph()
        for node_id in (
            NODE_PROBABILITY,
            NODE_CONDITIONAL_PROBABILITY,
            NODE_BAYES_THEOREM,
            NODE_CREDIBILITY_THEORY,
        ):
            graph.add_node(make_node(node_id=node_id, label=node_id.value))
        graph.connect(
            NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY, RelationshipType.RELATED
        )
        graph.connect(
            NODE_BAYES_THEOREM, NODE_CREDIBILITY_THEORY, RelationshipType.REINFORCES
        )
        clusters = graph.find_concept_clusters()
        assert len(clusters) == 2

    def test_structural_edges_do_not_form_clusters(self) -> None:
        graph = make_probability_chain_graph()
        graph.connect(
            NODE_PROBABILITY, NODE_CREDIBILITY_THEORY, RelationshipType.RELATED
        )
        clusters = graph.find_concept_clusters()
        assert len(clusters) == 1
        assert set(clusters[0].node_ids) == {NODE_PROBABILITY, NODE_CREDIBILITY_THEORY}


class TestDetectCycles:
    def test_no_cycles_in_valid_graph(self) -> None:
        graph = make_probability_chain_graph()
        assert graph.detect_cycles() == ()

    def test_no_cycles_in_empty_graph(self) -> None:
        graph = make_graph()
        assert graph.detect_cycles() == ()

    def test_detects_cycle_when_state_is_corrupted(self) -> None:
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
        cycles = graph.detect_cycles()
        assert len(cycles) == 1
        assert cycles[0][0] == cycles[0][-1]


class TestProduceSnapshot:
    def test_snapshot_reflects_state(self) -> None:
        graph = make_probability_chain_graph()
        snapshot = graph.produce_snapshot()
        assert snapshot.graph_id == graph.graph_id
        assert snapshot.node_count() == graph.node_count()
        assert snapshot.edge_count() == graph.edge_count()
        assert set(snapshot.nodes) == set(graph.nodes)
        assert set(snapshot.edges) == set(graph.edges)

    def test_snapshot_accepts_produced_at(self) -> None:
        graph = make_probability_chain_graph()
        when = datetime(2026, 7, 21, tzinfo=UTC)
        snapshot = graph.produce_snapshot(produced_at=when)
        assert snapshot.produced_at == when

    def test_snapshot_is_immutable_relative_to_future_mutation(self) -> None:
        graph = make_probability_chain_graph()
        snapshot = graph.produce_snapshot()
        graph.remove_node(NODE_PROBABILITY)
        assert snapshot.node_count() == 4
        assert graph.node_count() == 3


class TestEqualityAndRepr:
    def test_equality_same_object_reference(self) -> None:
        graph = KnowledgeGraph.create(GRAPH_001)
        assert graph == graph  # noqa: PLR0124 (deliberate self-comparison)

    def test_equality_by_identity(self) -> None:
        first = KnowledgeGraph.create(GRAPH_001)
        second = KnowledgeGraph.create(GRAPH_001)
        assert first == second

    def test_inequality_different_identity(self) -> None:
        first = KnowledgeGraph.create(GRAPH_001)
        second = KnowledgeGraph.create(KnowledgeGraphId("graph-002"))
        assert first != second

    def test_equal_objects_share_hash(self) -> None:
        first = KnowledgeGraph.create(GRAPH_001)
        second = KnowledgeGraph.create(GRAPH_001)
        assert hash(first) == hash(second)

    def test_not_equal_to_other_type(self) -> None:
        graph = KnowledgeGraph.create(GRAPH_001)
        assert graph != "not-a-graph"

    def test_repr_contains_counts(self) -> None:
        graph = make_probability_chain_graph()
        text = repr(graph)
        assert "nodes=4" in text
        assert "edges=3" in text


class TestEdgesFromAndTo:
    def test_edges_from(self) -> None:
        graph = make_probability_chain_graph()
        edges = graph.edges_from(NODE_CONDITIONAL_PROBABILITY)
        assert len(edges) == 1
        assert edges[0].target_node_id == NODE_PROBABILITY

    def test_edges_to(self) -> None:
        graph = make_probability_chain_graph()
        edges = graph.edges_to(NODE_PROBABILITY)
        assert len(edges) == 1
        assert edges[0].source_node_id == NODE_CONDITIONAL_PROBABILITY

    def test_edges_from_rejects_unregistered(self) -> None:
        graph = make_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.edges_from(NODE_PROBABILITY)

    def test_edges_to_rejects_unregistered(self) -> None:
        graph = make_graph()
        with pytest.raises(EducationalInvariantViolation):
            graph.edges_to(NODE_PROBABILITY)


class TestLargeGraph:
    def test_long_chain_transitive_reasoning(self) -> None:
        graph = make_graph()
        node_ids = [KnowledgeNodeId(f"concept-{i}") for i in range(50)]
        for node_id in node_ids:
            graph.add_node(
                KnowledgeNode(
                    node_id=node_id, label=node_id.value, kind=KnowledgeNodeKind.CONCEPT
                )
            )
        for later, earlier in zip(node_ids[1:], node_ids[:-1], strict=True):
            graph.connect(later, earlier, RelationshipType.PREREQUISITE)
        prerequisites = graph.find_prerequisites(node_ids[-1], transitive=True)
        assert len(prerequisites) == 49
        foundations = graph.find_foundations(node_ids[-1])
        assert foundations == (node_ids[0],)
        path = graph.find_learning_path(node_ids[0], node_ids[-1])
        assert len(path) == 50
