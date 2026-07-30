"""Generation 7 — Educational Certification Agent (EI-001D).

Produces a certified curriculum snapshot and Decision Ledger certification
entry. Does not invent educational structure — certifies Gen 6 (+ history).
"""

from __future__ import annotations

from dataclasses import replace

from app.application.curriculum_intelligence.agents.base import (
    CurriculumIntelligenceAgent,
    utc_now_iso,
)
from app.application.curriculum_intelligence.certification_engine import (
    DefaultCertificationEngine,
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
from app.application.curriculum_intelligence.ports.certification_engine_port import (
    CertificationEngine,
)
from app.domain.curriculum_intelligence.agent import (
    STANDARD_QUALITY_METRICS,
    AgentDescriptor,
)
from app.domain.curriculum_intelligence.certification import CertificationReport
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceRecord,
    confidence_band_from_score,
)
from app.domain.curriculum_intelligence.decision_ledger import (
    DecisionLedgerEntry,
    DecisionOutcome,
    DecisionType,
)
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
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
    agent_id="educational_certification_agent",
    name="EducationalCertificationAgent",
    purpose="educational_certification",
    consumes=("curriculum_generation_snapshot", "decision_ledger", "quality_history"),
    produces=(
        "curriculum_generation_snapshot",
        "certification_decision",
        "certification_report",
    ),
    dependencies=("educational_reconciliation_agent", "certification_engine"),
    version=_AGENT_VERSION,
    deterministic=True,
    supports_rollback=True,
    quality_metrics_produced=STANDARD_QUALITY_METRICS
    + ("quality_score", "decision_quality", "reasoning_confidence"),
)


class EducationalCertificationAgent(CurriculumIntelligenceAgent):
    """Generation 7 — Educational Certification."""

    generation_index = 7

    def __init__(self, *, engine: CertificationEngine | None = None) -> None:
        self._engine = engine or DefaultCertificationEngine()

    @property
    def descriptor(self) -> AgentDescriptor:
        return _DESCRIPTOR

    @property
    def last_certification_report(self) -> CertificationReport | None:
        """Most recent CertificationReport produced by ``execute``."""
        return getattr(self, "_last_report", None)

    def execute(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        if context.prior_snapshot is None:
            raise ValueError(
                "EducationalCertificationAgent requires a prior Gen 6 snapshot."
            )
        prior = context.prior_snapshot
        created_at = context.fixed_created_at_iso or utc_now_iso()
        generation_id = stable_id(
            "gen",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g7",
        )
        snapshot_id = stable_id(
            "snap",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g7",
        )
        decision_id = stable_id(
            "cert",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
        )

        # Certification scores the Gen 6 educational head (prior). Gen 7
        # snapshot carries the same active hierarchy plus a certification node.
        ledger = tuple(context.decision_ledger or ())
        quality_history = tuple(context.quality_history or ())
        regression_history = tuple(context.regression_history or ())

        if hasattr(self._engine, "certify_report"):
            report = self._engine.certify_report(
                prior,
                quality_history=quality_history or (prior,),
                regression_history=regression_history,
                decision_ledger=ledger,
                created_at_iso=created_at,
                decision_id=decision_id,
            )
        else:
            decision = self._engine.certify(
                prior,
                quality_history=quality_history or (prior,),
                regression_history=regression_history,
                decision_ledger=ledger,
                created_at_iso=created_at,
                decision_id=decision_id,
            )
            from app.domain.curriculum_intelligence.certification import (
                CertificationReport,
                DecisionQualityScores,
            )

            report = CertificationReport(
                decision=decision,
                decision_quality=DecisionQualityScores(
                    merge_quality=0.0,
                    split_quality=0.0,
                    objective_quality=0.0,
                    coverage_quality=0.0,
                    hierarchy_quality=0.0,
                    policy_consistency=0.0,
                    evidence_quality=decision.evidence_quality,
                    aggregate=decision.decision_quality,
                ),
                quality_vector=prior.metrics,
                hard_gate_failures=decision.hard_gate_failures,
                warnings=decision.warnings,
                reasons=decision.failure_reasons or decision.hard_gate_failures,
                ledger_entry_ids=tuple(e.decision_id for e in ledger),
            )
        self._last_report = report
        decision = report.decision

        # Rewrite decision to bind Gen 7 snapshot id (preview binds to Gen 7).
        decision = replace(decision, snapshot_id=snapshot_id)
        report = replace(report, decision=decision)
        self._last_report = report

        cert_node = self._certification_node(
            decision_id=decision_id,
            generation_id=generation_id,
            snapshot_id=snapshot_id,
            created_at=created_at,
            report=report,
        )

        # Carry forward the Gen 6 educational graph unchanged; Gen 7 adds
        # the certification report node only (no silent structure mutation).
        nodes = list(prior.nodes) + [cert_node]

        rejected = tuple(prior.rejected_nodes)
        metrics = compute_quality_snapshot(
            tuple(nodes),
            rejected_count=len(rejected),
            coverage_override=prior.metrics.coverage,
        )
        # Preserve Gen 6 educational scores on the certified snapshot.
        metrics = replace(
            metrics,
            coverage=prior.metrics.coverage,
            hierarchy=prior.metrics.hierarchy,
            duplicates=prior.metrics.duplicates,
            noise=prior.metrics.noise,
            granularity=prior.metrics.granularity,
            confidence=prior.metrics.confidence,
            evidence_quality=prior.metrics.evidence_quality,
            chapters=prior.metrics.chapters,
            sections=prior.metrics.sections,
            topics=prior.metrics.topics,
            objectives=prior.metrics.objectives,
            low_confidence_share=prior.metrics.low_confidence_share,
        )

        generation = Generation(
            generation_id=generation_id,
            chain_id=context.chain_id,
            generation_index=7,
            purpose=purpose_for_index(7),
            parent_generation_ids=(prior.generation_id,),
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
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
            generation_index=7,
            nodes=tuple(nodes),
        )
        snapshot = CurriculumGenerationSnapshot(
            snapshot_id=snapshot_id,
            generation=generation,
            nodes=tuple(nodes),
            rejected_nodes=rejected,
            metrics=metrics,
            provenance_bundle_id=prior.provenance_bundle_id or f"bundle-{snapshot_id}",
            created_at_iso=created_at,
            status=SnapshotStatus.ACCEPTED,
            generation_hash=generation_hash,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
        )

        # Append certification decision onto the pending ledger.
        cert_entry = DecisionLedgerEntry(
            decision_id=decision.decision_id,
            chain_id=context.chain_id,
            generation_index=7,
            generation_id=generation_id,
            agent_id=self.descriptor.agent_id,
            policy_id="certification_policy",
            evidence_refs=tuple(report.ledger_entry_ids[:20]),
            evidence_grade=EvidenceGrade.A,
            confidence=decision.confidence,
            reasoning_confidence=decision.reasoning_confidence,
            affected_node_ids=tuple(n.node_id for n in prior.active_nodes()[:50]),
            decision_type=DecisionType.CERTIFY,
            created_at_iso=created_at,
            decision_outcome=(
                DecisionOutcome.ACCEPTED
                if decision.outcome.value != "NOT_CERTIFIED"
                else DecisionOutcome.REJECTED
            ),
            reason="; ".join(report.reasons[:5]) or decision.outcome.value,
            detail=decision.outcome.value,
            snapshot_id=snapshot_id,
        )
        if context.pending_decisions is not None:
            context.pending_decisions.append(cert_entry)
        self._last_certification_decision = decision
        return snapshot

    def _certification_node(
        self,
        *,
        decision_id: str,
        generation_id: str,
        snapshot_id: str,
        created_at: str,
        report: CertificationReport,
    ) -> EducationalNode:
        decision = report.decision
        node_id = stable_id("node", "certification_report", snapshot_id)
        attrs = (
            ("certification_status", decision.outcome.value),
            ("quality_score", f"{decision.quality_score:.2f}"),
            ("coverage", f"{decision.coverage:.4f}"),
            ("hierarchy_score", f"{decision.hierarchy_score:.4f}"),
            ("granularity_score", f"{decision.granularity_score:.4f}"),
            ("evidence_quality", f"{decision.evidence_quality:.4f}"),
            ("confidence", f"{decision.confidence:.4f}"),
            ("reasoning_confidence", f"{decision.reasoning_confidence:.4f}"),
            ("decision_quality", f"{decision.decision_quality:.4f}"),
            ("hard_gate_failures", str(len(decision.hard_gate_failures))),
            ("warnings", str(len(decision.warnings))),
            ("decision_id", decision_id),
        )
        evidence = SupportingEvidence(
            page_number=None,
            paragraph_index=None,
            block_id=None,
            excerpt=f"Certification {decision.outcome.value}",
        )
        provenance = ProvenanceRecord(
            provenance_id=f"prov-{node_id}",
            subject_kind=ProvenanceSubjectKind.EDUCATIONAL_NODE,
            subject_id=node_id,
            source_document_id=0,
            source_version_label="certification",
            source_pages=(),
            source_paragraphs=(),
            source_block_ids=(),
            parser_version="ei-001d",
            mapper_version="ei-001d",
            graph_builder_version="ei-001d",
            pipeline_job_id="",
            extraction_id="",
            parse_id="",
            map_id="",
            graph_id="",
            chain_stage=ProvenanceChainStage.CURRICULUM_MAPPING,
            evidence=(evidence,),
            created_at_iso=created_at,
        )
        conf = ConfidenceRecord(
            confidence_id=f"conf-{node_id}",
            subject_kind="educational_node",
            subject_id=node_id,
            score=decision.confidence,
            band=confidence_band_from_score(decision.confidence),
            reason="educational_certification",
            factors=(),
            needs_review=decision.outcome.value == "NOT_CERTIFIED",
            review_threshold=0.6,
            provenance_id=provenance.provenance_id,
        )
        lineage = LineageRecord(
            created_generation=generation_id,
            created_generation_index=7,
            last_modified_generation=generation_id,
            last_modified_generation_index=7,
            operations=(
                LineageOperation(
                    operation_id=stable_id("op", node_id, generation_id, "created"),
                    kind=LineageOperationKind.CREATED,
                    generation_id=generation_id,
                    generation_index=7,
                    reason_code="cert:report",
                    reason_label="Educational certification report node",
                    created_at_iso=created_at,
                ),
            ),
        )
        return EducationalNode(
            node_id=node_id,
            generation_local_id=node_id,
            title=f"Certification: {decision.outcome.value}",
            kind="certification_report",
            role="certification",
            parent_node_id=None,
            confidence=conf,
            lineage=lineage,
            active=True,
            provenance_id=provenance.provenance_id,
            provenance=provenance,
            attributes=attrs,
            evidence_grade=EvidenceGrade.A,
            policy_id="certification_policy",
        )
