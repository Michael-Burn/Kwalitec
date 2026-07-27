"""Deterministic PDF extraction value objects (no LLM / OCR).

Extraction output is stored separately from curriculum business entities.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class BlockKind(StrEnum):
    """Low-level extracted block kinds from deterministic PDF parsing."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    TABLE = "table"
    IMAGE = "image"
    LIST_ITEM = "list_item"
    OTHER = "other"


@dataclass(frozen=True)
class ExtractedBlock:
    """A contiguous text or structural unit on a page."""

    block_id: str
    kind: BlockKind
    text: str
    order_index: int
    bbox: tuple[float, float, float, float] | None = None
    attributes: tuple[tuple[str, str], ...] = ()

    def attribute(self, key: str) -> str | None:
        for k, v in self.attributes:
            if k == key:
                return v
        return None


@dataclass(frozen=True)
class ExtractedPage:
    """One PDF page of extracted content."""

    page_number: int
    width: float | None
    height: float | None
    blocks: tuple[ExtractedBlock, ...]
    raw_text: str


@dataclass(frozen=True)
class ExtractedDocument:
    """Structured document produced by DocumentExtractionService.

    Never written directly into Subject / Topic / Mission entities.
    """

    extraction_id: str
    document_id: int
    page_count: int
    pages: tuple[ExtractedPage, ...]
    metadata: tuple[tuple[str, str], ...] = ()
    diagnostics: tuple[str, ...] = ()

    def metadata_value(self, key: str) -> str | None:
        for k, v in self.metadata:
            if k == key:
                return v
        return None

    @property
    def full_text(self) -> str:
        return "\n\n".join(p.raw_text for p in self.pages if p.raw_text.strip())
