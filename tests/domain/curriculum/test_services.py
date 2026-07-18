"""Navigation, prerequisite, and revision service tests (V2-004)."""

from __future__ import annotations

import pytest

from app.domain.curriculum import (
    CurriculumNavigationService,
    Dependency,
    DependencyType,
    PrerequisiteService,
    RevisionPathService,
    TopicStatus,
)
from tests.domain.curriculum.helpers import (
    build_graph,
    diamond_curriculum,
    linear_curriculum,
    make_curriculum,
    make_module,
    make_subject,
    make_topic,
    revision_pair_curriculum,
)


def _nav(curr=None):
    curriculum = curr or linear_curriculum()
    return CurriculumNavigationService(curriculum, build_graph(curriculum))


# ---------------------------------------------------------------------------
# CurriculumNavigationService
# ---------------------------------------------------------------------------


def test_navigation_ordered_next_previous() -> None:
    nav = _nav()
    assert [t.value for t in nav.ordered_topics()] == ["a", "b", "c"]
    assert nav.next_topic("a").value == "b"
    assert nav.previous_topic("c").value == "b"
    assert nav.next_topic("c") is None
    assert nav.previous_topic("a") is None
    assert nav.next_topic("ghost") is None


def test_available_topics_respects_prerequisites() -> None:
    nav = _nav()
    assert [t.value for t in nav.available_topics(set())] == ["a"]
    assert [t.value for t in nav.available_topics({"a"})] == ["b"]
    assert [t.value for t in nav.available_topics({"a", "b"})] == ["c"]
    assert nav.available_topics({"a", "b", "c"}) == ()


def test_available_excludes_active() -> None:
    nav = _nav()
    assert nav.available_topics(set(), active={"a"}) == ()


def test_recommended_topics_boost() -> None:
    topics = [
        make_topic("a", module_id="m1", sequence_index=0),
        make_topic("b", module_id="m1", sequence_index=1),
        make_topic("c", module_id="m1", sequence_index=2),
    ]
    module = make_module("m1", topics, subject_id="s1")
    subject = make_subject("s1", [module], curriculum_id="rec")
    deps = [
        Dependency.create("d1", "b", "a", DependencyType.REQUIRES),
        Dependency.create("d2", "c", "a", DependencyType.REQUIRES),
        Dependency.create("d3", "c", "a", DependencyType.RECOMMENDS),
    ]
    curr = make_curriculum("rec", subjects=[subject], dependencies=deps)
    nav = CurriculumNavigationService(curr, build_graph(curr))
    # After completing a: b and c available; c is recommend-boosted
    rec = [t.value for t in nav.recommended_topics({"a"})]
    assert rec[0] == "c"
    assert "b" in rec
    limited = nav.recommended_topics({"a"}, limit=1)
    assert len(limited) == 1
    with pytest.raises(ValueError):
        nav.recommended_topics({"a"}, limit=-1)


def test_learning_path_navigation() -> None:
    nav = _nav()
    path = nav.learning_path("path-prob")
    assert path is not None
    assert nav.next_on_path("path-prob", "a").value == "b"
    assert nav.previous_on_path("path-prob", "b").value == "a"
    assert nav.learning_path("missing") is None
    assert nav.next_on_path("missing", "a") is None


def test_status_for_all_states() -> None:
    nav = _nav()
    assert nav.status_for("a", completed=set()) is TopicStatus.AVAILABLE
    assert nav.status_for("b", completed=set()) is TopicStatus.LOCKED
    assert (
        nav.status_for("a", completed=set(), active={"a"}) is TopicStatus.ACTIVE
    )
    assert (
        nav.status_for("a", completed={"a"}) is TopicStatus.COMPLETED
    )
    assert (
        nav.status_for("a", completed=set(), archived={"a"})
        is TopicStatus.ARCHIVED
    )


def test_topological_study_order() -> None:
    nav = _nav(diamond_curriculum())
    order = [t.value for t in nav.topological_study_order()]
    assert order[0] == "a"
    assert order[-1] == "d"


# ---------------------------------------------------------------------------
# PrerequisiteService
# ---------------------------------------------------------------------------


def test_prerequisite_evaluate_eligible() -> None:
    g = build_graph(linear_curriculum())
    svc = PrerequisiteService(g)
    ev = svc.evaluate("c", {"a", "b"})
    assert ev.is_eligible
    assert ev.missing == ()
    assert [t.value for t in ev.satisfied] == ["b"]


def test_prerequisite_evaluate_missing() -> None:
    g = build_graph(linear_curriculum())
    svc = PrerequisiteService(g)
    ev = svc.evaluate("c", {"a"})
    assert not ev.is_eligible
    assert [t.value for t in ev.missing] == ["b"]


def test_eligible_and_blocked_topics() -> None:
    g = build_graph(linear_curriculum())
    svc = PrerequisiteService(g)
    assert [t.value for t in svc.eligible_topics(set())] == ["a"]
    assert [t.value for t in svc.blocked_topics(set())] == ["b", "c"]
    assert [t.value for t in svc.eligible_topics({"a"})] == ["b"]
    assert svc.blocked_topics({"a", "b", "c"}) == ()


def test_missing_and_transitive_missing() -> None:
    g = build_graph(linear_curriculum())
    svc = PrerequisiteService(g)
    assert [t.value for t in svc.missing_prerequisites("c", set())] == ["b"]
    assert [t.value for t in svc.transitive_missing("c", set())] == ["a", "b"]
    assert svc.transitive_missing("c", {"a", "b"}) == ()


def test_prerequisite_unknown_topic() -> None:
    g = build_graph(linear_curriculum())
    with pytest.raises(ValueError):
        PrerequisiteService(g).evaluate("ghost", set())


def test_blockers_are_successors() -> None:
    g = build_graph(linear_curriculum())
    ev = PrerequisiteService(g).evaluate("a", set())
    assert [t.value for t in ev.blockers] == ["b"]


def test_diamond_eligibility() -> None:
    g = build_graph(diamond_curriculum())
    svc = PrerequisiteService(g)
    assert [t.value for t in svc.eligible_topics({"a"})] == ["b", "c"]
    assert not svc.evaluate("d", {"a", "b"}).is_eligible
    assert svc.evaluate("d", {"a", "b", "c"}).is_eligible


# ---------------------------------------------------------------------------
# RevisionPathService
# ---------------------------------------------------------------------------


def test_related_concepts() -> None:
    g = build_graph(revision_pair_curriculum())
    svc = RevisionPathService(g)
    related = [t.value for t in svc.related_concepts("expectation")]
    assert "variance" in related
    assert "mgf" in related
    rev_only = [
        t.value
        for t in svc.related_concepts("expectation", include_related=False)
    ]
    assert rev_only == ["variance"]


def test_revision_clusters() -> None:
    g = build_graph(revision_pair_curriculum())
    svc = RevisionPathService(g)
    clusters = svc.revision_clusters()
    # One cluster {expectation, variance}, one singleton {mgf}
    sizes = sorted(len(c) for c in clusters)
    assert sizes == [1, 2]
    pair = svc.cluster_for("expectation")
    assert {t.value for t in pair} == {"expectation", "variance"}


def test_recommended_review_sequence() -> None:
    g = build_graph(revision_pair_curriculum())
    svc = RevisionPathService(g)
    seq = [t.value for t in svc.recommended_review_sequence("variance")]
    assert set(seq) == {"expectation", "variance"}
    # With completion: incomplete first
    seq2 = [
        t.value
        for t in svc.recommended_review_sequence(
            "variance", completed={"expectation"}
        )
    ]
    assert seq2[0] == "variance"
    assert seq2[-1] == "expectation"


def test_cluster_for_unknown() -> None:
    g = build_graph(revision_pair_curriculum())
    with pytest.raises(ValueError):
        RevisionPathService(g).cluster_for("ghost")


def test_singleton_clusters_for_unlinked() -> None:
    curr = linear_curriculum()
    g = build_graph(curr)
    clusters = RevisionPathService(g).revision_clusters()
    assert len(clusters) == 3
    assert all(len(c) == 1 for c in clusters)
