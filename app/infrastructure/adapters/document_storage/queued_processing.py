"""Phase-1 processing adapter — marks documents as queued for future workers."""

from __future__ import annotations

import logging
from uuid import uuid4

from app.application.curriculum_studio.ports.document_processing_port import (
    DocumentProcessingPort,
    ProcessingJobHandle,
)
from app.domain.curriculum_documents.processing_stage import DocumentProcessingStage
from app.extensions import db
from app.models.curriculum_studio_foundation import StudioFoundationDocument

logger = logging.getLogger(__name__)


class QueuedDocumentProcessingAdapter(DocumentProcessingPort):
    """Enqueue-only adapter for Phase 1.

    Persists processing_stage=queued and a job id. OCR / extract / embed
    workers in later phases consume QUEUED rows.
    """

    def enqueue(
        self,
        *,
        document_id: int,
        kind: str,
        storage_key: str,
        workspace_id: str,
        subject_code: str,
    ) -> ProcessingJobHandle:
        job_id = f"docjob-{uuid4().hex[:12]}"
        doc = db.session.get(StudioFoundationDocument, document_id)
        if doc is None:
            raise LookupError(f"Document not found: {document_id}")
        doc.processing_stage = DocumentProcessingStage.QUEUED.value
        db.session.flush()
        logger.info(
            "Enqueued curriculum document id=%s kind=%s job=%s workspace=%s subject=%s",
            document_id,
            kind,
            job_id,
            workspace_id,
            subject_code,
        )
        # storage_key retained for future workers; unused in Phase 1.
        _ = storage_key
        return ProcessingJobHandle(
            job_id=job_id,
            document_id=document_id,
            stage=DocumentProcessingStage.QUEUED.value,
        )
