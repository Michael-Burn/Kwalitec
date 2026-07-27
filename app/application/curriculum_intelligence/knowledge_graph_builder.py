"""KnowledgeGraphBuilder — curriculum entities → canonical graph edges."""

from __future__ import annotations

from uuid import uuid4

from app.domain.curriculum_intelligence.curriculum_entity import (
    CurriculumEntityKind,
    CurriculumMap,
)
from app.domain.curriculum_intelligence.knowledge_graph import (
    KnowledgeGraph,
    KnowledgeRelation,
    KnowledgeRelationType,
)

_PARENT_EDGE = {
    CurriculumEntityKind.LEARNING_OBJECTIVE: (
        KnowledgeRelationType.LEARNING_OBJECTIVE_OF
    ),
    CurriculumEntityKind.FORMULA: KnowledgeRelationType.FORMULA_FOR,
    CurriculumEntityKind.EXAMPLE: KnowledgeRelationType.EXAMPLE_OF,
    CurriculumEntityKind.PRACTICE_QUESTION: KnowledgeRelationType.TESTED_IN,
}


class KnowledgeGraphBuilder:
    """Build deterministic knowledge-graph relations from a CurriculumMap."""

    def build(
        self,
        curriculum_map: CurriculumMap,
        *,
        graph_id: str | None = None,
    ) -> KnowledgeGraph:
        """Create parent/child, formula, example, and sequential depends_on edges."""
        gid = (graph_id or "").strip() or f"graph-{uuid4().hex[:12]}"
        by_id = {e.entity_id: e for e in curriculum_map.entities}
        relations: list[KnowledgeRelation] = []
        diagnostics: list[str] = []

        # Hierarchy edges
        for ent in curriculum_map.entities:
            if not ent.parent_id or ent.parent_id not in by_id:
                continue
            parent = by_id[ent.parent_id]
            relations.append(
                self._rel(
                    KnowledgeRelationType.CHILD_OF,
                    ent.entity_id,
                    parent.entity_id,
                    curriculum_map.document_id,
                    confidence=1.0,
                )
            )
            relations.append(
                self._rel(
                    KnowledgeRelationType.PARENT_OF,
                    parent.entity_id,
                    ent.entity_id,
                    curriculum_map.document_id,
                    confidence=1.0,
                )
            )
            special = _PARENT_EDGE.get(ent.kind)
            if special is not None:
                relations.append(
                    self._rel(
                        special,
                        ent.entity_id,
                        parent.entity_id,
                        curriculum_map.document_id,
                        confidence=ent.confidence,
                        needs_review=ent.needs_review,
                    )
                )
            relations.append(
                self._rel(
                    KnowledgeRelationType.APPEARS_IN,
                    ent.entity_id,
                    parent.entity_id,
                    curriculum_map.document_id,
                    confidence=1.0,
                )
            )
            if ent.kind is CurriculumEntityKind.SOURCE_REFERENCE:
                relations.append(
                    self._rel(
                        KnowledgeRelationType.DERIVED_FROM,
                        parent.entity_id,
                        ent.entity_id,
                        curriculum_map.document_id,
                        confidence=ent.confidence,
                        needs_review=ent.needs_review,
                    )
                )

        # Sequential depends_on among sibling topics/modules
        children_by_parent: dict[str, list[str]] = {}
        for ent in curriculum_map.entities:
            if ent.parent_id:
                children_by_parent.setdefault(ent.parent_id, []).append(ent.entity_id)
        for siblings in children_by_parent.values():
            ordered = [
                sid
                for sid in siblings
                if by_id[sid].kind
                in {
                    CurriculumEntityKind.MODULE,
                    CurriculumEntityKind.TOPIC,
                    CurriculumEntityKind.SUBTOPIC,
                    CurriculumEntityKind.CONCEPT,
                }
            ]
            for prev_id, next_id in zip(ordered, ordered[1:], strict=False):
                relations.append(
                    self._rel(
                        KnowledgeRelationType.DEPENDS_ON,
                        next_id,
                        prev_id,
                        curriculum_map.document_id,
                        confidence=0.55,
                        needs_review=True,
                    )
                )
                relations.append(
                    self._rel(
                        KnowledgeRelationType.REQUIRES,
                        next_id,
                        prev_id,
                        curriculum_map.document_id,
                        confidence=0.5,
                        needs_review=True,
                    )
                )
                diagnostics.append(
                    f"Inferred sequential dependency {next_id}→{prev_id}"
                )

        # supports / extends for objectives under modules
        for ent in curriculum_map.entities:
            if ent.kind is CurriculumEntityKind.LEARNING_OBJECTIVE and ent.parent_id:
                relations.append(
                    self._rel(
                        KnowledgeRelationType.SUPPORTS,
                        ent.entity_id,
                        ent.parent_id,
                        curriculum_map.document_id,
                        confidence=0.7,
                    )
                )

        return KnowledgeGraph(
            graph_id=gid,
            document_id=curriculum_map.document_id,
            map_id=curriculum_map.map_id,
            entity_ids=tuple(e.entity_id for e in curriculum_map.entities),
            relations=tuple(relations),
            diagnostics=tuple(diagnostics),
        )

    @staticmethod
    def _rel(
        relation_type: KnowledgeRelationType,
        from_id: str,
        to_id: str,
        document_id: int,
        *,
        confidence: float,
        needs_review: bool = False,
    ) -> KnowledgeRelation:
        return KnowledgeRelation(
            relation_id=f"rel-{uuid4().hex[:12]}",
            relation_type=relation_type,
            from_entity_id=from_id,
            to_entity_id=to_id,
            source_document_id=document_id,
            confidence=confidence,
            needs_review=needs_review,
        )
