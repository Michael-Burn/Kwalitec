"""Curriculum Segmentation — fuse syllabus + CMP into a segment tree."""

from __future__ import annotations

import re

from app.application.curriculum_extraction.exceptions import SegmentationError
from app.application.curriculum_extraction.models import (
    CurriculumSegmentTree,
    ParsedHeading,
    SegmentNode,
    StructuralParseResult,
)
from app.domain.curriculum_extraction.canonical_document import (
    DocumentKind,
    StructuralLocator,
)
from app.domain.curriculum_extraction.provenance import ExtractionMethod

_MINUTES = re.compile(r"(\d+(?:\.\d+)?)\s*(?:h|hr|hours?)?", re.IGNORECASE)
_DIFFICULTY_WORDS = {
    "foundational": "foundational",
    "basic": "foundational",
    "intermediate": "intermediate",
    "advanced": "advanced",
    "capstone": "capstone",
}


class CurriculumSegmentationService:
    """Build Subject → Topic → Section → Subsection → LO skeleton.

    Syllabus headings drive learning objectives / outcomes.
    CMP headings deepen section/subsection hosts for educational objects.
    """

    STAGE_ID = "curriculum_segmentation"

    def segment(
        self,
        *,
        subject_code: str,
        edition_label: str,
        subject_title: str,
        provider: str,
        syllabus_parse: StructuralParseResult,
        cmp_parse: StructuralParseResult,
    ) -> CurriculumSegmentTree:
        """Fuse parses into a curriculum segment tree."""
        code = subject_code.strip().upper()
        if not syllabus_parse.headings:
            raise SegmentationError(
                "Syllabus has no numbered headings to segment"
            )

        tree = CurriculumSegmentTree(
            subject_code=code,
            edition_label=edition_label,
            subject_title=subject_title,
            provider=provider,
            object_cues=list(cmp_parse.object_cues) + list(syllabus_parse.object_cues),
            prerequisite_cues=(
                list(cmp_parse.prerequisite_cues)
                + list(syllabus_parse.prerequisite_cues)
            ),
            cross_reference_cues=(
                list(cmp_parse.cross_reference_cues)
                + list(syllabus_parse.cross_reference_cues)
            ),
            subject_locator=StructuralLocator.create(
                syllabus_parse.document_id,
                page_number=1,
                structural_path=code,
                section_heading=subject_title,
                paragraph_or_table_ref="subject",
            ),
        )

        # Prefer syllabus headings for hierarchy; merge CMP-only branches.
        headings = self._merge_headings(
            syllabus_parse.headings, cmp_parse.headings, tree
        )
        self._apply_metadata_cues(tree)
        tree.topics = self._build_topics(headings, tree)
        if not tree.topics:
            raise SegmentationError("Segmentation produced no topics")
        return tree

    def _merge_headings(
        self,
        syllabus: list[ParsedHeading],
        cmp: list[ParsedHeading],
        tree: CurriculumSegmentTree,
    ) -> list[ParsedHeading]:
        by_number: dict[str, ParsedHeading] = {}
        for heading in syllabus:
            by_number[heading.number] = heading
        for heading in cmp:
            if heading.number not in by_number:
                by_number[heading.number] = heading
                tree.diagnostics.append(
                    f"CMP-only heading merged: {heading.number}"
                )
            elif heading.title and heading.title != by_number[heading.number].title:
                tree.diagnostics.append(
                    f"CMP title differs for {heading.number}; keeping syllabus"
                )
        return sorted(
            by_number.values(),
            key=lambda h: [int(p) for p in h.number.split(".")],
        )

    def _apply_metadata_cues(self, tree: CurriculumSegmentTree) -> None:
        """Fold study-time / difficulty cues onto later segment attributes."""
        # Stored on tree for extract stage via object_cues; no-op here.
        _ = tree

    def _build_topics(
        self,
        headings: list[ParsedHeading],
        tree: CurriculumSegmentTree,
    ) -> list[SegmentNode]:
        topics: list[SegmentNode] = []
        topic_map: dict[str, SegmentNode] = {}
        section_map: dict[str, SegmentNode] = {}
        subsection_map: dict[str, SegmentNode] = {}

        for heading in headings:
            parts = heading.number.split(".")
            confidence, method = self._confidence_for(heading)
            minutes, difficulty = self._lookup_meta(tree, heading.number)

            if len(parts) == 1:
                node = SegmentNode(
                    kind="topic",
                    number=heading.number,
                    title=heading.title,
                    locator=heading.locator,
                    document_kind=heading.document_kind,
                    confidence=confidence,
                    extraction_method=method,
                    estimated_study_minutes=minutes,
                    difficulty=difficulty,
                )
                topics.append(node)
                topic_map[heading.number] = node
                continue

            if len(parts) == 2:
                parent = topic_map.get(parts[0])
                if parent is None:
                    parent = self._ensure_topic(parts[0], heading, topics, topic_map)
                node = SegmentNode(
                    kind="section",
                    number=heading.number,
                    title=heading.title,
                    locator=heading.locator,
                    document_kind=heading.document_kind,
                    confidence=confidence,
                    extraction_method=method,
                    estimated_study_minutes=minutes,
                    difficulty=difficulty,
                    parent_number=parent.number,
                )
                parent.children.append(node)
                section_map[heading.number] = node
                continue

            if len(parts) == 3:
                section_key = ".".join(parts[:2])
                section = section_map.get(section_key)
                if section is None:
                    topic = topic_map.get(parts[0])
                    if topic is None:
                        topic = self._ensure_topic(
                            parts[0], heading, topics, topic_map
                        )
                    section = SegmentNode(
                        kind="section",
                        number=section_key,
                        title=f"Section {section_key}",
                        locator=heading.locator,
                        document_kind=heading.document_kind,
                        confidence=85,
                        extraction_method=ExtractionMethod.HEURISTIC,
                        parent_number=topic.number,
                    )
                    topic.children.append(section)
                    section_map[section_key] = section
                node = SegmentNode(
                    kind="subsection",
                    number=heading.number,
                    title=heading.title,
                    locator=heading.locator,
                    document_kind=heading.document_kind,
                    confidence=confidence,
                    extraction_method=method,
                    estimated_study_minutes=minutes,
                    difficulty=difficulty,
                    parent_number=section.number,
                )
                section.children.append(node)
                subsection_map[heading.number] = node
                continue

            # Depth >= 4 → learning objective under nearest subsection.
            subsection_key = ".".join(parts[:3])
            subsection = subsection_map.get(subsection_key)
            if subsection is None:
                # Promote depth-3 missing: create subsection from this heading's
                # parent path, then attach LO.
                section_key = ".".join(parts[:2])
                section = section_map.get(section_key)
                if section is None:
                    topic = topic_map.get(parts[0])
                    if topic is None:
                        topic = self._ensure_topic(
                            parts[0], heading, topics, topic_map
                        )
                    section = SegmentNode(
                        kind="section",
                        number=section_key,
                        title=f"Section {section_key}",
                        locator=heading.locator,
                        document_kind=heading.document_kind,
                        confidence=85,
                        extraction_method=ExtractionMethod.HEURISTIC,
                        parent_number=topic.number,
                    )
                    topic.children.append(section)
                    section_map[section_key] = section
                subsection = SegmentNode(
                    kind="subsection",
                    number=subsection_key,
                    title=f"Subsection {subsection_key}",
                    locator=heading.locator,
                    document_kind=heading.document_kind,
                    confidence=85,
                    extraction_method=ExtractionMethod.HEURISTIC,
                    parent_number=section.number,
                )
                section.children.append(subsection)
                subsection_map[subsection_key] = subsection

            lo = SegmentNode(
                kind="learning_objective",
                number=heading.number,
                title=heading.title,
                locator=heading.locator,
                document_kind=heading.document_kind,
                confidence=99
                if heading.document_kind is DocumentKind.SYLLABUS
                else confidence,
                extraction_method=(
                    ExtractionMethod.STRUCTURED_FIELD
                    if heading.document_kind is DocumentKind.SYLLABUS
                    else method
                ),
                estimated_study_minutes=minutes,
                difficulty=difficulty,
                parent_number=subsection.number,
            )
            subsection.children.append(lo)

        # Ensure every section has at least one subsection and LO when syllabus
        # only provides depth-2 topics/sections.
        self._ensure_minimum_depth(topics)
        return topics

    def _ensure_topic(
        self,
        number: str,
        heading: ParsedHeading,
        topics: list[SegmentNode],
        topic_map: dict[str, SegmentNode],
    ) -> SegmentNode:
        node = SegmentNode(
            kind="topic",
            number=number,
            title=f"Topic {number}",
            locator=heading.locator,
            document_kind=heading.document_kind,
            confidence=85,
            extraction_method=ExtractionMethod.HEURISTIC,
        )
        topics.append(node)
        topic_map[number] = node
        return node

    def _ensure_minimum_depth(self, topics: list[SegmentNode]) -> None:
        for topic in topics:
            if not topic.children:
                section = SegmentNode(
                    kind="section",
                    number=f"{topic.number}.1",
                    title=topic.title,
                    locator=topic.locator,
                    document_kind=topic.document_kind,
                    confidence=80,
                    extraction_method=ExtractionMethod.HEURISTIC,
                    parent_number=topic.number,
                )
                topic.children.append(section)
            for section in topic.children:
                if section.kind != "section":
                    continue
                if not section.children:
                    subsection = SegmentNode(
                        kind="subsection",
                        number=f"{section.number}.1",
                        title=section.title,
                        locator=section.locator,
                        document_kind=section.document_kind,
                        confidence=80,
                        extraction_method=ExtractionMethod.HEURISTIC,
                        parent_number=section.number,
                    )
                    section.children.append(subsection)
                for subsection in section.children:
                    if subsection.kind != "subsection":
                        continue
                    if not any(
                        c.kind == "learning_objective" for c in subsection.children
                    ):
                        subsection.children.append(
                            SegmentNode(
                                kind="learning_objective",
                                number=f"{subsection.number}.1",
                                title=f"Understand {subsection.title}",
                                locator=subsection.locator,
                                document_kind=subsection.document_kind,
                                confidence=80,
                                extraction_method=ExtractionMethod.HEURISTIC,
                                parent_number=subsection.number,
                            )
                        )

    def _confidence_for(
        self, heading: ParsedHeading
    ) -> tuple[int, ExtractionMethod]:
        if heading.document_kind is DocumentKind.SYLLABUS:
            return 99, ExtractionMethod.STRUCTURED_FIELD
        return 95, ExtractionMethod.STRUCTURED_FIELD

    def _lookup_meta(
        self, tree: CurriculumSegmentTree, number: str
    ) -> tuple[int, str]:
        minutes = 0
        difficulty = "foundational"
        for cue in tree.object_cues:
            host = dict(cue.attributes).get("host_number")
            if host != number:
                continue
            if cue.object_kind == "study_time":
                match = _MINUTES.search(cue.body)
                if match:
                    value = float(match.group(1))
                    # Treat bare numbers as minutes; hours if 'h' present.
                    if re.search(r"h", cue.body, re.IGNORECASE):
                        minutes = int(value * 60)
                    else:
                        minutes = int(value)
            elif cue.object_kind == "difficulty":
                word = cue.body.strip().lower().split()[0]
                difficulty = _DIFFICULTY_WORDS.get(word, difficulty)
        return minutes, difficulty
