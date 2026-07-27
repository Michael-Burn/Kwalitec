"""CIP-003 EmbeddingExtensionPort implementation — indexes entities after ready."""

from __future__ import annotations

import logging

from app.application.curriculum_intelligence.ports.pdf_extraction_port import (
    EmbeddingExtensionPort,
)
from app.application.curriculum_retrieval.vector_index_service import VectorIndexService
from app.models.curriculum_intelligence import CipProcessingJob

logger = logging.getLogger(__name__)


class RetrievalEmbeddingExtension(EmbeddingExtensionPort):
    """Hook invoked at READY_FOR_EMBEDDINGS — builds the evidence retrieval index."""

    def __init__(self, vector_index: VectorIndexService | None = None) -> None:
        self._index = vector_index or VectorIndexService()

    def on_ready_for_embeddings(
        self,
        *,
        document_id: int,
        job_id: str,
        graph_id: str,
    ) -> None:
        workspace_id = ""
        job = CipProcessingJob.query.filter_by(job_id=job_id).first()
        if job is not None:
            workspace_id = job.workspace_id or ""
        try:
            count = self._index.rebuild_document(
                document_id=document_id,
                workspace_id=workspace_id,
                job_id=job_id,
                graph_id=graph_id,
            )
            logger.info(
                "CIP-003 indexed %s embeddings for document=%s job=%s",
                count,
                document_id,
                job_id,
            )
        except Exception:  # noqa: BLE001 — never fail the CIP pipeline on embed errors
            logger.exception(
                "CIP-003 embedding index failed for document=%s job=%s",
                document_id,
                job_id,
            )
