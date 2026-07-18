"""Additional classification and extraction edge coverage."""

from __future__ import annotations

import pytest

from app.application.curriculum_ingestion.document_classifier import (
    DocumentClassifier,
)
from app.application.curriculum_ingestion.extraction_service import (
    ExtractionService,
)
from app.application.curriculum_ingestion.policies.extraction_policy import (
    ExtractionPolicy,
)
from app.domain.curriculum_ingestion.curriculum_document import (
    CurriculumDocument,
    DocumentEntryType,
    DocumentKind,
)
from tests.domain.curriculum_ingestion.helpers import make_document, make_entry


@pytest.mark.parametrize(
    "meta_kind,expected",
    [
        ("syllabus", DocumentKind.SYLLABUS),
        ("cmp", DocumentKind.CMP),
        ("learning_objectives", DocumentKind.LEARNING_OBJECTIVES),
        ("formula_sheet", DocumentKind.FORMULA_SHEET),
        ("supporting_document", DocumentKind.SUPPORTING_DOCUMENT),
    ],
)
def test_classifier_metadata_kind(meta_kind, expected):
    doc = CurriculumDocument.create(
        "d1",
        "s3://x",
        "Untitled",
        entries=[make_entry("n1", DocumentEntryType.NOTE, "n", number=None)],
        declared_kind=None,
        metadata=(("document_kind", meta_kind),),
    )
    assert DocumentClassifier().classify(doc) is expected


@pytest.mark.parametrize(
    "title",
    [
        "specification overview",
        "SPEC sheet",
        "objectives list",
        "formulae booklet",
        "appendix supporting material",
        "core mathematics pack volume 1",
    ],
)
def test_classifier_title_variants(title):
    doc = CurriculumDocument.create(
        "d1",
        "s3://x",
        title,
        entries=[make_entry("n1", DocumentEntryType.NOTE, "n", number=None)],
        declared_kind=None,
    )
    kind = DocumentClassifier().classify(doc)
    assert kind is not DocumentKind.UNKNOWN


@pytest.mark.parametrize("kind", list(DocumentKind))
def test_extraction_respects_policy_allow_list(kind):
    entries = [
        make_entry("s1", DocumentEntryType.SECTION, "S", number="1"),
        make_entry("t1", DocumentEntryType.TOPIC, "T", number="1.1", parent_ref="s1"),
        make_entry(
            "o1", DocumentEntryType.OBJECTIVE, "O", number="1", parent_ref="t1"
        ),
        make_entry("f1", DocumentEntryType.FORMULA, "F", number=None),
        make_entry("n1", DocumentEntryType.NOTE, "N", number=None),
    ]
    doc = CurriculumDocument.create(
        "d1", "s3://x", "Doc", entries=entries, declared_kind=kind
    )
    result = ExtractionService().extract(
        [doc], [(doc.document_id, kind)], result_id="ext"
    )
    allowed = ExtractionPolicy.extractable_entry_types(kind)
    if DocumentEntryType.SECTION not in allowed:
        assert result.section_count == 0
    if DocumentEntryType.TOPIC not in allowed:
        assert result.topic_count == 0
    if DocumentEntryType.OBJECTIVE not in allowed:
        assert result.objective_count == 0


@pytest.mark.parametrize("i", range(40))
def test_extraction_metadata_entries(i):
    doc = CurriculumDocument.create(
        "d1",
        "s3://x",
        "Syllabus",
        declared_kind=DocumentKind.SYLLABUS,
        entries=[
            make_entry(
                f"m{i}",
                DocumentEntryType.METADATA,
                f"value-{i}",
                number=None,
                attributes=(("key", f"k{i}"),),
            ),
            make_entry("s1", DocumentEntryType.SECTION, "S", number="1"),
            make_entry(
                "t1",
                DocumentEntryType.TOPIC,
                "T",
                number="1.1",
                parent_ref="s1",
            ),
            make_entry(
                "o1", DocumentEntryType.OBJECTIVE, "O", number="1", parent_ref="t1"
            ),
        ],
    )
    result = ExtractionService().extract(
        [doc],
        [(doc.document_id, DocumentKind.SYLLABUS)],
        result_id=f"ext-{i}",
    )
    assert any(k == f"k{i}" for k, _ in result.metadata)


@pytest.mark.parametrize(
    "prereq_text",
    [f"topic-{i}" for i in range(1, 21)],
)
def test_extraction_prerequisite_entries(prereq_text):
    doc = make_document(
        entries=[
            make_entry("s1", DocumentEntryType.SECTION, "S", number="1"),
            make_entry(
                "t1",
                DocumentEntryType.TOPIC,
                "T",
                number="1.1",
                parent_ref="s1",
            ),
            make_entry(
                "p1",
                DocumentEntryType.PREREQUISITE,
                prereq_text,
                number=None,
                parent_ref="t1",
            ),
            make_entry(
                "o1", DocumentEntryType.OBJECTIVE, "O", number="1", parent_ref="t1"
            ),
        ]
    )
    result = ExtractionService().extract(
        [doc],
        [(doc.document_id, DocumentKind.SYLLABUS)],
        result_id="ext",
    )
    assert ( "t1", prereq_text) in result.prerequisite_refs or any(
        p[1] == prereq_text for p in result.prerequisite_refs
    )
