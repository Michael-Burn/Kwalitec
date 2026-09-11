"""Prove OEA write/read share the durable SessionDocumentStore path.

Mirrors Twin and Spacing durability wiring: tagged Assessment Evidence must
land in ``v2_aggregate_documents`` when durable store is ON, and a fresh
store construction (restart simulation) must see the same rows.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import (
    NS_OEA_ASSESSMENT_EVIDENCE,
    discard_objective_assessment_evidence_store_for_tests,
    get_objective_assessment_evidence_store,
    reset_objective_assessment_evidence_store,
)
from app.extensions import db
from app.infrastructure.composition import (
    build_objective_assessment_evidence_store,
    build_session_document_store,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.models.v2_aggregate import V2AggregateDocument


def _sample_record(*, evidence_id: str) -> AssessmentEvidenceRecord:
    return AssessmentEvidenceRecord(
        evidence_id=evidence_id,
        student_id="4244",
        objective_id="CS1-B-T01-LO04",
        item_id="kc-durable-oea-1",
        package_id="CS1-EP001-PKG-OEA-DURABLE",
        session_id="lsr-oea-durable",
        response_type="mcq",
        scored_correct=True,
        occurred_at=datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
        source="package_activity_engine",
        selected_misconception_tag="",
    )


def test_oea_append_survives_restart_via_sql(ctx, monkeypatch) -> None:
    """Write via canonical store; read after discarding the process singleton."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    discard_objective_assessment_evidence_store_for_tests()

    eid = "oae-durable-restart-1"
    writer = get_objective_assessment_evidence_store()
    stored = writer.append(_sample_record(evidence_id=eid))
    assert stored.evidence_id == eid

    rows = (
        db.session.query(V2AggregateDocument)
        .filter_by(aggregate_name="LearningSessionDocument")
        .all()
    )
    oea_rows = [
        r
        for r in rows
        if NS_OEA_ASSESSMENT_EVIDENCE in (r.aggregate_id or "")
        and eid in (r.aggregate_id or "")
    ]
    assert oea_rows, (
        "expected durable OEA row in v2_aggregate_documents; "
        f"found aggregate_ids={[r.aggregate_id for r in rows]}"
    )

    # Simulate process restart: drop singleton, keep SQL rows.
    discard_objective_assessment_evidence_store_for_tests()
    del writer

    fresh = get_objective_assessment_evidence_store()
    restored = fresh.get(eid)
    assert restored is not None
    assert restored.student_id == "4244"
    assert restored.objective_id == "CS1-B-T01-LO04"
    assert restored.item_id == "kc-durable-oea-1"
    assert restored.scored_correct is True
    assert restored.package_id == "CS1-EP001-PKG-OEA-DURABLE"

    independent = build_objective_assessment_evidence_store()
    again = independent.get(eid)
    assert again is not None
    assert again.session_id == "lsr-oea-durable"


def test_bare_in_memory_oea_store_isolates_when_explicit(
    ctx, monkeypatch
) -> None:
    """Explicit bare SessionDocumentStore must not see durable SQL rows."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    discard_objective_assessment_evidence_store_for_tests()

    eid = "oae-durable-isolate-1"
    get_objective_assessment_evidence_store().append(
        _sample_record(evidence_id=eid)
    )

    bare = build_objective_assessment_evidence_store(
        document_store=SessionDocumentStore()
    )
    assert bare.get(eid) is None


def test_reset_drops_singleton_without_wiping_sql(ctx, monkeypatch) -> None:
    """reset_… in durable mode drops singleton only; SQL rows remain."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    discard_objective_assessment_evidence_store_for_tests()

    eid = "oae-durable-reset-1"
    get_objective_assessment_evidence_store().append(
        _sample_record(evidence_id=eid)
    )
    reset_objective_assessment_evidence_store()

    # Fresh construction after reset still sees SQL.
    restored = get_objective_assessment_evidence_store().get(eid)
    assert restored is not None
    assert restored.evidence_id == eid


def test_oea_clear_does_not_wipe_other_namespaces(ctx, monkeypatch) -> None:
    """OEA clear must not delete Twin / session documents on the shared store."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    discard_objective_assessment_evidence_store_for_tests()

    shared = build_session_document_store()
    shared.save("sdt.daily_loop_twin", "999::CS1", {"learner_id": "999"})
    oea = build_objective_assessment_evidence_store(document_store=shared)
    oea.append(_sample_record(evidence_id="oae-clear-ns-1"))
    assert oea.count() == 1

    oea.clear()
    assert oea.count() == 0
    assert shared.get("sdt.daily_loop_twin", "999::CS1") is not None
