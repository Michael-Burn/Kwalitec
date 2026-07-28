"""Canonical Structured Document — Educational Intelligence input contract.

Educational Intelligence never operates on PDF bytes. Adapters (PDF, Word,
HTML, …) must produce CanonicalDocuments before the extraction pipeline runs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DocumentKind(StrEnum):
    """Supported curriculum source document kinds."""

    CMP = "cmp"
    SYLLABUS = "syllabus"


class BlockKind(StrEnum):
    """Structural block kinds inside a Canonical Document."""

    HEADING = "heading"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    LIST = "list"
    LIST_ITEM = "list_item"
    CAPTION = "caption"
    OTHER = "other"


@dataclass(frozen=True)
class StructuralLocator:
    """Permanent structural reference back to a Canonical Document location."""

    document_id: str
    page_number: int | None
    block_id: str | None
    structural_path: str
    section_heading: str
    paragraph_or_table_ref: str

    @classmethod
    def create(
        cls,
        document_id: str,
        *,
        page_number: int | None = None,
        block_id: str | None = None,
        structural_path: str = "",
        section_heading: str = "",
        paragraph_or_table_ref: str = "",
    ) -> StructuralLocator:
        """Build a locator after normalising identifiers."""
        doc = (document_id or "").strip()
        if not doc:
            raise ValueError("document_id must be non-empty")
        if page_number is not None and page_number < 1:
            raise ValueError("page_number must be >= 1 when set")
        return cls(
            document_id=doc,
            page_number=page_number,
            block_id=(block_id or "").strip() or None,
            structural_path=(structural_path or "").strip(),
            section_heading=(section_heading or "").strip(),
            paragraph_or_table_ref=(paragraph_or_table_ref or "").strip(),
        )


@dataclass(frozen=True)
class CanonicalBlock:
    """One structural unit on a canonical page."""

    block_id: str
    kind: BlockKind
    text: str
    level: int = 0
    structural_path: str = ""
    attributes: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not (self.block_id or "").strip():
            raise ValueError("block_id must be non-empty")
        if self.level < 0:
            raise ValueError("level must be non-negative")

    def attribute(self, key: str) -> str | None:
        for k, v in self.attributes:
            if k == key:
                return v
        return None


@dataclass(frozen=True)
class CanonicalPage:
    """One page (or logical page unit) of a Canonical Document."""

    page_number: int
    blocks: tuple[CanonicalBlock, ...]

    def __post_init__(self) -> None:
        if self.page_number < 1:
            raise ValueError("page_number must be >= 1")


@dataclass(frozen=True)
class CanonicalDocument:
    """Canonical Structured Document consumed by the extraction pipeline.

    Never contains PDF bytes. ``source_ref`` is an opaque locator (URI / path
    key) for operator recovery — not embedded content.
    """

    document_id: str
    document_kind: DocumentKind
    title: str
    source_ref: str
    pages: tuple[CanonicalPage, ...]
    metadata: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not (self.document_id or "").strip():
            raise ValueError("document_id must be non-empty")
        if not (self.title or "").strip():
            raise ValueError("title must be non-empty")
        if not (self.source_ref or "").strip():
            raise ValueError("source_ref must be non-empty")
        if not isinstance(self.document_kind, DocumentKind):
            object.__setattr__(
                self, "document_kind", DocumentKind(self.document_kind)
            )

    def metadata_value(self, key: str) -> str | None:
        for k, v in self.metadata:
            if k == key:
                return v
        return None

    @property
    def block_count(self) -> int:
        return sum(len(p.blocks) for p in self.pages)

    def all_blocks(self) -> tuple[tuple[CanonicalPage, CanonicalBlock], ...]:
        """Flatten pages to (page, block) pairs in document order."""
        pairs: list[tuple[CanonicalPage, CanonicalBlock]] = []
        for page in self.pages:
            for block in page.blocks:
                pairs.append((page, block))
        return tuple(pairs)
