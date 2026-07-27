"""CIP processing adapter — enqueue + run curriculum intelligence pipeline.

Replaces the Phase-1 queue-only stub while preserving DocumentProcessingPort.
"""

from __future__ import annotations

import logging
from uuid import uuid4

from app.application.curriculum_intelligence.pipeline_coordinator import (
    PipelineCoordinator,
)
from app.application.curriculum_intelligence.processing_job_service import (
    ProcessingJobService,
)
from app.application.curriculum_studio.ports.document_processing_port import (
    DocumentProcessingPort,
    ProcessingJobHandle,
)
from app.application.curriculum_studio.ports.document_storage_port import (
    DocumentStoragePort,
)
from app.domain.curriculum_documents.processing_stage import DocumentProcessingStage
from app.domain.curriculum_intelligence.pipeline_stage import PipelineStage
from app.extensions import db
from app.infrastructure.adapters.curriculum_intelligence.pypdf_extractor import (
    PyPdfExtractionAdapter,
)
from app.models.curriculum_studio_foundation import StudioFoundationDocument

logger = logging.getLogger(__name__)


class CurriculumIntelligenceProcessingAdapter(DocumentProcessingPort):
    """Enqueue a CIP job and optionally run the pipeline synchronously.

    ``auto_run=True`` (default) advances the document through the CIP stages
    immediately after upload so Founders see Verified→Ready without a worker.
    Async workers can set ``auto_run=False`` and consume QUEUED jobs later.
    """

    def __init__(
        self,
        storage: DocumentStoragePort,
        *,
        auto_run: bool = True,
        coordinator: PipelineCoordinator | None = None,
        jobs: ProcessingJobService | None = None,
    ) -> None:
        self._storage = storage
        self._auto_run = auto_run
        self._jobs = jobs or ProcessingJobService()
        self._coordinator = coordinator or PipelineCoordinator(
            storage=storage,
            extractor_port=PyPdfExtractionAdapter(),
            jobs=self._jobs,
        )

    def enqueue(
        self,
        *,
        document_id: int,
        kind: str,
        storage_key: str,
        workspace_id: str,
        subject_code: str,
    ) -> ProcessingJobHandle:
        doc = db.session.get(StudioFoundationDocument, document_id)
        if doc is None:
            raise LookupError(f"Document not found: {document_id}")

        job_id = f"cip-{uuid4().hex[:12]}"
        job = self._jobs.create_job(
            document_id=document_id,
            workspace_id=workspace_id,
            subject_code=subject_code,
            kind=kind,
            storage_key=storage_key,
            job_id=job_id,
        )
        db.session.flush()

        final_stage = PipelineStage.QUEUED.value
        if self._auto_run:
            # Commit queued state so extraction can re-read durable rows if needed.
            db.session.commit()
            job = self._coordinator.run_job(job.job_id)
            final_stage = job.status
        else:
            doc.processing_stage = DocumentProcessingStage.QUEUED.value
            db.session.flush()

        logger.info(
            "CIP enqueue document=%s job=%s stage=%s auto_run=%s",
            document_id,
            job.job_id,
            final_stage,
            self._auto_run,
        )
        return ProcessingJobHandle(
            job_id=job.job_id,
            document_id=document_id,
            stage=final_stage,
        )
