"""Curriculum Ingestion Engine — public application facade.

Transforms abstract curriculum documents into normalised educational
structures via a deterministic pipeline:

    Document → Classification → Extraction → Normalization
            → Validation → Preview → Curriculum Package

Does NOT teach. Does NOT generate activities, sessions, or missions.
Does NOT persist. Does NOT use Flask. Does NOT perform AI reasoning.
"""

from __future__ import annotations

from app.application.curriculum_ingestion._snapshots import ingestion_snapshot
from app.application.curriculum_ingestion.document_classifier import (
    DocumentClassifier,
)
from app.application.curriculum_ingestion.dto.ingestion_request import (
    DocumentEntryPayload,
    DocumentPayload,
    IngestionRequest,
)
from app.application.curriculum_ingestion.dto.ingestion_snapshot import (
    IngestionSnapshot,
)
from app.application.curriculum_ingestion.exceptions import (
    CurriculumIngestionError,
    IllegalState,
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
    DocumentEntry,
)
from app.domain.curriculum_ingestion.ingestion_job import IngestionJob
from app.domain.curriculum_ingestion.ingestion_state import IngestionState


class CurriculumIngestionEngine:
    """Public facade for the Curriculum Ingestion pipeline.

    Framework-independent. Callers remain responsible for persistence.
    """

    ENGINE_ID = "curriculum_ingestion"
    ENGINE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        classifier: DocumentClassifier | None = None,
        extractor: ExtractionService | None = None,
        normalizer: NormalizationService | None = None,
        validator: ValidationService | None = None,
        mapper: MappingService | None = None,
        previewer: PreviewService | None = None,
    ) -> None:
        self.classifier = classifier or DocumentClassifier()
        self.extractor = extractor or ExtractionService()
        self.normalizer = normalizer or NormalizationService()
        self.validator = validator or ValidationService()
        self.mapper = mapper or MappingService()
        self.previewer = previewer or PreviewService(self.mapper)

    def ingest(self, request: IngestionRequest) -> IngestionSnapshot:
        """Run the full deterministic ingestion pipeline.

        When ``request.require_pass`` is True and validation blocks,
        raises ``ValidationFailed`` after the report is attached (job failed).
        """
        documents = tuple(
            self._document_from_payload(payload) for payload in request.documents
        )
        job = IngestionJob.create(
            request.job_id, documents, metadata=request.metadata
        )
        try:
            job = self._run_pipeline(job)
        except CurriculumIngestionError:
            raise
        except ValueError as exc:
            job = job.mark_failed(str(exc))
            raise CurriculumIngestionError(str(exc)) from exc

        package = None
        if job.normalization is not None:
            package = self.mapper.map_package(
                job, job.normalization, job.report
            )

        snapshot = ingestion_snapshot(job, package=package)
        if (
            request.require_pass
            and job.report is not None
            and job.report.blocks_ingestion
        ):
            raise ValidationFailed(
                f"Validation blocked ingestion for {job.job_id}: "
                f"{job.report.summary}"
            )
        return snapshot

    def classify_only(self, request: IngestionRequest) -> IngestionSnapshot:
        """Run classification only; leave job in CLASSIFIED."""
        documents = tuple(
            self._document_from_payload(payload) for payload in request.documents
        )
        job = IngestionJob.create(
            request.job_id, documents, metadata=request.metadata
        )
        kinds = self.classifier.classify_many(job.documents)
        job = job.with_classification(kinds)
        return ingestion_snapshot(job)

    def create_job(self, request: IngestionRequest) -> IngestionJob:
        """Construct a domain IngestionJob without running the pipeline."""
        documents = tuple(
            self._document_from_payload(payload) for payload in request.documents
        )
        return IngestionJob.create(
            request.job_id, documents, metadata=request.metadata
        )

    def run_job(self, job: IngestionJob) -> IngestionJob:
        """Run the pipeline on an existing job starting at RECEIVED."""
        if job.state is not IngestionState.RECEIVED:
            raise IllegalState(
                f"run_job requires RECEIVED state, got {job.state.value}"
            )
        return self._run_pipeline(job)

    def _run_pipeline(self, job: IngestionJob) -> IngestionJob:
        """Execute classify → extract → normalize → validate → preview → complete."""
        kinds = self.classifier.classify_many(job.documents)
        job = job.with_classification(kinds)

        extraction = self.extractor.extract(
            job.documents,
            job.classified_kinds,
            result_id=f"ext-{job.job_id}",
        )
        job = job.with_extraction(extraction)

        normalization = self.normalizer.normalize(
            extraction, result_id=f"norm-{job.job_id}"
        )
        job = job.with_normalization(normalization)

        report = self.validator.validate(
            job, normalization, report_id=f"val-{job.job_id}"
        )
        job = job.with_report(report)

        if report.blocks_ingestion:
            return job.mark_failed(report.summary)

        job = job.mark_preview_ready()
        # Preview is a projection; package mapping confirms readiness.
        self.mapper.map_package(job, normalization, report)
        return job.mark_completed()

    def _document_from_payload(
        self, payload: DocumentPayload
    ) -> CurriculumDocument:
        entries = tuple(
            self._entry_from_payload(entry) for entry in payload.entries
        )
        return CurriculumDocument.create(
            payload.document_id,
            payload.source_ref,
            payload.title,
            entries=entries,
            declared_kind=payload.declared_kind,
            metadata=payload.metadata,
        )

    def _entry_from_payload(self, payload: DocumentEntryPayload) -> DocumentEntry:
        return DocumentEntry.create(
            payload.entry_id,
            payload.entry_type,
            payload.text,
            number=payload.number,
            parent_ref=payload.parent_ref,
            attributes=payload.attributes,
        )
