"""Additional edge-case and algorithm coverage for V2-004."""

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
    LearningPath,
    Module,
    Prerequisite,
    RevisionLink,
    Subject,
    Topic,
    TopicDifficulty,
    TopicId,
)
from app.domain.curriculum.value_objects.dependency_type import (
    HARD_DEPENDENCY_TYPES,
    SOFT_DEPENDENCY_TYPES,
)
from tests.domain.curriculum.helpers import (
    build_graph,
    diamond_curriculum,
    linear_curriculum,
    make_curriculum,
    make_module,
    make_subject,
    make_topic,
)


def test_hard_and_soft_dependency_sets() -> None:
    assert DependencyType.REQUIRES in HARD_DEPENDENCY_TYPES
    assert DependencyType.REVISION in SOFT_DEPENDENCY_TYPES
    assert HARD_DEPENDENCY_TYPES.isdisjoint(SOFT_DEPENDENCY_TYPES)


def test_topic_journey_ref_and_id_property() -> None:
    t = Topic.create("t1", "Name", journey_ref=" journey-9 ")
    assert t.journey_ref == "journey-9"
    assert t.id == "t1"


def test_module_topic_ids_order() -> None:
    m = make_module(
        "m1",
        [
            make_topic("b", module_id="m1", sequence_index=1),
            make_topic("a", module_id="m1", sequence_index=0),
        ],
    )
    assert [t.value for t in m.topic_ids()] == ["a", "b"]


def test_subject_topic_ids() -> None:
    s = make_subject(
        "s1",
        [
            make_module(
                "m1",
                [make_topic("x", module_id="m1")],
                subject_id="s1",
            )
        ],
    )
    assert s.topic_ids()[0].value == "x"


def test_dependency_rationale_optional() -> None:
    d = Dependency.create("d1", "a", "b", DependencyType.OPTIONAL, rationale="  note ")
    assert d.rationale == "note"


def test_learning_path_description() -> None:
    p = LearningPath.create(
        "p1", "Path", ["a"], description=" structural route "
    )
    assert p.description == "structural route"


def test_revision_pair_method() -> None:
    link = RevisionLink.create("r1", "b", "a")
    assert link.pair() == (TopicId("a"), TopicId("b"))


def test_graph_neighbours_type_filter() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    g.connect_topics("a", "b", DependencyType.RELATED)
    g.connect_topics("a", "b", DependencyType.RECOMMENDS)
    related = g.neighbours("a", dependency_type=DependencyType.RELATED, direction="out")
    assert [t.value for t in related] == ["b"]


def test_bfs_none_dependency_type_walks_all() -> None:
    g = CurriculumGraph()
    for tid in ("a", "b", "c"):
        g.add_topic(GraphNode.create(tid, tid))
    g.connect_topics("a", "b", DependencyType.RELATED)
    g.connect_topics("b", "c", DependencyType.OPTIONAL)
    order = [t.value for t in g.bfs("a", dependency_type=None)]
    assert order == ["a", "b", "c"]


def test_dfs_avoids_revisiting() -> None:
    g = build_graph(diamond_curriculum())
    # from d outbound: d→b, d→c, then to a
    order = [t.value for t in g.dfs("d")]
    assert order.count("a") == 1
    assert order[0] == "d"


def test_topological_isolated_nodes_included() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("z", "Z"))
    g.add_topic(GraphNode.create("a", "A"))
    g.add_topic(GraphNode.create("b", "B"))
    g.connect_topics("b", "a", DependencyType.REQUIRES)
    order = [t.value for t in g.topological_ordering()]
    assert set(order) == {"a", "b", "z"}
    assert order.index("a") < order.index("b")


def test_shortest_path_diamond() -> None:
    g = build_graph(diamond_curriculum())
    path = g.shortest_prerequisite_path("d", "a")
    assert path is not None
    assert path[0].value == "d"
    assert path[-1].value == "a"
    # shortest length is 3 nodes (d-b-a or d-c-a)
    assert len(path) == 3


def test_builder_skips_duplicate_revision_directions() -> None:
    topics = [make_topic("a"), make_topic("b")]
    # Pre-seed via Dependency REVISION both ways, then RevisionLink
    deps = [
        Dependency.create("r1", "a", "b", DependencyType.REVISION),
        Dependency.create("r2", "b", "a", DependencyType.REVISION),
    ]
    g = GraphBuilder().build_from_topics(
        topics,
        dependencies=deps,
        revision_links=[RevisionLink.create("rl", "a", "b")],
    )
    rev = [e for e in g.edges() if e.dependency_type is DependencyType.REVISION]
    assert len(rev) == 2


def test_validator_single_node_no_disconnected_issue() -> None:
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("solo", "Solo"))
    result = GraphValidator().validate(g)
    assert result.is_valid


def test_curriculum_duplicate_dependency_id() -> None:
    topics = [
        make_topic("a", module_id="m1"),
        make_topic("b", module_id="m1", sequence_index=1),
    ]
    m = make_module("m1", topics, subject_id="s1")
    s = make_subject("s1", [m], curriculum_id="c1")
    deps = [
        Dependency.create("same", "b", "a", DependencyType.REQUIRES),
        Dependency.create("same", "b", "a", DependencyType.RELATED),
    ]
    with pytest.raises(ValueError, match="duplicate dependency"):
        make_curriculum("c1", subjects=[s], dependencies=deps)


def test_curriculum_duplicate_prerequisite_id() -> None:
    curr = linear_curriculum()
    with pytest.raises(ValueError, match="duplicate prerequisite"):
        make_curriculum(
            "demo-curr",
            subjects=list(curr.subjects),
            prerequisites=[
                Prerequisite.create("p1", "b", "a"),
                Prerequisite.create("p1", "c", "b"),
            ],
        )


def test_curriculum_duplicate_path_id() -> None:
    curr = linear_curriculum()
    paths = [
        LearningPath.create("p", "One", ["a"], curriculum_id="demo-curr"),
        LearningPath.create("p", "Two", ["b"], curriculum_id="demo-curr"),
    ]
    with pytest.raises(ValueError, match="duplicate path"):
        make_curriculum(
            "demo-curr",
            subjects=list(curr.subjects),
            learning_paths=paths,
        )


def test_curriculum_path_curriculum_id_mismatch() -> None:
    curr = linear_curriculum()
    with pytest.raises(ValueError, match="curriculum_id must match"):
        make_curriculum(
            "demo-curr",
            subjects=list(curr.subjects),
            learning_paths=[
                LearningPath.create("p", "X", ["a"], curriculum_id="other")
            ],
        )


def test_subject_module_subject_mismatch() -> None:
    m = make_module("m1", [], subject_id="other")
    with pytest.raises(ValueError):
        make_subject("s1", [m])


def test_module_with_topic_subject_mismatch_via_module_id() -> None:
    m = make_module("m1", [])
    with pytest.raises(ValueError):
        m.with_topic(make_topic("a", module_id="other"))


def test_empty_name_rejected_everywhere() -> None:
    with pytest.raises(ValueError):
        Topic.create("t", "  ")
    with pytest.raises(ValueError):
        Module.create("m", "")
    with pytest.raises(ValueError):
        Subject.create("s", "")
    with pytest.raises(ValueError):
        LearningPath.create("p", " ")


def test_graph_edge_create_with_edge_id() -> None:
    e = GraphEdge.create("a", "b", "requires", edge_id=" e1 ")
    assert e.edge_id == "e1"
    assert e.dependency_type is DependencyType.REQUIRES


def test_add_edge_missing_nodes() -> None:
    g = CurriculumGraph()
    edge = GraphEdge.create("a", "b", DependencyType.REQUIRES)
    with pytest.raises(ValueError):
        g.add_edge(edge)


def test_neighbours_missing_topic() -> None:
    g = CurriculumGraph()
    with pytest.raises(ValueError):
        g.neighbours("ghost")


def test_all_prerequisites_missing() -> None:
    g = CurriculumGraph()
    with pytest.raises(ValueError):
        g.all_prerequisites("ghost")


def test_difficulty_string_on_node() -> None:
    n = GraphNode.create("t", "T", difficulty="capstone")
    assert n.difficulty is TopicDifficulty.CAPSTONE


def test_multi_subject_curriculum_order() -> None:
    s0 = make_subject(
        "s0",
        [make_module("m0", [make_topic("a", module_id="m0")], subject_id="s0")],
        sequence_index=0,
        curriculum_id="multi",
    )
    s1 = make_subject(
        "s1",
        [make_module("m1", [make_topic("b", module_id="m1")], subject_id="s1")],
        sequence_index=1,
        curriculum_id="multi",
    )
    curr = make_curriculum("multi", subjects=[s1, s0])
    assert [t.value for t in curr.topic_ids()] == ["a", "b"]
