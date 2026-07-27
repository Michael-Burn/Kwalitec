"""Educational structural parse tree (deterministic heuristics)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class StructuralKind(StrEnum):
    """Recognised educational document structures."""

    DOCUMENT = "document"
    HEADING = "heading"
    SUB_HEADING = "sub_heading"
    NUMBERED_SECTION = "numbered_section"
    LIST = "list"
    LIST_ITEM = "list_item"
    TABLE = "table"
    EXAMPLE = "example"
    DEFINITION = "definition"
    FORMULA_BLOCK = "formula_block"
    WORKED_EXAMPLE = "worked_example"
    PRACTICE_QUESTION = "practice_question"
    NOTE = "note"
    WARNING = "warning"
    REFERENCE = "reference"
    PARAGRAPH = "paragraph"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class StructuralNode:
    """Hierarchical node produced by StructuralParserService."""

    node_id: str
    kind: StructuralKind
    title: str
    text: str
    level: int
    source_page: int | None
    source_block_ids: tuple[str, ...]
    children: tuple[StructuralNode, ...]
    confidence: float
    needs_review: bool = False
    attributes: tuple[tuple[str, str], ...] = ()

    def attribute(self, key: str) -> str | None:
        for k, v in self.attributes:
            if k == key:
                return v
        return None


@dataclass(frozen=True)
class StructuralDocument:
    """Root parse result for one extracted document."""

    parse_id: str
    extraction_id: str
    document_id: int
    root: StructuralNode
    diagnostics: tuple[str, ...] = ()
