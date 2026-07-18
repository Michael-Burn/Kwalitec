"""Shared helpers for curriculum ingestion application tests."""

from __future__ import annotations

from app.application.curriculum_ingestion.dto.ingestion_request import (
    DocumentEntryPayload,
    DocumentPayload,
    IngestionRequest,
)
from app.application.curriculum_ingestion.ingestion_engine import (
    CurriculumIngestionEngine,
)
from app.domain.curriculum_ingestion.curriculum_document import DocumentEntryType


def entry(
    entry_id: str,
    entry_type: str,
    text: str,
    *,
    number: str | None = None,
    parent_ref: str | None = None,
    attributes: tuple[tuple[str, str], ...] = (),
) -> DocumentEntryPayload:
    return DocumentEntryPayload(
        entry_id=entry_id,
        entry_type=entry_type,
        text=text,
        number=number,
        parent_ref=parent_ref,
        attributes=attributes,
    )


def syllabus_payload(
    document_id: str = "doc-syllabus",
    *,
    subject_code: str = "CS1",
    topic_title: str = "Probability",
) -> DocumentPayload:
    return DocumentPayload(
        document_id=document_id,
        source_ref=f"s3://curriculum/{document_id}.json",
        title="Syllabus CS1",
        declared_kind="syllabus",
        metadata=(("subject_code", subject_code),),
        entries=(
            entry("s1", "section", "Chapter 1", number="1"),
            entry(
                "t1",
                "topic",
                topic_title,
                number="1.1",
                parent_ref="s1",
            ),
            entry(
                "o1",
                "objective",
                f"Understand {topic_title}",
                number="1",
                parent_ref="t1",
            ),
        ),
    )


def objectives_payload(document_id: str = "doc-lo") -> DocumentPayload:
    return DocumentPayload(
        document_id=document_id,
        source_ref=f"s3://curriculum/{document_id}.json",
        title="Learning Objectives CS1",
        declared_kind="learning_objectives",
        metadata=(("subject_code", "CS1"),),
        entries=(
            entry("o1", "objective", "Define probability", number="1", parent_ref="t1"),
            entry(
                "o2",
                "objective",
                "Compute expectation",
                number="2",
                parent_ref="t1",
            ),
        ),
    )


def make_request(
    job_id: str = "job-1",
    *,
    documents: tuple[DocumentPayload, ...] | None = None,
    require_pass: bool = True,
) -> IngestionRequest:
    return IngestionRequest(
        job_id=job_id,
        documents=documents or (syllabus_payload(),),
        metadata=(("source", "test"),),
        require_pass=require_pass,
    )


def make_engine() -> CurriculumIngestionEngine:
    return CurriculumIngestionEngine()


def multi_topic_payload(n: int = 5, *, subject_code: str = "CS1") -> DocumentPayload:
    entries: list[DocumentEntryPayload] = [
        entry("s1", DocumentEntryType.SECTION.value, "Chapter 1", number="1")
    ]
    for i in range(1, n + 1):
        tid = f"t{i}"
        entries.append(
            entry(
                tid,
                "topic",
                f"Topic {i}",
                number=f"1.{i}",
                parent_ref="s1",
            )
        )
        entries.append(
            entry(
                f"o{i}",
                "objective",
                f"Objective for topic {i}",
                number="1",
                parent_ref=tid,
            )
        )
    return DocumentPayload(
        document_id="doc-multi",
        source_ref="s3://curriculum/multi.json",
        title="Syllabus Multi",
        declared_kind="syllabus",
        metadata=(("subject_code", subject_code),),
        entries=tuple(entries),
    )
