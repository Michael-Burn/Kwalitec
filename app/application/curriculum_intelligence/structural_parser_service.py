"""StructuralParserService — educational document hierarchy (deterministic)."""

from __future__ import annotations

import re
from uuid import uuid4

from app.application.curriculum_intelligence.content_classification_service import (
    ContentClassificationService,
)
from app.domain.curriculum_intelligence.content_role import ContentRole
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
_CHAPTER = re.compile(
    r"^(?:Page\s+\d+\s+)?(?P<code>CS1-\d+[a-z]?)\s*[:\-]?\s*(?P<title>.*)$",
    re.IGNORECASE,
)
_WEIGHTED_CHAPTER = re.compile(
    r"^(?P<num>\d+)\s+(?P<title>.+?)\s*[\[{]\s*(?P<weight>\d+)\s*%\s*[\]}]\s*$",
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
_ACTION_VERBS = re.compile(
    r"^(?:"
    r"describe|define|explain|understand|apply|evaluate|calculate|construct|"
    r"discuss|compare|state|use|complete|produce|interpret|determine|"
    r"generate|derive|identify|analyse|analyze|assess|perform|fit|"
    r"select|demonstrate|summarise|summarize|outline|list|show|"
    r"compute|estimate|test|prove|solve|recognise|recognize"
    r")\b",
    re.IGNORECASE,
)


class StructuralParserService:
    """Parse extracted blocks into a hierarchical educational structure.

    Heuristic and deterministic — uncertain classifications are flagged
    ``needs_review`` rather than guessed via LLM. Non-educational material is
    tagged with ``content_role`` and excluded from curriculum mapping.
    """

    REVIEW_CONFIDENCE = 0.55

    def __init__(
        self, classifier: ContentClassificationService | None = None
    ) -> None:
        self._classifier = classifier or ContentClassificationService()

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
        rejected = 0

        start_page = self._detect_educational_start_page(extracted)
        educational_started = start_page is None  # permissive when no gate needed
        if start_page is not None:
            educational_started = False
            diagnostics.append(f"educational_start_page={start_page}")
        else:
            diagnostics.append("educational_start_permissive")

        for page in extracted.pages:
            if start_page is not None and page.page_number >= start_page:
                educational_started = True
            for block in page.blocks:
                text = (block.text or "").strip()
                if not text:
                    continue
                if self._classifier.marks_educational_start(text.splitlines()[0]):
                    educational_started = True

                kind, title, body, confidence, attrs = self._classify(
                    block.kind, text, educational_started=educational_started
                )
                role = dict(attrs).get("content_role", ContentRole.EDUCATIONAL.value)
                if role in {
                    ContentRole.NAVIGATION.value,
                    ContentRole.BLANK_ARTEFACT.value,
                }:
                    rejected += 1
                    diagnostics.append(
                        f"Rejected {role} on page {page.page_number}: {title[:60]}"
                    )
                    continue

                needs_review = confidence < self.REVIEW_CONFIDENCE
                if needs_review:
                    diagnostics.append(
                        f"Low-confidence {kind.value} on page {page.page_number}"
                    )
                level = self._level_for(kind, text, attrs)
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

        if rejected:
            diagnostics.append(f"rejected_non_educational_nodes={rejected}")
        if educational_started or start_page is None:
            diagnostics.append("educational_body_detected")
        else:
            diagnostics.append("educational_body_not_detected")

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

    def _detect_educational_start_page(
        self, extracted: ExtractedDocument
    ) -> int | None:
        """Return page where educational body begins, or None for permissive mode.

        CMP packs with publisher chrome are gated until the first ``CS1-NN`` chapter.
        Syllabus PDFs start at the first weighted topic. Synthetic fixtures without
        chrome remain permissive so existing pipeline tests stay valid.
        """
        has_chrome = False
        first_chapter: int | None = None
        first_weighted: int | None = None
        for page in extracted.pages:
            for block in page.blocks:
                line = (block.text or "").strip().splitlines()[0] if block.text else ""
                if not line:
                    continue
                role = self._classifier.classify_line(line)
                if role in {
                    ContentRole.PUBLISHER_METADATA,
                    ContentRole.COPYRIGHT,
                    ContentRole.FRONT_MATTER,
                    ContentRole.QUALIFICATION_INFORMATION,
                } or line.upper() == "AGOGO CDO":
                    has_chrome = True
                if _CHAPTER.match(line):
                    if first_chapter is None:
                        first_chapter = page.page_number
                if _WEIGHTED_CHAPTER.match(line) and first_weighted is None:
                    first_weighted = page.page_number
        # Prefer chapter anchors for CMP; weighted topics for syllabus.
        # has_chrome retained for diagnostics only.
        _ = has_chrome
        if first_chapter is not None:
            return first_chapter
        if first_weighted is not None:
            return first_weighted
        # No chapter/weighted anchors — permissive (synthetic fixtures).
        return None

    def _classify(
        self,
        block_kind: BlockKind,
        text: str,
        *,
        educational_started: bool,
    ) -> tuple[StructuralKind, str, str, float, tuple[tuple[str, str], ...]]:
        line = text.splitlines()[0].strip()
        attrs: list[tuple[str, str]] = []
        role = self._classifier.classify_line(line)

        # Before educational body: demote non-start headings to front matter.
        if not educational_started and not self._classifier.marks_educational_start(
            line
        ):
            if role == ContentRole.EDUCATIONAL:
                role = ContentRole.FRONT_MATTER
            attrs.append(("content_role", role.value))
            if role != ContentRole.EDUCATIONAL:
                return (
                    StructuralKind.PARAGRAPH,
                    line[:120],
                    text,
                    0.4,
                    tuple(attrs),
                )

        attrs.append(("content_role", role.value))

        if block_kind is BlockKind.TABLE:
            return StructuralKind.TABLE, "Table", text, 0.85, tuple(attrs)
        if block_kind is BlockKind.IMAGE:
            attrs.append(("media", "image"))
            return StructuralKind.UNKNOWN, "Image", text, 0.4, tuple(attrs)

        ch = _CHAPTER.match(line)
        if ch:
            code = ch.group("code")
            title = (ch.group("title") or "").strip() or code
            # ActEd running headers look like "CS1-01: Title Page 12".
            # Keep them as chapter markers (unique per code) rather than dropping
            # all CS1-NN signals — otherwise CMP modules never form.
            is_running = bool(re.search(r"\bpage\s+\d+\b", line, re.IGNORECASE))
            if is_running:
                title = re.sub(
                    r"\s+page\s+\d+\s*$", "", title, flags=re.IGNORECASE
                ).strip()
                title = title or code
                attrs.append(("section_number", code))
                attrs.append(("chapter_code", code))
                attrs.append(("running_header", "true"))
                # Low-confidence chapter cue — mapping dedupes by chapter_code.
                label = (
                    f"{code}: {title}" if title.upper() != code.upper() else code
                )
                return (
                    StructuralKind.NUMBERED_SECTION,
                    label,
                    text,
                    0.72,
                    tuple(attrs),
                )
            attrs.append(("section_number", code))
            attrs.append(("chapter_code", code))
            return (
                StructuralKind.NUMBERED_SECTION,
                f"{code}: {title}" if title != code else code,
                text,
                0.95,
                tuple(attrs),
            )

        weighted = _WEIGHTED_CHAPTER.match(line)
        if weighted:
            attrs.append(("section_number", weighted.group("num")))
            attrs.append(("topic_weight_pct", weighted.group("weight")))
            return (
                StructuralKind.NUMBERED_SECTION,
                weighted.group("title").strip(),
                text,
                0.96,
                tuple(attrs),
            )

        if block_kind is BlockKind.HEADING:
            m = _NUMBERED_SECTION.match(line)
            if m:
                return self._numbered_node(m, text, attrs)
            if role.value in {
                ContentRole.FRONT_MATTER.value,
                ContentRole.QUALIFICATION_INFORMATION.value,
                ContentRole.ASSESSMENT_LOGISTICS.value,
                ContentRole.TABLE_OF_CONTENTS.value,
                ContentRole.PUBLISHER_METADATA.value,
            }:
                return StructuralKind.PARAGRAPH, line[:120], text, 0.35, tuple(attrs)
            return StructuralKind.HEADING, line, text, 0.85, tuple(attrs)

        m = _NUMBERED_SECTION.match(line)
        if m:
            return self._numbered_node(m, text, attrs)

        m = _DEFINITION.match(line)
        if m:
            body = m.group("body").strip() or text
            attrs[-1] = ("content_role", ContentRole.DEFINITION.value)
            return StructuralKind.DEFINITION, "Definition", body, 0.82, tuple(attrs)

        m = _EXAMPLE.match(line)
        if m:
            kind = (
                StructuralKind.WORKED_EXAMPLE
                if line.lower().startswith("worked")
                else StructuralKind.EXAMPLE
            )
            body = m.group("body").strip() or text
            attrs[-1] = (
                "content_role",
                ContentRole.WORKED_EXAMPLE.value
                if kind is StructuralKind.WORKED_EXAMPLE
                else ContentRole.EXAMPLE.value,
            )
            return kind, kind.value.replace("_", " ").title(), body, 0.8, tuple(attrs)

        m = _PRACTICE.match(line)
        if m:
            body = m.group("body").strip() or text
            attrs[-1] = ("content_role", ContentRole.EXERCISE.value)
            return (
                StructuralKind.PRACTICE_QUESTION,
                "Practice",
                body,
                0.78,
                tuple(attrs),
            )

        m = _WARNING.match(line)
        if m:
            return (
                StructuralKind.WARNING,
                "Warning",
                m.group("body").strip(),
                0.8,
                tuple(attrs),
            )

        m = _NOTE.match(line)
        if m:
            return (
                StructuralKind.NOTE,
                "Note",
                m.group("body").strip(),
                0.8,
                tuple(attrs),
            )

        m = _REFERENCE.match(line)
        if m:
            return (
                StructuralKind.REFERENCE,
                "Reference",
                m.group("body").strip(),
                0.75,
                tuple(attrs),
            )

        if _LIST_ITEM.match(line) or block_kind is BlockKind.LIST_ITEM:
            return StructuralKind.LIST_ITEM, line[:120], text, 0.7, tuple(attrs)

        if _FORMULA.search(text) and len(text) < 280:
            attrs[-1] = ("content_role", ContentRole.FORMULA.value)
            return StructuralKind.FORMULA_BLOCK, "Formula", text, 0.65, tuple(attrs)

        if self._looks_like_heading(line, role):
            return StructuralKind.HEADING, line, text, 0.6, tuple(attrs)

        return StructuralKind.PARAGRAPH, line[:120], text, 0.7, tuple(attrs)

    def _numbered_node(
        self,
        match: re.Match[str],
        text: str,
        attrs: list[tuple[str, str]],
    ) -> tuple[StructuralKind, str, str, float, tuple[tuple[str, str], ...]]:
        num = match.group("num")
        title = match.group("title").strip()
        depth = num.count(".")
        attrs.append(("section_number", num))
        attrs.append(("number_depth", str(depth)))
        # Depth ≥2 syllabus/CMP items are learning objectives when educational.
        if depth >= 2:
            attrs.append(("educational_role", "learning_objective"))
            for i, (k, _v) in enumerate(attrs):
                if k == "content_role":
                    attrs[i] = ("content_role", ContentRole.LEARNING_OBJECTIVE.value)
                    break
            return (
                StructuralKind.SUB_HEADING,
                title or num,
                text,
                0.92,
                tuple(attrs),
            )
        if depth == 0:
            return (
                StructuralKind.NUMBERED_SECTION,
                title or num,
                text,
                0.9,
                tuple(attrs),
            )
        # depth == 1 → section / topic host
        return StructuralKind.SUB_HEADING, title or num, text, 0.88, tuple(attrs)

    @staticmethod
    def _looks_like_heading(line: str, role: ContentRole) -> bool:
        if role in {
            ContentRole.FRONT_MATTER,
            ContentRole.QUALIFICATION_INFORMATION,
            ContentRole.ASSESSMENT_LOGISTICS,
            ContentRole.TABLE_OF_CONTENTS,
            ContentRole.PUBLISHER_METADATA,
            ContentRole.NAVIGATION,
            ContentRole.COPYRIGHT,
        }:
            return False
        if len(line) > 90 or len(line) < 3:
            return False
        if line.endswith("."):
            return False
        # Reject sentence-like fragments and TOC rows.
        if " page " in line.lower():
            return False
        letters = [c for c in line if c.isalpha()]
        if not letters:
            return False
        upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
        words = line.split()
        # Require strong ALL-CAPS signal OR short Title Case without verbs of prose.
        if upper_ratio >= 0.85 and len(words) <= 8:
            return True
        if (
            line[:1].isupper()
            and ":" not in line
            and len(words) <= 6
            and upper_ratio >= 0.4
        ):
            return True
        return False

    @staticmethod
    def _level_for(
        kind: StructuralKind,
        text: str,
        attrs: list[tuple[str, str]] | tuple[tuple[str, str], ...],
    ) -> int:
        attr_map = dict(attrs)
        if "chapter_code" in attr_map:
            return 1
        if "topic_weight_pct" in attr_map:
            return 1
        depth_s = attr_map.get("number_depth")
        if depth_s is not None:
            return 1 + int(depth_s)
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
                    self._sync_stack(stack, root_children)
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
                    self._sync_stack(stack, root_children)
                else:
                    root_children.append(node)
        return root_children

    @staticmethod
    def _sync_stack(
        stack: list[StructuralNode], root_children: list[StructuralNode]
    ) -> None:
        """Refresh stack entries from the forest after immutable parent updates."""
        by_id: dict[str, StructuralNode] = {}

        def index(nodes: list[StructuralNode] | tuple[StructuralNode, ...]) -> None:
            for n in nodes:
                by_id[n.node_id] = n
                if n.children:
                    index(n.children)

        index(root_children)
        for i, node in enumerate(stack):
            fresh = by_id.get(node.node_id)
            if fresh is not None:
                stack[i] = fresh

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
