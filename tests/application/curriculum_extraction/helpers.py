"""Shared Canonical Document fixtures for EI-002 extraction tests."""

from __future__ import annotations

from app.domain.curriculum_extraction.canonical_document import (
    BlockKind,
    CanonicalBlock,
    CanonicalDocument,
    CanonicalPage,
    DocumentKind,
)


def _block(
    block_id: str,
    text: str,
    *,
    kind: BlockKind = BlockKind.PARAGRAPH,
    level: int = 0,
) -> CanonicalBlock:
    return CanonicalBlock(
        block_id=block_id,
        kind=kind,
        text=text,
        level=level,
        structural_path=block_id,
    )


def syllabus_document(
    document_id: str = "syllabus-cs1",
    *,
    subject_code: str = "CS1",
) -> CanonicalDocument:
    """Minimal IFoA-style syllabus Canonical Document."""
    return CanonicalDocument(
        document_id=document_id,
        document_kind=DocumentKind.SYLLABUS,
        title="CS1 Syllabus 2026",
        source_ref="ref://syllabus/cs1-2026",
        metadata=(("subject_code", subject_code),),
        pages=(
            CanonicalPage(
                page_number=1,
                blocks=(
                    _block("s-h1", "1 Data analysis", kind=BlockKind.HEADING, level=1),
                    _block(
                        "s-h2",
                        "1.1 Purpose and function of data analysis",
                        kind=BlockKind.HEADING,
                        level=2,
                    ),
                    _block(
                        "s-h3",
                        "1.1.1 Aims of a data analysis",
                        kind=BlockKind.HEADING,
                        level=3,
                    ),
                    _block(
                        "s-lo1",
                        "1.1.1.1 Describe descriptive, inferential and predictive aims",
                        kind=BlockKind.HEADING,
                        level=4,
                    ),
                    _block(
                        "s-lo2",
                        "1.1.1.2 Identify stages of a data analysis",
                        kind=BlockKind.HEADING,
                        level=4,
                    ),
                    _block(
                        "s-meta1",
                        "Estimated study time: 120",
                        kind=BlockKind.PARAGRAPH,
                    ),
                    _block(
                        "s-meta2",
                        "Difficulty: foundational",
                        kind=BlockKind.PARAGRAPH,
                    ),
                    _block(
                        "s-prereq",
                        "Prerequisite: 1.1.1.1",
                        kind=BlockKind.PARAGRAPH,
                    ),
                ),
            ),
        ),
    )


def cmp_document(
    document_id: str = "cmp-cs1",
    *,
    subject_code: str = "CS1",
) -> CanonicalDocument:
    """Minimal IFoA-style CMP Canonical Document with educational objects."""
    return CanonicalDocument(
        document_id=document_id,
        document_kind=DocumentKind.CMP,
        title="CS1 Core Reading 2026",
        source_ref="ref://cmp/cs1-2026",
        metadata=(("subject_code", subject_code),),
        pages=(
            CanonicalPage(
                page_number=1,
                blocks=(
                    _block("c-h1", "1 Data analysis", kind=BlockKind.HEADING, level=1),
                    _block(
                        "c-h2",
                        "1.1 Purpose and function of data analysis",
                        kind=BlockKind.HEADING,
                        level=2,
                    ),
                    _block(
                        "c-h3",
                        "1.1.1 Aims of a data analysis",
                        kind=BlockKind.HEADING,
                        level=3,
                    ),
                    _block(
                        "c-def",
                        "Definition: Data analysis is the process of inspecting data",
                        kind=BlockKind.PARAGRAPH,
                    ),
                    _block(
                        "c-for",
                        "Formula: P(A|B) = P(B|A)P(A)/P(B)",
                        kind=BlockKind.PARAGRAPH,
                    ),
                    _block(
                        "c-we",
                        "Worked example: Compute a sample mean from five observations",
                        kind=BlockKind.PARAGRAPH,
                    ),
                    _block(
                        "c-pe",
                        "Practice: Classify aims of a business data analysis",
                        kind=BlockKind.PARAGRAPH,
                    ),
                    _block(
                        "c-rr",
                        "Reading: CMP Unit 1 pages 1-12",
                        kind=BlockKind.PARAGRAPH,
                    ),
                    _block(
                        "c-cross",
                        "See also: 1.1",
                        kind=BlockKind.PARAGRAPH,
                    ),
                ),
            ),
            CanonicalPage(
                page_number=2,
                blocks=(
                    _block(
                        "c-table",
                        "Summary of analysis stages",
                        kind=BlockKind.TABLE,
                    ),
                ),
            ),
        ),
    )
