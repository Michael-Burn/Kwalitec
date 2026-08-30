"""CanonicalTopicId artefact/import join tests (ADR-027 Phase 2 Stage 1)."""

from __future__ import annotations

from types import SimpleNamespace

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
    ProgressModelSnapshot,
)
from app.application.student_twin.canonical_topic_id import CanonicalTopicId


class _FakeFoundation:
    def __init__(self, snapshot: EducationalArtefactSnapshot | None) -> None:
        self._snapshot = snapshot

    def derive_active(self, subject_code: str):
        return self._snapshot


def _cs1_artefacts() -> EducationalArtefactSnapshot:
    topics = (
        {
            "topic_id": "CS1-A-T01",
            "code": "1.1",
            "title": "Statistical distributions",
        },
        {
            "topic_id": "CS1-A-T02",
            "code": "1.2",
            "title": "Moments",
        },
    )
    return EducationalArtefactSnapshot(
        curriculum_identity="ifoa:cs1:2026",
        subject_code="CS1",
        version_label="2026",
        topics=topics,
        progress_model=ProgressModelSnapshot(
            curriculum_identity="ifoa:cs1:2026",
            topic_ids=("CS1-A-T01", "CS1-A-T02"),
            topics=(
                {"topic_id": "CS1-A-T01", "topic_code": "1.1"},
                {"topic_id": "CS1-A-T02", "topic_code": "1.2"},
            ),
        ),
    )


def test_resolve_from_runtime_published_id():
    helper = CanonicalTopicId(foundation=_FakeFoundation(_cs1_artefacts()))
    assert (
        helper.resolve_from_runtime_topic_id("CS1-A-T01", subject_code="CS1")
        == "CS1-A-T01"
    )


def test_resolve_from_runtime_topic_code():
    helper = CanonicalTopicId(foundation=_FakeFoundation(_cs1_artefacts()))
    assert (
        helper.resolve_from_runtime_topic_id("1.1", subject_code="CS1")
        == "CS1-A-T01"
    )


def test_reject_blank_node_and_pure_int():
    helper = CanonicalTopicId(foundation=_FakeFoundation(_cs1_artefacts()))
    assert helper.resolve_from_runtime_topic_id("", subject_code="CS1") is None
    assert (
        helper.resolve_from_runtime_topic_id("node-abc", subject_code="CS1")
        is None
    )
    assert helper.resolve_from_runtime_topic_id("42", subject_code="CS1") is None
    assert CanonicalTopicId.is_hygienic_twin_key("CS1-A-T01")
    assert not CanonicalTopicId.is_hygienic_twin_key("node-x")
    assert not CanonicalTopicId.is_hygienic_twin_key("7")
    assert not CanonicalTopicId.is_hygienic_twin_key("")


def test_resolve_from_orm_topic_title_join():
    helper = CanonicalTopicId(foundation=_FakeFoundation(_cs1_artefacts()))
    topic = SimpleNamespace(name="Statistical distributions", id=101)
    assert (
        helper.resolve_from_orm_topic(topic, subject_code="CS1") == "CS1-A-T01"
    )


def test_resolve_from_orm_topic_miss_returns_none():
    helper = CanonicalTopicId(foundation=_FakeFoundation(_cs1_artefacts()))
    topic = SimpleNamespace(name="Unknown title", id=999)
    assert helper.resolve_from_orm_topic(topic, subject_code="CS1") is None


def test_missing_artefacts_fail_closed():
    helper = CanonicalTopicId(foundation=_FakeFoundation(None))
    assert (
        helper.resolve_from_runtime_topic_id("CS1-A-T01", subject_code="CS1")
        is None
    )
    topic = SimpleNamespace(name="Statistical distributions", id=1)
    assert helper.resolve_from_orm_topic(topic, subject_code="CS1") is None


def test_orm_topic_id_for_published_reverse_join():
    helper = CanonicalTopicId(foundation=_FakeFoundation(_cs1_artefacts()))
    topics = (
        SimpleNamespace(name="Moments", id=2),
        SimpleNamespace(name="Statistical distributions", id=1),
    )
    assert (
        helper.orm_topic_id_for_published(
            "CS1-A-T01", subject_code="CS1", topics=topics
        )
        == 1
    )
