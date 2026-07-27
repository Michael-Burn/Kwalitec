"""Text normalisation helpers for extracted curriculum documents."""

from __future__ import annotations

import re
import unicodedata

from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind,
    ExtractedBlock,
    ExtractedDocument,
    ExtractedPage,
)

_WS = re.compile(r"[ \t]+")
_BLANK = re.compile(r"\n{3,}")


class DocumentNormalizationService:
    """Deterministic cleanup of extracted text before structural parse."""

    def normalize(self, extracted: ExtractedDocument) -> ExtractedDocument:
        """Return a copy with normalised whitespace and unicode."""
        pages: list[ExtractedPage] = []
        for page in extracted.pages:
            blocks = tuple(
                ExtractedBlock(
                    block_id=b.block_id,
                    kind=b.kind,
                    text=self._normalize_text(b.text),
                    order_index=b.order_index,
                    bbox=b.bbox,
                    attributes=b.attributes,
                )
                for b in page.blocks
                if self._keep_block(b)
            )
            raw = self._normalize_text(page.raw_text)
            pages.append(
                ExtractedPage(
                    page_number=page.page_number,
                    width=page.width,
                    height=page.height,
                    blocks=blocks,
                    raw_text=raw,
                )
            )
        diagnostics = (
            *extracted.diagnostics,
            "normalised_whitespace",
            "normalised_unicode_nfkc",
        )
        return ExtractedDocument(
            extraction_id=extracted.extraction_id,
            document_id=extracted.document_id,
            page_count=len(pages),
            pages=tuple(pages),
            metadata=extracted.metadata,
            diagnostics=diagnostics,
        )

    @staticmethod
    def _normalize_text(text: str) -> str:
        value = unicodedata.normalize("NFKC", text or "")
        value = value.replace("\r\n", "\n").replace("\r", "\n")
        value = _WS.sub(" ", value)
        value = _BLANK.sub("\n\n", value)
        return value.strip()

    @staticmethod
    def _keep_block(block: ExtractedBlock) -> bool:
        if block.kind is BlockKind.IMAGE:
            return True
        return bool((block.text or "").strip())
