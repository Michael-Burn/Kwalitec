"""Edge cases and malformed structures for Curriculum Ingestion domain."""

from __future__ import annotations

import pytest

from app.domain.curriculum_ingestion.curriculum_document import (
    CurriculumDocument,
    DocumentEntryType,
    DocumentKind,
)
from app.domain.curriculum_ingestion.extraction_result import ExtractionResult
from app.domain.curriculum_ingestion.ingestion_job import IngestionJob
from app.domain.curriculum_ingestion.ingestion_report import (
    IngestionIssue,
    IngestionIssueCode,
    IngestionIssueSeverity,
)
from app.domain.curriculum_ingestion.normalization_result import (
    NormalizedSection,
    NormalizedTopic,
)
from tests.domain.curriculum_ingestion.helpers import (
    make_document,
    make_entry,
    make_extraction,
    make_job,
    make_objective,
    make_section,
    make_topic,
)


@pytest.mark.parametrize(
    "field,kwargs",
    [
        ("entry_id", {"entry_id": ""}),
        ("text", {"text": "  "}),
        ("number", {"number": " "}),
        ("parent_ref", {"parent_ref": ""}),
    ],
)
def test_entry_rejects_blank_optional_strings(field, kwargs):
    base = {"entry_id": "e1", "entry_type": "topic", "text": "T"}
    base.update(kwargs)
    with pytest.raises(ValueError):
        make_entry(**base)


@pytest.mark.parametrize(
    "bad_ref",
    ["data:text/plain,hi", "DATA:application/pdf;base64,xx", "%PDF-1.7 binary"],
)
def test_document_rejects_embedded_content(bad_ref):
    with pytest.raises(ValueError):
        CurriculumDocument.create("d1", bad_ref, "Title")


def test_document_with_entries_replaces():
    doc = make_document()
    updated = doc.with_entries([make_entry("only", text="Only")])
    assert updated.entry_count == 1
    assert updated.document_id == doc.document_id


def test_job_duplicate_document_ids():
    docs = [make_document("same"), make_document("same")]
    with pytest.raises(ValueError, match="duplicate document"):
        IngestionJob.create("j1", docs)


def test_job_document_by_id():
    job = make_job()
    assert job.document_by_id("doc-1") is not None
    assert job.document_by_id("missing") is None


def test_extraction_requires_document_ids():
    with pytest.raises(ValueError, match="document_ids"):
        ExtractionResult.create("r1", [])


@pytest.mark.parametrize(
    "order_index",
    [-1, -5],
)
def test_normalized_section_rejects_negative_order(order_index):
    with pytest.raises(ValueError, match="order_index"):
        NormalizedSection.create("s", "T", "1", order_index)


def test_normalized_topic_prereq_validation():
    with pytest.raises(ValueError):
        NormalizedTopic.create(
            "t", "T", "s", "1", 0, prerequisite_ids=["  "]
        )


@pytest.mark.parametrize(
    "severity,code,blocking",
    [
        (IngestionIssueSeverity.BLOCKING, IngestionIssueCode.OTHER, True),
        (
            IngestionIssueSeverity.ERROR,
            IngestionIssueCode.MISSING_OBJECTIVES,
            True,
        ),
        (
            IngestionIssueSeverity.WARNING,
            IngestionIssueCode.MISSING_METADATA,
            False,
        ),
        (IngestionIssueSeverity.INFO, IngestionIssueCode.OTHER, False),
        (
            IngestionIssueSeverity.ERROR,
            IngestionIssueCode.INCONSISTENT_NUMBERING,
            False,
        ),
    ],
)
def test_issue_blocking_matrix(severity, code, blocking):
    issue = IngestionIssue.create(code, "m", severity=severity)
    assert issue.is_blocking is blocking


@pytest.mark.parametrize("n", range(1, 21))
def test_document_scales_to_many_entries(n):
    entries = [
        make_entry(f"e{i}", DocumentEntryType.NOTE, f"Note {i}", number=None)
        for i in range(n)
    ]
    doc = CurriculumDocument.create(
        "d1",
        "s3://x",
        "Notes",
        entries=entries,
        declared_kind=DocumentKind.SUPPORTING_DOCUMENT,
    )
    assert doc.entry_count == n


@pytest.mark.parametrize("n", range(1, 16))
def test_extraction_scales_topics(n):
    topics = [make_topic(f"t{i}", f"Topic {i}", number=f"1.{i}") for i in range(n)]
    objectives = [
        make_objective(f"o{i}", topic_ref=f"t{i}") for i in range(n)
    ]
    result = make_extraction(topics=topics, objectives=objectives)
    assert result.topic_count == n
    assert result.objective_count == n


@pytest.mark.parametrize(
    "kind",
    ["CMP", " Syllabus ", "LEARNING_OBJECTIVES", "Formula_Sheet"],
)
def test_document_kind_normalises_tokens(kind):
    from app.domain.curriculum_ingestion.curriculum_document import (
        resolve_document_kind,
    )

    resolved = resolve_document_kind(kind)
    assert isinstance(resolved, DocumentKind)


def test_section_parent_optional():
    section = make_section()
    assert section.parent_section_id is None


def test_topic_without_section():
    topic = make_topic(section_ref=None)
    assert topic.section_ref is None


def test_objective_without_topic():
    objective = make_objective(topic_ref=None)
    assert objective.topic_ref is None


@pytest.mark.parametrize(
    "title",
    [f"Chapter {i}" for i in range(1, 31)],
)
def test_many_section_titles(title):
    section = make_section(section_id=title.lower().replace(" ", "-"), title=title)
    assert section.title == title
