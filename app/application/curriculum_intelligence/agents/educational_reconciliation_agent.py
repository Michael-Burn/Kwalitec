"""Generation 6 — Educational Reconciliation Agent.

Compares official syllabus, CMP support, and generation history via
CoveragePolicy. Emits coverage matrix findings on the snapshot.
"""

from __future__ import annotations

import re
from dataclasses import replace

from app.application.curriculum_intelligence.agents.base import (
    CurriculumIntelligenceAgent,
    record_educational_decisions,
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
from app.application.curriculum_intelligence.policies.coverage_policy import (
    CoveragePolicy,
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
from app.domain.curriculum_intelligence.curriculum_entity import CurriculumEntityKind
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
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
    agent_id="educational_reconciliation_agent",
    name="EducationalReconciliationAgent",
    purpose="educational_reconciliation",
    consumes=("curriculum_generation_snapshot", "extracted_document"),
    produces=("curriculum_generation_snapshot", "coverage_matrix"),
    dependencies=("objective_intelligence_agent", "coverage_policy"),
    version=_AGENT_VERSION,
    deterministic=True,
    supports_rollback=True,
    quality_metrics_produced=STANDARD_QUALITY_METRICS,
)

_NUM = re.compile(r"^(\d+(?:\.\d+)*)\b")


class EducationalReconciliationAgent(CurriculumIntelligenceAgent):
    """Generation 6 — syllabus / CMP / history educational reconciliation."""

    generation_index = 6

    def __init__(
        self,
        *,
        policy: CoveragePolicy | None = None,
        classifier: ContentClassificationService | None = None,
        normalizer: DocumentNormalizationService | None = None,
        parser: StructuralParserService | None = None,
        mapper: CurriculumMappingService | None = None,
    ) -> None:
        self._policy = policy or CoveragePolicy()
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
                "EducationalReconciliationAgent requires a prior Gen 5 snapshot."
            )
        prior = context.prior_snapshot
        created_at = context.fixed_created_at_iso or utc_now_iso()
        generation_id = stable_id(
            "gen",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g6",
        )
        snapshot_id = stable_id(
            "snap",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g6",
        )

        syllabus_objectives = self._extract_syllabus_objectives(context)
        # Fallback: derive from prior active LO / topic syllabus refs.
        if not syllabus_objectives:
            syllabus_objectives = _objectives_from_nodes(prior.nodes)

        matrix = self._policy.reconcile(
            working_nodes=prior.nodes,
            syllabus_objectives=syllabus_objectives,
            decision_prefix=f"cov-{generation_id[-8:]}",
        )

        nodes: list[EducationalNode] = []
        for node in prior.nodes:
            grade = node.evidence_grade or (
                EvidenceGrade.A if node.lineage.syllabus_refs else EvidenceGrade.B
            )
            nodes.append(
                replace(
                    node,
                    evidence_grade=grade,
                    policy_id=node.policy_id or self._policy.policy_id,
                )
            )

        # Coverage summary node (Curriculum Memory artefact, not hierarchy authority).
        summary_id = stable_id("node", generation_id, "coverage_summary")
        summary_attrs = (
            ("coverage_covered", str(matrix.covered)),
            ("coverage_missing", str(matrix.missing)),
            ("coverage_unexpected", str(matrix.unexpected)),
            ("coverage_hierarchy_issues", str(matrix.hierarchy_issues)),
            ("coverage_completeness", f"{matrix.completeness:.4f}"),
            ("coverage_hierarchy_consistent", str(matrix.hierarchy_consistent)),
            ("syllabus_objective_count", str(matrix.syllabus_objective_count)),
            ("policy_id", self._policy.policy_id),
            ("finding_count", str(len(matrix.findings))),
        )
        for finding in matrix.findings[:40]:
            summary_attrs = summary_attrs + (
                (
                    f"finding:{finding.finding_id}",
                    f"{finding.kind.value}|{finding.syllabus_ref or ''}|"
                    f"{finding.title[:80]}|{finding.evidence_grade.value}",
                ),
            )

        score = min(0.99, 0.7 + 0.3 * matrix.completeness)
        conf = ConfidenceRecord(
            confidence_id=f"conf-{summary_id}",
            subject_kind="educational_node",
            subject_id=summary_id,
            score=score,
            band=confidence_band_from_score(score),
            reason="educational_reconciliation",
            factors=(),
            needs_review=matrix.missing > 0,
            review_threshold=0.6,
            provenance_id=f"prov-{summary_id}",
        )
        prov = ProvenanceRecord(
            provenance_id=f"prov-{summary_id}",
            subject_kind=ProvenanceSubjectKind.EDUCATIONAL_NODE,
            subject_id=summary_id,
            source_document_id=(
                context.source_document_ids[0] if context.source_document_ids else 0
            ),
            source_version_label="reconciliation",
            source_pages=(),
            source_paragraphs=(),
            source_block_ids=(f"recon-{summary_id}",),
            parser_version="ei-recon/1.0",
            mapper_version="ei-recon/1.0",
            graph_builder_version="ei-recon/1.0",
            pipeline_job_id="",
            extraction_id="",
            parse_id="",
            map_id="",
            graph_id="",
            chain_stage=ProvenanceChainStage.CURRICULUM_MAPPING,
            evidence=(
                SupportingEvidence(
                    page_number=None,
                    paragraph_index=0,
                    block_id=f"recon-{summary_id}",
                    excerpt=f"completeness={matrix.completeness:.4f}",
                ),
            ),
            created_at_iso=created_at,
        )
        op = LineageOperation(
            operation_id=stable_id("op", summary_id, "created"),
            kind=LineageOperationKind.CREATED,
            generation_id=generation_id,
            generation_index=6,
            reason_code="reconciliation:coverage_matrix",
            reason_label=(
                "Educational reconciliation coverage matrix against syllabus authority"
            ),
            evidence_refs=tuple(
                d.syllabus_ref for d in matrix.decisions if d.syllabus_ref
            )[:20],
            confidence=score,
            created_at_iso=created_at,
        )
        summary = EducationalNode(
            node_id=summary_id,
            generation_local_id="g6-coverage",
            title="Educational Coverage Matrix",
            kind="coverage_report",
            role=ContentRole.EDUCATIONAL.value,
            parent_node_id=None,
            confidence=conf,
            lineage=LineageRecord(
                created_generation=generation_id,
                created_generation_index=6,
                last_modified_generation=generation_id,
                last_modified_generation_index=6,
                operations=(op,),
            ),
            active=True,
            provenance_id=prov.provenance_id,
            provenance=prov,
            attributes=summary_attrs,
            evidence_grade=EvidenceGrade.A,
            policy_id=self._policy.policy_id,
        )
        nodes.append(summary)

        node_tuple = tuple(nodes)
        metrics = compute_quality_snapshot(
            node_tuple,
            rejected_count=len(prior.rejected_nodes),
            coverage_override=matrix.completeness,
        )
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
            generation_index=6,
            nodes=node_tuple,
        )
        generation = Generation(
            generation_id=generation_id,
            chain_id=context.chain_id,
            generation_index=6,
            purpose=purpose_for_index(6),
            parent_generation_ids=(prior.generation_id,),
            source_document_ids=context.source_document_ids,
            workspace_id=context.workspace_id,
            created_at_iso=created_at,
            calibration_profile_id=calibration_id,
        )
        record_educational_decisions(
            context,
            matrix.decisions,
            generation_index=6,
            generation_id=generation_id,
            agent_id=self.descriptor.agent_id,
            created_at_iso=created_at,
            snapshot_id=snapshot_id,
        )
        return CurriculumGenerationSnapshot(
            snapshot_id=snapshot_id,
            generation=generation,
            nodes=node_tuple,
            rejected_nodes=prior.rejected_nodes,
            metrics=metrics,
            provenance_bundle_id=f"bundle-{snapshot_id}",
            created_at_iso=created_at,
            status=SnapshotStatus.ACCEPTED,
            generation_hash=generation_hash,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
        )

    def _extract_syllabus_objectives(
        self, context: GenerationRunContext
    ) -> tuple[tuple[str, str], ...]:
        syllabus_doc = _select_syllabus_document(context.source_documents)
        if syllabus_doc is None:
            return ()
        normalized = self._normalizer.normalize(syllabus_doc)
        structural = self._parser.parse(normalized)
        curriculum_map = self._mapper.map(
            structural,
            subject_code=context.subject_code,
            version_label=context.version_label,
        )
        rows: list[tuple[str, str]] = []
        for entity in curriculum_map.entities:
            if entity.kind not in {
                CurriculumEntityKind.LEARNING_OBJECTIVE,
                CurriculumEntityKind.TOPIC,
            }:
                continue
            number = ""
            for key, value in entity.attributes:
                if key == "section_number":
                    number = value
                    break
            if not number:
                match = _NUM.match(entity.title.strip())
                number = match.group(1) if match else ""
            if number.count(".") < 1:
                continue
            rows.append((number, entity.title))
        # Prefer finest grain (depth ≥ 2).
        fine = [r for r in rows if r[0].count(".") >= 2]
        chosen = fine or rows
        # Stable unique by number.
        seen: set[str] = set()
        unique: list[tuple[str, str]] = []
        for number, title in sorted(chosen, key=lambda r: r[0]):
            if number in seen:
                continue
            seen.add(number)
            unique.append((number, title))
        return tuple(unique)


def _objectives_from_nodes(
    nodes: tuple[EducationalNode, ...],
) -> tuple[tuple[str, str], ...]:
    rows: list[tuple[str, str]] = []
    for node in nodes:
        if not node.active:
            continue
        if node.kind not in {"learning_objective", "objective", "topic", "concept"}:
            continue
        ref = node.lineage.syllabus_refs[0] if node.lineage.syllabus_refs else ""
        if not ref:
            match = _NUM.match(node.title.strip())
            ref = match.group(1) if match else ""
        if ref.count(".") >= 1:
            rows.append((ref, node.title))
    seen: set[str] = set()
    unique: list[tuple[str, str]] = []
    for number, title in sorted(rows, key=lambda r: r[0]):
        if number in seen:
            continue
        seen.add(number)
        unique.append((number, title))
    return tuple(unique)


def _select_syllabus_document(
    documents: tuple[ExtractedDocument, ...],
) -> ExtractedDocument | None:
    if not documents:
        return None
    for doc in documents:
        meta = " ".join(v for _k, v in doc.metadata).lower()
        title = (doc.metadata_value("title") or "").lower()
        kind = (doc.metadata_value("document_kind") or "").lower()
        if "syllabus" in f"{meta} {title} {kind}":
            return doc
    return documents[0]
