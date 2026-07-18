"""Classification, extraction, normalisation, and validation service tests."""

from __future__ import annotations

import pytest

from app.application.curriculum_ingestion.document_classifier import (
    DocumentClassifier,
)
from app.application.curriculum_ingestion.exceptions import (
    ClassificationError,
    ExtractionError,
    PreviewError,
    ValidationFailed,
)
from app.application.curriculum_ingestion.extraction_service import (
    ExtractionService,
)
from app.application.curriculum_ingestion.mapping_service import MappingService
from app.application.curriculum_ingestion.normalization_service import (
    NormalizationService,
)
from app.application.curriculum_ingestion.preview_service import PreviewService
from app.application.curriculum_ingestion.validation_service import (
    ValidationService,
)
from app.domain.curriculum_ingestion.curriculum_document import (
    CurriculumDocument,
    DocumentEntryType,
    DocumentKind,
)
from app.domain.curriculum_ingestion.ingestion_state import IngestionState
from tests.application.curriculum_ingestion.helpers import (
    make_engine,
    make_request,
    multi_topic_payload,
    objectives_payload,
    syllabus_payload,
)
from tests.domain.curriculum_ingestion.helpers import (
    make_document,
    make_entry,
    make_extraction,
    make_job,
    make_normalized,
)


@pytest.mark.parametrize(
    "title,expected",
    [
        ("CS1 Syllabus 2026", DocumentKind.SYLLABUS),
        ("Learning Objectives Pack", DocumentKind.LEARNING_OBJECTIVES),
        ("Formula Sheet", DocumentKind.FORMULA_SHEET),
        ("CMP Core Pack", DocumentKind.CMP),
        ("Supporting Notes", DocumentKind.SUPPORTING_DOCUMENT),
    ],
)
def test_classifier_from_title(title, expected):
    doc = CurriculumDocument.create(
        "d1",
        "s3://x",
        title,
        entries=[make_entry("n1", DocumentEntryType.NOTE, "note", number=None)],
        declared_kind=None,
    )
    assert DocumentClassifier().classify(doc) is expected


@pytest.mark.parametrize("kind", list(DocumentKind))
def test_classifier_respects_declared_kind(kind):
    if kind is DocumentKind.UNKNOWN:
        return
    doc = make_document(declared_kind=kind)
    assert DocumentClassifier().classify(doc) is kind


def test_classifier_from_entry_fingerprint_objectives():
    doc = CurriculumDocument.create(
        "d1",
        "s3://x",
        "Untitled",
        entries=[
            make_entry("o1", DocumentEntryType.OBJECTIVE, "A", number="1"),
            make_entry("o2", DocumentEntryType.OBJECTIVE, "B", number="2"),
        ],
        declared_kind=None,
    )
    assert DocumentClassifier().classify(doc) is DocumentKind.LEARNING_OBJECTIVES


def test_classifier_from_formulas():
    doc = CurriculumDocument.create(
        "d1",
        "s3://x",
        "Untitled",
        entries=[
            make_entry("f1", DocumentEntryType.FORMULA, "E=mc2", number=None),
            make_entry("f2", DocumentEntryType.FORMULA, "a^2+b^2", number=None),
        ],
        declared_kind=None,
    )
    assert DocumentClassifier().classify(doc) is DocumentKind.FORMULA_SHEET


def test_classifier_many_requires_documents():
    with pytest.raises(ClassificationError):
        DocumentClassifier().classify_many([])


def test_extraction_produces_structures():
    doc = make_document()
    result = ExtractionService().extract(
        [doc],
        [(doc.document_id, DocumentKind.SYLLABUS)],
        result_id="ext-1",
    )
    assert result.section_count == 1
    assert result.topic_count == 1
    assert result.objective_count == 1


def test_extraction_empty_documents_raises():
    with pytest.raises(ExtractionError):
        ExtractionService().extract([], [], result_id="ext-1")


def test_normalization_canonicalises_ids():
    extraction = make_extraction()
    result = NormalizationService().normalize(extraction, result_id="norm-1")
    assert result.sections[0].section_id.startswith("section-")
    assert result.topics[0].topic_id.startswith("topic-")
    assert result.objectives[0].objective_id.startswith("objective-")


def test_normalization_default_section_when_missing():
    extraction = make_extraction(sections=[], topics=[
        __import__(
            "tests.domain.curriculum_ingestion.helpers", fromlist=["make_topic"]
        ).make_topic(section_ref=None)
    ])
    result = NormalizationService().normalize(extraction, result_id="norm-1")
    assert result.section_count == 1
    assert result.topics[0].section_id == "section-default"


def test_validation_detects_missing_objectives():
    job = make_job()
    job = job.with_classification((("doc-1", DocumentKind.SYLLABUS),))
    normalization = make_normalized(with_objectives=False)
    report = ValidationService().validate(job, normalization, report_id="v1")
    codes = {i.code.value for i in report.issues}
    assert "missing_objectives" in codes
    assert report.blocks_ingestion


def test_validation_raise_on_block():
    job = make_job()
    job = job.with_classification((("doc-1", DocumentKind.SYLLABUS),))
    normalization = make_normalized(with_objectives=False)
    with pytest.raises(ValidationFailed):
        ValidationService().validate(
            job, normalization, report_id="v1", raise_on_block=True
        )


def test_mapping_package_preview():
    engine = make_engine()
    snap = engine.ingest(make_request(require_pass=True))
    assert snap.package is not None
    assert snap.package.ready
    assert snap.package.topic_ids
    assert snap.state == IngestionState.COMPLETED.value


def test_preview_service_requires_normalization():
    job = make_job()
    with pytest.raises(PreviewError):
        PreviewService().preview(job)


def test_engine_classify_only():
    snap = make_engine().classify_only(make_request())
    assert snap.state == IngestionState.CLASSIFIED.value
    assert snap.classified_kinds


@pytest.mark.parametrize("n", range(1, 21))
def test_engine_multi_topic_ingest(n):
    request = make_request(
        job_id=f"job-multi-{n}",
        documents=(multi_topic_payload(n),),
    )
    snap = make_engine().ingest(request)
    assert snap.passed
    assert snap.normalization is not None
    assert snap.normalization.topic_count == n
    assert snap.normalization.objective_count == n


@pytest.mark.parametrize(
    "code",
    ["CS1", "CM1", "CB2", "FS1", "FM1", "CP1", "CP2", "MEI1"],
)
def test_engine_subject_codes(code):
    payload = syllabus_payload(subject_code=code, topic_title=f"Topic {code}")
    snap = make_engine().ingest(
        make_request(job_id=f"job-{code}", documents=(payload,))
    )
    assert ("subject_code", code) in snap.normalization.metadata


def test_engine_combines_syllabus_and_objectives():
    request = make_request(
        documents=(syllabus_payload(), objectives_payload()),
    )
    snap = make_engine().ingest(request)
    assert snap.document_count == 2
    assert snap.passed


def test_engine_require_pass_false_allows_failure():
    # Document with topics but no objectives → blocking
    from app.application.curriculum_ingestion.dto.ingestion_request import (
        DocumentEntryPayload,
        DocumentPayload,
        IngestionRequest,
    )

    payload = DocumentPayload(
        document_id="bad",
        source_ref="s3://x",
        title="Syllabus",
        declared_kind="syllabus",
        entries=(
            DocumentEntryPayload("s1", "section", "Ch1", number="1"),
            DocumentEntryPayload(
                "t1",
                "topic",
                "Lonely",
                number="1.1",
                parent_ref="s1",
            ),
        ),
        metadata=(),
    )
    snap = make_engine().ingest(
        IngestionRequest(job_id="bad-job", documents=(payload,), require_pass=False)
    )
    assert not snap.passed
    assert snap.state == IngestionState.FAILED.value


def test_mapping_service_direct():
    engine = make_engine()
    job = engine.create_job(make_request())
    job = engine.run_job(job)
    package = MappingService().map_package(job, job.normalization, job.report)
    assert package.package_id.startswith("pkg-")
