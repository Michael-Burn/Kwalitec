"""Structural Parsing — heading hierarchy and educational object cues."""

from __future__ import annotations

import re

from app.application.curriculum_extraction.models import (
    ParsedCrossReferenceCue,
    ParsedHeading,
    ParsedObjectCue,
    ParsedPrerequisiteCue,
    StructuralParseResult,
)
from app.domain.curriculum_extraction.canonical_document import (
    BlockKind,
    CanonicalDocument,
    StructuralLocator,
)
from app.domain.curriculum_extraction.provenance import ExtractionMethod

_NUMBERED_HEADING = re.compile(
    r"^(?P<num>\d+(?:\.\d+){0,5})\s+[—\-:]?\s*(?P<title>.+)$"
)
_DEFINITION = re.compile(
    r"^(?:definition)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_FORMULA = re.compile(
    r"^(?:formula)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_WORKED = re.compile(
    r"^(?:worked\s+example|example)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_PRACTICE = re.compile(
    r"^(?:practice|exercise|question)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_READING = re.compile(
    r"^(?:reading|reference|cmp\s*ref|further\s+reading)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_STUDY_TIME = re.compile(
    r"^(?:estimated\s+study\s+time|study\s+time)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_DIFFICULTY = re.compile(
    r"^(?:difficulty)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_PREREQ = re.compile(
    r"^(?:prerequisite|requires)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_CROSS = re.compile(
    r"^(?:see\s+also|cross[\s-]?reference)\b[:\s—-]*(?P<body>.+)$",
    re.IGNORECASE,
)
_NUMBER_TOKEN = re.compile(r"\d+(?:\.\d+){0,5}")
_INLINE_FORMULA = re.compile(
    r"(?:=|≈|≤|≥|∑|∫|√)|(?:\b[A-Za-z]\s*=\s*[^=]+)"
)


class StructuralParserService:
    """Parse Canonical Documents into headings and educational cues.

    Deterministic heuristics only — no LLM / OCR.
    """

    STAGE_ID = "structural_parsing"

    def parse(self, document: CanonicalDocument) -> StructuralParseResult:
        """Extract headings and object cues from one Canonical Document."""
        result = StructuralParseResult(
            document_id=document.document_id,
            document_kind=document.document_kind,
        )
        heading_stack: list[str] = []
        current_number = ""

        for page, block in document.all_blocks():
            text = (block.text or "").strip()
            if not text:
                continue
            first_line = text.splitlines()[0].strip()
            locator = StructuralLocator.create(
                document.document_id,
                page_number=page.page_number,
                block_id=block.block_id,
                structural_path=block.structural_path
                or "/".join(heading_stack)
                or first_line[:80],
                section_heading=heading_stack[-1] if heading_stack else "",
                paragraph_or_table_ref=(
                    f"{block.kind.value}:{block.block_id}"
                ),
            )

            heading = self._try_heading(
                block.kind, first_line, text, locator, document
            )
            if heading is not None:
                result.headings.append(heading)
                current_number = heading.number
                self._update_heading_stack(heading_stack, heading)
                continue

            cue = self._try_object_cue(
                first_line, text, locator, document, current_number
            )
            if cue is not None:
                result.object_cues.append(cue)
                continue

            prereq = self._try_prerequisite(
                first_line, locator, document, current_number
            )
            if prereq is not None:
                result.prerequisite_cues.append(prereq)
                continue

            cross = self._try_cross_reference(
                first_line, locator, document, current_number
            )
            if cross is not None:
                result.cross_reference_cues.append(cross)
                continue

            if (
                block.kind is BlockKind.PARAGRAPH
                and _INLINE_FORMULA.search(text)
                and current_number
            ):
                result.object_cues.append(
                    ParsedObjectCue(
                        object_kind="formula",
                        title=f"Formula near {current_number}",
                        body=text[:500],
                        locator=locator,
                        document_kind=document.document_kind,
                        confidence=88,
                        extraction_method=ExtractionMethod.HEURISTIC,
                        attributes=(("host_number", current_number),),
                    )
                )

        if not result.headings:
            result.diagnostics.append(
                f"No numbered headings found in {document.document_id}"
            )
        return result

    def _try_heading(
        self,
        kind: BlockKind,
        first_line: str,
        text: str,
        locator: StructuralLocator,
        document: CanonicalDocument,
    ) -> ParsedHeading | None:
        match = _NUMBERED_HEADING.match(first_line)
        if match is None:
            return None
        if kind not in {
            BlockKind.HEADING,
            BlockKind.PARAGRAPH,
            BlockKind.LIST_ITEM,
            BlockKind.OTHER,
        }:
            return None
        number = match.group("num")
        title = match.group("title").strip()
        depth = number.count(".") + 1
        return ParsedHeading(
            number=number,
            title=title,
            depth=depth,
            locator=locator,
            document_kind=document.document_kind,
            raw_text=text,
        )

    def _try_object_cue(
        self,
        first_line: str,
        text: str,
        locator: StructuralLocator,
        document: CanonicalDocument,
        current_number: str,
    ) -> ParsedObjectCue | None:
        patterns: list[tuple[re.Pattern[str], str, int]] = [
            (_DEFINITION, "definition", 92),
            (_FORMULA, "formula", 93),
            (_WORKED, "worked_example", 91),
            (_PRACTICE, "practice_exercise", 90),
            (_READING, "reading_reference", 94),
            (_STUDY_TIME, "study_time", 96),
            (_DIFFICULTY, "difficulty", 96),
        ]
        for pattern, kind, confidence in patterns:
            match = pattern.match(first_line)
            if match is None:
                continue
            body = (match.group("body") or "").strip() or text
            title = body.splitlines()[0][:200] if body else kind.replace("_", " ")
            attrs: list[tuple[str, str]] = []
            if current_number:
                attrs.append(("host_number", current_number))
            method = (
                ExtractionMethod.STRUCTURED_FIELD
                if confidence >= 94
                else ExtractionMethod.HEURISTIC
            )
            # Syllabus LOs expressed as numbered headings are not object cues.
            return ParsedObjectCue(
                object_kind=kind,
                title=title,
                body=body,
                locator=locator,
                document_kind=document.document_kind,
                confidence=confidence,
                extraction_method=method,
                attributes=tuple(attrs),
            )
        return None

    def _try_prerequisite(
        self,
        first_line: str,
        locator: StructuralLocator,
        document: CanonicalDocument,
        current_number: str,
    ) -> ParsedPrerequisiteCue | None:
        match = _PREREQ.match(first_line)
        if match is None or not current_number:
            return None
        numbers = _NUMBER_TOKEN.findall(match.group("body") or "")
        if not numbers:
            return None
        return ParsedPrerequisiteCue(
            from_number=current_number,
            to_number=numbers[0],
            locator=locator,
            document_kind=document.document_kind,
        )

    def _try_cross_reference(
        self,
        first_line: str,
        locator: StructuralLocator,
        document: CanonicalDocument,
        current_number: str,
    ) -> ParsedCrossReferenceCue | None:
        match = _CROSS.match(first_line)
        if match is None or not current_number:
            return None
        numbers = _NUMBER_TOKEN.findall(match.group("body") or "")
        if not numbers:
            return None
        return ParsedCrossReferenceCue(
            from_number=current_number,
            to_number=numbers[0],
            locator=locator,
            document_kind=document.document_kind,
        )

    def _update_heading_stack(
        self, stack: list[str], heading: ParsedHeading
    ) -> None:
        label = f"{heading.number} {heading.title}"
        while len(stack) >= heading.depth:
            stack.pop()
        stack.append(label)
