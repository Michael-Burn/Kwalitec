"""ValidationService — produce immutable ingestion validation reports."""

from __future__ import annotations

from app.application.curriculum_ingestion.exceptions import ValidationFailed
from app.application.curriculum_ingestion.policies.validation_policy import (
    ValidationPolicy,
)
from app.domain.curriculum_ingestion.curriculum_document import DocumentKind
from app.domain.curriculum_ingestion.ingestion_job import IngestionJob
from app.domain.curriculum_ingestion.ingestion_report import IngestionReport
from app.domain.curriculum_ingestion.normalization_result import NormalizationResult


class ValidationService:
    """Validate normalised structures. No PDF parsing. No teaching."""

    def validate(
        self,
        job: IngestionJob,
        normalization: NormalizationResult,
        *,
        report_id: str,
        raise_on_block: bool = False,
    ) -> IngestionReport:
        """Run validation and return an immutable IngestionReport."""
        document_empty = all(doc.entry_count == 0 for doc in job.documents)
        has_unknown = any(
            kind is DocumentKind.UNKNOWN for _, kind in job.classified_kinds
        )
        # Also empty when normalisation has no topics from structural docs
        if (
            not document_empty
            and normalization.topic_count == 0
            and normalization.section_count <= 1
            and normalization.objective_count == 0
        ):
            # Soft signal — treat as empty structural yield when all docs empty-ish
            if all(doc.entry_count == 0 for doc in job.documents):
                document_empty = True

        issues = ValidationPolicy.collect_issues(
            normalization,
            document_empty=document_empty,
            has_unknown_kind=has_unknown,
        )
        report = IngestionReport.create(
            report_id, job.job_id, issues=issues
        )
        if raise_on_block and report.blocks_ingestion:
            raise ValidationFailed(
                f"Validation blocked ingestion for {job.job_id}: {report.summary}"
            )
        return report
