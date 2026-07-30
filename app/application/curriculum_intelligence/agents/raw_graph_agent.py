"""Generation 1 — Raw Educational Graph Agent.

Retain all educational candidates. Do not remove information.
Attach provenance and confidence. Store every candidate in Curriculum Memory.
"""

from __future__ import annotations

from app.application.curriculum_intelligence.agents.base import (
    CurriculumIntelligenceAgent,
    utc_now_iso,
)
from app.application.curriculum_intelligence.content_classification_service import (
    ContentClassificationService,
)
from app.application.curriculum_intelligence.generation_hash import (
    compute_generation_hash,
    stable_id,
)
from app.application.curriculum_intelligence.generation_quality import (
    compute_quality_snapshot,
)
from app.application.curriculum_intelligence.mock_generation_runners import (
    GenerationRunContext,
)
from app.domain.curriculum_intelligence.agent import (
    STANDARD_QUALITY_METRICS,
    AgentDescriptor,
)
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceRecord,
    confidence_band_from_score,
)
from app.domain.curriculum_intelligence.content_role import ContentRole
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument
from app.domain.curriculum_intelligence.generation import (
    CurriculumGenerationSnapshot,
    EducationalNode,
    Generation,
    LineageOperation,
    LineageOperationKind,
    LineageRecord,
    SnapshotStatus,
    purpose_for_index,
)
from app.domain.curriculum_intelligence.provenance import (
    ProvenanceChainStage,
    ProvenanceRecord,
    ProvenanceSubjectKind,
    SupportingEvidence,
)

_AGENT_VERSION = "1.0.0"
_DESCRIPTOR = AgentDescriptor(
    agent_id="raw_graph_agent",
    name="RawGraphAgent",
    purpose="raw_educational_graph",
    consumes=("extracted_document",),
    produces=("curriculum_generation_snapshot", "educational_node"),
    dependencies=(),
    version=_AGENT_VERSION,
    deterministic=True,
    supports_rollback=True,
    quality_metrics_produced=STANDARD_QUALITY_METRICS,
)


class RawGraphAgent(CurriculumIntelligenceAgent):
    """Generation 1 — maximal educational graph; never deletes."""

    generation_index = 1

    def __init__(
        self, classifier: ContentClassificationService | None = None
    ) -> None:
        self._classifier = classifier or ContentClassificationService()

    @property
    def descriptor(self) -> AgentDescriptor:
        return _DESCRIPTOR

    def execute(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        created_at = context.fixed_created_at_iso or utc_now_iso()
        documents = context.source_documents
        if not documents:
            documents = _empty_seed_documents(context.source_document_ids)

        chain_seed = (
            ",".join(str(i) for i in context.source_document_ids),
            self.descriptor.version,
            ",".join(d.extraction_id for d in documents),
        )
        generation_id = stable_id("gen", *chain_seed, "g1")
        snapshot_id = stable_id("snap", *chain_seed, "g1")

        nodes: list[EducationalNode] = []
        index = 0
        for doc in documents:
            for page in doc.pages:
                for block in page.blocks:
                    text = (block.text or "").strip()
                    if not text:
                        role = ContentRole.BLANK_ARTEFACT
                        title = ""
                    else:
                        role = self._classifier.classify_line(text)
                        title = text if len(text) <= 240 else text[:237] + "..."
                    node_id = stable_id(
                        "node",
                        str(doc.document_id),
                        doc.extraction_id,
                        str(page.page_number),
                        block.block_id,
                        "g1",
                    )
                    local_id = f"g1-{index}"
                    index += 1
                    prov = _provenance(
                        node_id=node_id,
                        document_id=doc.document_id,
                        page_number=page.page_number,
                        block_id=block.block_id,
                        excerpt=text[:200],
                        created_at_iso=created_at,
                        extraction_id=doc.extraction_id,
                    )
                    score = _role_confidence(role)
                    conf = ConfidenceRecord(
                        confidence_id=f"conf-{node_id}",
                        subject_kind="educational_node",
                        subject_id=node_id,
                        score=score,
                        band=confidence_band_from_score(score),
                        reason="raw_graph_capture",
                        factors=(),
                        needs_review=score < 0.6,
                        review_threshold=0.6,
                        provenance_id=prov.provenance_id,
                    )
                    op = LineageOperation(
                        operation_id=stable_id("op", node_id, "created"),
                        kind=LineageOperationKind.CREATED,
                        generation_id=generation_id,
                        generation_index=1,
                        reason_code="raw_capture",
                        reason_label="Captured by RawGraphAgent (retain-all)",
                        evidence_refs=(prov.provenance_id,),
                        confidence=score,
                        created_at_iso=created_at,
                    )
                    lineage = LineageRecord(
                        created_generation=generation_id,
                        created_generation_index=1,
                        last_modified_generation=generation_id,
                        last_modified_generation_index=1,
                        operations=(op,),
                        parent_history=(None,),
                        cmp_evidence=(prov.provenance_id,),
                    )
                    kind = _provisional_kind(role, block.kind.value)
                    nodes.append(
                        EducationalNode(
                            node_id=node_id,
                            generation_local_id=local_id,
                            title=title or f"(blank:{block.block_id})",
                            kind=kind,
                            role=role.value,
                            parent_node_id=None,
                            confidence=conf,
                            lineage=lineage,
                            active=True,
                            provenance_id=prov.provenance_id,
                            provenance=prov,
                            body=text,
                            attributes=(
                                ("source_page", str(page.page_number)),
                                ("block_kind", block.kind.value),
                                ("document_id", str(doc.document_id)),
                            ),
                        )
                    )

        metrics = compute_quality_snapshot(nodes, rejected_count=0)
        calibration_id = (
            context.calibration_profile.profile_id
            if context.calibration_profile
            else None
        )
        generation_hash = compute_generation_hash(
            source_document_ids=context.source_document_ids,
            parent_snapshot_hash="",
            calibration_profile_id=calibration_id,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
            generation_index=1,
            nodes=tuple(nodes),
        )
        generation = Generation(
            generation_id=generation_id,
            chain_id=context.chain_id,
            generation_index=1,
            purpose=purpose_for_index(1),
            parent_generation_ids=(),
            source_document_ids=context.source_document_ids,
            workspace_id=context.workspace_id,
            created_at_iso=created_at,
            calibration_profile_id=calibration_id,
        )
        return CurriculumGenerationSnapshot(
            snapshot_id=snapshot_id,
            generation=generation,
            nodes=tuple(nodes),
            rejected_nodes=(),
            metrics=metrics,
            provenance_bundle_id=f"bundle-{snapshot_id}",
            created_at_iso=created_at,
            status=SnapshotStatus.ACCEPTED,
            generation_hash=generation_hash,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
        )


def _role_confidence(role: ContentRole) -> float:
    if role is ContentRole.EDUCATIONAL:
        return 0.85
    if role is ContentRole.LEARNING_OBJECTIVE:
        return 0.9
    if role in {
        ContentRole.DEFINITION,
        ContentRole.EXAMPLE,
        ContentRole.WORKED_EXAMPLE,
    }:
        return 0.8
    if role is ContentRole.BLANK_ARTEFACT:
        return 0.95
    return 0.75


def _provisional_kind(role: ContentRole, block_kind: str) -> str:
    if role is ContentRole.LEARNING_OBJECTIVE:
        return "candidate_objective"
    if role is ContentRole.EDUCATIONAL:
        return "candidate"
    return f"candidate_{role.value}"


def _provenance(
    *,
    node_id: str,
    document_id: int,
    page_number: int,
    block_id: str,
    excerpt: str,
    created_at_iso: str,
    extraction_id: str,
) -> ProvenanceRecord:
    evidence = SupportingEvidence(
        page_number=page_number,
        paragraph_index=0,
        block_id=block_id,
        excerpt=excerpt,
    )
    return ProvenanceRecord(
        provenance_id=f"prov-{node_id}",
        subject_kind=ProvenanceSubjectKind.EDUCATIONAL_NODE,
        subject_id=node_id,
        source_document_id=document_id,
        source_version_label="raw-graph",
        source_pages=(page_number,),
        source_paragraphs=(0,),
        source_block_ids=(block_id,),
        parser_version="ei-raw-graph/1.0",
        mapper_version="ei-raw-graph/1.0",
        graph_builder_version="ei-raw-graph/1.0",
        pipeline_job_id="",
        extraction_id=extraction_id,
        parse_id="",
        map_id="",
        graph_id="",
        chain_stage=ProvenanceChainStage.DOCUMENT,
        evidence=(evidence,),
        created_at_iso=created_at_iso,
    )


def _empty_seed_documents(
    source_document_ids: tuple[int, ...],
) -> tuple[ExtractedDocument, ...]:
    """Fallback when no ExtractedDocument is supplied (orchestrator-only tests)."""
    from app.domain.curriculum_intelligence.extracted_document import (
        BlockKind,
        ExtractedBlock,
        ExtractedPage,
    )

    doc_id = source_document_ids[0] if source_document_ids else 0
    page = ExtractedPage(
        page_number=1,
        width=612.0,
        height=792.0,
        blocks=(
            ExtractedBlock(
                block_id="seed-subject",
                kind=BlockKind.HEADING,
                text="Subject Root",
                order_index=0,
            ),
            ExtractedBlock(
                block_id="seed-a",
                kind=BlockKind.PARAGRAPH,
                text="Topic A",
                order_index=1,
            ),
            ExtractedBlock(
                block_id="seed-b",
                kind=BlockKind.PARAGRAPH,
                text="Topic B",
                order_index=2,
            ),
            ExtractedBlock(
                block_id="seed-noise",
                kind=BlockKind.HEADING,
                text="Combined Materials Pack",
                order_index=3,
            ),
        ),
        raw_text="Subject Root\nTopic A\nTopic B\nCombined Materials Pack",
    )
    return (
        ExtractedDocument(
            extraction_id="seed-raw",
            document_id=doc_id,
            page_count=1,
            pages=(page,),
            metadata=(("title", "seed"),),
        ),
    )
