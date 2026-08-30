"""LearnerTwinQueryPort adapter tests (ADR-027 Phase 2 Stage 1)."""

from __future__ import annotations

from app.application.student_twin.daily_loop_codec import encode_daily_loop_twin
from app.application.student_twin.query import MapStudyProgress
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.domain.student_twin.evidence_type import EvidenceType
from app.infrastructure.adapters.student_twin.query_adapter import (
    DailyLoopLearnerTwinQueryAdapter,
)
from tests.application.student_twin.helpers import make_engine, success_events
from tests.domain.student_twin.helpers import make_event


class _FakePersistence:
    def __init__(self, documents: dict | None = None) -> None:
        self._documents = documents or {}

    def load_twin(self, *, learner_id: str, subject_code: str | None = None):
        subject = (subject_code or "").strip()
        if subject:
            keyed = self._documents.get(f"{learner_id}::{subject}")
            if keyed is not None:
                return keyed
        return self._documents.get(learner_id)


def _seeded_document(
    *,
    user_id: int = 42,
    subject_code: str = "CS1",
    topic_id: str = "CS1-A-T01",
    with_evidence: bool = True,
) -> dict:
    engine = make_engine()
    twin = engine.create_twin(
        str(user_id),
        twin_id=f"twin-dl-{user_id}-{subject_code}",
        subject_code=subject_code,
    )
    if with_evidence:
        twin = engine.ingest_many(
            twin,
            success_events(3, topic_id=topic_id, prefix="ek"),
        )
    return encode_daily_loop_twin(twin)


def test_empty_twin_returns_honest_absence():
    adapter = DailyLoopLearnerTwinQueryAdapter(
        persistence=_FakePersistence(),
        study_progress=MapStudyProgress(),
    )
    snap = adapter.knowledge_snapshot(user_id=7, subject_code="CS1")
    assert snap.overall_estimated_knowledge is None
    assert snap.topics == ()
    fact = adapter.topic_knowledge(
        user_id=7, subject_code="CS1", topic_id="CS1-A-T01"
    )
    assert fact.has_estimated_knowledge is False
    assert fact.estimated_knowledge is None
    assert fact.estimated_mastery is None
    assert fact.evidence_count == 0


def test_topic_with_twin_evidence_has_estimated_knowledge():
    doc = _seeded_document(with_evidence=True)
    adapter = DailyLoopLearnerTwinQueryAdapter(
        persistence=_FakePersistence({"42::CS1": doc}),
        study_progress=MapStudyProgress(),
        engine=StudentTwinEngine(),
    )
    fact = adapter.topic_knowledge(
        user_id=42, subject_code="CS1", topic_id="CS1-A-T01"
    )
    assert fact.has_estimated_knowledge is True
    assert fact.estimated_knowledge is not None
    assert 0.0 <= fact.estimated_knowledge <= 1.0
    assert fact.evidence_count == 3
    assert fact.last_practised_at is not None

    with_ek = adapter.topics_with_estimated_knowledge(
        user_id=42, subject_code="CS1"
    )
    assert len(with_ek) == 1
    assert with_ek[0].topic_id == "CS1-A-T01"


def test_study_progress_complete_without_twin_evidence_is_not_ek():
    """Acceptance: covered Study Progress must not mint Estimated Knowledge."""
    doc = _seeded_document(with_evidence=False)
    adapter = DailyLoopLearnerTwinQueryAdapter(
        persistence=_FakePersistence({"99::CS1": doc}),
        study_progress=MapStudyProgress({"CS1-A-T01"}),
        engine=StudentTwinEngine(),
    )
    fact = adapter.topic_knowledge(
        user_id=99, subject_code="CS1", topic_id="CS1-A-T01"
    )
    assert adapter.topic_covered(
        user_id=99, subject_code="CS1", topic_id="CS1-A-T01"
    )
    assert fact.has_estimated_knowledge is False
    assert fact.estimated_knowledge is None
    assert fact.evidence_count == 0


def test_topic_without_progress_and_without_evidence():
    adapter = DailyLoopLearnerTwinQueryAdapter(
        persistence=_FakePersistence(),
        study_progress=MapStudyProgress(),
    )
    assert not adapter.topic_covered(
        user_id=1, subject_code="CS1", topic_id="CS1-A-T01"
    )
    fact = adapter.topic_knowledge(
        user_id=1, subject_code="CS1", topic_id="CS1-A-T01"
    )
    assert fact.has_estimated_knowledge is False


def test_snapshot_lists_only_topics_with_records():
    engine = make_engine()
    twin = engine.create_twin("5", twin_id="twin-5", subject_code="CS1")
    twin = engine.ingest_evidence(
        twin,
        make_event(
            "e-a",
            EvidenceType.PRACTICE_RESULT,
            day=1,
            topic_id="CS1-A-T01",
            outcome="success",
            score=0.9,
        ),
    )
    twin = engine.ingest_evidence(
        twin,
        make_event(
            "e-b",
            EvidenceType.PRACTICE_RESULT,
            day=2,
            topic_id="CS1-A-T02",
            outcome="fail",
            score=0.2,
        ),
    )
    doc = encode_daily_loop_twin(twin)
    adapter = DailyLoopLearnerTwinQueryAdapter(
        persistence=_FakePersistence({"5::CS1": doc}),
        study_progress=MapStudyProgress(),
        engine=StudentTwinEngine(),
    )
    snap = adapter.knowledge_snapshot(user_id=5, subject_code="CS1")
    ids = {f.topic_id for f in snap.topics}
    assert ids == {"CS1-A-T01", "CS1-A-T02"}
    assert snap.overall_estimated_knowledge is not None
