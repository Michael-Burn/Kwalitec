"""Domain tests for Curriculum Extraction (EI-002)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.domain.curriculum_extraction.canonical_document import (
    BlockKind,
    CanonicalBlock,
    CanonicalDocument,
    CanonicalPage,
    DocumentKind,
    StructuralLocator,
)
from app.domain.curriculum_extraction.confidence import (
    ConfidenceBand,
    ExtractionConfidence,
    confidence_band,
)
from app.domain.curriculum_extraction.provenance import (
    ExtractionMethod,
    ExtractionProvenance,
)
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.curriculum_extraction.validation import (
    IssueSeverity,
    ValidationIssue,
    ValidationReport,
)


def test_canonical_document_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="document_id"):
        CanonicalDocument(
            document_id="",
            document_kind=DocumentKind.CMP,
            title="t",
            source_ref="ref://x",
            pages=(),
        )


def test_canonical_block_and_page() -> None:
    block = CanonicalBlock(
        block_id="b1",
        kind=BlockKind.HEADING,
        text="1 Topic",
        level=1,
    )
    page = CanonicalPage(page_number=1, blocks=(block,))
    doc = CanonicalDocument(
        document_id="d1",
        document_kind=DocumentKind.SYLLABUS,
        title="Syllabus",
        source_ref="ref://s",
        pages=(page,),
        metadata=(("subject_code", "CS1"),),
    )
    assert doc.block_count == 1
    assert doc.metadata_value("subject_code") == "CS1"
    assert doc.all_blocks()[0][1].block_id == "b1"


def test_confidence_bands() -> None:
    assert confidence_band(100) is ConfidenceBand.HIGHLY_RELIABLE
    assert confidence_band(99) is ConfidenceBand.HIGHLY_RELIABLE
    assert confidence_band(90) is ConfidenceBand.REVIEW_RECOMMENDED
    assert confidence_band(89) is ConfidenceBand.MANUAL_CONFIRMATION
    conf = ExtractionConfidence.of(85)
    assert conf.requires_manual_confirmation()


def test_provenance_create() -> None:
    locator = StructuralLocator.create(
        "cmp-1",
        page_number=2,
        block_id="b9",
        structural_path="1/1.1",
        section_heading="1.1 Purpose",
        paragraph_or_table_ref="paragraph:b9",
    )
    prov = ExtractionProvenance.create(
        "CS1.T01",
        locator,
        document_kind=DocumentKind.CMP,
        confidence=92,
        extraction_method=ExtractionMethod.HEURISTIC,
    )
    assert prov.confidence.band is ConfidenceBand.REVIEW_RECOMMENDED
    assert prov.locator.page_number == 2


def test_validation_report_blockers() -> None:
    report = ValidationReport(
        issues=(
            ValidationIssue(
                code="orphan_node",
                severity=IssueSeverity.BLOCKER,
                message="missing",
            ),
            ValidationIssue(
                code="low_confidence",
                severity=IssueSeverity.WARNING,
                message="review",
            ),
        )
    )
    assert not report.passed
    assert len(report.blockers) == 1
    assert len(report.warnings) == 1


def test_publication_state_draft() -> None:
    assert PublicationState.DRAFT.value == "draft"


def test_domain_purity_no_flask_sqlalchemy_pdf_bytes() -> None:
    root = Path("app/domain/curriculum_extraction")
    forbidden = {
        "flask",
        "sqlalchemy",
        "app.extensions",
        "app.models",
        "app.presentation",
    }
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mod = alias.name.split(".")[0]
                    assert mod not in forbidden, path
            elif isinstance(node, ast.ImportFrom) and node.module:
                top = node.module.split(".")[0]
                if node.module.startswith("app."):
                    assert not node.module.startswith("app.models"), path
                    assert not node.module.startswith("app.extensions"), path
                    assert not node.module.startswith("app.presentation"), path
                assert top != "flask", path
                assert "pdf" not in node.module.lower() or "canonical" in str(
                    path
                )
