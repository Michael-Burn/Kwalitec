"""Domain entity tests for Curriculum Ingestion."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.domain.curriculum_ingestion.curriculum_document import (
    DocumentEntryType,
    DocumentKind,
    resolve_document_kind,
    resolve_entry_type,
)
from app.domain.curriculum_ingestion.ingestion_report import (
    IngestionIssueCode,
    IngestionIssueSeverity,
)
from app.domain.curriculum_ingestion.ingestion_state import (
    IngestionState,
    IngestionTransitionEvent,
    has_reached,
    is_failure_state,
    is_terminal_ingestion_state,
    next_ingestion_state,
    pipeline_index,
    resolve_ingestion_state,
)
from tests.domain.curriculum_ingestion.helpers import (
    make_document,
    make_entry,
    make_extraction,
    make_issue,
    make_job,
    make_normalized,
    make_objective,
    make_report,
    make_section,
    make_topic,
)


@pytest.mark.parametrize(
    "kind",
    [
        DocumentKind.CMP,
        DocumentKind.SYLLABUS,
        DocumentKind.LEARNING_OBJECTIVES,
        DocumentKind.FORMULA_SHEET,
        DocumentKind.SUPPORTING_DOCUMENT,
        DocumentKind.UNKNOWN,
    ],
)
def test_document_kind_roundtrip(kind):
    assert resolve_document_kind(kind.value) is kind
    assert resolve_document_kind(kind) is kind


@pytest.mark.parametrize(
    "alias,expected",
    [
        ("objectives", DocumentKind.LEARNING_OBJECTIVES),
        ("lo", DocumentKind.LEARNING_OBJECTIVES),
        ("formula", DocumentKind.FORMULA_SHEET),
        ("supporting", DocumentKind.SUPPORTING_DOCUMENT),
        ("core_maths_pack", DocumentKind.CMP),
    ],
)
def test_document_kind_aliases(alias, expected):
    assert resolve_document_kind(alias) is expected


@pytest.mark.parametrize("bad", ["", "nope", "pdf", "mission"])
def test_document_kind_rejects_unknown(bad):
    with pytest.raises(ValueError):
        resolve_document_kind(bad)


@pytest.mark.parametrize("etype", list(DocumentEntryType))
def test_entry_type_roundtrip(etype):
    assert resolve_entry_type(etype.value) is etype


@pytest.mark.parametrize(
    "alias,expected",
    [
        ("chapter", DocumentEntryType.SECTION),
        ("lo", DocumentEntryType.OBJECTIVE),
        ("prereq", DocumentEntryType.PREREQUISITE),
        ("meta", DocumentEntryType.METADATA),
    ],
)
def test_entry_type_aliases(alias, expected):
    assert resolve_entry_type(alias) is expected


def test_document_create_defaults():
    doc = make_document()
    assert doc.document_id == "doc-1"
    assert doc.entry_count == 3
    assert doc.declared_kind is DocumentKind.SYLLABUS
    assert doc.metadata_value("subject_code") == "CS1"


def test_document_rejects_empty_id():
    with pytest.raises(ValueError, match="document_id"):
        make_document(document_id="  ")


def test_document_rejects_data_uri():
    from app.domain.curriculum_ingestion.curriculum_document import CurriculumDocument

    with pytest.raises(ValueError, match="data URI"):
        CurriculumDocument.create("d1", "data:application/pdf;base64,aaa", "T")


def test_document_rejects_pdf_marker():
    from app.domain.curriculum_ingestion.curriculum_document import CurriculumDocument

    with pytest.raises(ValueError, match="PDF"):
        CurriculumDocument.create("d1", "%PDF-1.4", "T")


def test_document_rejects_duplicate_entries():
    from app.domain.curriculum_ingestion.curriculum_document import CurriculumDocument

    e = make_entry("e1")
    with pytest.raises(ValueError, match="duplicate"):
        CurriculumDocument.create(
            "d1", "s3://x", "T", entries=[e, make_entry("e1", text="Other")]
        )


def test_document_frozen():
    doc = make_document()
    with pytest.raises(FrozenInstanceError):
        doc.title = "X"  # type: ignore[misc]


def test_entry_attribute_lookup():
    entry = make_entry(attributes=(("Topic_Ref", "t9"),))
    assert entry.attribute("topic_ref") == "t9"
    assert entry.attribute("missing", "d") == "d"


def test_entries_of_type():
    doc = make_document()
    assert len(doc.entries_of_type(DocumentEntryType.TOPIC)) == 1
    assert len(doc.entries_of_type("objective")) == 1


@pytest.mark.parametrize("state", list(IngestionState))
def test_resolve_ingestion_state(state):
    assert resolve_ingestion_state(state.value) is state


@pytest.mark.parametrize(
    "event,start,end",
    [
        (
            IngestionTransitionEvent.MARK_CLASSIFIED,
            IngestionState.RECEIVED,
            IngestionState.CLASSIFIED,
        ),
        (
            IngestionTransitionEvent.MARK_EXTRACTED,
            IngestionState.CLASSIFIED,
            IngestionState.EXTRACTED,
        ),
        (
            IngestionTransitionEvent.MARK_NORMALIZED,
            IngestionState.EXTRACTED,
            IngestionState.NORMALIZED,
        ),
        (
            IngestionTransitionEvent.MARK_VALIDATED,
            IngestionState.NORMALIZED,
            IngestionState.VALIDATED,
        ),
        (
            IngestionTransitionEvent.MARK_PREVIEW_READY,
            IngestionState.VALIDATED,
            IngestionState.PREVIEW_READY,
        ),
        (
            IngestionTransitionEvent.MARK_COMPLETED,
            IngestionState.PREVIEW_READY,
            IngestionState.COMPLETED,
        ),
        (
            IngestionTransitionEvent.MARK_FAILED,
            IngestionState.RECEIVED,
            IngestionState.FAILED,
        ),
        (
            IngestionTransitionEvent.RESET_TO_RECEIVED,
            IngestionState.FAILED,
            IngestionState.RECEIVED,
        ),
    ],
)
def test_lawful_transitions(event, start, end):
    assert next_ingestion_state(start, event) is end


@pytest.mark.parametrize(
    "event,start",
    [
        (IngestionTransitionEvent.MARK_EXTRACTED, IngestionState.RECEIVED),
        (IngestionTransitionEvent.MARK_COMPLETED, IngestionState.VALIDATED),
        (IngestionTransitionEvent.MARK_CLASSIFIED, IngestionState.COMPLETED),
    ],
)
def test_illegal_transitions(event, start):
    with pytest.raises(ValueError, match="Illegal"):
        next_ingestion_state(start, event)


def test_pipeline_index_and_has_reached():
    assert pipeline_index(IngestionState.RECEIVED) == 0
    assert pipeline_index(IngestionState.FAILED) == -1
    assert has_reached(IngestionState.VALIDATED, IngestionState.EXTRACTED)
    assert not has_reached(IngestionState.EXTRACTED, IngestionState.VALIDATED)
    assert is_terminal_ingestion_state(IngestionState.COMPLETED)
    assert is_failure_state(IngestionState.FAILED)


def test_job_lifecycle_helpers():
    job = make_job()
    assert job.state is IngestionState.RECEIVED
    kinds = (("doc-1", DocumentKind.SYLLABUS),)
    job = job.with_classification(kinds)
    assert job.state is IngestionState.CLASSIFIED
    extraction = make_extraction()
    job = job.with_extraction(extraction)
    assert job.state is IngestionState.EXTRACTED
    normalization = make_normalized()
    job = job.with_normalization(normalization)
    assert job.state is IngestionState.NORMALIZED
    report = make_report()
    job = job.with_report(report)
    assert job.state is IngestionState.VALIDATED
    job = job.mark_preview_ready().mark_completed()
    assert job.state is IngestionState.COMPLETED


def test_job_rejects_empty_documents():
    from app.domain.curriculum_ingestion.ingestion_job import IngestionJob

    with pytest.raises(ValueError, match="documents"):
        IngestionJob.create("j1", [])


def test_job_mark_failed():
    job = make_job().mark_failed("boom")
    assert job.state is IngestionState.FAILED
    assert job.failure_reason == "boom"


def test_extraction_result_counts():
    result = make_extraction()
    assert result.section_count == 1
    assert result.topic_count == 1
    assert result.objective_count == 1


def test_normalization_lookups():
    result = make_normalized()
    assert result.topic_by_id("topic-probability") is not None
    assert result.section_by_id("missing") is None


def test_report_passed_without_issues():
    report = make_report()
    assert report.passed
    assert not report.blocks_ingestion


def test_report_blocks_on_error():
    report = make_report(issues=[make_issue()])
    assert not report.passed
    assert report.blocking_issues


@pytest.mark.parametrize("code", list(IngestionIssueCode))
def test_issue_codes_constructible(code):
    issue = make_issue(code=code, severity=IngestionIssueSeverity.INFO)
    assert issue.code is code


def test_extracted_entities_frozen():
    for entity in (make_section(), make_topic(), make_objective()):
        with pytest.raises(FrozenInstanceError):
            entity.title = "x"  # type: ignore[misc]
