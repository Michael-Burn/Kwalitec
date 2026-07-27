"""Immutable snapshots for Curriculum Studio foundation (PI-001A)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SubjectSnapshot:
    subject_id: int
    subject_code: str
    title: str
    version_count: int = 0
    created_at: str = ""


@dataclass(frozen=True)
class DocumentSnapshot:
    document_id: int
    kind: str
    reference: str
    title: str
    uploaded_at: str = ""


@dataclass(frozen=True)
class VersionSnapshot:
    version_id: int
    subject_code: str
    version_label: str
    stage: str
    publication_state: str
    processing_state: str | None = None
    ingestion_job_id: str | None = None
    has_cmp: bool = False
    has_syllabus: bool = False
    validation_passed: bool | None = None
    reviewed_by: str | None = None
    documents: tuple[DocumentSnapshot, ...] = field(default_factory=tuple)
    updated_at: str = ""


@dataclass(frozen=True)
class ProcessingSnapshot:
    version_id: int
    processing_state: str | None
    ingestion_job_id: str | None
    stage: str
    publication_state: str
    section_count: int = 0
    topic_count: int = 0
    objective_count: int = 0
    validation_passed: bool | None = None
    validation_summary: str = ""


@dataclass(frozen=True)
class ParsedCurriculumSnapshot:
    version_id: int
    subject_code: str
    version_label: str
    sections: tuple[dict, ...] = field(default_factory=tuple)
    topics: tuple[dict, ...] = field(default_factory=tuple)
    objectives: tuple[dict, ...] = field(default_factory=tuple)
    processing_state: str | None = None


@dataclass(frozen=True)
class ValidationSnapshot:
    version_id: int
    passed: bool
    summary: str
    issue_count: int = 0
    issues: tuple[dict, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AuditEventSnapshot:
    event_id: str
    subject_code: str
    version_id: int | None
    stage: str
    event_type: str
    actor_id: str
    message: str
    created_at: str = ""


@dataclass(frozen=True)
class PublishedPackageSnapshot:
    package_id: int
    subject_code: str
    version_id: int
    version_label: str
    is_active: bool
    published_by: str
    published_at: str
    package: dict = field(default_factory=dict)
