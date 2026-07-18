"""Regression and malformed-structure coverage for Curriculum Ingestion."""

from __future__ import annotations

import pytest

from app.application.curriculum_ingestion.dto.ingestion_request import (
    DocumentPayload,
    IngestionRequest,
)
from app.application.curriculum_ingestion.exceptions import IllegalState
from app.domain.curriculum_ingestion.ingestion_state import IngestionState
from tests.application.curriculum_ingestion.helpers import (
    entry,
    make_engine,
    make_request,
    syllabus_payload,
)


def test_empty_entries_document_fails_validation():
    payload = DocumentPayload(
        document_id="empty",
        source_ref="s3://x",
        title="Syllabus Empty",
        declared_kind="syllabus",
        entries=(),
        metadata=(("subject_code", "CS1"),),
    )
    snap = make_engine().ingest(
        IngestionRequest(job_id="empty", documents=(payload,), require_pass=False)
    )
    assert not snap.passed
    assert snap.state == IngestionState.FAILED.value


def test_unknown_section_parent_on_topic():
    payload = DocumentPayload(
        document_id="orphan-section",
        source_ref="s3://x",
        title="Syllabus",
        declared_kind="syllabus",
        metadata=(("subject_code", "CS1"),),
        entries=(
            entry("t1", "topic", "Orphan", number="1.1", parent_ref="missing-section"),
            entry("o1", "objective", "Obj", number="1", parent_ref="t1"),
        ),
    )
    snap = make_engine().ingest(
        IngestionRequest(job_id="orphan", documents=(payload,), require_pass=False)
    )
    codes = {i.code for i in snap.validation.issues}
    assert "unknown_section" in codes


def test_duplicate_topic_titles_fail():
    payload = DocumentPayload(
        document_id="dup",
        source_ref="s3://x",
        title="Syllabus",
        declared_kind="syllabus",
        metadata=(("subject_code", "CS1"),),
        entries=(
            entry("s1", "section", "Ch1", number="1"),
            entry("t1", "topic", "Same Title", number="1.1", parent_ref="s1"),
            entry("t2", "topic", "Same Title", number="1.2", parent_ref="s1"),
            entry("o1", "objective", "A", number="1", parent_ref="t1"),
            entry("o2", "objective", "B", number="1", parent_ref="t2"),
        ),
    )
    snap = make_engine().ingest(
        IngestionRequest(job_id="dup", documents=(payload,), require_pass=False)
    )
    assert any(i.code == "duplicate_topic" for i in snap.validation.issues)


def test_self_prerequisite_malformed():
    payload = DocumentPayload(
        document_id="self",
        source_ref="s3://x",
        title="Syllabus",
        declared_kind="syllabus",
        metadata=(("subject_code", "CS1"),),
        entries=(
            entry("s1", "section", "Ch1", number="1"),
            entry(
                "t1",
                "topic",
                "Loop",
                number="1.1",
                parent_ref="s1",
                attributes=(("prerequisites", "t1"),),
            ),
            entry("o1", "objective", "A", number="1", parent_ref="t1"),
        ),
    )
    snap = make_engine().ingest(
        IngestionRequest(job_id="self", documents=(payload,), require_pass=False)
    )
    assert any(i.code == "malformed_hierarchy" for i in snap.validation.issues)


def test_run_job_rejects_non_received():
    engine = make_engine()
    job = engine.create_job(make_request())
    job = engine.run_job(job)
    with pytest.raises(IllegalState):
        engine.run_job(job)


def test_completed_snapshot_has_package():
    snap = make_engine().ingest(make_request())
    assert snap.state == "completed"
    assert snap.package is not None
    assert snap.package.section_ids
    assert snap.package.topic_ids
    assert snap.package.objective_ids


def test_no_sessions_missions_activities_in_output():
    snap = make_engine().ingest(make_request())
    blob = repr(snap)
    assert "session_id" not in blob
    assert "mission_id" not in blob
    assert "activity_id" not in blob


@pytest.mark.parametrize(
    "entry_type",
    ["section", "topic", "objective", "prerequisite", "metadata", "formula", "note"],
)
def test_all_entry_types_accepted_in_payload(entry_type):
    payload = DocumentPayload(
        document_id=f"doc-{entry_type}",
        source_ref="s3://x",
        title="Syllabus Mixed",
        declared_kind="syllabus",
        metadata=(("subject_code", "CS1"),),
        entries=(
            entry("s1", "section", "Ch1", number="1"),
            entry("t1", "topic", "T", number="1.1", parent_ref="s1"),
            entry("o1", "objective", "O", number="1", parent_ref="t1"),
            entry("x1", entry_type, "Extra distinct", number="9", parent_ref="t1"),
        ),
    )
    snap = make_engine().ingest(
        make_request(
            job_id=f"et-{entry_type}",
            documents=(payload,),
            require_pass=False,
        )
    )
    assert snap.normalization is not None


@pytest.mark.parametrize("n", range(10))
def test_regression_happy_path_stable(n):
    snap = make_engine().ingest(make_request(job_id="stable"))
    assert snap.passed
    assert snap.extraction.section_count == 1
    assert snap.normalization.topic_count == 1
    assert snap.validation.passed
    assert n >= 0


@pytest.mark.parametrize(
    "source_ref",
    [
        "s3://bucket/a.json",
        "file://local/syllabus.json",
        "curriculum://cs1/2026.1/syllabus",
        "ref:asset-123",
    ],
)
def test_abstract_source_refs_accepted(source_ref):
    payload = syllabus_payload()
    payload = DocumentPayload(
        document_id=payload.document_id,
        source_ref=source_ref,
        title=payload.title,
        entries=payload.entries,
        declared_kind=payload.declared_kind,
        metadata=payload.metadata,
    )
    snap = make_engine().ingest(
        make_request(job_id="src", documents=(payload,))
    )
    assert snap.package.document_refs[0][1] == source_ref
