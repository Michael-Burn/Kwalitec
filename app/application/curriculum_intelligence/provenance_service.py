"""ProvenanceService — immutable production-chain records (CIP-002)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from uuid import uuid4

from app.domain.curriculum_intelligence.curriculum_entity import (
    CurriculumKnowledgeEntity,
)
from app.domain.curriculum_intelligence.knowledge_graph import KnowledgeRelation
from app.domain.curriculum_intelligence.provenance import (
    GRAPH_BUILDER_VERSION,
    MAPPER_VERSION,
    PARSER_VERSION,
    ProvenanceChainStage,
    ProvenanceRecord,
    ProvenanceSubjectKind,
    SupportingEvidence,
)
from app.domain.curriculum_intelligence.structural_document import StructuralNode
from app.extensions import db
from app.models.curriculum_intelligence import (
    CipProvenanceEvidence,
    CipProvenanceRecord,
    CipStructuralNode,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


def _csv_ints(values: tuple[int, ...] | list[int]) -> str:
    return ",".join(str(v) for v in values)


def _csv_strs(values: tuple[str, ...] | list[str]) -> str:
    return ",".join(values)


def _parse_int_csv(raw: str) -> tuple[int, ...]:
    parts = [p.strip() for p in (raw or "").split(",") if p.strip()]
    out: list[int] = []
    for part in parts:
        try:
            out.append(int(part))
        except ValueError:
            continue
    return tuple(out)


def _parse_str_csv(raw: str) -> tuple[str, ...]:
    return tuple(p.strip() for p in (raw or "").split(",") if p.strip())


class ProvenanceService:
    """Create and query immutable provenance records for CIP artefacts."""

    def record_entity(
        self,
        entity: CurriculumKnowledgeEntity,
        *,
        pipeline_job_id: str,
        extraction_id: str,
        parse_id: str,
        map_id: str,
        graph_id: str = "",
        version_label: str = "",
    ) -> ProvenanceRecord:
        """Persist provenance for one mapped curriculum entity."""
        structural = None
        paragraphs: list[int] = []
        block_ids: list[str] = []
        excerpt = (entity.body or entity.title or "")[:400]
        if entity.structural_node_id:
            structural = CipStructuralNode.query.filter_by(
                node_id=entity.structural_node_id
            ).first()
        if structural is not None:
            try:
                block_ids = list(json.loads(structural.source_block_ids_json or "[]"))
            except json.JSONDecodeError:
                block_ids = []
            # Paragraph index approximated as order among blocks on the page.
            if structural.source_page is not None:
                paragraphs = [1]
            excerpt = (structural.text or structural.title or excerpt)[:400]

        evidence = (
            SupportingEvidence(
                page_number=entity.source_pages[0] if entity.source_pages else None,
                paragraph_index=paragraphs[0] if paragraphs else None,
                block_id=block_ids[0] if block_ids else None,
                excerpt=excerpt,
                evidence_role="source",
            ),
        )
        return self._persist(
            subject_kind=ProvenanceSubjectKind.ENTITY,
            subject_id=entity.entity_id,
            source_document_id=entity.source_document_id,
            source_version_label=version_label or entity.version_label,
            source_pages=entity.source_pages,
            source_paragraphs=tuple(paragraphs),
            source_block_ids=tuple(block_ids),
            pipeline_job_id=pipeline_job_id,
            extraction_id=extraction_id,
            parse_id=parse_id,
            map_id=map_id,
            graph_id=graph_id,
            chain_stage=ProvenanceChainStage.CURRICULUM_MAPPING,
            evidence=evidence,
            attributes=(("entity_kind", entity.kind.value),),
        )

    def record_relation(
        self,
        relation: KnowledgeRelation,
        *,
        pipeline_job_id: str,
        extraction_id: str,
        parse_id: str,
        map_id: str,
        graph_id: str,
        version_label: str = "",
    ) -> ProvenanceRecord:
        """Persist provenance for one knowledge-graph relation."""
        evidence = (
            SupportingEvidence(
                page_number=None,
                paragraph_index=None,
                block_id=None,
                excerpt=(
                    f"{relation.relation_type.value}: "
                    f"{relation.from_entity_id} → {relation.to_entity_id}"
                )[:400],
                evidence_role="derived",
            ),
        )
        return self._persist(
            subject_kind=ProvenanceSubjectKind.RELATION,
            subject_id=relation.relation_id,
            source_document_id=relation.source_document_id,
            source_version_label=version_label,
            source_pages=(),
            source_paragraphs=(),
            source_block_ids=(),
            pipeline_job_id=pipeline_job_id,
            extraction_id=extraction_id,
            parse_id=parse_id,
            map_id=map_id,
            graph_id=graph_id,
            chain_stage=ProvenanceChainStage.KNOWLEDGE_GRAPH,
            evidence=evidence,
            attributes=(("relation_type", relation.relation_type.value),),
        )

    def record_structural_node(
        self,
        node: StructuralNode,
        *,
        document_id: int,
        pipeline_job_id: str,
        extraction_id: str,
        parse_id: str,
        version_label: str = "",
    ) -> ProvenanceRecord:
        """Persist provenance for a structural parse node (parser stage)."""
        pages = (node.source_page,) if node.source_page is not None else ()
        evidence = (
            SupportingEvidence(
                page_number=node.source_page,
                paragraph_index=1 if node.source_page is not None else None,
                block_id=node.source_block_ids[0] if node.source_block_ids else None,
                excerpt=(node.text or node.title or "")[:400],
                evidence_role="parsed",
            ),
        )
        return self._persist(
            subject_kind=ProvenanceSubjectKind.STRUCTURAL_NODE,
            subject_id=node.node_id,
            source_document_id=document_id,
            source_version_label=version_label,
            source_pages=pages,
            source_paragraphs=(1,) if pages else (),
            source_block_ids=node.source_block_ids,
            pipeline_job_id=pipeline_job_id,
            extraction_id=extraction_id,
            parse_id=parse_id,
            map_id="",
            graph_id="",
            chain_stage=ProvenanceChainStage.PARSER,
            evidence=evidence,
            attributes=(("structural_kind", node.kind.value),),
        )

    def get_for_subject(
        self, *, subject_kind: str, subject_id: str
    ) -> ProvenanceRecord | None:
        """Return the latest provenance record for a subject."""
        row = (
            CipProvenanceRecord.query.filter_by(
                subject_kind=subject_kind, subject_id=subject_id
            )
            .order_by(CipProvenanceRecord.id.desc())
            .first()
        )
        if row is None:
            return None
        return self._to_domain(row)

    def chain_for_entity(self, entity_id: str) -> list[dict[str, str]]:
        """Navigable provenance chain for Founder inspection."""
        prov = self.get_for_subject(
            subject_kind=ProvenanceSubjectKind.ENTITY.value, subject_id=entity_id
        )
        if prov is None:
            return []
        return [
            {
                "stage": ProvenanceChainStage.DOCUMENT.value,
                "ref": str(prov.source_document_id),
            },
            {
                "stage": ProvenanceChainStage.EXTRACTION.value,
                "ref": prov.extraction_id,
            },
            {"stage": ProvenanceChainStage.PARSER.value, "ref": prov.parse_id},
            {
                "stage": ProvenanceChainStage.CURRICULUM_MAPPING.value,
                "ref": prov.map_id,
            },
            {
                "stage": ProvenanceChainStage.KNOWLEDGE_GRAPH.value,
                "ref": prov.graph_id or "",
            },
        ]

    def replace_document_subjects(
        self, *, document_id: int, subject_kinds: tuple[str, ...]
    ) -> None:
        """Remove prior provenance for subject kinds on a document (re-run)."""
        rows = CipProvenanceRecord.query.filter(
            CipProvenanceRecord.source_document_id == document_id,
            CipProvenanceRecord.subject_kind.in_(subject_kinds),
        ).all()
        for row in rows:
            db.session.delete(row)
        db.session.flush()

    def _persist(
        self,
        *,
        subject_kind: ProvenanceSubjectKind,
        subject_id: str,
        source_document_id: int,
        source_version_label: str,
        source_pages: tuple[int, ...],
        source_paragraphs: tuple[int, ...],
        source_block_ids: tuple[str, ...],
        pipeline_job_id: str,
        extraction_id: str,
        parse_id: str,
        map_id: str,
        graph_id: str,
        chain_stage: ProvenanceChainStage,
        evidence: tuple[SupportingEvidence, ...],
        attributes: tuple[tuple[str, str], ...] = (),
    ) -> ProvenanceRecord:
        now = _utc_now()
        provenance_id = f"prov-{uuid4().hex[:12]}"
        row = CipProvenanceRecord(
            provenance_id=provenance_id,
            subject_kind=subject_kind.value,
            subject_id=subject_id,
            source_document_id=source_document_id,
            source_version_label=source_version_label or "",
            source_pages_csv=_csv_ints(source_pages),
            source_paragraphs_csv=_csv_ints(source_paragraphs),
            source_block_ids_csv=_csv_strs(source_block_ids),
            parser_version=PARSER_VERSION,
            mapper_version=MAPPER_VERSION,
            graph_builder_version=GRAPH_BUILDER_VERSION,
            pipeline_job_id=pipeline_job_id or "",
            extraction_id=extraction_id or "",
            parse_id=parse_id or "",
            map_id=map_id or "",
            graph_id=graph_id or "",
            chain_stage=chain_stage.value,
            attributes_json=json.dumps(
                dict(attributes), ensure_ascii=False, separators=(",", ":")
            ),
            created_at=now,
        )
        db.session.add(row)
        db.session.flush()
        for ev in evidence:
            db.session.add(
                CipProvenanceEvidence(
                    evidence_id=f"pev-{uuid4().hex[:12]}",
                    provenance_id=provenance_id,
                    page_number=ev.page_number,
                    paragraph_index=ev.paragraph_index,
                    block_id=ev.block_id,
                    excerpt=ev.excerpt or "",
                    evidence_role=ev.evidence_role,
                )
            )
        return ProvenanceRecord(
            provenance_id=provenance_id,
            subject_kind=subject_kind,
            subject_id=subject_id,
            source_document_id=source_document_id,
            source_version_label=source_version_label or "",
            source_pages=source_pages,
            source_paragraphs=source_paragraphs,
            source_block_ids=source_block_ids,
            parser_version=PARSER_VERSION,
            mapper_version=MAPPER_VERSION,
            graph_builder_version=GRAPH_BUILDER_VERSION,
            pipeline_job_id=pipeline_job_id or "",
            extraction_id=extraction_id or "",
            parse_id=parse_id or "",
            map_id=map_id or "",
            graph_id=graph_id or "",
            chain_stage=chain_stage,
            evidence=evidence,
            created_at_iso=_iso(now),
            attributes=attributes,
        )

    @staticmethod
    def _to_domain(row: CipProvenanceRecord) -> ProvenanceRecord:
        evidence = tuple(
            SupportingEvidence(
                page_number=e.page_number,
                paragraph_index=e.paragraph_index,
                block_id=e.block_id,
                excerpt=e.excerpt,
                evidence_role=e.evidence_role,
            )
            for e in row.evidence
        )
        try:
            attrs = json.loads(row.attributes_json or "{}")
        except json.JSONDecodeError:
            attrs = {}
        if not isinstance(attrs, dict):
            attrs = {}
        return ProvenanceRecord(
            provenance_id=row.provenance_id,
            subject_kind=ProvenanceSubjectKind(row.subject_kind),
            subject_id=row.subject_id,
            source_document_id=row.source_document_id,
            source_version_label=row.source_version_label,
            source_pages=_parse_int_csv(row.source_pages_csv),
            source_paragraphs=_parse_int_csv(row.source_paragraphs_csv),
            source_block_ids=_parse_str_csv(row.source_block_ids_csv),
            parser_version=row.parser_version,
            mapper_version=row.mapper_version,
            graph_builder_version=row.graph_builder_version,
            pipeline_job_id=row.pipeline_job_id,
            extraction_id=row.extraction_id,
            parse_id=row.parse_id,
            map_id=row.map_id,
            graph_id=row.graph_id,
            chain_stage=ProvenanceChainStage(row.chain_stage),
            evidence=evidence,
            created_at_iso=_iso(row.created_at) if row.created_at else "",
            attributes=tuple(sorted((str(k), str(v)) for k, v in attrs.items())),
        )
