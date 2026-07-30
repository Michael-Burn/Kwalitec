"""CurriculumMappingService — structural tree → curriculum entities."""

from __future__ import annotations

from uuid import uuid4

from app.domain.curriculum_intelligence.content_role import (
    ContentRole,
    is_curriculum_role,
)
from app.domain.curriculum_intelligence.curriculum_entity import (
    CurriculumEntityKind,
    CurriculumKnowledgeEntity,
    CurriculumMap,
)
from app.domain.curriculum_intelligence.structural_document import (
    StructuralDocument,
    StructuralKind,
    StructuralNode,
)

_KIND_MAP: dict[StructuralKind, CurriculumEntityKind] = {
    StructuralKind.NUMBERED_SECTION: CurriculumEntityKind.MODULE,
    StructuralKind.HEADING: CurriculumEntityKind.TOPIC,
    StructuralKind.SUB_HEADING: CurriculumEntityKind.SUBTOPIC,
    StructuralKind.DEFINITION: CurriculumEntityKind.CONCEPT,
    StructuralKind.FORMULA_BLOCK: CurriculumEntityKind.FORMULA,
    StructuralKind.EXAMPLE: CurriculumEntityKind.EXAMPLE,
    StructuralKind.WORKED_EXAMPLE: CurriculumEntityKind.EXAMPLE,
    StructuralKind.PRACTICE_QUESTION: CurriculumEntityKind.PRACTICE_QUESTION,
    StructuralKind.REFERENCE: CurriculumEntityKind.SOURCE_REFERENCE,
    StructuralKind.NOTE: CurriculumEntityKind.CONCEPT,
    StructuralKind.WARNING: CurriculumEntityKind.CONCEPT,
}

_OBJECTIVE_HINTS = (
    "objective",
    "learning outcome",
    "by the end",
    "students will",
    "candidates will",
    "syllabus objective",
)

_NON_TOPIC_TITLES = frozenset(
    {
        "objectives",
        "contents",
        "introduction",
        "syllabus objectives",
        "aim",
        "solution",
        "question",
        "summary",
        "chapter summary",
    }
)


def _prose_title(title: str) -> bool:
    """Reject formula fragments and OCR debris as curriculum titles."""
    text = (title or "").strip()
    if len(text) < 4:
        return False
    letters = sum(1 for c in text if c.isalpha())
    if letters < 6:
        return False
    return (letters / max(len(text), 1)) >= 0.35



class CurriculumMappingService:
    """Map structural nodes to curriculum hierarchy entities.

    EQ-001: only educational content roles become hierarchy entities;
    numbered depth ≥2 maps to learning objectives; chapters/modules are
    reserved for weighted syllabus topics and CMP chapter codes.
    """

    REVIEW_CONFIDENCE = 0.6

    def map(
        self,
        structural: StructuralDocument,
        *,
        map_id: str | None = None,
        subject_code: str,
        version_label: str,
    ) -> CurriculumMap:
        """Produce a CurriculumMap from a StructuralDocument."""
        mid = (map_id or "").strip() or f"map-{uuid4().hex[:12]}"
        entities: list[CurriculumKnowledgeEntity] = []
        diagnostics: list[str] = []

        subject_id = f"ent-{uuid4().hex[:10]}"
        entities.append(
            CurriculumKnowledgeEntity(
                entity_id=subject_id,
                kind=CurriculumEntityKind.SUBJECT,
                title=subject_code or structural.root.title,
                body="",
                parent_id=None,
                child_ids=(),
                source_document_id=structural.document_id,
                source_pages=(),
                version_label=version_label,
                confidence=1.0,
                needs_review=False,
                structural_node_id=structural.root.node_id,
            )
        )

        child_ids_by_parent: dict[str, list[str]] = {subject_id: []}
        uncertain = 0
        skipped = 0
        chapter_entity_ids: dict[str, str] = {}

        def walk(
            node: StructuralNode, parent_id: str, parent_kind: CurriculumEntityKind
        ) -> None:
            nonlocal uncertain, skipped
            mapped_kind = self._map_kind(node)
            if mapped_kind is None:
                skipped += 1
                for child in node.children:
                    walk(child, parent_id, parent_kind)
                return

            # Deduplicate ActEd running-header chapter cues (CS1-NN … Page N).
            chapter_code = (node.attribute("chapter_code") or "").upper()
            if chapter_code and mapped_kind is CurriculumEntityKind.MODULE:
                existing = chapter_entity_ids.get(chapter_code)
                if existing is not None:
                    for child in node.children:
                        walk(child, existing, CurriculumEntityKind.MODULE)
                    return

            confidence = min(node.confidence, self._kind_confidence(node, mapped_kind))
            needs_review = node.needs_review or confidence < self.REVIEW_CONFIDENCE
            if needs_review:
                uncertain += 1
                diagnostics.append(
                    f"Uncertain mapping {node.kind.value}→{mapped_kind.value} "
                    f"(page {node.source_page})"
                )

            entity_id = f"ent-{uuid4().hex[:10]}"
            if chapter_code and mapped_kind is CurriculumEntityKind.MODULE:
                chapter_entity_ids[chapter_code] = entity_id
            pages = (node.source_page,) if node.source_page is not None else ()
            attrs = (*node.attributes, ("mapped_kind", mapped_kind.value))
            # Preserve section numbers on entity titles for reconciliation.
            section_num = node.attribute("section_number")
            title = node.title or mapped_kind.value
            if (
                section_num
                and mapped_kind
                in {
                    CurriculumEntityKind.MODULE,
                    CurriculumEntityKind.TOPIC,
                    CurriculumEntityKind.SUBTOPIC,
                    CurriculumEntityKind.LEARNING_OBJECTIVE,
                }
                and not title.lower().startswith(section_num.lower())
                and not section_num.upper().startswith("CS1-")
            ):
                title = f"{section_num} {title}"

            entities.append(
                CurriculumKnowledgeEntity(
                    entity_id=entity_id,
                    kind=mapped_kind,
                    title=title,
                    body=node.text,
                    parent_id=parent_id,
                    child_ids=(),
                    source_document_id=structural.document_id,
                    source_pages=pages,
                    version_label=version_label,
                    confidence=confidence,
                    needs_review=needs_review,
                    structural_node_id=node.node_id,
                    attributes=attrs,
                )
            )
            child_ids_by_parent.setdefault(parent_id, []).append(entity_id)
            child_ids_by_parent.setdefault(entity_id, [])
            for child in node.children:
                walk(child, entity_id, mapped_kind)

        for child in structural.root.children:
            walk(child, subject_id, CurriculumEntityKind.SUBJECT)

        if skipped:
            diagnostics.append(f"skipped_non_curriculum_nodes={skipped}")

        # Materialise child_ids
        final: list[CurriculumKnowledgeEntity] = []
        for ent in entities:
            kids = tuple(child_ids_by_parent.get(ent.entity_id, []))
            final.append(
                CurriculumKnowledgeEntity(
                    entity_id=ent.entity_id,
                    kind=ent.kind,
                    title=ent.title,
                    body=ent.body,
                    parent_id=ent.parent_id,
                    child_ids=kids,
                    source_document_id=ent.source_document_id,
                    source_pages=ent.source_pages,
                    version_label=ent.version_label,
                    confidence=ent.confidence,
                    needs_review=ent.needs_review,
                    structural_node_id=ent.structural_node_id,
                    attributes=ent.attributes,
                )
            )

        return CurriculumMap(
            map_id=mid,
            document_id=structural.document_id,
            parse_id=structural.parse_id,
            subject_code=subject_code,
            version_label=version_label,
            entities=tuple(final),
            diagnostics=tuple(diagnostics),
            uncertain_count=uncertain,
        )

    def _map_kind(self, node: StructuralNode) -> CurriculumEntityKind | None:
        role = node.attribute("content_role")
        if role and not is_curriculum_role(role):
            return None

        if node.kind is StructuralKind.DOCUMENT:
            return None

        if node.attribute("educational_role") == "learning_objective":
            if not _prose_title(node.title or ""):
                return None
            return CurriculumEntityKind.LEARNING_OBJECTIVE

        if node.kind is StructuralKind.PARAGRAPH:
            lower = (node.title + " " + node.text).lower()
            if any(h in lower for h in _OBJECTIVE_HINTS):
                return CurriculumEntityKind.LEARNING_OBJECTIVE
            return None

        if node.kind in {
            StructuralKind.LIST,
            StructuralKind.LIST_ITEM,
            StructuralKind.TABLE,
            StructuralKind.UNKNOWN,
        }:
            return None

        depth_s = node.attribute("number_depth")
        depth = int(depth_s) if depth_s is not None else None

        if node.kind is StructuralKind.NUMBERED_SECTION:
            # Chapters: CS1-NN or weighted syllabus topics (1 Data analysis [10%]).
            if node.attribute("chapter_code") or node.attribute("topic_weight_pct"):
                return CurriculumEntityKind.MODULE
            title = (node.title or "").strip()
            if title.lower() in _NON_TOPIC_TITLES or not _prose_title(title):
                return None
            if depth == 0 or depth is None:
                # Unit intros ("0 Introduction") are topics, not chapters.
                return CurriculumEntityKind.TOPIC
            if depth == 1:
                return CurriculumEntityKind.TOPIC
            return CurriculumEntityKind.LEARNING_OBJECTIVE

        if node.kind is StructuralKind.SUB_HEADING:
            title = (node.title or "").strip()
            if title.lower() in _NON_TOPIC_TITLES or not _prose_title(title):
                return None
            if depth is not None and depth >= 2:
                return CurriculumEntityKind.LEARNING_OBJECTIVE
            if depth == 1:
                return CurriculumEntityKind.TOPIC
            return CurriculumEntityKind.SUBTOPIC

        if node.kind is StructuralKind.HEADING:
            title = (node.title or "").strip()
            if title.lower() in _NON_TOPIC_TITLES or not _prose_title(title):
                return None
            if role in {
                ContentRole.FRONT_MATTER.value,
                ContentRole.QUALIFICATION_INFORMATION.value,
            }:
                return None
            # Unnumbered headings become topics only when educational, short,
            # and not ALL-CAPS marketing fragments (CMP product grids).
            words = title.split()
            if len(words) > 10 or len(words) < 2:
                return None
            letters = [c for c in title if c.isalpha()]
            if letters:
                upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
                if upper_ratio >= 0.9 and len(words) <= 4:
                    return None
            return CurriculumEntityKind.TOPIC

        return _KIND_MAP.get(node.kind)

    @staticmethod
    def _kind_confidence(node: StructuralNode, kind: CurriculumEntityKind) -> float:
        if kind is CurriculumEntityKind.LEARNING_OBJECTIVE:
            if node.attribute("educational_role") == "learning_objective":
                return min(node.confidence, 0.93)
            return min(node.confidence, 0.75)
        if node.kind is StructuralKind.NOTE:
            return min(node.confidence, 0.5)
        if node.attribute("topic_weight_pct") or node.attribute("chapter_code"):
            return min(node.confidence, 0.97)
        return node.confidence
