"""Persistence helpers for CIP entities (application-owned orchestration)."""

from __future__ import annotations

import json
from typing import Any

from app.domain.curriculum_intelligence.curriculum_entity import CurriculumMap
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument
from app.domain.curriculum_intelligence.knowledge_graph import KnowledgeGraph
from app.domain.curriculum_intelligence.structural_document import (
    StructuralDocument,
    StructuralNode,
)
from app.extensions import db
from app.models.curriculum_intelligence import (
    CipCurriculumEntity,
    CipExtractedBlock,
    CipExtractedDocument,
    CipExtractedPage,
    CipKnowledgeRelation,
    CipStructuralNode,
)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


class CipPersistenceService:
    """Write CIP artefacts to normalised tables. Idempotent per job artefact ids."""

    def replace_extraction(self, extracted: ExtractedDocument, *, job_id: str) -> None:
        """Persist extraction, replacing any prior rows for the same extraction_id."""
        existing = CipExtractedDocument.query.filter_by(
            extraction_id=extracted.extraction_id
        ).first()
        if existing is not None:
            db.session.delete(existing)
            db.session.flush()

        root = CipExtractedDocument(
            extraction_id=extracted.extraction_id,
            document_id=extracted.document_id,
            job_id=job_id,
            page_count=extracted.page_count,
            metadata_json=_dumps(dict(extracted.metadata)),
            diagnostics_json=_dumps(list(extracted.diagnostics)),
        )
        db.session.add(root)
        db.session.flush()
        for page in extracted.pages:
            page_row = CipExtractedPage(
                extraction_id=extracted.extraction_id,
                page_number=page.page_number,
                width=page.width,
                height=page.height,
                raw_text=page.raw_text,
            )
            db.session.add(page_row)
            db.session.flush()
            for block in page.blocks:
                db.session.add(
                    CipExtractedBlock(
                        block_id=block.block_id,
                        page_id=page_row.id,
                        kind=block.kind.value,
                        text=block.text,
                        order_index=block.order_index,
                        bbox_json=_dumps(block.bbox) if block.bbox else None,
                        attributes_json=_dumps(dict(block.attributes)),
                    )
                )

    def replace_structural(self, structural: StructuralDocument) -> None:
        """Persist structural nodes for a parse_id (replace prior)."""
        CipStructuralNode.query.filter_by(parse_id=structural.parse_id).delete()
        db.session.flush()

        def walk(node: StructuralNode, parent_id: str | None) -> None:
            db.session.add(
                CipStructuralNode(
                    node_id=node.node_id,
                    parse_id=structural.parse_id,
                    document_id=structural.document_id,
                    parent_node_id=parent_id,
                    kind=node.kind.value,
                    title=node.title,
                    text=node.text,
                    level=node.level,
                    source_page=node.source_page,
                    source_block_ids_json=_dumps(list(node.source_block_ids)),
                    confidence=node.confidence,
                    needs_review=node.needs_review,
                    attributes_json=_dumps(dict(node.attributes)),
                )
            )
            for child in node.children:
                walk(child, node.node_id)

        walk(structural.root, None)

    def replace_curriculum_map(self, curriculum_map: CurriculumMap) -> None:
        """Persist mapped entities for a map_id (replace prior)."""
        CipCurriculumEntity.query.filter_by(map_id=curriculum_map.map_id).delete()
        db.session.flush()
        for ent in curriculum_map.entities:
            db.session.add(
                CipCurriculumEntity(
                    entity_id=ent.entity_id,
                    map_id=curriculum_map.map_id,
                    document_id=curriculum_map.document_id,
                    kind=ent.kind.value,
                    title=ent.title,
                    body=ent.body,
                    parent_entity_id=ent.parent_id,
                    version_label=ent.version_label,
                    source_pages_json=_dumps(list(ent.source_pages)),
                    structural_node_id=ent.structural_node_id,
                    confidence=ent.confidence,
                    needs_review=ent.needs_review,
                    attributes_json=_dumps(dict(ent.attributes)),
                )
            )

    def replace_knowledge_graph(self, graph: KnowledgeGraph) -> None:
        """Persist graph relations for a graph_id (replace prior)."""
        CipKnowledgeRelation.query.filter_by(graph_id=graph.graph_id).delete()
        db.session.flush()
        for rel in graph.relations:
            db.session.add(
                CipKnowledgeRelation(
                    relation_id=rel.relation_id,
                    graph_id=graph.graph_id,
                    document_id=graph.document_id,
                    relation_type=rel.relation_type.value,
                    from_entity_id=rel.from_entity_id,
                    to_entity_id=rel.to_entity_id,
                    confidence=rel.confidence,
                    needs_review=rel.needs_review,
                    attributes_json=_dumps(dict(rel.attributes)),
                )
            )
