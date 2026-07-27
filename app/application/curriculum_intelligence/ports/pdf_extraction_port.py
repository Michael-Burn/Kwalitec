"""PdfExtractionPort — deterministic PDF → structured document.

Implementations must not call LLMs or OCR engines.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument


class PdfExtractionPort(ABC):
    """Extract pages/blocks/metadata from PDF bytes."""

    @abstractmethod
    def extract(
        self,
        pdf_bytes: bytes,
        *,
        extraction_id: str,
        document_id: int,
    ) -> ExtractedDocument:
        """Return a structured ExtractedDocument. Raises on unreadable PDF."""


class EmbeddingExtensionPort(ABC):
    """CIP-003 extension point — intentionally a no-op until embeddings land."""

    @abstractmethod
    def on_ready_for_embeddings(
        self,
        *,
        document_id: int,
        job_id: str,
        graph_id: str,
    ) -> None:
        """Hook invoked when the graph is ready for embedding/retrieval."""


class NullEmbeddingExtension(EmbeddingExtensionPort):
    """Default stub — records nothing, embeds nothing (CIP-003 later)."""

    def on_ready_for_embeddings(
        self,
        *,
        document_id: int,
        job_id: str,
        graph_id: str,
    ) -> None:
        _ = (document_id, job_id, graph_id)
