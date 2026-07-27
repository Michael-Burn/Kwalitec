"""DocumentExtractionService — PDF bytes → ExtractedDocument."""

from __future__ import annotations

from app.application.curriculum_intelligence.exceptions import ExtractionError
from app.application.curriculum_intelligence.ports.pdf_extraction_port import (
    PdfExtractionPort,
)
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument


class DocumentExtractionService:
    """Deterministic document extraction. No LLM. No OCR. No embeddings."""

    def __init__(self, extractor: PdfExtractionPort) -> None:
        self._extractor = extractor

    def extract(
        self,
        pdf_bytes: bytes,
        *,
        extraction_id: str,
        document_id: int,
    ) -> ExtractedDocument:
        """Extract structured pages/blocks from PDF bytes."""
        if not pdf_bytes:
            raise ExtractionError("PDF payload is empty.", code="empty_pdf")
        if not pdf_bytes.startswith(b"%PDF"):
            raise ExtractionError(
                "Payload is not a PDF document.",
                code="not_pdf",
            )
        try:
            result = self._extractor.extract(
                pdf_bytes,
                extraction_id=extraction_id,
                document_id=document_id,
            )
        except ExtractionError:
            raise
        except Exception as exc:  # noqa: BLE001 — boundary to port
            raise ExtractionError(
                f"Deterministic extraction failed: {exc}",
                code="extractor_error",
            ) from exc
        if result.page_count < 1 or not result.pages:
            raise ExtractionError(
                "Extraction produced no pages.",
                code="empty_extraction",
            )
        return result
