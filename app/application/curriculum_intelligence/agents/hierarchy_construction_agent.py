"""Generation 3 — Hierarchy Construction Agent.

Lifts EQ-001 structural parse + curriculum mapping into Subject → Chapter →
Section → Topic → Learning Objective with syllabus-first authority.
"""

from __future__ import annotations

from dataclasses import replace

from app.application.curriculum_intelligence.agents.base import (
    CurriculumIntelligenceAgent,
    utc_now_iso,
)
from app.application.curriculum_intelligence.content_classification_service import (
    ContentClassificationService,
)
from app.application.curriculum_intelligence.curriculum_mapping_service import (
    CurriculumMappingService,
)
from app.application.curriculum_intelligence.document_normalization_service import (
    DocumentNormalizationService,
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
from app.application.curriculum_intelligence.structural_parser_service import (
    StructuralParserService,
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
from app.domain.curriculum_intelligence.curriculum_entity import (
    CurriculumEntityKind,
    CurriculumKnowledgeEntity,
    CurriculumMap,
)
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument
from app.domain.curriculum_intelligence.generation import (
    CurriculumGenerationSnapshot,
    EducationalNode,
    Generation,
    LineageOperation,
    LineageOperationKind,
    LineageRecord,
    RejectedNode,
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
    agent_id="hierarchy_construction_agent",
    name="HierarchyConstructionAgent",
    purpose="hierarchy_construction",
    consumes=("curriculum_generation_snapshot", "extracted_document"),
    produces=("curriculum_generation_snapshot", "hierarchy"),
    dependencies=("noise_elimination_agent",),
    version=_AGENT_VERSION,
    deterministic=True,
    supports_rollback=True,
    quality_metrics_produced=STANDARD_QUALITY_METRICS,
)

_KIND_MAP: dict[CurriculumEntityKind, str] = {
    CurriculumEntityKind.SUBJECT: "subject",
    CurriculumEntityKind.MODULE: "chapter",
    CurriculumEntityKind.TOPIC: "topic",
    CurriculumEntityKind.SUBTOPIC: "section",
    CurriculumEntityKind.LEARNING_OBJECTIVE: "learning_objective",
}


class HierarchyConstructionAgent(CurriculumIntelligenceAgent):
    """Generation 3 — syllabus-first educational hierarchy."""

    generation_index = 3

    def __init__(
        self,
        *,
        classifier: ContentClassificationService | None = None,
        normalizer: DocumentNormalizationService | None = None,
        parser: StructuralParserService | None = None,
        mapper: CurriculumMappingService | None = None,
    ) -> None:
        self._classifier = classifier or ContentClassificationService()
        self._normalizer = normalizer or DocumentNormalizationService()
        self._parser = parser or StructuralParserService(self._classifier)
        self._mapper = mapper or CurriculumMappingService()

    @property
    def descriptor(self) -> AgentDescriptor:
        return _DESCRIPTOR

    def execute(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        if context.prior_snapshot is None:
            raise ValueError(
                "HierarchyConstructionAgent requires a prior Gen 2 snapshot."
            )
        prior = context.prior_snapshot
        created_at = context.fixed_created_at_iso or utc_now_iso()
        generation_id = stable_id(
            "gen",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g3",
        )
        snapshot_id = stable_id(
            "snap",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g3",
        )

        syllabus_doc = _select_syllabus_document(context.source_documents)
        if syllabus_doc is None and context.source_documents:
            syllabus_doc = context.source_documents[0]

        hierarchy_nodes: list[EducationalNode] = []
        if syllabus_doc is not None:
            curriculum_map = self._build_map(syllabus_doc, context)
            hierarchy_nodes = self._entities_to_nodes(
                curriculum_map,
                generation_id=generation_id,
                created_at=created_at,
            )

        # Carry forward rejected (inactive) noise nodes from Gen 2 — never delete.
        carried: list[EducationalNode] = []
        rejected: list[RejectedNode] = list(prior.rejected_nodes)
        for node in prior.nodes:
            if not node.active:
                carried.append(node)
                continue
            # Active Gen 2 candidates are superseded by hierarchy construction;
            # record a soft supersession only when not represented in hierarchy.
            # They remain queryable via inactive carry when unmatched.
            matched = _match_prior(node, hierarchy_nodes)
            if matched is None:
                op = LineageOperation(
                    operation_id=stable_id(
                        "op", node.node_id, generation_id, "supersede"
                    ),
                    kind=LineageOperationKind.REJECTED,
                    generation_id=generation_id,
                    generation_index=3,
                    reason_code="hierarchy:not_promoted",
                    reason_label=(
                        "Not promoted into Subject→Chapter→Section→Topic→LO chain"
                    ),
                    evidence_refs=(node.provenance_id,) if node.provenance_id else (),
                    confidence=node.confidence.score,
                    created_at_iso=created_at,
                )
                inactive = replace(
                    node, active=False, lineage=node.lineage.with_appended(op)
                )
                carried.append(inactive)
                rejected.append(
                    RejectedNode(
                        node=inactive,
                        rejected_at_generation=generation_id,
                        reason_code=op.reason_code,
                        reason_label=op.reason_label,
                        confidence=node.confidence.score,
                        evidence_refs=op.evidence_refs,
                    )
                )

        nodes = tuple(hierarchy_nodes + carried)
        metrics = compute_quality_snapshot(nodes, rejected_count=len(rejected))
        calibration_id = (
            context.calibration_profile.profile_id
            if context.calibration_profile
            else prior.generation.calibration_profile_id
        )
        generation_hash = compute_generation_hash(
            source_document_ids=context.source_document_ids,
            parent_snapshot_hash=prior.generation_hash,
            calibration_profile_id=calibration_id,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
            generation_index=3,
            nodes=nodes,
        )
        generation = Generation(
            generation_id=generation_id,
            chain_id=context.chain_id,
            generation_index=3,
            purpose=purpose_for_index(3),
            parent_generation_ids=(prior.generation_id,),
            source_document_ids=context.source_document_ids,
            workspace_id=context.workspace_id,
            created_at_iso=created_at,
            calibration_profile_id=calibration_id,
        )
        return CurriculumGenerationSnapshot(
            snapshot_id=snapshot_id,
            generation=generation,
            nodes=nodes,
            rejected_nodes=tuple(rejected),
            metrics=metrics,
            provenance_bundle_id=f"bundle-{snapshot_id}",
            created_at_iso=created_at,
            status=SnapshotStatus.ACCEPTED,
            generation_hash=generation_hash,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
        )

    def _build_map(
        self, document: ExtractedDocument, context: GenerationRunContext
    ) -> CurriculumMap:
        normalized = self._normalizer.normalize(document)
        structural = self._parser.parse(normalized)
        return self._mapper.map(
            structural,
            subject_code=context.subject_code,
            version_label=context.version_label,
        )

    def _entities_to_nodes(
        self,
        curriculum_map: CurriculumMap,
        *,
        generation_id: str,
        created_at: str,
    ) -> list[EducationalNode]:
        entity_to_node: dict[str, str] = {}
        nodes: list[EducationalNode] = []
        for index, entity in enumerate(curriculum_map.entities):
            kind = _KIND_MAP.get(entity.kind)
            if kind is None:
                # Teaching support entities are out of Gen 3 hierarchy scope.
                continue
            node_id = stable_id(
                "node",
                generation_id,
                entity.kind.value,
                entity.title,
                str(entity.source_pages),
                str(index),
            )
            entity_to_node[entity.entity_id] = node_id

        for index, entity in enumerate(curriculum_map.entities):
            kind = _KIND_MAP.get(entity.kind)
            if kind is None:
                continue
            node_id = entity_to_node[entity.entity_id]
            parent_node_id = (
                entity_to_node.get(entity.parent_id) if entity.parent_id else None
            )
            page = entity.source_pages[0] if entity.source_pages else 0
            prov = _hierarchy_provenance(
                node_id=node_id,
                document_id=entity.source_document_id,
                page_number=page,
                title=entity.title,
                created_at_iso=created_at,
            )
            score = float(entity.confidence)
            conf = ConfidenceRecord(
                confidence_id=f"conf-{node_id}",
                subject_kind="educational_node",
                subject_id=node_id,
                score=score,
                band=confidence_band_from_score(score),
                reason="hierarchy_construction",
                factors=(),
                needs_review=entity.needs_review,
                review_threshold=0.6,
                provenance_id=prov.provenance_id,
            )
            role = (
                ContentRole.LEARNING_OBJECTIVE.value
                if kind == "learning_objective"
                else ContentRole.EDUCATIONAL.value
            )
            op = LineageOperation(
                operation_id=stable_id("op", node_id, "created"),
                kind=LineageOperationKind.CREATED,
                generation_id=generation_id,
                generation_index=3,
                reason_code="hierarchy:syllabus_first",
                reason_label=(
                    "Constructed via syllabus-first "
                    "Subject→Chapter→Section→Topic→LO"
                ),
                evidence_refs=(prov.provenance_id,),
                confidence=score,
                created_at_iso=created_at,
            )
            syllabus_refs = ()
            section_num = _attr(entity, "section_number")
            if section_num:
                syllabus_refs = (section_num,)
            lineage = LineageRecord(
                created_generation=generation_id,
                created_generation_index=3,
                last_modified_generation=generation_id,
                last_modified_generation_index=3,
                operations=(op,),
                syllabus_refs=syllabus_refs,
                parent_history=(parent_node_id,),
            )
            attrs = list(entity.attributes)
            attrs.append(("hierarchy_kind", kind))
            nodes.append(
                EducationalNode(
                    node_id=node_id,
                    generation_local_id=f"g3-{index}",
                    title=entity.title,
                    kind=kind,
                    role=role,
                    parent_node_id=parent_node_id,
                    confidence=conf,
                    lineage=lineage,
                    active=True,
                    provenance_id=prov.provenance_id,
                    provenance=prov,
                    body=entity.body,
                    attributes=tuple(attrs),
                )
            )
        return nodes


def _attr(entity: CurriculumKnowledgeEntity, key: str) -> str | None:
    for k, v in entity.attributes:
        if k == key:
            return v
    return None


def _match_prior(
    prior: EducationalNode, hierarchy: list[EducationalNode]
) -> EducationalNode | None:
    title = prior.title.strip().lower()
    if not title:
        return None
    for node in hierarchy:
        if node.title.strip().lower() == title:
            return node
        # Numbered syllabus titles often prefix the prior candidate text.
        if title in node.title.strip().lower() or node.title.strip().lower() in title:
            return node
    return None


def _select_syllabus_document(
    documents: tuple[ExtractedDocument, ...],
) -> ExtractedDocument | None:
    """Prefer documents whose metadata/title indicates an official syllabus."""
    if not documents:
        return None
    for doc in documents:
        meta = " ".join(v for _k, v in doc.metadata).lower()
        title = (doc.metadata_value("title") or "").lower()
        kind = (doc.metadata_value("document_kind") or "").lower()
        blob = f"{meta} {title} {kind}"
        if "syllabus" in blob:
            return doc
    # Heuristic: weighted topic headings indicate syllabus authority.
    for doc in documents:
        text = doc.full_text[:2000]
        if "[" in text and "%" in text and any(
            line.strip()[:1].isdigit() for line in text.splitlines()[:40]
        ):
            return doc
    return documents[0] if len(documents) == 1 else documents[0]


def _hierarchy_provenance(
    *,
    node_id: str,
    document_id: int,
    page_number: int,
    title: str,
    created_at_iso: str,
) -> ProvenanceRecord:
    evidence = SupportingEvidence(
        page_number=page_number or None,
        paragraph_index=0,
        block_id=f"hier-{node_id}",
        excerpt=title[:200],
    )
    return ProvenanceRecord(
        provenance_id=f"prov-{node_id}",
        subject_kind=ProvenanceSubjectKind.EDUCATIONAL_NODE,
        subject_id=node_id,
        source_document_id=document_id,
        source_version_label="hierarchy",
        source_pages=(page_number,) if page_number else (),
        source_paragraphs=(0,),
        source_block_ids=(evidence.block_id or "",),
        parser_version="ei-hierarchy/1.0",
        mapper_version="ei-hierarchy/1.0",
        graph_builder_version="ei-hierarchy/1.0",
        pipeline_job_id="",
        extraction_id="",
        parse_id="",
        map_id="",
        graph_id="",
        chain_stage=ProvenanceChainStage.CURRICULUM_MAPPING,
        evidence=(evidence,),
        created_at_iso=created_at_iso,
    )
