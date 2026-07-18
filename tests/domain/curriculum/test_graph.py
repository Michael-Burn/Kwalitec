"""Graph construction, traversal, and algorithm tests (V2-004)."""

from __future__ import annotations

import pytest

from app.domain.curriculum import (
    CurriculumGraph,
    Dependency,
    DependencyType,
    GraphBuilder,
    GraphEdge,
    GraphNode,
    GraphValidator,
    Prerequisite,
    RevisionLink,
    TopicDifficulty,
)
from app.domain.curriculum.graph.graph_validator import (
    validate_dependency_endpoints,
    validate_requires_dag,
)
from tests.domain.curriculum.helpers import (
    build_graph,
    diamond_curriculum,
    linear_curriculum,
    make_topic,
    revision_pair_curriculum,
)

# ---------------------------------------------------------------------------
# GraphNode / GraphEdge
# ---------------------------------------------------------------------------


def test_graph_node_from_topic() -> None:
    topic = make_topic("t1", difficulty=TopicDifficulty.ADVANCED)
    node = GraphNode.from_topic(topic)
    assert node.topic_id.value == "t1"
    assert node.difficulty is TopicDifficulty.ADVANCED
    assert node.payload is topic


def test_graph_node_create_rejects_negative_effort() -> None:
    with pytest.raises(ValueError):
        GraphNode.create("t1", "X", estimated_effort_minutes=-1)


def test_graph_edge_self_loop_and_hard() -> None:
    with pytest.raises(ValueError):
        GraphEdge.create("a", "a", DependencyType.REQUIRES)
    edge = GraphEdge.create("a", "b", DependencyType.REQUIRES)
    assert edge.is_hard
    soft = GraphEdge.create("a", "b", DependencyType.RELATED)
    assert not soft.is_hard


# ---------------------------------------------------------------------------
# Mutation
# ---------------------------------------------------------------------------


def test_add_remove_topic() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    assert g.has_topic("a")
    assert g.topic_count() == 1
    with pytest.raises(ValueError):
        g.add_topic(GraphNode.create("a", "A"))
    assert g.remove_topic("a") is True
    assert g.remove_topic("a") is False


def test_connect_and_remove_clears_edges() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    g.connect_topics("b", "a", DependencyType.REQUIRES)
    assert g.edge_count() == 1
    g.remove_topic("a")
    assert g.edge_count() == 0
    assert not g.has_topic("a")


def test_connect_missing_endpoint() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    with pytest.raises(ValueError, match="target"):
        g.connect_topics("a", "b", DependencyType.REQUIRES)
    with pytest.raises(ValueError, match="source"):
        g.connect_topics("b", "a", DependencyType.REQUIRES)


def test_duplicate_edge_rejected() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    g.connect_topics("b", "a", DependencyType.REQUIRES)
    with pytest.raises(ValueError, match="duplicate"):
        g.connect_topics("b", "a", DependencyType.REQUIRES)


def test_add_edge_prebuilt() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    edge = GraphEdge.create("b", "a", DependencyType.RECOMMENDS, edge_id="e1")
    g.add_edge(edge)
    assert g.edge_count() == 1


# ---------------------------------------------------------------------------
# Neighbours / prereqs / successors / revision
# ---------------------------------------------------------------------------


def test_neighbours_directions() -> None:
    g = build_graph(linear_curriculum())
    assert [t.value for t in g.find_prerequisites("b")] == ["a"]
    assert [t.value for t in g.find_successors("a")] == ["b"]
    assert [t.value for t in g.neighbours("b", direction="out")] == ["a"]
    with pytest.raises(ValueError):
        g.neighbours("b", direction="sideways")


def test_transitive_prerequisites_and_successors() -> None:
    g = build_graph(linear_curriculum())
    assert [t.value for t in g.all_prerequisites("c")] == ["a", "b"]
    assert [t.value for t in g.all_successors("a")] == ["b", "c"]
    assert [t.value for t in g.all_prerequisites("c", transitive=False)] == ["b"]


def test_revision_neighbours() -> None:
    g = build_graph(revision_pair_curriculum())
    links = g.find_revision_links("expectation")
    assert [t.value for t in links] == ["variance"]


# ---------------------------------------------------------------------------
# Traversal
# ---------------------------------------------------------------------------


def test_dfs_bfs_linear() -> None:
    g = build_graph(linear_curriculum())
    # out along REQUIRES: c → b → a
    dfs = [t.value for t in g.dfs("c")]
    assert dfs[0] == "c"
    assert set(dfs) == {"a", "b", "c"}
    bfs = [t.value for t in g.bfs("c")]
    assert bfs[0] == "c"
    assert bfs[1] == "b"
    assert bfs[2] == "a"


def test_dfs_missing_start() -> None:
    g = CurriculumGraph()
    with pytest.raises(ValueError):
        g.dfs("ghost")


def test_bfs_inbound_successors() -> None:
    g = build_graph(linear_curriculum())
    order = [t.value for t in g.bfs("a", direction="in")]
    assert order[0] == "a"
    assert "b" in order


# ---------------------------------------------------------------------------
# Topological sort / cycles
# ---------------------------------------------------------------------------


def test_topological_ordering_linear() -> None:
    g = build_graph(linear_curriculum())
    order = [t.value for t in g.topological_ordering()]
    assert order.index("a") < order.index("b") < order.index("c")


def test_topological_ordering_diamond() -> None:
    g = build_graph(diamond_curriculum())
    order = [t.value for t in g.topological_ordering()]
    assert order.index("a") < order.index("b")
    assert order.index("a") < order.index("c")
    assert order.index("b") < order.index("d")
    assert order.index("c") < order.index("d")


def test_cycle_detection() -> None:
    g = CurriculumGraph()
    for tid in ("a", "b", "c"):
        g.add_topic(GraphNode.create(tid, tid.upper()))
    g.connect_topics("a", "b", DependencyType.REQUIRES)
    g.connect_topics("b", "c", DependencyType.REQUIRES)
    g.connect_topics("c", "a", DependencyType.REQUIRES)
    assert g.has_cycle()
    cycles = g.detect_cycles()
    assert len(cycles) >= 1
    with pytest.raises(ValueError, match="cycle"):
        g.topological_ordering()


def test_no_cycle_on_dag() -> None:
    g = build_graph(diamond_curriculum())
    assert not g.has_cycle()
    assert g.detect_cycles() == ()


def test_soft_edges_do_not_create_requires_cycle() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    g.connect_topics("a", "b", DependencyType.RELATED)
    g.connect_topics("b", "a", DependencyType.RELATED)
    assert not g.has_cycle()
    order = g.topological_ordering()
    assert len(order) == 2


# ---------------------------------------------------------------------------
# Shortest prerequisite path
# ---------------------------------------------------------------------------


def test_shortest_prerequisite_path() -> None:
    g = build_graph(linear_curriculum())
    path = g.shortest_prerequisite_path("c", "a")
    assert path is not None
    assert [t.value for t in path] == ["c", "b", "a"]
    assert g.shortest_prerequisite_path("a", "c") is None
    assert [t.value for t in g.shortest_prerequisite_path("a", "a")] == ["a"]


def test_shortest_path_missing_topic() -> None:
    g = build_graph(linear_curriculum())
    with pytest.raises(ValueError):
        g.shortest_prerequisite_path("a", "ghost")


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def test_builder_from_curriculum_merges_prereq_and_deps() -> None:
    curr = linear_curriculum()
    # Add an overlapping REQUIRES dependency — should not duplicate.
    from tests.domain.curriculum.helpers import make_curriculum

    deps = list(curr.dependencies) + [
        Dependency.create("d-overlap", "b", "a", DependencyType.REQUIRES)
    ]
    curr2 = make_curriculum(
        curr.curriculum_id.value,
        subjects=list(curr.subjects),
        prerequisites=list(curr.prerequisites),
        dependencies=deps,
        learning_paths=list(curr.learning_paths),
    )
    g = GraphBuilder().build_from_curriculum(curr2)
    # One REQUIRES edge b→a
    requires = [
        e
        for e in g.edges()
        if e.dependency_type is DependencyType.REQUIRES
        and e.source_id.value == "b"
    ]
    assert len(requires) == 1


def test_builder_from_topics() -> None:
    topics = [make_topic("a"), make_topic("b")]
    g = GraphBuilder().build_from_topics(
        topics,
        prerequisites=[Prerequisite.create("p1", "b", "a")],
        revision_links=[RevisionLink.create("r1", "a", "b")],
    )
    assert g.topic_count() == 2
    assert g.find_prerequisites("b")[0].value == "a"
    assert "b" in {t.value for t in g.find_revision_links("a")}


def test_builder_revision_bidirectional() -> None:
    g = build_graph(revision_pair_curriculum())
    # Two REVISION edges for the pair
    rev = [e for e in g.edges() if e.dependency_type is DependencyType.REVISION]
    assert len(rev) == 2


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


def test_validator_clean_dag() -> None:
    g = build_graph(linear_curriculum())
    result = GraphValidator(allow_disconnected=True).validate(g)
    assert result.is_valid
    assert not result.has_cycles


def test_validator_reports_cycle() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    g.connect_topics("a", "b", DependencyType.REQUIRES)
    g.connect_topics("b", "a", DependencyType.REQUIRES)
    result = GraphValidator().validate(g)
    assert not result.is_valid
    assert result.has_cycles
    with pytest.raises(ValueError):
        GraphValidator().assert_valid(g)


def test_validator_disconnected_nodes() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    g.add_topic(GraphNode.create("c", "C"))
    g.connect_topics("b", "a", DependencyType.REQUIRES)
    result = GraphValidator().validate(g)
    assert any("disconnected" in i for i in result.issues)
    assert any(t.value == "c" for t in result.disconnected_topic_ids)


def test_validator_allow_disconnected() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    validator = GraphValidator(allow_disconnected=True)
    result = validator.validate(g)
    assert result.is_valid
    assert validator.informational_messages()


def test_validate_requires_dag_helper() -> None:
    assert validate_requires_dag(build_graph(linear_curriculum()))
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    g.connect_topics("a", "b", DependencyType.REQUIRES)
    g.connect_topics("b", "a", DependencyType.REQUIRES)
    assert not validate_requires_dag(g)


def test_validate_dependency_endpoints_empty_on_valid() -> None:
    assert validate_dependency_endpoints(build_graph(linear_curriculum())) == ()


def test_graph_validate_delegates() -> None:
    g = build_graph(linear_curriculum())
    # linear is fully connected via REQUIRES — should be clean
    issues = g.validate()
    assert issues == ()


def test_nodes_stable_order() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("c", "C"))
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    assert [n.topic_id.value for n in g.nodes()] == ["a", "b", "c"]


def test_get_node() -> None:
    g = build_graph(linear_curriculum())
    assert g.get_node("a") is not None
    assert g.get_node("ghost") is None
