"""Text normalisation helpers for extracted curriculum documents."""

from __future__ import annotations

import re
import unicodedata

from app.application.curriculum_intelligence.content_classification_service import (
    ContentClassificationService,
)
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

    def __init__(
        self, classifier: ContentClassificationService | None = None
    ) -> None:
        self._classifier = classifier or ContentClassificationService()

    def normalize(self, extracted: ExtractedDocument) -> ExtractedDocument:
        """Return a copy with normalised whitespace and unicode."""
        pages: list[ExtractedPage] = []
        dropped_chrome = 0
        for page in extracted.pages:
            kept: list[ExtractedBlock] = []
            for b in page.blocks:
                if not self._keep_block(b):
                    continue
                text = self._normalize_text(b.text)
                if (
                    b.kind is not BlockKind.IMAGE
                    and self._classifier.is_boilerplate_line(text)
                ):
                    dropped_chrome += 1
                    continue
                kept.append(
                    ExtractedBlock(
                        block_id=b.block_id,
                        kind=b.kind,
                        text=text,
                        order_index=len(kept),
                        bbox=b.bbox,
                        attributes=b.attributes,
                    )
                )
            raw = self._normalize_text(page.raw_text)
            pages.append(
                ExtractedPage(
                    page_number=page.page_number,
                    width=page.width,
                    height=page.height,
                    blocks=tuple(kept),
                    raw_text=raw,
                )
            )
        diagnostics = [
            *extracted.diagnostics,
            "normalised_whitespace",
            "normalised_unicode_nfkc",
            "stripped_page_chrome",
        ]
        if dropped_chrome:
            diagnostics.append(f"dropped_chrome_blocks={dropped_chrome}")
        return ExtractedDocument(
            extraction_id=extracted.extraction_id,
            document_id=extracted.document_id,
            page_count=len(pages),
            pages=tuple(pages),
            metadata=extracted.metadata,
            diagnostics=tuple(diagnostics),
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
