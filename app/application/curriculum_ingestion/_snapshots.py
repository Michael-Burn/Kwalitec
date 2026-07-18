"""DTO projection helpers for Curriculum Ingestion."""

from __future__ import annotations

from app.application.curriculum_ingestion.dto.extraction_snapshot import (
    ExtractedObjectiveSnapshot,
    ExtractedSectionSnapshot,
    ExtractedTopicSnapshot,
    ExtractionSnapshot,
)
from app.application.curriculum_ingestion.dto.ingestion_snapshot import (
    CurriculumPackagePreview,
    IngestionSnapshot,
)
from app.application.curriculum_ingestion.dto.normalization_snapshot import (
    NormalizationSnapshot,
    NormalizedObjectiveSnapshot,
    NormalizedSectionSnapshot,
    NormalizedTopicSnapshot,
)
from app.application.curriculum_ingestion.dto.validation_snapshot import (
    ValidationIssueSnapshot,
    ValidationSnapshot,
)
from app.domain.curriculum_ingestion.extraction_result import ExtractionResult
from app.domain.curriculum_ingestion.ingestion_job import IngestionJob
from app.domain.curriculum_ingestion.ingestion_report import IngestionReport
from app.domain.curriculum_ingestion.normalization_result import NormalizationResult


def extraction_snapshot(result: ExtractionResult) -> ExtractionSnapshot:
    """Project ExtractionResult → ExtractionSnapshot."""
    return ExtractionSnapshot(
        result_id=result.result_id,
        document_ids=result.document_ids,
        document_kinds=tuple(
            (did, kind.value) for did, kind in result.document_kinds
        ),
        section_count=result.section_count,
        topic_count=result.topic_count,
        objective_count=result.objective_count,
        sections=tuple(
            ExtractedSectionSnapshot(
                section_id=s.section_id,
                title=s.title,
                number=s.number,
                source_entry_id=s.source_entry_id,
                parent_section_id=s.parent_section_id,
            )
            for s in result.sections
        ),
        topics=tuple(
            ExtractedTopicSnapshot(
                topic_id=t.topic_id,
                title=t.title,
                section_ref=t.section_ref,
                number=t.number,
                source_entry_id=t.source_entry_id,
                prerequisite_refs=t.prerequisite_refs,
            )
            for t in result.topics
        ),
        objectives=tuple(
            ExtractedObjectiveSnapshot(
                objective_id=o.objective_id,
                text=o.text,
                topic_ref=o.topic_ref,
                number=o.number,
                source_entry_id=o.source_entry_id,
            )
            for o in result.objectives
        ),
        prerequisite_refs=result.prerequisite_refs,
        metadata=result.metadata,
        notes=result.notes,
    )


def normalization_snapshot(result: NormalizationResult) -> NormalizationSnapshot:
    """Project NormalizationResult → NormalizationSnapshot."""
    return NormalizationSnapshot(
        result_id=result.result_id,
        extraction_result_id=result.extraction_result_id,
        section_count=result.section_count,
        topic_count=result.topic_count,
        objective_count=result.objective_count,
        sections=tuple(
            NormalizedSectionSnapshot(
                section_id=s.section_id,
                title=s.title,
                number=s.number,
                order_index=s.order_index,
                parent_section_id=s.parent_section_id,
                source_ids=s.source_ids,
            )
            for s in result.sections
        ),
        topics=tuple(
            NormalizedTopicSnapshot(
                topic_id=t.topic_id,
                title=t.title,
                section_id=t.section_id,
                number=t.number,
                order_index=t.order_index,
                prerequisite_ids=t.prerequisite_ids,
                source_ids=t.source_ids,
            )
            for t in result.topics
        ),
        objectives=tuple(
            NormalizedObjectiveSnapshot(
                objective_id=o.objective_id,
                text=o.text,
                topic_id=o.topic_id,
                number=o.number,
                order_index=o.order_index,
                source_ids=o.source_ids,
            )
            for o in result.objectives
        ),
        prerequisite_edges=result.prerequisite_edges,
        metadata=result.metadata,
    )


def validation_snapshot(report: IngestionReport) -> ValidationSnapshot:
    """Project IngestionReport → ValidationSnapshot."""
    return ValidationSnapshot(
        report_id=report.report_id,
        job_id=report.job_id,
        passed=report.passed,
        summary=report.summary,
        issue_count=report.issue_count,
        blocking_count=len(report.blocking_issues),
        blocks_ingestion=report.blocks_ingestion,
        issues=tuple(
            ValidationIssueSnapshot(
                code=i.code.value,
                message=i.message,
                severity=i.severity.value,
                path=i.path,
                is_blocking=i.is_blocking,
            )
            for i in report.issues
        ),
    )


def ingestion_snapshot(
    job: IngestionJob,
    *,
    package: CurriculumPackagePreview | None = None,
) -> IngestionSnapshot:
    """Project IngestionJob (+ optional package) → IngestionSnapshot."""
    extraction = (
        extraction_snapshot(job.extraction) if job.extraction is not None else None
    )
    normalization = (
        normalization_snapshot(job.normalization)
        if job.normalization is not None
        else None
    )
    validation = (
        validation_snapshot(job.report) if job.report is not None else None
    )
    passed = job.report.passed if job.report is not None else False
    return IngestionSnapshot(
        job_id=job.job_id,
        state=job.state.value,
        document_count=job.document_count,
        classified_kinds=tuple(
            (did, kind.value) for did, kind in job.classified_kinds
        ),
        extraction=extraction,
        normalization=normalization,
        validation=validation,
        package=package,
        failure_reason=job.failure_reason,
        metadata=job.metadata,
        passed=passed,
    )
