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
    """CIP-003 extension point — index educational entities for retrieval."""

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
    """No-op stub for tests that intentionally skip indexing."""

    def on_ready_for_embeddings(
        self,
        *,
        document_id: int,
        job_id: str,
        graph_id: str,
    ) -> None:
        _ = (document_id, job_id, graph_id)


# Process-local default embedding extension (bound by infrastructure
# composition / tests). Falls back to a no-op when unbound so pipeline
# stages that omit ``embeddings`` injection still complete safely.
_default_embedding_extension: EmbeddingExtensionPort | None = None


def bind_default_embedding_extension_port(
    port: EmbeddingExtensionPort | None,
) -> None:
    """Bind the process-local default embedding extension port."""
    global _default_embedding_extension
    _default_embedding_extension = port


def get_default_embedding_extension_port() -> EmbeddingExtensionPort:
    """Return the bound default embedding extension, or a no-op stub."""
    return _default_embedding_extension or NullEmbeddingExtension()
