"""Prove Twin write/read share the durable SessionDocumentStore path.

Regression for the two-layer defect:
1. Writes must land in ``v2_aggregate_documents`` when durable store is ON.
2. Policy V1's real reader (``DailyLoopLearnerTwinQueryAdapter`` /
   ``learner_twin_query``) must see that evidence via a *fresh* store
   construction (restart simulation), not a separate empty in-memory map.
"""

from __future__ import annotations

from app.application.student_twin.daily_loop_codec import encode_daily_loop_twin
from app.application.student_twin.query import MapStudyProgress
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.extensions import db
from app.infrastructure.adapters.student_twin.cutover_bridge import (
    learner_twin_query,
)
from app.infrastructure.adapters.student_twin.daily_loop_persistence import (
    DailyLoopTwinPersistence,
)
from app.infrastructure.adapters.student_twin.query_adapter import (
    DailyLoopLearnerTwinQueryAdapter,
)
from app.infrastructure.composition import build_session_document_store
from app.models.v2_aggregate import V2AggregateDocument
from tests.application.student_twin.helpers import make_engine, success_events


def _seed_document(*, user_id: int, subject_code: str, topic_id: str) -> dict:
    engine = make_engine()
    twin = engine.create_twin(
        str(user_id),
        twin_id=f"twin-durable-{user_id}-{subject_code}",
        subject_code=subject_code,
    )
    twin = engine.ingest_many(
        twin,
        success_events(3, topic_id=topic_id, prefix="dur"),
    )
    return encode_daily_loop_twin(twin)


def test_write_path_and_policy_v1_read_path_share_durable_store(
    ctx, monkeypatch
) -> None:
    """Write via composition store; read via default Policy V1 factory after restart."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")

    user_id = 4242
    subject_code = "CS1"
    topic_id = "CS1-A-T01"
    document = _seed_document(
        user_id=user_id, subject_code=subject_code, topic_id=topic_id
    )

    # Layer 1 / write path: same factory session composition uses.
    write_store = build_session_document_store()
    writer = DailyLoopTwinPersistence(store=write_store)
    writer.save_twin(
        learner_id=str(user_id),
        subject_code=subject_code,
        document=document,
    )

    rows = (
        db.session.query(V2AggregateDocument)
        .filter_by(aggregate_name="LearningSessionDocument")
        .all()
    )
    twin_rows = [
        r
        for r in rows
        if "sdt.daily_loop_twin" in (r.aggregate_id or "")
        and str(user_id) in (r.aggregate_id or "")
    ]
    assert twin_rows, (
        "expected durable Twin row in v2_aggregate_documents; "
        f"found aggregate_ids={[r.aggregate_id for r in rows]}"
    )

    # Simulate process restart: discard write_store, build fresh readers.
    del write_store
    del writer

    # Layer 2 / Policy V1 read path: default adapter construction + factory.
    fresh_adapter = DailyLoopLearnerTwinQueryAdapter(
        study_progress=MapStudyProgress(),
        engine=StudentTwinEngine(),
    )
    fact = fresh_adapter.topic_knowledge(
        user_id=user_id, subject_code=subject_code, topic_id=topic_id
    )
    assert fact.has_estimated_knowledge is True
    assert fact.evidence_count == 3

    factory_adapter = learner_twin_query()
    factory_fact = factory_adapter.topic_knowledge(
        user_id=user_id, subject_code=subject_code, topic_id=topic_id
    )
    assert factory_fact.has_estimated_knowledge is True
    assert factory_fact.evidence_count == 3


def test_bare_in_memory_store_still_isolates_when_durable_off(
    ctx, monkeypatch
) -> None:
    """With durable OFF, a bare SessionDocumentStore must not see durable rows."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "0")

    from app.infrastructure.session.store import SessionDocumentStore

    user_id = 5151
    subject_code = "CS1"
    topic_id = "CS1-A-T01"
    document = _seed_document(
        user_id=user_id, subject_code=subject_code, topic_id=topic_id
    )

    # Opt into durable only for the write side of this isolation proof.
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    durable = DailyLoopTwinPersistence(store=build_session_document_store())
    durable.save_twin(
        learner_id=str(user_id),
        subject_code=subject_code,
        document=document,
    )

    # Explicit bare memory store (the old default) must miss durable data.
    bare = DailyLoopTwinPersistence(store=SessionDocumentStore())
    assert (
        bare.load_twin(learner_id=str(user_id), subject_code=subject_code)
        is None
    )
