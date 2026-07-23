"""Value object tests for Knowledge Dependency Graph."""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph import (
    ConceptCluster,
    DependencyStrength,
    DependencyStrengthBand,
    KnowledgeEdge,
    KnowledgeNode,
    KnowledgeNodeId,
    KnowledgeNodeKind,
    KnowledgePath,
    KnowledgeRelationship,
    KnowledgeRelationshipId,
    KnowledgeSnapshot,
    LearningDepth,
    RelationshipMetadata,
    RelationshipType,
)
from tests.domain.education.knowledge_graph.conftest import (
    NODE_BAYES_THEOREM,
    NODE_CONDITIONAL_PROBABILITY,
    NODE_PROBABILITY,
    make_edge,
    make_node,
)


class TestKnowledgeNodeId:
    def test_construction(self) -> None:
        node_id = KnowledgeNodeId("probability")
        assert node_id.value == "probability"
        assert str(node_id) == "probability"

    def test_rejects_blank(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeNodeId("   ")

    def test_rejects_interior_whitespace(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeNodeId("bad id")

    def test_immutable(self) -> None:
        node_id = KnowledgeNodeId("probability")
        with pytest.raises(dataclasses.FrozenInstanceError):
            node_id.value = "other"  # type: ignore[misc]

    def test_structural_equality(self) -> None:
        assert KnowledgeNodeId("probability") == KnowledgeNodeId("probability")
        assert KnowledgeNodeId("probability") != KnowledgeNodeId("other")


class TestKnowledgeGraphIdAndRelationshipIdStr:
    def test_knowledge_graph_id_str(self) -> None:
        from domain.education.knowledge_graph import KnowledgeGraphId

        assert str(KnowledgeGraphId("graph-001")) == "graph-001"

    def test_knowledge_relationship_id_str(self) -> None:
        relationship_id = KnowledgeRelationshipId.for_edge(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        assert str(relationship_id) == relationship_id.value


class TestKnowledgeRelationshipIdForEdge:
    def test_deterministic(self) -> None:
        first = KnowledgeRelationshipId.for_edge(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        second = KnowledgeRelationshipId.for_edge(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        assert first == second

    def test_varies_by_type(self) -> None:
        prereq = KnowledgeRelationshipId.for_edge(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        supports = KnowledgeRelationshipId.for_edge(
            NODE_CONDITIONAL_PROBABILITY, NODE_PROBABILITY, RelationshipType.SUPPORTS
        )
        assert prereq != supports

    def test_varies_by_direction(self) -> None:
        forward = KnowledgeRelationshipId.for_edge(
            NODE_CONDITIONAL_PROBABILITY,
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        backward = KnowledgeRelationshipId.for_edge(
            NODE_PROBABILITY,
            NODE_CONDITIONAL_PROBABILITY,
            RelationshipType.PREREQUISITE,
        )
        assert forward != backward


class TestKnowledgeNode:
    def test_construction_defaults(self) -> None:
        node = make_node()
        assert node.node_id == NODE_PROBABILITY
        assert node.label == "Probability"
        assert node.kind is KnowledgeNodeKind.CONCEPT
        assert node.description is None

    def test_wrong_node_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeNode(node_id="probability", label="Probability")  # type: ignore[arg-type]

    def test_blank_label_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeNode(node_id=NODE_PROBABILITY, label="   ")

    def test_wrong_kind_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeNode(node_id=NODE_PROBABILITY, label="Probability", kind="concept")  # type: ignore[arg-type]

    def test_blank_description_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeNode(
                node_id=NODE_PROBABILITY, label="Probability", description="   "
            )

    def test_with_label(self) -> None:
        node = make_node()
        updated = node.with_label("Probability Theory")
        assert updated.label == "Probability Theory"
        assert updated.node_id == node.node_id
        assert node.label == "Probability"

    def test_with_kind(self) -> None:
        node = make_node()
        updated = node.with_kind(KnowledgeNodeKind.SKILL)
        assert updated.kind is KnowledgeNodeKind.SKILL
        assert node.kind is KnowledgeNodeKind.CONCEPT

    def test_with_description(self) -> None:
        node = make_node()
        updated = node.with_description("Foundational concept")
        assert updated.description == "Foundational concept"
        assert node.description is None

    def test_immutable(self) -> None:
        node = make_node()
        with pytest.raises(dataclasses.FrozenInstanceError):
            node.label = "Other"  # type: ignore[misc]

    def test_str(self) -> None:
        node = make_node()
        assert str(node) == "probability:Probability"

    def test_structural_equality(self) -> None:
        assert make_node() == make_node()


class TestDependencyStrength:
    def test_factories(self) -> None:
        assert DependencyStrength.optional().band is DependencyStrengthBand.OPTIONAL
        assert DependencyStrength.helpful().band is DependencyStrengthBand.HELPFUL
        assert DependencyStrength.important().band is DependencyStrengthBand.IMPORTANT
        assert DependencyStrength.critical().band is DependencyStrengthBand.CRITICAL

    def test_wrong_band_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            DependencyStrength(band="critical")  # type: ignore[arg-type]

    @pytest.mark.parametrize("weight", [-0.1, 1.1])
    def test_weight_out_of_range(self, weight: float) -> None:
        with pytest.raises(EducationalInvariantViolation):
            DependencyStrength(band=DependencyStrengthBand.HELPFUL, weight=weight)

    def test_weight_bool_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            DependencyStrength(band=DependencyStrengthBand.HELPFUL, weight=True)  # type: ignore[arg-type]

    def test_weight_coerced_to_float(self) -> None:
        strength = DependencyStrength(band=DependencyStrengthBand.HELPFUL, weight=1)
        assert strength.weight == 1.0
        assert isinstance(strength.weight, float)

    def test_rank_ordering(self) -> None:
        assert (
            DependencyStrength.critical().rank() > DependencyStrength.important().rank()
        )
        assert (
            DependencyStrength.important().rank() > DependencyStrength.helpful().rank()
        )
        assert (
            DependencyStrength.helpful().rank() > DependencyStrength.optional().rank()
        )

    def test_is_stronger_than(self) -> None:
        assert DependencyStrength.critical().is_stronger_than(
            DependencyStrength.optional()
        )
        assert not DependencyStrength.optional().is_stronger_than(
            DependencyStrength.critical()
        )

    def test_str(self) -> None:
        assert str(DependencyStrength.critical()) == "critical"


class TestRelationshipMetadata:
    def test_empty_factory(self) -> None:
        metadata = RelationshipMetadata.empty()
        assert metadata.description is None
        assert metadata.tags == ()

    def test_blank_description_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            RelationshipMetadata(description="   ")

    def test_tags_normalised_to_tuple(self) -> None:
        metadata = RelationshipMetadata(tags=["a", "b"])
        assert metadata.tags == ("a", "b")

    def test_duplicate_tags_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            RelationshipMetadata(tags=("a", "a"))

    def test_blank_tag_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            RelationshipMetadata(tags=("  ",))

    def test_wrong_tags_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            RelationshipMetadata(tags="not-a-collection")  # type: ignore[arg-type]

    def test_with_description(self) -> None:
        metadata = RelationshipMetadata.empty().with_description("rationale")
        assert metadata.description == "rationale"

    def test_with_tag_appends(self) -> None:
        metadata = RelationshipMetadata.empty().with_tag("bridge")
        assert metadata.tags == ("bridge",)

    def test_with_tag_idempotent(self) -> None:
        metadata = RelationshipMetadata(tags=("bridge",))
        updated = metadata.with_tag("bridge")
        assert updated is metadata


class TestLearningDepth:
    def test_foundation(self) -> None:
        depth = LearningDepth.foundation()
        assert depth.level == 0
        assert depth.is_foundation()

    def test_next(self) -> None:
        depth = LearningDepth.foundation().next()
        assert depth.level == 1
        assert not depth.is_foundation()

    def test_negative_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningDepth(level=-1)

    def test_bool_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningDepth(level=True)  # type: ignore[arg-type]

    def test_non_int_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningDepth(level=1.5)  # type: ignore[arg-type]

    def test_deeper_than(self) -> None:
        assert LearningDepth(level=2).deeper_than(LearningDepth(level=1))
        assert not LearningDepth(level=1).deeper_than(LearningDepth(level=2))

    def test_str(self) -> None:
        assert str(LearningDepth(level=3)) == "3"


class TestKnowledgeRelationship:
    def test_of_defaults(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        assert relationship.strength.band is DependencyStrengthBand.HELPFUL
        assert relationship.metadata == RelationshipMetadata.empty()

    def test_wrong_target_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeRelationship(
                target_node_id="probability",  # type: ignore[arg-type]
                relationship_type=RelationshipType.PREREQUISITE,
                strength=DependencyStrength.helpful(),
                metadata=RelationshipMetadata.empty(),
            )

    def test_wrong_relationship_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeRelationship(
                target_node_id=NODE_PROBABILITY,
                relationship_type="prerequisite",  # type: ignore[arg-type]
                strength=DependencyStrength.helpful(),
                metadata=RelationshipMetadata.empty(),
            )

    def test_wrong_strength_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeRelationship(
                target_node_id=NODE_PROBABILITY,
                relationship_type=RelationshipType.PREREQUISITE,
                strength="critical",  # type: ignore[arg-type]
                metadata=RelationshipMetadata.empty(),
            )

    def test_wrong_metadata_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeRelationship(
                target_node_id=NODE_PROBABILITY,
                relationship_type=RelationshipType.PREREQUISITE,
                strength=DependencyStrength.helpful(),
                metadata="none",  # type: ignore[arg-type]
            )

    def test_assert_not_self_raises(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        with pytest.raises(EducationalInvariantViolation):
            relationship.assert_not_self(NODE_PROBABILITY)

    def test_assert_not_self_passes(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        relationship.assert_not_self(NODE_CONDITIONAL_PROBABILITY)

    def test_assert_not_self_wrong_owner_type(self) -> None:
        relationship = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        with pytest.raises(EducationalInvariantViolation):
            relationship.assert_not_self("probability")  # type: ignore[arg-type]

    def test_same_edge_true(self) -> None:
        first = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        second = KnowledgeRelationship.of(
            NODE_PROBABILITY,
            RelationshipType.PREREQUISITE,
            strength=DependencyStrength.critical(),
        )
        assert first.same_edge(second)

    def test_same_edge_false_different_target(self) -> None:
        first = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        second = KnowledgeRelationship.of(
            NODE_CONDITIONAL_PROBABILITY, RelationshipType.PREREQUISITE
        )
        assert not first.same_edge(second)

    def test_same_edge_false_different_type(self) -> None:
        first = KnowledgeRelationship.of(
            NODE_PROBABILITY, RelationshipType.PREREQUISITE
        )
        second = KnowledgeRelationship.of(NODE_PROBABILITY, RelationshipType.SUPPORTS)
        assert not first.same_edge(second)


class TestKnowledgeEdge:
    def test_properties_delegate_to_relationship(self) -> None:
        edge = make_edge()
        assert edge.target_node_id == NODE_PROBABILITY
        assert edge.relationship_type is RelationshipType.PREREQUISITE
        assert edge.strength == edge.relationship.strength
        assert edge.metadata == edge.relationship.metadata

    def test_wrong_relationship_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeEdge(
                relationship_id="bad-id",  # type: ignore[arg-type]
                source_node_id=NODE_CONDITIONAL_PROBABILITY,
                relationship=KnowledgeRelationship.of(
                    NODE_PROBABILITY, RelationshipType.PREREQUISITE
                ),
            )

    def test_wrong_source_node_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeEdge(
                relationship_id=KnowledgeRelationshipId.for_edge(
                    NODE_CONDITIONAL_PROBABILITY,
                    NODE_PROBABILITY,
                    RelationshipType.PREREQUISITE,
                ),
                source_node_id="conditional-probability",  # type: ignore[arg-type]
                relationship=KnowledgeRelationship.of(
                    NODE_PROBABILITY, RelationshipType.PREREQUISITE
                ),
            )

    def test_wrong_relationship_type_on_edge(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeEdge(
                relationship_id=KnowledgeRelationshipId.for_edge(
                    NODE_CONDITIONAL_PROBABILITY,
                    NODE_PROBABILITY,
                    RelationshipType.PREREQUISITE,
                ),
                source_node_id=NODE_CONDITIONAL_PROBABILITY,
                relationship="prerequisite",  # type: ignore[arg-type]
            )

    def test_same_edge_true(self) -> None:
        first = make_edge()
        second = make_edge()
        assert first.same_edge(second)

    def test_same_edge_false_different_source(self) -> None:
        first = make_edge(source_node_id=NODE_CONDITIONAL_PROBABILITY)
        second = make_edge(source_node_id=NODE_BAYES_THEOREM)
        assert not first.same_edge(second)

    def test_str(self) -> None:
        edge = make_edge()
        assert str(edge) == "conditional-probability --prerequisite--> probability"


class TestKnowledgePath:
    def test_single_node_path(self) -> None:
        path = KnowledgePath((NODE_PROBABILITY,))
        assert path.start == NODE_PROBABILITY
        assert path.end == NODE_PROBABILITY
        assert path.step_count == 0
        assert len(path) == 1

    def test_multi_node_path(self) -> None:
        path = KnowledgePath(
            (NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY, NODE_BAYES_THEOREM)
        )
        assert path.start == NODE_PROBABILITY
        assert path.end == NODE_BAYES_THEOREM
        assert path.step_count == 2
        assert list(path) == [
            NODE_PROBABILITY,
            NODE_CONDITIONAL_PROBABILITY,
            NODE_BAYES_THEOREM,
        ]

    def test_list_coerced_to_tuple(self) -> None:
        path = KnowledgePath([NODE_PROBABILITY])  # type: ignore[arg-type]
        assert path.nodes == (NODE_PROBABILITY,)

    def test_empty_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgePath(())

    def test_wrong_collection_type_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgePath({NODE_PROBABILITY})  # type: ignore[arg-type]

    def test_wrong_element_type_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgePath(("probability",))  # type: ignore[arg-type]

    def test_repeated_node_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgePath((NODE_PROBABILITY, NODE_PROBABILITY))

    def test_contains(self) -> None:
        path = KnowledgePath((NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY))
        assert path.contains(NODE_PROBABILITY)
        assert not path.contains(NODE_BAYES_THEOREM)


class TestConceptCluster:
    def test_construction(self) -> None:
        cluster = ConceptCluster(
            cluster_id="cluster-1",
            node_ids=(NODE_PROBABILITY, NODE_CONDITIONAL_PROBABILITY),
        )
        assert cluster.size == 2
        assert cluster.contains(NODE_PROBABILITY)

    def test_blank_cluster_id_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptCluster(
                cluster_id="  ", node_ids=(NODE_PROBABILITY, NODE_BAYES_THEOREM)
            )

    def test_min_size_enforced(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptCluster(cluster_id="cluster-1", node_ids=(NODE_PROBABILITY,))

    def test_wrong_collection_type_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptCluster(
                cluster_id="cluster-1",
                node_ids={NODE_PROBABILITY, NODE_BAYES_THEOREM},  # type: ignore[arg-type]
            )

    def test_list_coerced_to_tuple(self) -> None:
        cluster = ConceptCluster(
            cluster_id="cluster-1",
            node_ids=[NODE_PROBABILITY, NODE_BAYES_THEOREM],  # type: ignore[arg-type]
        )
        assert cluster.node_ids == (NODE_PROBABILITY, NODE_BAYES_THEOREM)

    def test_wrong_element_type_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptCluster(cluster_id="cluster-1", node_ids=("probability", "bayes"))  # type: ignore[arg-type]

    def test_duplicate_members_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConceptCluster(
                cluster_id="cluster-1", node_ids=(NODE_PROBABILITY, NODE_PROBABILITY)
            )


class TestKnowledgeSnapshot:
    def _valid_kwargs(self, **overrides: object) -> dict[str, object]:
        from domain.education.knowledge_graph import KnowledgeGraphId

        defaults: dict[str, object] = {
            "graph_id": KnowledgeGraphId("graph-001"),
            "nodes": (make_node(),),
            "edges": (),
        }
        defaults.update(overrides)
        return defaults

    def test_construction(self) -> None:
        snapshot = KnowledgeSnapshot(**self._valid_kwargs())
        assert snapshot.node_count() == 1
        assert snapshot.edge_count() == 0
        assert snapshot.produced_at is None

    def test_produced_at_accepted(self) -> None:
        when = datetime(2026, 7, 21, tzinfo=UTC)
        snapshot = KnowledgeSnapshot(**self._valid_kwargs(produced_at=when))
        assert snapshot.produced_at == when

    def test_wrong_graph_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeSnapshot(**self._valid_kwargs(graph_id="graph-001"))

    def test_wrong_nodes_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeSnapshot(**self._valid_kwargs(nodes="not-a-tuple"))

    def test_nodes_list_coerced(self) -> None:
        snapshot = KnowledgeSnapshot(**self._valid_kwargs(nodes=[make_node()]))
        assert isinstance(snapshot.nodes, tuple)

    def test_wrong_node_element_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeSnapshot(**self._valid_kwargs(nodes=("not-a-node",)))

    def test_duplicate_node_ids_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeSnapshot(**self._valid_kwargs(nodes=(make_node(), make_node())))

    def test_wrong_edges_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeSnapshot(**self._valid_kwargs(edges="not-a-tuple"))

    def test_edges_list_coerced(self) -> None:
        snapshot = KnowledgeSnapshot(
            **self._valid_kwargs(
                nodes=(
                    make_node(node_id=NODE_PROBABILITY, label="Probability"),
                    make_node(
                        node_id=NODE_CONDITIONAL_PROBABILITY,
                        label="Conditional Probability",
                    ),
                ),
                edges=[make_edge()],
            )
        )
        assert isinstance(snapshot.edges, tuple)
        assert snapshot.edge_count() == 1

    def test_wrong_edge_element_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeSnapshot(**self._valid_kwargs(edges=("not-an-edge",)))

    def test_duplicate_edges_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeSnapshot(
                **self._valid_kwargs(
                    nodes=(
                        make_node(node_id=NODE_PROBABILITY, label="Probability"),
                        make_node(
                            node_id=NODE_CONDITIONAL_PROBABILITY,
                            label="Conditional Probability",
                        ),
                    ),
                    edges=(make_edge(), make_edge()),
                )
            )

    def test_wrong_produced_at_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeSnapshot(**self._valid_kwargs(produced_at="2026-07-21"))
