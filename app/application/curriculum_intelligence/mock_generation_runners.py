"""Mock GenerationRunners for EI-001A orchestrator foundation.

No educational intelligence — runners emit deterministic placeholder graphs
so sequencing, snapshots, regression, and rollback can be exercised.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from uuid import uuid4

from app.application.curriculum_intelligence.generation_hash import (
    compute_generation_hash,
)
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceBand,
    ConfidenceRecord,
    confidence_band_from_score,
)
from app.domain.curriculum_intelligence.extracted_document import ExtractedDocument
from app.domain.curriculum_intelligence.generation import (
    CalibrationProfile,
    CurriculumGenerationSnapshot,
    EducationalNode,
    Generation,
    LineageOperation,
    LineageOperationKind,
    LineageRecord,
    QualitySnapshot,
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


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class GenerationRunContext:
    """Inputs available to a generation runner / agent."""

    chain_id: str
    workspace_id: str
    source_document_ids: tuple[int, ...]
    prior_snapshot: CurriculumGenerationSnapshot | None
    calibration_profile: CalibrationProfile | None = None
    source_documents: tuple[ExtractedDocument, ...] = ()
    subject_code: str = "CS1"
    version_label: str = "default"
    fixed_created_at_iso: str | None = None
    # Phase D — Decision Ledger sink + Gen 7 certification inputs.
    pending_decisions: list | None = None
    decision_ledger: tuple = ()
    quality_history: tuple = ()
    regression_history: tuple = ()


class GenerationRunner:
    """One educational purpose; Phase A mock implementations only."""

    generation_index: int

    def run(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        raise NotImplementedError


def _confidence(
    subject_id: str, score: float, provenance_id: str | None
) -> ConfidenceRecord:
    band = confidence_band_from_score(score)
    return ConfidenceRecord(
        confidence_id=f"conf-{subject_id}",
        subject_kind="educational_node",
        subject_id=subject_id,
        score=score,
        band=band,
        reason="mock_runner",
        factors=(),
        needs_review=band in {ConfidenceBand.LOW, ConfidenceBand.VERY_LOW},
        review_threshold=0.6,
        provenance_id=provenance_id,
    )


def _provenance(
    node_id: str, document_id: int, created_at_iso: str
) -> ProvenanceRecord:
    evidence = SupportingEvidence(
        page_number=1,
        paragraph_index=0,
        block_id=f"block-{node_id}",
        excerpt=f"mock evidence for {node_id}",
    )
    return ProvenanceRecord(
        provenance_id=f"prov-{node_id}",
        subject_kind=ProvenanceSubjectKind.EDUCATIONAL_NODE,
        subject_id=node_id,
        source_document_id=document_id,
        source_version_label="mock",
        source_pages=(1,),
        source_paragraphs=(0,),
        source_block_ids=(evidence.block_id or "",),
        parser_version="ei-mock/1.0",
        mapper_version="ei-mock/1.0",
        graph_builder_version="ei-mock/1.0",
        pipeline_job_id="mock-job",
        extraction_id="mock-extraction",
        parse_id="mock-parse",
        map_id="mock-map",
        graph_id="mock-graph",
        chain_stage=ProvenanceChainStage.DOCUMENT,
        evidence=(evidence,),
        created_at_iso=created_at_iso,
    )


def _empty_metrics(*, active: int = 0, rejected: int = 0) -> QualitySnapshot:
    return QualitySnapshot(
        coverage=1.0,
        hierarchy=1.0,
        duplicates=0.0,
        noise=0.0,
        granularity=0.5,
        confidence=0.9,
        active_node_count=active,
        rejected_node_count=rejected,
        low_confidence_share=0.0,
    )


class MockRawGraphRunner(GenerationRunner):
    """Generation 1 — emit a maximal placeholder educational graph."""

    generation_index = 1

    def __init__(self, *, seed_titles: tuple[str, ...] | None = None) -> None:
        self._seed_titles = seed_titles or (
            "Subject Root",
            "Topic A",
            "Topic B",
            "Front Matter Noise",
        )

    def run(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        created_at = _utc_now_iso()
        generation_id = f"gen-{uuid4().hex[:12]}"
        snapshot_id = f"snap-{uuid4().hex[:12]}"
        document_id = (
            context.source_document_ids[0] if context.source_document_ids else 0
        )
        nodes: list[EducationalNode] = []
        for index, title in enumerate(self._seed_titles):
            node_id = f"node-{uuid4().hex[:12]}"
            local_id = f"g1-{index}"
            prov = _provenance(node_id, document_id, created_at)
            op = LineageOperation(
                operation_id=f"op-{uuid4().hex[:12]}",
                kind=LineageOperationKind.CREATED,
                generation_id=generation_id,
                generation_index=1,
                reason_code="raw_capture",
                reason_label="Captured by mock raw graph runner",
                evidence_refs=(prov.provenance_id,),
                confidence=0.9,
                created_at_iso=created_at,
            )
            lineage = LineageRecord(
                created_generation=generation_id,
                created_generation_index=1,
                last_modified_generation=generation_id,
                last_modified_generation_index=1,
                operations=(op,),
                parent_history=(None,),
            )
            if "Noise" in title or "Front" in title:
                role = "front_matter"
            else:
                role = "educational_content"
            nodes.append(
                EducationalNode(
                    node_id=node_id,
                    generation_local_id=local_id,
                    title=title,
                    kind="topic" if index else "subject",
                    role=role,
                    parent_node_id=nodes[0].node_id if index else None,
                    confidence=_confidence(node_id, 0.9, prov.provenance_id),
                    lineage=lineage,
                    active=True,
                    provenance_id=prov.provenance_id,
                    provenance=prov,
                )
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
            calibration_profile_id=(
                context.calibration_profile.profile_id
                if context.calibration_profile
                else None
            ),
        )
        metrics = _empty_metrics(active=len(nodes))
        generation_hash = compute_generation_hash(
            source_document_ids=context.source_document_ids,
            parent_snapshot_hash="",
            calibration_profile_id=generation.calibration_profile_id,
            agent_id="mock_raw_graph",
            agent_version="1.0.0",
            generation_index=1,
            nodes=tuple(nodes),
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
            agent_id="mock_raw_graph",
            agent_version="1.0.0",
        )


class MockPassThroughRunner(GenerationRunner):
    """Generations 2–7 mock — copy prior graph with optional metric override."""

    def __init__(
        self,
        generation_index: int,
        *,
        metrics_override: QualitySnapshot | None = None,
        reject_roles: frozenset[str] | None = None,
    ) -> None:
        if generation_index < 2 or generation_index > 7:
            raise ValueError("MockPassThroughRunner supports indices 2..7")
        self.generation_index = generation_index
        self._metrics_override = metrics_override
        self._reject_roles = reject_roles or frozenset()

    def run(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        if context.prior_snapshot is None:
            raise ValueError(
                f"Generation {self.generation_index} requires a prior snapshot."
            )
        created_at = _utc_now_iso()
        generation_id = f"gen-{uuid4().hex[:12]}"
        snapshot_id = f"snap-{uuid4().hex[:12]}"
        prior = context.prior_snapshot
        parent_ids = (prior.generation_id,)

        nodes: list[EducationalNode] = []
        rejected: list[RejectedNode] = list(prior.rejected_nodes)
        for node in prior.nodes:
            if not node.active:
                nodes.append(node)
                continue
            if node.role in self._reject_roles:
                op = LineageOperation(
                    operation_id=f"op-{uuid4().hex[:12]}",
                    kind=LineageOperationKind.REJECTED,
                    generation_id=generation_id,
                    generation_index=self.generation_index,
                    reason_code="mock_noise_reject",
                    reason_label=f"Rejected role {node.role}",
                    evidence_refs=(node.provenance_id,) if node.provenance_id else (),
                    confidence=node.confidence.score,
                    created_at_iso=created_at,
                )
                lineage = node.lineage.with_appended(op)
                inactive = replace(node, active=False, lineage=lineage)
                nodes.append(inactive)
                rejected.append(
                    RejectedNode(
                        node=inactive,
                        rejected_at_generation=generation_id,
                        reason_code=op.reason_code,
                        reason_label=op.reason_label,
                        confidence=node.confidence.score,
                    )
                )
                continue
            nodes.append(node)

        active_count = sum(1 for n in nodes if n.active)
        metrics = self._metrics_override or _empty_metrics(
            active=active_count, rejected=len(rejected)
        )
        if self._metrics_override is None:
            metrics = replace(
                metrics,
                active_node_count=active_count,
                rejected_node_count=len(rejected),
            )

        generation = Generation(
            generation_id=generation_id,
            chain_id=context.chain_id,
            generation_index=self.generation_index,
            purpose=purpose_for_index(self.generation_index),
            parent_generation_ids=parent_ids,
            source_document_ids=context.source_document_ids,
            workspace_id=context.workspace_id,
            created_at_iso=created_at,
            calibration_profile_id=(
                context.calibration_profile.profile_id
                if context.calibration_profile
                else None
            ),
        )
        generation_hash = compute_generation_hash(
            source_document_ids=context.source_document_ids,
            parent_snapshot_hash=prior.generation_hash,
            calibration_profile_id=generation.calibration_profile_id,
            agent_id=f"mock_passthrough_{self.generation_index}",
            agent_version="1.0.0",
            generation_index=self.generation_index,
            nodes=tuple(nodes),
        )
        return CurriculumGenerationSnapshot(
            snapshot_id=snapshot_id,
            generation=generation,
            nodes=tuple(nodes),
            rejected_nodes=tuple(rejected),
            metrics=metrics,
            provenance_bundle_id=f"bundle-{snapshot_id}",
            created_at_iso=created_at,
            status=SnapshotStatus.ACCEPTED,
            generation_hash=generation_hash,
            agent_id=f"mock_passthrough_{self.generation_index}",
            agent_version="1.0.0",
        )


def default_mock_runners(
    *,
    regressing_index: int | None = None,
) -> dict[int, GenerationRunner]:
    """Build the standard mock runner map for orchestrator tests."""
    runners: dict[int, GenerationRunner] = {1: MockRawGraphRunner()}
    for index in range(2, 8):
        metrics = None
        reject_roles = frozenset({"front_matter"}) if index == 2 else frozenset()
        if regressing_index is not None and index == regressing_index:
            metrics = QualitySnapshot(
                coverage=0.5,
                hierarchy=0.5,
                duplicates=0.2,
                noise=0.4,
                granularity=0.2,
                confidence=0.5,
            )
        runners[index] = MockPassThroughRunner(
            index, metrics_override=metrics, reject_roles=reject_roles
        )
    return runners
