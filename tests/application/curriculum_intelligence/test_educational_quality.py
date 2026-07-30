"""EQ-001 educational quality tests for CIP classification and mapping."""

from __future__ import annotations

from app.application.curriculum_intelligence.content_classification_service import (
    ContentClassificationService,
)
from app.application.curriculum_intelligence.curriculum_mapping_service import (
    CurriculumMappingService,
)
from app.application.curriculum_intelligence.document_normalization_service import (
    DocumentNormalizationService,
)
from app.application.curriculum_intelligence.educational_quality_audit_service import (
    EducationalQualityAuditService,
)
from app.application.curriculum_intelligence.structural_parser_service import (
    StructuralParserService,
)
from app.application.curriculum_intelligence.syllabus_reconciliation_service import (
    CoverageStatus,
    SyllabusReconciliationService,
)
from app.domain.curriculum_intelligence.content_role import ContentRole
from app.domain.curriculum_intelligence.curriculum_entity import CurriculumEntityKind
from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind,
    ExtractedBlock,
    ExtractedDocument,
    ExtractedPage,
)


def _doc_from_pages(
    pages: list[tuple[int, list[tuple[BlockKind, str]]]],
) -> ExtractedDocument:
    extracted_pages = []
    for page_no, blocks in pages:
        extracted_pages.append(
            ExtractedPage(
                page_number=page_no,
                width=612.0,
                height=792.0,
                blocks=tuple(
                    ExtractedBlock(
                        block_id=f"b-{page_no}-{i}",
                        kind=kind,
                        text=text,
                        order_index=i,
                    )
                    for i, (kind, text) in enumerate(blocks)
                ),
                raw_text="\n".join(t for _, t in blocks),
            )
        )
    return ExtractedDocument(
        extraction_id="eq001-test",
        document_id=1,
        page_count=len(extracted_pages),
        pages=tuple(extracted_pages),
        metadata=(("title", "CS1 test"),),
    )


def test_classifier_rejects_front_matter_and_chrome():
    clf = ContentClassificationService()
    assert clf.classify_line("AGOGO CDO") is ContentRole.NAVIGATION
    assert clf.classify_line("Associateship Qualification") is (
        ContentRole.QUALIFICATION_INFORMATION
    )
    assert clf.classify_line("Combined Materials Pack") is ContentRole.FRONT_MATTER
    assert clf.classify_line("1 Data analysis [10%]") is ContentRole.EDUCATIONAL
    assert clf.classify_line("1.1.1 Aims of a data analysis") is (
        ContentRole.LEARNING_OBJECTIVE
    )


def test_syllabus_extraction_produces_chapters_topics_objectives():
    doc = _doc_from_pages(
        [
            (
                1,
                [
                    (BlockKind.HEADING, "Associateship Qualification"),
                    (BlockKind.HEADING, "Actuarial Statistics (CS1)"),
                    (BlockKind.PARAGRAPH, "Syllabus for the 2026 Examinations"),
                    (BlockKind.HEADING, "April 2025"),
                ],
            ),
            (
                2,
                [
                    (BlockKind.HEADING, "Aim"),
                    (BlockKind.PARAGRAPH, "This subject provides…"),
                    (BlockKind.HEADING, "Objectives"),
                    (BlockKind.HEADING, "1 Data analysis [10%]"),
                    (
                        BlockKind.PARAGRAPH,
                        "1.1 Describe the purpose and function of data analysis",
                    ),
                    (
                        BlockKind.PARAGRAPH,
                        "1.1.1 Aims of a data analysis (e.g. descriptive)",
                    ),
                    (
                        BlockKind.PARAGRAPH,
                        "1.1.2 Stages and suitable tools used "
                        "to conduct a data analysis",
                    ),
                    (BlockKind.PARAGRAPH, "1.2 Complete exploratory data analysis"),
                    (
                        BlockKind.PARAGRAPH,
                        "1.2.1 Appropriate tools to calculate "
                        "suitable summary statistics",
                    ),
                    (BlockKind.HEADING, "2 Random variables and distributions [20%]"),
                    (
                        BlockKind.PARAGRAPH,
                        "2.1 Understand the characteristics of "
                        "basic univariate distributions",
                    ),
                    (
                        BlockKind.PARAGRAPH,
                        "2.1.1 Geometric, binomial, negative binomial distributions",
                    ),
                ],
            ),
        ]
    )
    normalized = DocumentNormalizationService().normalize(doc)
    structural = StructuralParserService().parse(normalized)
    mapped = CurriculumMappingService().map(
        structural, subject_code="CS1", version_label="2026"
    )
    modules = [e for e in mapped.entities if e.kind is CurriculumEntityKind.MODULE]
    topics = [
        e
        for e in mapped.entities
        if e.kind in {CurriculumEntityKind.TOPIC, CurriculumEntityKind.SUBTOPIC}
    ]
    objectives = [
        e
        for e in mapped.entities
        if e.kind is CurriculumEntityKind.LEARNING_OBJECTIVE
    ]
    titles = {e.title.lower() for e in mapped.entities}
    assert not any("associateship" in t for t in titles)
    assert not any(t == "aim" for t in titles)
    assert len(modules) == 2
    assert any("data analysis" in m.title.lower() for m in modules)
    assert len(topics) >= 2
    assert len(objectives) >= 3
    assert any("1.1.1" in o.title for o in objectives)
    assert any("1.1.2" in o.title for o in objectives)


def test_cmp_front_matter_excluded_until_chapter():
    doc = _doc_from_pages(
        [
            (
                1,
                [
                    (BlockKind.HEADING, "AGOGO CDO"),
                    (BlockKind.HEADING, "Combined Materials Pack"),
                    (BlockKind.PARAGRAPH, "The Actuarial Education Company"),
                ],
            ),
            (
                2,
                [
                    (BlockKind.HEADING, "Contents"),
                    (BlockKind.PARAGRAPH, "Part 1 Section 1 Before you start Page 2"),
                    (BlockKind.PARAGRAPH, "1.1 Before you start"),
                ],
            ),
            (
                35,
                [
                    (BlockKind.HEADING, "CS1-01: Probability distributions"),
                    (BlockKind.PARAGRAPH, "0 Introduction"),
                    (BlockKind.PARAGRAPH, "1.4 Geometric distribution"),
                    (
                        BlockKind.PARAGRAPH,
                        "1.4.1 Define the geometric distribution",
                    ),
                ],
            ),
        ]
    )
    normalized = DocumentNormalizationService().normalize(doc)
    structural = StructuralParserService().parse(normalized)
    mapped = CurriculumMappingService().map(
        structural, subject_code="CS1", version_label="2019"
    )
    titles = [e.title for e in mapped.entities]
    assert not any("AGOGO" in t for t in titles)
    assert not any("Combined Materials" in t for t in titles)
    assert not any("Before you start" in t for t in titles)
    modules = [e for e in mapped.entities if e.kind is CurriculumEntityKind.MODULE]
    assert any("CS1-01" in m.title for m in modules)
    objectives = [
        e
        for e in mapped.entities
        if e.kind is CurriculumEntityKind.LEARNING_OBJECTIVE
    ]
    assert any("1.4.1" in o.title for o in objectives)


def test_syllabus_reconciliation_coverage_matrix():
    syl_doc = _doc_from_pages(
        [
            (
                1,
                [
                    (BlockKind.HEADING, "1 Data analysis [10%]"),
                    (BlockKind.PARAGRAPH, "1.1 Describe the purpose of data analysis"),
                    (BlockKind.PARAGRAPH, "1.1.1 Aims of a data analysis"),
                    (BlockKind.PARAGRAPH, "1.1.2 Stages of data analysis"),
                ],
            )
        ]
    )
    cmp_doc = _doc_from_pages(
        [
            (
                1,
                [
                    (BlockKind.HEADING, "CS1-10: Data Analysis"),
                    (BlockKind.PARAGRAPH, "1.1 Describe the purpose of data analysis"),
                    (BlockKind.PARAGRAPH, "1.1.1 Aims of a data analysis"),
                ],
            )
        ]
    )
    syl = CurriculumMappingService().map(
        StructuralParserService().parse(
            DocumentNormalizationService().normalize(syl_doc)
        ),
        subject_code="CS1",
        version_label="s",
    )
    cmp = CurriculumMappingService().map(
        StructuralParserService().parse(
            DocumentNormalizationService().normalize(cmp_doc)
        ),
        subject_code="CS1",
        version_label="c",
    )
    matrix = SyllabusReconciliationService().reconcile(syl, cmp)
    assert matrix.syllabus_objective_count >= 2
    assert matrix.covered + matrix.partially_covered >= 1
    assert any(r.status is CoverageStatus.COVERED for r in matrix.rows) or any(
        r.status is CoverageStatus.PARTIALLY_COVERED for r in matrix.rows
    )


def test_quality_audit_indicators():
    doc = _doc_from_pages(
        [
            (
                1,
                [
                    (BlockKind.HEADING, "1 Data analysis [10%]"),
                    (BlockKind.PARAGRAPH, "1.1 Describe the purpose of data analysis"),
                    (BlockKind.PARAGRAPH, "1.1.1 Aims of a data analysis"),
                ],
            )
        ]
    )
    mapped = CurriculumMappingService().map(
        StructuralParserService().parse(
            DocumentNormalizationService().normalize(doc)
        ),
        subject_code="CS1",
        version_label="q",
    )
    audit = EducationalQualityAuditService().audit_map(mapped, label="test")
    qi = EducationalQualityAuditService().quality_indicators(audit)
    assert audit.chapters == 1
    assert audit.objectives >= 1
    assert qi.front_matter_contamination == 0.0
    assert qi.parser_confidence > 0.5
