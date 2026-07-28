"""PDF → Canonical Structured Document adapter (infrastructure only).

Educational Intelligence never consumes PDF bytes. This adapter converts
``ExtractedDocument`` (via ``PdfExtractionPort``) into a CanonicalDocument.
"""

from __future__ import annotations

from app.application.curriculum_intelligence.ports.pdf_extraction_port import (
    PdfExtractionPort,
)
from app.domain.curriculum_extraction.canonical_document import (
    BlockKind,
    CanonicalBlock,
    CanonicalDocument,
    CanonicalPage,
    DocumentKind,
)
from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind as ExtractedBlockKind,
)
from app.domain.curriculum_intelligence.extracted_document import (
    ExtractedDocument,
)

_KIND_MAP = {
    ExtractedBlockKind.HEADING: BlockKind.HEADING,
    ExtractedBlockKind.PARAGRAPH: BlockKind.PARAGRAPH,
    ExtractedBlockKind.TABLE: BlockKind.TABLE,
    ExtractedBlockKind.LIST_ITEM: BlockKind.LIST_ITEM,
    ExtractedBlockKind.IMAGE: BlockKind.OTHER,
    ExtractedBlockKind.OTHER: BlockKind.OTHER,
}


class PdfCanonicalAdapter:
    """Infrastructure adapter: PDF bytes → CanonicalDocument.

    Uses ``PdfExtractionPort`` for deterministic text extraction. Does not
    modify CIP pipeline stage contracts.
    """

    def __init__(self, extractor: PdfExtractionPort) -> None:
        self._extractor = extractor

    def to_canonical(
        self,
        pdf_bytes: bytes,
        *,
        document_id: str,
        document_kind: DocumentKind | str,
        title: str,
        source_ref: str,
        extraction_id: str,
        numeric_document_id: int = 0,
        metadata: tuple[tuple[str, str], ...] = (),
    ) -> CanonicalDocument:
        """Extract PDF bytes then map to a Canonical Structured Document."""
        if not pdf_bytes:
            raise ValueError("pdf_bytes must be non-empty")
        extracted = self._extractor.extract(
            pdf_bytes,
            extraction_id=extraction_id,
            document_id=numeric_document_id,
        )
        return self.from_extracted(
            extracted,
            document_id=document_id,
            document_kind=document_kind,
            title=title,
            source_ref=source_ref,
            metadata=metadata,
        )

    def from_extracted(
        self,
        extracted: ExtractedDocument,
        *,
        document_id: str,
        document_kind: DocumentKind | str,
        title: str,
        source_ref: str,
        metadata: tuple[tuple[str, str], ...] = (),
    ) -> CanonicalDocument:
        """Map an already-extracted CIP document into Canonical form."""
        kind = (
            document_kind
            if isinstance(document_kind, DocumentKind)
            else DocumentKind(document_kind)
        )
        pages: list[CanonicalPage] = []
        for page in extracted.pages:
            blocks: list[CanonicalBlock] = []
            for block in page.blocks:
                blocks.append(
                    CanonicalBlock(
                        block_id=block.block_id,
                        kind=_KIND_MAP.get(block.kind, BlockKind.OTHER),
                        text=block.text or "",
                        level=1 if block.kind is ExtractedBlockKind.HEADING else 0,
                        structural_path=f"p{page.page_number}/{block.block_id}",
                        attributes=block.attributes,
                    )
                )
            pages.append(
                CanonicalPage(
                    page_number=page.page_number,
                    blocks=tuple(blocks),
                )
            )
        merged_meta = tuple(extracted.metadata) + metadata
        return CanonicalDocument(
            document_id=document_id,
            document_kind=kind,
            title=title,
            source_ref=source_ref,
            pages=tuple(pages),
            metadata=merged_meta,
        )
