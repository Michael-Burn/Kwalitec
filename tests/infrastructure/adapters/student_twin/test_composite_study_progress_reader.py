"""Canonical Study Progress ownership via CompositeStudyProgressReader."""

from __future__ import annotations

from types import SimpleNamespace

from app.infrastructure.adapters.student_twin.query_adapter import (
    CompositeStudyProgressReader,
)


class _FakeCanonical:
    def orm_topic_id_for_published(
        self, topic_id: str, *, subject_code: str, topics
    ) -> int | None:
        mapping = {t.code: t.id for t in topics}
        return mapping.get(topic_id)


def test_runtime_c_enrolment_ignores_stage_a_topic_progress():
    """With Runtime C enrolment, Stage A completed rows are historical only."""
    stage_a_hits: list[str] = []

    def runtime_completed(user_id: int, subject_code: str):
        return frozenset()  # enrolled but no progressed topics yet

    def runtime_enrolled(user_id: int, subject_code: str) -> bool:
        return True

    reader = CompositeStudyProgressReader(
        canonical=_FakeCanonical(),
        runtime_completed=runtime_completed,
        runtime_enrolled=runtime_enrolled,
        orm_topics_loader=lambda _code: (
            SimpleNamespace(id=101, code="t1"),
        ),
    )

    # Monkey-patch Stage A path to prove it is not consulted when enrolled.
    original = reader._topic_progress_completed

    def tracking_stage_a(**kwargs):
        stage_a_hits.append(kwargs.get("topic_id") or "")
        return original(**kwargs)

    reader._topic_progress_completed = tracking_stage_a  # type: ignore[method-assign]

    assert not reader.topic_covered(
        user_id=1, subject_code="CS1", topic_id="t1"
    )
    assert stage_a_hits == []


def test_runtime_c_progressed_topics_are_sole_authority_when_enrolled():
    reader = CompositeStudyProgressReader(
        canonical=_FakeCanonical(),
        runtime_completed=lambda _u, _s: frozenset({"t1"}),
        runtime_enrolled=lambda _u, _s: True,
        orm_topics_loader=lambda _code: (
            SimpleNamespace(id=101, code="t1"),
        ),
    )
    assert reader.topic_covered(user_id=1, subject_code="CS1", topic_id="t1")
    assert not reader.topic_covered(
        user_id=1, subject_code="CS1", topic_id="t2"
    )


def test_stage_a_legacy_fallback_only_without_runtime_c_enrolment(monkeypatch):
    """No Runtime C enrolment: Stage A TopicProgress remains the legacy reader."""
    reader = CompositeStudyProgressReader(
        canonical=_FakeCanonical(),
        runtime_completed=lambda _u, _s: frozenset({"should-not-use"}),
        runtime_enrolled=lambda _u, _s: False,
        orm_topics_loader=lambda _code: (
            SimpleNamespace(id=101, code="t1"),
        ),
    )

    class _Row:
        completed = True

    class _Query:
        def filter_by(self, **_kwargs):
            return self

        def first(self):
            return _Row()

    monkeypatch.setattr(
        "app.infrastructure.adapters.student_twin.query_adapter.TopicProgress",
        SimpleNamespace(query=_Query()),
    )

    assert reader.topic_covered(user_id=1, subject_code="CS1", topic_id="t1")
