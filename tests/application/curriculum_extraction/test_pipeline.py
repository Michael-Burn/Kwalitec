"""Application tests for Curriculum Extraction Pipeline (EI-002)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.curriculum_extraction.dto import ExtractionRequest
from app.application.curriculum_extraction.extraction_engine import (
    CurriculumExtractionEngine,
)
from app.domain.curriculum_extraction.canonical_document import DocumentKind
from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind as ExtractedBlockKind,
)
from app.domain.curriculum_intelligence.extracted_document import (
    ExtractedBlock,
    ExtractedDocument,
    ExtractedPage,
)
from app.domain.curriculum_knowledge_graph.entities.definition import Definition
from app.domain.curriculum_knowledge_graph.entities.formula import Formula
from app.domain.curriculum_knowledge_graph.entities.learning_objective import (
    LearningObjective,
)
from app.domain.curriculum_knowledge_graph.entities.practice_exercise import (
    PracticeExercise,
)
from app.domain.curriculum_knowledge_graph.entities.reading_reference import (
    ReadingReference,
)
from app.domain.curriculum_knowledge_graph.entities.section import Section
from app.domain.curriculum_knowledge_graph.entities.subsection import Subsection
from app.domain.curriculum_knowledge_graph.entities.syllabus_outcome import (
    SyllabusOutcome,
)
from app.domain.curriculum_knowledge_graph.entities.topic import Topic
from app.domain.curriculum_knowledge_graph.entities.worked_example import (
    WorkedExample,
)
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.infrastructure.adapters.curriculum_extraction import PdfCanonicalAdapter
from app.models.curriculum_knowledge_graph import (
    CkgGraphEdition,
    CkgNodeProvenance,
    CkgSubject,
    CkgValidationReport,
)
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)


def _request(*, persist: bool = True, job_id: str = "job-ei002-1") -> ExtractionRequest:
    return ExtractionRequest(
        job_id=job_id,
        subject_code="CS1",
        edition_label="2026",
        subject_title="Actuarial Statistics",
        cmp_document=cmp_document(),
        syllabus_document=syllabus_document(),
        persist=persist,
    )


def test_full_pipeline_persists_draft(app, db, ctx) -> None:
    engine = CurriculumExtractionEngine()
    result = engine.extract(_request())

    assert result.validation.passed, result.validation.to_dict()
    assert result.persisted is True
    assert result.edition_id is not None
    assert result.graph is not None

    nodes = result.graph.nodes()
    types = {type(n) for n in nodes}
    for required in (
        Topic,
        Section,
        Subsection,
        LearningObjective,
        Definition,
        Formula,
        WorkedExample,
        PracticeExercise,
        ReadingReference,
        SyllabusOutcome,
    ):
        assert required in types, f"missing {required.__name__}"

    assert result.graph.edges(relationship_type=CkgRelationshipType.CONTAINS)
    assert result.graph.edges(relationship_type=CkgRelationshipType.REFERENCES)
    assert result.graph.edges(relationship_type=CkgRelationshipType.REQUIRES)
    assert result.graph.edges(
        relationship_type=CkgRelationshipType.CROSS_REFERENCES
    )

    for node in nodes:
        assert node.stable_id.value in result.provenance

    edition = CkgGraphEdition.query.filter_by(edition_id=result.edition_id).one()
    assert edition.publication_state == "draft"
    assert edition.validation_status == "passed"
    assert CkgSubject.query.filter_by(stable_id="CS1").one()
    assert CkgNodeProvenance.query.filter_by(
        edition_id=result.edition_id
    ).count() == len(nodes)
    assert CkgValidationReport.query.filter_by(
        edition_id=result.edition_id, passed=True
    ).count() == 1


def test_validation_failure_does_not_persist(app, db, ctx) -> None:
    engine = CurriculumExtractionEngine()
    # Empty CMP pages → import error before persist; use broken hierarchy by
    # running without syllabus headings via a custom empty syllabus replacement.
    from app.domain.curriculum_extraction.canonical_document import (
        BlockKind,
        CanonicalBlock,
        CanonicalDocument,
        CanonicalPage,
    )

    empty_syllabus = CanonicalDocument(
        document_id="bad-syllabus",
        document_kind=DocumentKind.SYLLABUS,
        title="Bad",
        source_ref="ref://bad",
        metadata=(("subject_code", "CS1"),),
        pages=(
            CanonicalPage(
                page_number=1,
                blocks=(
                    CanonicalBlock(
                        block_id="p1",
                        kind=BlockKind.PARAGRAPH,
                        text="No numbered headings here",
                    ),
                ),
            ),
        ),
    )
    request = ExtractionRequest(
        job_id="job-fail",
        subject_code="CS1",
        edition_label="2026",
        subject_title="Actuarial Statistics",
        cmp_document=cmp_document(),
        syllabus_document=empty_syllabus,
        persist=True,
    )
    with pytest.raises(Exception, match="heading|segment"):
        engine.extract(request)
    assert CkgGraphEdition.query.count() == 0


def test_persist_false_skips_orm(app, db, ctx) -> None:
    engine = CurriculumExtractionEngine()
    result = engine.extract(_request(persist=False))
    assert result.validation.passed
    assert result.persisted is False
    assert result.edition_id is None
    assert CkgGraphEdition.query.count() == 0


def test_replace_on_reextract(app, db, ctx) -> None:
    engine = CurriculumExtractionEngine()
    first = engine.extract(_request(job_id="job-a"))
    second = engine.extract(_request(job_id="job-b"))
    assert first.persisted and second.persisted
    assert CkgGraphEdition.query.filter_by(subject_code="CS1").count() == 1
    edition = CkgGraphEdition.query.filter_by(subject_code="CS1").one()
    assert edition.publication_state == "draft"
    assert edition.edition_id == second.edition_id


def test_pdf_adapter_maps_extracted_document() -> None:
    class _StubPort:
        def extract(self, pdf_bytes, *, extraction_id, document_id):
            assert pdf_bytes == b"%PDF-stub"
            return ExtractedDocument(
                extraction_id=extraction_id,
                document_id=document_id,
                page_count=1,
                pages=(
                    ExtractedPage(
                        page_number=1,
                        width=100,
                        height=100,
                        raw_text="1 Topic",
                        blocks=(
                            ExtractedBlock(
                                block_id="eb1",
                                kind=ExtractedBlockKind.HEADING,
                                text="1 Topic",
                                order_index=0,
                            ),
                        ),
                    ),
                ),
                metadata=(("title", "From PDF"),),
            )

    adapter = PdfCanonicalAdapter(_StubPort())
    doc = adapter.to_canonical(
        b"%PDF-stub",
        document_id="pdf-cmp",
        document_kind=DocumentKind.CMP,
        title="CMP from PDF",
        source_ref="ref://pdf/cmp",
        extraction_id="ex-1",
        metadata=(("subject_code", "CS1"),),
    )
    assert doc.document_kind is DocumentKind.CMP
    assert doc.pages[0].blocks[0].text == "1 Topic"
    assert doc.metadata_value("subject_code") == "CS1"


def test_application_purity_no_presentation_or_pdf_bytes_in_stages() -> None:
    root = Path("app/application/curriculum_extraction")
    for path in root.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("app.presentation")
                assert "digital_twin" not in node.module
                assert "mission" not in node.module or "permission" in node.module
        assert "pdf_bytes" not in source or path.name.startswith("dto")
