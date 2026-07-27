"""CurriculumMappingService — structural tree → curriculum entities."""

from __future__ import annotations

from uuid import uuid4

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

_OBJECTIVE_HINTS = ("objective", "learning outcome", "by the end", "students will")


class CurriculumMappingService:
    """Map structural nodes to curriculum hierarchy entities.

    Uncertain mappings are retained with ``needs_review=True`` rather than
    dropped or guessed via LLM.
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

        def walk(
            node: StructuralNode, parent_id: str, parent_kind: CurriculumEntityKind
        ) -> None:
            nonlocal uncertain
            mapped_kind = self._map_kind(node)
            if mapped_kind is None:
                for child in node.children:
                    walk(child, parent_id, parent_kind)
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
            pages = (node.source_page,) if node.source_page is not None else ()
            entities.append(
                CurriculumKnowledgeEntity(
                    entity_id=entity_id,
                    kind=mapped_kind,
                    title=node.title or mapped_kind.value,
                    body=node.text,
                    parent_id=parent_id,
                    child_ids=(),
                    source_document_id=structural.document_id,
                    source_pages=pages,
                    version_label=version_label,
                    confidence=confidence,
                    needs_review=needs_review,
                    structural_node_id=node.node_id,
                    attributes=node.attributes,
                )
            )
            child_ids_by_parent.setdefault(parent_id, []).append(entity_id)
            child_ids_by_parent.setdefault(entity_id, [])
            for child in node.children:
                walk(child, entity_id, mapped_kind)

        for child in structural.root.children:
            walk(child, subject_id, CurriculumEntityKind.SUBJECT)

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
        if node.kind is StructuralKind.DOCUMENT:
            return None
        if node.kind is StructuralKind.PARAGRAPH:
            lower = (node.title + " " + node.text).lower()
            if any(h in lower for h in _OBJECTIVE_HINTS):
                return CurriculumEntityKind.LEARNING_OBJECTIVE
            return None
        if node.kind in {
            StructuralKind.LIST,
            StructuralKind.LIST_ITEM,
            StructuralKind.TABLE,
        }:
            return None
        if node.kind is StructuralKind.UNKNOWN:
            return None
        return _KIND_MAP.get(node.kind)

    @staticmethod
    def _kind_confidence(node: StructuralNode, kind: CurriculumEntityKind) -> float:
        if kind is CurriculumEntityKind.LEARNING_OBJECTIVE:
            return min(node.confidence, 0.7)
        if node.kind is StructuralKind.NOTE:
            return min(node.confidence, 0.5)
        return node.confidence
