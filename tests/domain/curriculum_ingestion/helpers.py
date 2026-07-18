"""Shared helpers for curriculum ingestion domain tests."""

from __future__ import annotations

from app.domain.curriculum_ingestion.curriculum_document import (
    CurriculumDocument,
    DocumentEntry,
    DocumentEntryType,
    DocumentKind,
)
from app.domain.curriculum_ingestion.extracted_objective import ExtractedObjective
from app.domain.curriculum_ingestion.extracted_section import ExtractedSection
from app.domain.curriculum_ingestion.extracted_topic import ExtractedTopic
from app.domain.curriculum_ingestion.extraction_result import ExtractionResult
from app.domain.curriculum_ingestion.ingestion_job import IngestionJob
from app.domain.curriculum_ingestion.ingestion_report import (
    IngestionIssue,
    IngestionIssueCode,
    IngestionIssueSeverity,
    IngestionReport,
)
from app.domain.curriculum_ingestion.normalization_result import (
    NormalizationResult,
    NormalizedObjective,
    NormalizedSection,
    NormalizedTopic,
)


def make_entry(
    entry_id: str = "e1",
    entry_type: DocumentEntryType | str = DocumentEntryType.TOPIC,
    text: str = "Topic A",
    *,
    number: str | None = "1",
    parent_ref: str | None = None,
    attributes: tuple[tuple[str, str], ...] | None = None,
) -> DocumentEntry:
    return DocumentEntry.create(
        entry_id,
        entry_type,
        text,
        number=number,
        parent_ref=parent_ref,
        attributes=attributes,
    )


def make_document(
    document_id: str = "doc-1",
    *,
    title: str = "Syllabus CS1",
    source_ref: str = "s3://bucket/syllabus.json",
    declared_kind: DocumentKind | str | None = DocumentKind.SYLLABUS,
    entries: list[DocumentEntry] | None = None,
    metadata: tuple[tuple[str, str], ...] | None = None,
) -> CurriculumDocument:
    if entries is None:
        entries = [
            make_entry("s1", DocumentEntryType.SECTION, "Chapter 1", number="1"),
            make_entry(
                "t1",
                DocumentEntryType.TOPIC,
                "Probability",
                number="1.1",
                parent_ref="s1",
            ),
            make_entry(
                "o1",
                DocumentEntryType.OBJECTIVE,
                "Define probability",
                number="1",
                parent_ref="t1",
            ),
        ]
    meta = metadata or (("subject_code", "CS1"),)
    return CurriculumDocument.create(
        document_id,
        source_ref,
        title,
        entries=entries,
        declared_kind=declared_kind,
        metadata=meta,
    )


def make_job(
    job_id: str = "job-1",
    *,
    documents: list[CurriculumDocument] | None = None,
) -> IngestionJob:
    return IngestionJob.create(job_id, documents or [make_document()])


def make_section(
    section_id: str = "sec-1", title: str = "Chapter 1", number: str | None = "1"
) -> ExtractedSection:
    return ExtractedSection.create(section_id, title, number=number)


def make_topic(
    topic_id: str = "top-1",
    title: str = "Probability",
    *,
    section_ref: str | None = "sec-1",
    number: str | None = "1.1",
    prerequisite_refs: tuple[str, ...] = (),
) -> ExtractedTopic:
    return ExtractedTopic.create(
        topic_id,
        title,
        section_ref=section_ref,
        number=number,
        prerequisite_refs=prerequisite_refs,
    )


def make_objective(
    objective_id: str = "obj-1",
    text: str = "Define probability",
    *,
    topic_ref: str | None = "top-1",
    number: str | None = "1",
) -> ExtractedObjective:
    return ExtractedObjective.create(
        objective_id, text, topic_ref=topic_ref, number=number
    )


def make_extraction(
    result_id: str = "ext-1",
    *,
    document_ids: tuple[str, ...] = ("doc-1",),
    sections: list[ExtractedSection] | None = None,
    topics: list[ExtractedTopic] | None = None,
    objectives: list[ExtractedObjective] | None = None,
    metadata: tuple[tuple[str, str], ...] = (("subject_code", "CS1"),),
) -> ExtractionResult:
    return ExtractionResult.create(
        result_id,
        document_ids,
        sections=sections if sections is not None else [make_section()],
        topics=topics if topics is not None else [make_topic()],
        objectives=objectives if objectives is not None else [make_objective()],
        metadata=metadata,
    )


def make_normalized(
    result_id: str = "norm-1",
    *,
    extraction_result_id: str = "ext-1",
    with_objectives: bool = True,
) -> NormalizationResult:
    section = NormalizedSection.create("section-ch1", "Chapter 1", "1", 0)
    topic = NormalizedTopic.create(
        "topic-probability", "Probability", "section-ch1", "1.1", 0
    )
    objectives: list[NormalizedObjective] = []
    if with_objectives:
        objectives.append(
            NormalizedObjective.create(
                "objective-define",
                "Define probability",
                "topic-probability",
                "1",
                0,
            )
        )
    return NormalizationResult.create(
        result_id,
        extraction_result_id,
        sections=[section],
        topics=[topic],
        objectives=objectives,
        metadata=(("subject_code", "CS1"),),
    )


def make_issue(
    code: IngestionIssueCode = IngestionIssueCode.MISSING_OBJECTIVES,
    message: str = "missing",
    *,
    severity: IngestionIssueSeverity = IngestionIssueSeverity.ERROR,
) -> IngestionIssue:
    return IngestionIssue.create(code, message, severity=severity)


def make_report(
    report_id: str = "val-1",
    job_id: str = "job-1",
    *,
    issues: list[IngestionIssue] | None = None,
) -> IngestionReport:
    return IngestionReport.create(report_id, job_id, issues=issues or [])
