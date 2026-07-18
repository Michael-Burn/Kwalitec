"""Entity invariant tests for Curriculum Graph domain (V2-004)."""

from __future__ import annotations

import pytest

from app.domain.curriculum import (
    Curriculum,
    CurriculumId,
    CurriculumVersion,
    Dependency,
    DependencyType,
    LearningPath,
    Prerequisite,
    RevisionLink,
    Topic,
    TopicDifficulty,
    TopicId,
    TopicStatus,
)
from app.domain.curriculum.value_objects.dependency_type import is_hard_dependency
from app.domain.curriculum.value_objects.topic_difficulty import (
    difficulty_at_least,
    difficulty_rank,
)
from app.domain.curriculum.value_objects.topic_status import (
    is_studyable_status,
    is_terminal_topic_status,
)
from tests.domain.curriculum.helpers import (
    linear_curriculum,
    make_curriculum,
    make_module,
    make_subject,
    make_topic,
)

# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


def test_topic_id_strips_and_rejects_empty() -> None:
    assert TopicId("  a  ").value == "a"
    with pytest.raises(ValueError):
        TopicId("  ")
    with pytest.raises(ValueError):
        TopicId.of("")


def test_topic_id_of_passthrough() -> None:
    tid = TopicId("x")
    assert TopicId.of(tid) is tid


def test_curriculum_id_orderable() -> None:
    assert CurriculumId("a") < CurriculumId("b")


def test_dependency_type_hard_soft() -> None:
    assert is_hard_dependency(DependencyType.REQUIRES)
    assert not is_hard_dependency(DependencyType.RECOMMENDS)
    assert DependencyType.OPTIONAL.value == "optional"


def test_difficulty_rank_and_compare() -> None:
    assert difficulty_rank(TopicDifficulty.FOUNDATIONAL) == 1
    assert difficulty_at_least(
        TopicDifficulty.ADVANCED, TopicDifficulty.INTERMEDIATE
    )
    assert not difficulty_at_least(
        TopicDifficulty.FOUNDATIONAL, TopicDifficulty.CAPSTONE
    )


def test_topic_status_helpers() -> None:
    assert is_studyable_status(TopicStatus.AVAILABLE)
    assert is_studyable_status(TopicStatus.ACTIVE)
    assert not is_studyable_status(TopicStatus.LOCKED)
    assert is_terminal_topic_status(TopicStatus.COMPLETED)
    assert is_terminal_topic_status(TopicStatus.ARCHIVED)


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------


def test_topic_create_defaults() -> None:
    t = Topic.create("t1", "Intro")
    assert t.topic_id.value == "t1"
    assert t.difficulty is TopicDifficulty.FOUNDATIONAL
    assert t.estimated_effort_minutes == 0
    assert t.learning_objective_refs == ()


def test_topic_rejects_negative_effort_and_index() -> None:
    with pytest.raises(ValueError):
        Topic.create("t1", "X", estimated_effort_minutes=-1)
    with pytest.raises(ValueError):
        Topic.create("t1", "X", sequence_index=-1)


def test_topic_rejects_duplicate_objective_refs() -> None:
    with pytest.raises(ValueError):
        Topic.create("t1", "X", learning_objective_refs=["o1", "o1"])


def test_topic_metadata_dict_and_unique_keys() -> None:
    t = Topic.create("t1", "X", metadata={"k": "v"})
    assert t.metadata == (("k", "v"),)
    with pytest.raises(ValueError):
        Topic.create("t1", "X", metadata=[("k", "a"), ("k", "b")])


def test_topic_string_difficulty() -> None:
    t = Topic.create("t1", "X", difficulty="advanced")
    assert t.difficulty is TopicDifficulty.ADVANCED


# ---------------------------------------------------------------------------
# Module / Subject
# ---------------------------------------------------------------------------


def test_module_ordered_topics_and_duplicate_reject() -> None:
    a = make_topic("a", module_id="m1", sequence_index=1)
    b = make_topic("b", module_id="m1", sequence_index=0)
    m = make_module("m1", [a, b], subject_id="s1")
    assert [t.id for t in m.ordered_topics()] == ["b", "a"]
    with pytest.raises(ValueError):
        make_module("m1", [a, a])


def test_module_topic_module_mismatch() -> None:
    t = make_topic("a", module_id="other")
    with pytest.raises(ValueError):
        make_module("m1", [t])


def test_module_with_topic() -> None:
    m = make_module("m1", [make_topic("a", module_id="m1")])
    m2 = m.with_topic(make_topic("b", module_id="m1"))
    assert len(m2.topics) == 2
    with pytest.raises(ValueError):
        m2.with_topic(make_topic("a", module_id="m1"))


def test_subject_all_topics_and_with_module() -> None:
    m1 = make_module(
        "m1",
        [make_topic("a", module_id="m1")],
        sequence_index=1,
        subject_id="s1",
    )
    m0 = make_module(
        "m0",
        [make_topic("z", module_id="m0")],
        sequence_index=0,
        subject_id="s1",
    )
    s = make_subject("s1", [m1, m0], curriculum_id="c1")
    assert [t.id for t in s.all_topics()] == ["z", "a"]
    s2 = s.with_module(
        make_module("m2", [make_topic("b", module_id="m2")], subject_id="s1")
    )
    assert len(s2.modules) == 3


def test_subject_duplicate_module_reject() -> None:
    m = make_module("m1", [], subject_id="s1")
    with pytest.raises(ValueError):
        make_subject("s1", [m, m])


# ---------------------------------------------------------------------------
# Dependency / Prerequisite / RevisionLink / LearningPath
# ---------------------------------------------------------------------------


def test_dependency_rejects_self_loop() -> None:
    with pytest.raises(ValueError):
        Dependency.create("d1", "a", "a", DependencyType.REQUIRES)


def test_dependency_string_type() -> None:
    d = Dependency.create("d1", "a", "b", "recommends")
    assert d.dependency_type is DependencyType.RECOMMENDS


def test_prerequisite_rejects_self() -> None:
    with pytest.raises(ValueError):
        Prerequisite.create("p1", "a", "a")


def test_prerequisite_as_dependency_id() -> None:
    p = Prerequisite.create("p1", "b", "a")
    assert p.as_dependency_id() == "prereq:p1"


def test_revision_link_canonical_order() -> None:
    link = RevisionLink.create("r1", "variance", "expectation")
    assert link.topic_a_id.value == "expectation"
    assert link.topic_b_id.value == "variance"
    assert link.involves("variance")
    assert link.other("expectation").value == "variance"
    with pytest.raises(ValueError):
        link.other("mgf")


def test_revision_link_self_loop_reject() -> None:
    with pytest.raises(ValueError):
        RevisionLink.create("r1", "a", "a")


def test_learning_path_next_previous_and_unique() -> None:
    path = LearningPath.create("p1", "Route", ["a", "b", "c"])
    assert path.length() == 3
    assert path.next_after("a").value == "b"
    assert path.previous_before("c").value == "b"
    assert path.next_after("c") is None
    assert path.previous_before("a") is None
    assert path.index_of("missing") is None
    with pytest.raises(ValueError):
        LearningPath.create("p1", "Route", ["a", "a"])


def test_learning_path_with_topic() -> None:
    path = LearningPath.create("p1", "Route", ["a"])
    path2 = path.with_topic("b")
    assert path2.topic_ids[-1].value == "b"
    with pytest.raises(ValueError):
        path2.with_topic("a")


# ---------------------------------------------------------------------------
# Curriculum aggregate
# ---------------------------------------------------------------------------


def test_curriculum_version_mismatch_reject() -> None:
    version = CurriculumVersion.create("other", "2026")
    with pytest.raises(ValueError):
        Curriculum.create("demo", "Demo", version)


def test_curriculum_version_schema_and_notes() -> None:
    with pytest.raises(ValueError):
        CurriculumVersion.create("c1", "2026", schema_version=0)
    v = CurriculumVersion.create("c1", "2026", notes="structural")
    assert v.notes == "structural"


def test_curriculum_duplicate_topic_across_modules() -> None:
    t = make_topic("a", module_id="m1")
    m1 = make_module("m1", [t], subject_id="s1")
    m2 = make_module(
        "m2", [make_topic("a", module_id="m2")], subject_id="s1"
    )
    s = make_subject("s1", [m1, m2], curriculum_id="c1")
    with pytest.raises(ValueError, match="duplicate topic"):
        make_curriculum("c1", subjects=[s])


def test_curriculum_prerequisite_unknown_topic() -> None:
    curr = linear_curriculum()
    with pytest.raises(ValueError, match="not in curriculum"):
        make_curriculum(
            curr.curriculum_id.value,
            subjects=list(curr.subjects),
            prerequisites=[Prerequisite.create("px", "ghost", "a")],
        )


def test_curriculum_get_topic_and_ordered_subjects() -> None:
    curr = linear_curriculum()
    assert curr.get_topic("b") is not None
    assert curr.get_topic("missing") is None
    assert len(curr.ordered_subjects()) == 1
    assert [t.value for t in curr.topic_ids()] == ["a", "b", "c"]


def test_curriculum_duplicate_revision_pair() -> None:
    topics = [
        make_topic("a", module_id="m1"),
        make_topic("b", module_id="m1", sequence_index=1),
    ]
    m = make_module("m1", topics, subject_id="s1")
    s = make_subject("s1", [m], curriculum_id="c1")
    links = [
        RevisionLink.create("r1", "a", "b"),
        RevisionLink.create("r2", "b", "a"),
    ]
    with pytest.raises(ValueError, match="duplicate revision"):
        make_curriculum("c1", subjects=[s], revision_links=links)


def test_curriculum_learning_path_topic_must_exist() -> None:
    curr = linear_curriculum()
    with pytest.raises(ValueError, match="learning path topic"):
        make_curriculum(
            "demo-curr",
            subjects=list(curr.subjects),
            learning_paths=[
                LearningPath.create("p", "X", ["a", "ghost"], curriculum_id="demo-curr")
            ],
        )


def test_empty_curriculum_ok() -> None:
    curr = make_curriculum("empty")
    assert curr.all_topics() == ()
