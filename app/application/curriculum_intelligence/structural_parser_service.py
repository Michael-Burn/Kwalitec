"""StructuralParserService — educational document hierarchy (deterministic)."""

from __future__ import annotations

import re
from uuid import uuid4

from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind,
    ExtractedDocument,
)
from app.domain.curriculum_intelligence.structural_document import (
    StructuralDocument,
    StructuralKind,
    StructuralNode,
)

_NUMBERED_SECTION = re.compile(
    r"^(?P<num>\d+(?:\.\d+){0,4})\s+(?P<title>.+)$",
    re.IGNORECASE,
)
_LIST_ITEM = re.compile(r"^(?:[-*•]|\d+[.)])\s+\S")
_DEFINITION = re.compile(
    r"^(?:definition|define[sd]?)\b[:\s-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_EXAMPLE = re.compile(
    r"^(?:worked\s+example|example)\b[:\s-]*(?P<body>.*)$",
    re.IGNORECASE,
)
_PRACTICE = re.compile(
    r"^(?:practice|exercise|question|problem)\s*(?:\d+[.)]?)?\s*[:\-]?\s*(?P<body>.*)$",
    re.IGNORECASE,
)
_NOTE = re.compile(r"^(?:note|n\.b\.)\b[:\s-]*(?P<body>.+)$", re.IGNORECASE)
_WARNING = re.compile(
    r"^(?:warning|caution|important)\b[:\s-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_REFERENCE = re.compile(
    r"^(?:reference|see also|further reading)\b[:\s-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_FORMULA = re.compile(r"(?:=|≈|≤|≥|∑|∫|√)|(?:\b[A-Za-z]\s*=\s*)|(?:\([^)]+=[^)]+\))")


class StructuralParserService:
    """Parse extracted blocks into a hierarchical educational structure.

    Heuristic and deterministic — uncertain classifications are flagged
    ``needs_review`` rather than guessed via LLM.
    """

    REVIEW_CONFIDENCE = 0.55

    def parse(
        self,
        extracted: ExtractedDocument,
        *,
        parse_id: str | None = None,
    ) -> StructuralDocument:
        """Build a StructuralDocument from an ExtractedDocument."""
        pid = (parse_id or "").strip() or f"parse-{uuid4().hex[:12]}"
        flat: list[StructuralNode] = []
        diagnostics: list[str] = []

        for page in extracted.pages:
            for block in page.blocks:
                text = (block.text or "").strip()
                if not text:
                    continue
                kind, title, body, confidence, attrs = self._classify(block.kind, text)
                needs_review = confidence < self.REVIEW_CONFIDENCE
                if needs_review:
                    diagnostics.append(
                        f"Low-confidence {kind.value} on page {page.page_number}"
                    )
                level = self._level_for(kind, text)
                flat.append(
                    StructuralNode(
                        node_id=f"sn-{uuid4().hex[:10]}",
                        kind=kind,
                        title=title[:500],
                        text=body,
                        level=level,
                        source_page=page.page_number,
                        source_block_ids=(block.block_id,),
                        children=(),
                        confidence=confidence,
                        needs_review=needs_review,
                        attributes=attrs,
                    )
                )

        root_children = self._nest(flat)
        root = StructuralNode(
            node_id=f"sn-root-{uuid4().hex[:8]}",
            kind=StructuralKind.DOCUMENT,
            title=extracted.metadata_value("title")
            or f"Document {extracted.document_id}",
            text="",
            level=0,
            source_page=None,
            source_block_ids=(),
            children=tuple(root_children),
            confidence=1.0,
            needs_review=False,
        )
        return StructuralDocument(
            parse_id=pid,
            extraction_id=extracted.extraction_id,
            document_id=extracted.document_id,
            root=root,
            diagnostics=tuple(diagnostics),
        )

    def _classify(
        self, block_kind: BlockKind, text: str
    ) -> tuple[StructuralKind, str, str, float, tuple[tuple[str, str], ...]]:
        line = text.splitlines()[0].strip()
        attrs: list[tuple[str, str]] = []

        if block_kind is BlockKind.TABLE:
            return StructuralKind.TABLE, "Table", text, 0.85, ()
        if block_kind is BlockKind.IMAGE:
            return StructuralKind.UNKNOWN, "Image", text, 0.4, (("media", "image"),)
        if block_kind is BlockKind.HEADING:
            m = _NUMBERED_SECTION.match(line)
            if m:
                attrs.append(("section_number", m.group("num")))
                return (
                    StructuralKind.NUMBERED_SECTION,
                    m.group("title").strip() or line,
                    text,
                    0.9,
                    tuple(attrs),
                )
            return StructuralKind.HEADING, line, text, 0.85, ()

        m = _NUMBERED_SECTION.match(line)
        if m:
            attrs.append(("section_number", m.group("num")))
            depth = m.group("num").count(".")
            kind = (
                StructuralKind.NUMBERED_SECTION
                if depth == 0
                else StructuralKind.SUB_HEADING
            )
            return kind, m.group("title").strip() or line, text, 0.88, tuple(attrs)

        m = _DEFINITION.match(line)
        if m:
            body = m.group("body").strip() or text
            return StructuralKind.DEFINITION, "Definition", body, 0.82, ()

        m = _EXAMPLE.match(line)
        if m:
            kind = (
                StructuralKind.WORKED_EXAMPLE
                if line.lower().startswith("worked")
                else StructuralKind.EXAMPLE
            )
            body = m.group("body").strip() or text
            return kind, kind.value.replace("_", " ").title(), body, 0.8, ()

        m = _PRACTICE.match(line)
        if m:
            body = m.group("body").strip() or text
            return StructuralKind.PRACTICE_QUESTION, "Practice", body, 0.78, ()

        m = _WARNING.match(line)
        if m:
            return StructuralKind.WARNING, "Warning", m.group("body").strip(), 0.8, ()

        m = _NOTE.match(line)
        if m:
            return StructuralKind.NOTE, "Note", m.group("body").strip(), 0.8, ()

        m = _REFERENCE.match(line)
        if m:
            return (
                StructuralKind.REFERENCE,
                "Reference",
                m.group("body").strip(),
                0.75,
                (),
            )

        if _LIST_ITEM.match(line) or block_kind is BlockKind.LIST_ITEM:
            return StructuralKind.LIST_ITEM, line[:120], text, 0.7, ()

        if _FORMULA.search(text) and len(text) < 280:
            return StructuralKind.FORMULA_BLOCK, "Formula", text, 0.65, ()

        if self._looks_like_heading(line):
            return StructuralKind.HEADING, line, text, 0.6, ()

        return StructuralKind.PARAGRAPH, line[:120], text, 0.7, ()

    @staticmethod
    def _looks_like_heading(line: str) -> bool:
        if len(line) > 90 or len(line) < 3:
            return False
        if line.endswith("."):
            return False
        letters = [c for c in line if c.isalpha()]
        if not letters:
            return False
        upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
        return upper_ratio >= 0.7 or (
            line[:1].isupper() and ":" not in line and len(line.split()) <= 10
        )

    @staticmethod
    def _level_for(kind: StructuralKind, text: str) -> int:
        if kind is StructuralKind.DOCUMENT:
            return 0
        if kind is StructuralKind.NUMBERED_SECTION:
            m = _NUMBERED_SECTION.match(text.splitlines()[0].strip())
            if m:
                return 1 + m.group("num").count(".")
            return 1
        if kind in {StructuralKind.HEADING, StructuralKind.SUB_HEADING}:
            return 2 if kind is StructuralKind.SUB_HEADING else 1
        return 3

    def _nest(self, flat: list[StructuralNode]) -> list[StructuralNode]:
        """Nest nodes by heading level into a forest under the document root."""
        if not flat:
            return []
        root_children: list[StructuralNode] = []
        stack: list[StructuralNode] = []

        for node in flat:
            is_section = node.kind in {
                StructuralKind.HEADING,
                StructuralKind.SUB_HEADING,
                StructuralKind.NUMBERED_SECTION,
            }
            if is_section:
                while stack and stack[-1].level >= node.level:
                    stack.pop()
                placed = node
                if stack:
                    parent = stack[-1]
                    updated = self._with_child(parent, placed)
                    stack[-1] = updated
                    self._replace_in_forest(root_children, parent.node_id, updated)
                    stack.append(placed)
                else:
                    root_children.append(placed)
                    stack.append(placed)
            else:
                if stack:
                    parent = stack[-1]
                    updated = self._with_child(parent, node)
                    stack[-1] = updated
                    self._replace_in_forest(root_children, parent.node_id, updated)
                else:
                    root_children.append(node)
        return root_children

    @staticmethod
    def _with_child(parent: StructuralNode, child: StructuralNode) -> StructuralNode:
        return StructuralNode(
            node_id=parent.node_id,
            kind=parent.kind,
            title=parent.title,
            text=parent.text,
            level=parent.level,
            source_page=parent.source_page,
            source_block_ids=parent.source_block_ids,
            children=(*parent.children, child),
            confidence=parent.confidence,
            needs_review=parent.needs_review,
            attributes=parent.attributes,
        )

    def _replace_in_forest(
        self,
        nodes: list[StructuralNode],
        node_id: str,
        replacement: StructuralNode,
    ) -> bool:
        for i, node in enumerate(nodes):
            if node.node_id == node_id:
                nodes[i] = replacement
                return True
            children = list(node.children)
            if self._replace_in_forest(children, node_id, replacement):
                nodes[i] = StructuralNode(
                    node_id=node.node_id,
                    kind=node.kind,
                    title=node.title,
                    text=node.text,
                    level=node.level,
                    source_page=node.source_page,
                    source_block_ids=node.source_block_ids,
                    children=tuple(children),
                    confidence=node.confidence,
                    needs_review=node.needs_review,
                    attributes=node.attributes,
                )
                return True
        return False
