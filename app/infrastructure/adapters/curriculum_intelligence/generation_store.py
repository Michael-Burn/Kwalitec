"""SQLAlchemy adapter for EI-001 GenerationStorePort.

Application code depends on the port only; this adapter owns ORM mapping.
Snapshot content is insert-once; only ``status`` may be updated.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any

from app.application.curriculum_intelligence.exceptions import (
    LineageAppendError,
    SnapshotImmutableError,
    SnapshotNotFoundError,
)
from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceBand,
    ConfidenceFactor,
    ConfidenceRecord,
)
from app.domain.curriculum_intelligence.decision_ledger import (
    DecisionLedgerEntry,
    DecisionOutcome,
    DecisionType,
)
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
from app.domain.curriculum_intelligence.generation import (
    CalibrationProfile,
    CertificationDecision,
    CertificationOutcome,
    CurriculumGenerationSnapshot,
    DifficultyBiasStyle,
    EducationalNode,
    Generation,
    GranularityStyle,
    HierarchyStyle,
    LineageOperation,
    LineageOperationKind,
    LineageRecord,
    QualitySnapshot,
    RegressionReport,
    RejectedNode,
    SnapshotStatus,
    TopicDensityStyle,
)
from app.domain.curriculum_intelligence.provenance import (
    ProvenanceChainStage,
    ProvenanceRecord,
    ProvenanceSubjectKind,
    SupportingEvidence,
)
from app.extensions import db
from app.models.curriculum_generation import (
    EiCalibrationProfile,
    EiCertificationRecord,
    EiDecisionLedgerEntry,
    EiEducationalNode,
    EiGeneration,
    EiGenerationChain,
    EiGenerationSnapshot,
    EiLineageOperation,
    EiRegressionReport,
)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    return json.loads(raw)


def _parse_dt(value: datetime | str) -> datetime:
    if isinstance(value, datetime):
        return value.replace(tzinfo=None) if value.tzinfo else value
    text = value.replace("Z", "+00:00")
    return datetime.fromisoformat(text).replace(tzinfo=None)


def _iso(value: datetime) -> str:
    return value.replace(tzinfo=UTC).isoformat().replace("+00:00", "Z")


def _quality_to_dict(metrics: QualitySnapshot) -> dict[str, Any]:
    return asdict(metrics)


def _quality_from_dict(data: dict[str, Any]) -> QualitySnapshot:
    return QualitySnapshot(
        coverage=float(data.get("coverage", 0.0)),
        hierarchy=float(data.get("hierarchy", 0.0)),
        duplicates=float(data.get("duplicates", 0.0)),
        noise=float(data.get("noise", 0.0)),
        granularity=float(data.get("granularity", 0.0)),
        confidence=float(data.get("confidence", 0.0)),
        active_node_count=int(data.get("active_node_count", 0)),
        rejected_node_count=int(data.get("rejected_node_count", 0)),
        low_confidence_share=float(data.get("low_confidence_share", 0.0)),
        chapters=int(data.get("chapters", 0)),
        sections=int(data.get("sections", 0)),
        topics=int(data.get("topics", 0)),
        objectives=int(data.get("objectives", 0)),
        evidence_quality=float(data.get("evidence_quality", 0.0)),
    )


def _confidence_to_dict(record: ConfidenceRecord) -> dict[str, Any]:
    return {
        "confidence_id": record.confidence_id,
        "subject_kind": record.subject_kind,
        "subject_id": record.subject_id,
        "score": record.score,
        "band": record.band.value,
        "reason": record.reason,
        "factors": [asdict(f) for f in record.factors],
        "needs_review": record.needs_review,
        "review_threshold": record.review_threshold,
        "provenance_id": record.provenance_id,
    }


def _confidence_from_dict(data: dict[str, Any]) -> ConfidenceRecord:
    factors = tuple(
        ConfidenceFactor(**f) for f in data.get("factors", [])
    )
    return ConfidenceRecord(
        confidence_id=data["confidence_id"],
        subject_kind=data["subject_kind"],
        subject_id=data["subject_id"],
        score=float(data["score"]),
        band=ConfidenceBand(data["band"]),
        reason=data.get("reason", ""),
        factors=factors,
        needs_review=bool(data.get("needs_review", False)),
        review_threshold=float(data.get("review_threshold", 0.6)),
        provenance_id=data.get("provenance_id"),
    )


def _lineage_op_to_dict(op: LineageOperation) -> dict[str, Any]:
    return {
        "operation_id": op.operation_id,
        "kind": op.kind.value,
        "generation_id": op.generation_id,
        "generation_index": op.generation_index,
        "reason_code": op.reason_code,
        "reason_label": op.reason_label,
        "related_node_ids": list(op.related_node_ids),
        "evidence_refs": list(op.evidence_refs),
        "confidence": op.confidence,
        "created_at_iso": op.created_at_iso,
    }


def _lineage_op_from_dict(data: dict[str, Any]) -> LineageOperation:
    return LineageOperation(
        operation_id=data["operation_id"],
        kind=LineageOperationKind(data["kind"]),
        generation_id=data["generation_id"],
        generation_index=int(data["generation_index"]),
        reason_code=data.get("reason_code", ""),
        reason_label=data.get("reason_label", ""),
        related_node_ids=tuple(data.get("related_node_ids", [])),
        evidence_refs=tuple(data.get("evidence_refs", [])),
        confidence=data.get("confidence"),
        created_at_iso=data.get("created_at_iso", ""),
    )


def _lineage_to_dict(record: LineageRecord) -> dict[str, Any]:
    return {
        "created_generation": record.created_generation,
        "created_generation_index": record.created_generation_index,
        "last_modified_generation": record.last_modified_generation,
        "last_modified_generation_index": record.last_modified_generation_index,
        "operations": [_lineage_op_to_dict(op) for op in record.operations],
        "related_node_ids": list(record.related_node_ids),
        "syllabus_refs": list(record.syllabus_refs),
        "cmp_evidence": list(record.cmp_evidence),
        "parent_history": list(record.parent_history),
        "merged_from": list(record.merged_from),
        "split_into": list(record.split_into),
        "rejection_reason_code": record.rejection_reason_code,
        "rejection_reason_label": record.rejection_reason_label,
    }


def _lineage_from_dict(data: dict[str, Any]) -> LineageRecord:
    return LineageRecord(
        created_generation=data["created_generation"],
        created_generation_index=int(data["created_generation_index"]),
        last_modified_generation=data["last_modified_generation"],
        last_modified_generation_index=int(data["last_modified_generation_index"]),
        operations=tuple(
            _lineage_op_from_dict(op) for op in data.get("operations", [])
        ),
        related_node_ids=tuple(data.get("related_node_ids", [])),
        syllabus_refs=tuple(data.get("syllabus_refs", [])),
        cmp_evidence=tuple(data.get("cmp_evidence", [])),
        parent_history=tuple(data.get("parent_history", [])),
        merged_from=tuple(data.get("merged_from", [])),
        split_into=tuple(data.get("split_into", [])),
        rejection_reason_code=data.get("rejection_reason_code"),
        rejection_reason_label=data.get("rejection_reason_label"),
    )


def _provenance_to_dict(record: ProvenanceRecord) -> dict[str, Any]:
    return {
        "provenance_id": record.provenance_id,
        "subject_kind": record.subject_kind.value,
        "subject_id": record.subject_id,
        "source_document_id": record.source_document_id,
        "source_version_label": record.source_version_label,
        "source_pages": list(record.source_pages),
        "source_paragraphs": list(record.source_paragraphs),
        "source_block_ids": list(record.source_block_ids),
        "parser_version": record.parser_version,
        "mapper_version": record.mapper_version,
        "graph_builder_version": record.graph_builder_version,
        "pipeline_job_id": record.pipeline_job_id,
        "extraction_id": record.extraction_id,
        "parse_id": record.parse_id,
        "map_id": record.map_id,
        "graph_id": record.graph_id,
        "chain_stage": record.chain_stage.value,
        "evidence": [asdict(e) for e in record.evidence],
        "created_at_iso": record.created_at_iso,
        "attributes": [list(pair) for pair in record.attributes],
    }


def _provenance_from_dict(data: dict[str, Any]) -> ProvenanceRecord:
    evidence = tuple(SupportingEvidence(**e) for e in data.get("evidence", []))
    attributes = tuple(tuple(pair) for pair in data.get("attributes", []))
    return ProvenanceRecord(
        provenance_id=data["provenance_id"],
        subject_kind=ProvenanceSubjectKind(data["subject_kind"]),
        subject_id=data["subject_id"],
        source_document_id=int(data["source_document_id"]),
        source_version_label=data.get("source_version_label", ""),
        source_pages=tuple(data.get("source_pages", [])),
        source_paragraphs=tuple(data.get("source_paragraphs", [])),
        source_block_ids=tuple(data.get("source_block_ids", [])),
        parser_version=data.get("parser_version", ""),
        mapper_version=data.get("mapper_version", ""),
        graph_builder_version=data.get("graph_builder_version", ""),
        pipeline_job_id=data.get("pipeline_job_id", ""),
        extraction_id=data.get("extraction_id", ""),
        parse_id=data.get("parse_id", ""),
        map_id=data.get("map_id", ""),
        graph_id=data.get("graph_id", ""),
        chain_stage=ProvenanceChainStage(data["chain_stage"]),
        evidence=evidence,
        created_at_iso=data.get("created_at_iso", ""),
        attributes=attributes,  # type: ignore[arg-type]
    )


class SqlAlchemyGenerationStore(GenerationStorePort):
    """Durable Generation Store backed by ``ei_*`` tables."""

    def append_snapshot(self, snapshot: CurriculumGenerationSnapshot) -> None:
        existing = EiGenerationSnapshot.query.filter_by(
            snapshot_id=snapshot.snapshot_id
        ).first()
        if existing:
            raise SnapshotImmutableError(
                f"Snapshot {snapshot.snapshot_id!r} already exists "
                "and cannot be rewritten."
            )

        chain = EiGenerationChain.query.filter_by(chain_id=snapshot.chain_id).first()
        if chain is None:
            chain = EiGenerationChain(
                chain_id=snapshot.chain_id,
                workspace_id=snapshot.generation.workspace_id,
            )
            db.session.add(chain)
        elif (
            snapshot.generation.workspace_id
            and not (chain.workspace_id or "").strip()
        ):
            chain.workspace_id = snapshot.generation.workspace_id
        elif (
            snapshot.generation.workspace_id
            and chain.workspace_id
            and chain.workspace_id != snapshot.generation.workspace_id
        ):
            # Workspace rebinding: one active chain per workspace.
            chain.workspace_id = snapshot.generation.workspace_id

        existing_gen = EiGeneration.query.filter_by(
            generation_id=snapshot.generation_id
        ).first()
        if existing_gen is None:
            gen = snapshot.generation
            db.session.add(
                EiGeneration(
                    generation_id=gen.generation_id,
                    chain_id=gen.chain_id,
                    generation_index=gen.generation_index,
                    purpose=gen.purpose,
                    parent_generation_ids_json=_dumps(list(gen.parent_generation_ids)),
                    source_document_ids_json=_dumps(list(gen.source_document_ids)),
                    workspace_id=gen.workspace_id,
                    calibration_profile_id=gen.calibration_profile_id,
                    created_at=_parse_dt(gen.created_at_iso),
                )
            )

        db.session.add(
            EiGenerationSnapshot(
                snapshot_id=snapshot.snapshot_id,
                generation_id=snapshot.generation_id,
                chain_id=snapshot.chain_id,
                generation_index=snapshot.generation_index,
                provenance_bundle_id=snapshot.provenance_bundle_id,
                status=snapshot.status.value,
                metrics_json=_dumps(_quality_to_dict(snapshot.metrics)),
                generation_hash=snapshot.generation_hash or "",
                agent_id=snapshot.agent_id or "",
                agent_version=snapshot.agent_version or "",
                created_at=_parse_dt(snapshot.created_at_iso),
            )
        )

        for node in snapshot.nodes:
            self._insert_node_row(snapshot, node, rejected=None)
            for op in node.lineage.operations:
                self._ensure_lineage_op(snapshot.chain_id, node.node_id, op)

        for rejected in snapshot.rejected_nodes:
            # Rejected nodes already present in nodes as inactive; store extra row flag
            # only when the rejected payload is not already covered.
            existing = any(n.node_id == rejected.node.node_id for n in snapshot.nodes)
            if not existing:
                self._insert_node_row(snapshot, rejected.node, rejected=rejected)

        db.session.flush()

    def _insert_node_row(
        self,
        snapshot: CurriculumGenerationSnapshot,
        node: EducationalNode,
        *,
        rejected: RejectedNode | None,
    ) -> None:
        attrs = dict(node.attributes)
        if node.evidence_grade is not None:
            attrs["_evidence_grade"] = node.evidence_grade.value
        if node.policy_id:
            attrs["_policy_id"] = node.policy_id
        db.session.add(
            EiEducationalNode(
                snapshot_id=snapshot.snapshot_id,
                chain_id=snapshot.chain_id,
                node_id=node.node_id,
                generation_local_id=node.generation_local_id,
                title=node.title,
                kind=node.kind,
                role=node.role,
                parent_node_id=node.parent_node_id,
                active=node.active,
                body=node.body,
                provenance_id=node.provenance_id,
                confidence_json=_dumps(_confidence_to_dict(node.confidence)),
                lineage_json=_dumps(_lineage_to_dict(node.lineage)),
                provenance_json=(
                    _dumps(_provenance_to_dict(node.provenance))
                    if node.provenance is not None
                    else None
                ),
                attributes_json=_dumps(attrs),
                is_rejected_record=rejected is not None or not node.active,
                rejection_reason_code=(
                    rejected.reason_code
                    if rejected is not None
                    else node.lineage.rejection_reason_code
                ),
                rejection_reason_label=(
                    rejected.reason_label
                    if rejected is not None
                    else node.lineage.rejection_reason_label
                ),
                rejected_at_generation=(
                    rejected.rejected_at_generation if rejected is not None else None
                ),
                rejection_confidence=(
                    rejected.confidence if rejected is not None else None
                ),
            )
        )

    def _ensure_lineage_op(
        self, chain_id: str, node_id: str, operation: LineageOperation
    ) -> None:
        existing_op = EiLineageOperation.query.filter_by(
            operation_id=operation.operation_id
        ).first()
        if existing_op:
            return
        db.session.add(
            EiLineageOperation(
                operation_id=operation.operation_id,
                chain_id=chain_id,
                node_id=node_id,
                kind=operation.kind.value,
                generation_id=operation.generation_id,
                generation_index=operation.generation_index,
                reason_code=operation.reason_code,
                reason_label=operation.reason_label,
                related_node_ids_json=_dumps(list(operation.related_node_ids)),
                evidence_refs_json=_dumps(list(operation.evidence_refs)),
                confidence=operation.confidence,
                created_at=_parse_dt(operation.created_at_iso or datetime.now(UTC)),
            )
        )

    def get_snapshot(self, snapshot_id: str) -> CurriculumGenerationSnapshot | None:
        row = EiGenerationSnapshot.query.filter_by(snapshot_id=snapshot_id).first()
        if row is None:
            return None
        return self._hydrate_snapshot(row)

    def get_generation(self, generation_id: str) -> Generation | None:
        row = EiGeneration.query.filter_by(generation_id=generation_id).first()
        if row is None:
            return None
        return self._generation_from_row(row)

    def list_snapshots(self, chain_id: str) -> list[CurriculumGenerationSnapshot]:
        rows = (
            EiGenerationSnapshot.query.filter_by(chain_id=chain_id)
            .order_by(
                EiGenerationSnapshot.generation_index,
                EiGenerationSnapshot.created_at,
                EiGenerationSnapshot.snapshot_id,
            )
            .all()
        )
        return [self._hydrate_snapshot(row) for row in rows]

    def get_active_snapshot(self, chain_id: str) -> CurriculumGenerationSnapshot | None:
        chain = EiGenerationChain.query.filter_by(chain_id=chain_id).first()
        if chain is None or not chain.active_snapshot_id:
            return None
        return self.get_snapshot(chain.active_snapshot_id)

    def set_active_snapshot(self, chain_id: str, snapshot_id: str) -> None:
        snap = EiGenerationSnapshot.query.filter_by(snapshot_id=snapshot_id).first()
        if snap is None:
            raise SnapshotNotFoundError(f"Snapshot {snapshot_id!r} not found.")
        if snap.chain_id != chain_id:
            raise SnapshotNotFoundError(
                f"Snapshot {snapshot_id!r} does not belong to chain {chain_id!r}."
            )
        if snap.status != SnapshotStatus.ACCEPTED.value:
            raise SnapshotImmutableError(
                "Only accepted snapshots may become the active head."
            )
        chain = EiGenerationChain.query.filter_by(chain_id=chain_id).first()
        if chain is None:
            # Prefer workspace from the snapshot generation when available.
            snap_row = EiGenerationSnapshot.query.filter_by(
                snapshot_id=snapshot_id
            ).first()
            workspace_id = ""
            if snap_row is not None:
                gen = EiGeneration.query.filter_by(
                    generation_id=snap_row.generation_id
                ).first()
                if gen is not None:
                    workspace_id = gen.workspace_id or ""
            chain = EiGenerationChain(chain_id=chain_id, workspace_id=workspace_id)
            db.session.add(chain)
        chain.active_snapshot_id = snapshot_id
        db.session.flush()

    def ensure_chain(self, chain_id: str, workspace_id: str) -> str:
        chain = EiGenerationChain.query.filter_by(chain_id=chain_id).first()
        if chain is None:
            chain = EiGenerationChain(
                chain_id=chain_id, workspace_id=workspace_id or ""
            )
            db.session.add(chain)
        else:
            if workspace_id and chain.workspace_id != workspace_id:
                # Clear previous binding for this workspace if another chain held it.
                prior = (
                    EiGenerationChain.query.filter_by(workspace_id=workspace_id)
                    .filter(EiGenerationChain.chain_id != chain_id)
                    .all()
                )
                for other in prior:
                    other.workspace_id = ""
                chain.workspace_id = workspace_id
            elif workspace_id and not (chain.workspace_id or "").strip():
                chain.workspace_id = workspace_id
        db.session.flush()
        return chain_id

    def get_chain_id_for_workspace(self, workspace_id: str) -> str | None:
        if not (workspace_id or "").strip():
            return None
        chain = (
            EiGenerationChain.query.filter_by(workspace_id=workspace_id)
            .order_by(EiGenerationChain.updated_at.desc())
            .first()
        )
        return chain.chain_id if chain is not None else None

    def bind_workspace_chain(self, workspace_id: str, chain_id: str) -> None:
        self.ensure_chain(chain_id, workspace_id)

    def update_snapshot_status(
        self, snapshot_id: str, status: SnapshotStatus
    ) -> CurriculumGenerationSnapshot:
        row = EiGenerationSnapshot.query.filter_by(snapshot_id=snapshot_id).first()
        if row is None:
            raise SnapshotNotFoundError(f"Snapshot {snapshot_id!r} not found.")
        row.status = status.value
        db.session.flush()
        return self._hydrate_snapshot(row)

    def append_lineage_operation(
        self,
        *,
        chain_id: str,
        node_id: str,
        operation: LineageOperation,
    ) -> None:
        existing_op = EiLineageOperation.query.filter_by(
            operation_id=operation.operation_id
        ).first()
        if existing_op:
            raise LineageAppendError(
                f"Lineage operation {operation.operation_id!r} already recorded."
            )
        self._ensure_lineage_op(chain_id, node_id, operation)
        db.session.flush()

    def get_lineage_for_node(
        self, *, chain_id: str, node_id: str
    ) -> LineageRecord | None:
        rows = (
            EiLineageOperation.query.filter_by(chain_id=chain_id, node_id=node_id)
            .order_by(EiLineageOperation.id)
            .all()
        )
        if not rows:
            return None
        ops = tuple(
            LineageOperation(
                operation_id=r.operation_id,
                kind=LineageOperationKind(r.kind),
                generation_id=r.generation_id,
                generation_index=r.generation_index,
                reason_code=r.reason_code,
                reason_label=r.reason_label,
                related_node_ids=tuple(_loads(r.related_node_ids_json, [])),
                evidence_refs=tuple(_loads(r.evidence_refs_json, [])),
                confidence=r.confidence,
                created_at_iso=_iso(r.created_at),
            )
            for r in rows
        )
        first, last = ops[0], ops[-1]
        rejection = next(
            (op for op in reversed(ops) if op.kind is LineageOperationKind.REJECTED),
            None,
        )
        return LineageRecord(
            created_generation=first.generation_id,
            created_generation_index=first.generation_index,
            last_modified_generation=last.generation_id,
            last_modified_generation_index=last.generation_index,
            operations=ops,
            rejection_reason_code=rejection.reason_code if rejection else None,
            rejection_reason_label=rejection.reason_label if rejection else None,
        )

    def append_regression_report(self, report: RegressionReport) -> None:
        db.session.add(
            EiRegressionReport(
                report_id=report.report_id,
                chain_id=report.chain_id,
                candidate_generation_id=report.candidate_generation_id,
                candidate_snapshot_id=report.candidate_snapshot_id,
                baseline_generation_ids_json=_dumps(
                    list(report.baseline_generation_ids)
                ),
                accepted=report.accepted,
                reason=report.reason,
                candidate_metrics_json=_dumps(_quality_to_dict(report.candidate_metrics)),
                baseline_metrics_json=_dumps(_quality_to_dict(report.baseline_metrics)),
                gate_failures_json=_dumps(list(report.gate_failures)),
                created_at=_parse_dt(report.created_at_iso),
            )
        )
        db.session.flush()

    def list_regression_reports(self, chain_id: str) -> list[RegressionReport]:
        rows = (
            EiRegressionReport.query.filter_by(chain_id=chain_id)
            .order_by(EiRegressionReport.id)
            .all()
        )
        return [
            RegressionReport(
                report_id=r.report_id,
                chain_id=r.chain_id,
                candidate_generation_id=r.candidate_generation_id,
                candidate_snapshot_id=r.candidate_snapshot_id,
                baseline_generation_ids=tuple(
                    _loads(r.baseline_generation_ids_json, [])
                ),
                accepted=r.accepted,
                reason=r.reason,
                candidate_metrics=_quality_from_dict(
                    _loads(r.candidate_metrics_json, {})
                ),
                baseline_metrics=_quality_from_dict(
                    _loads(r.baseline_metrics_json, {})
                ),
                gate_failures=tuple(_loads(r.gate_failures_json, [])),
                created_at_iso=_iso(r.created_at),
            )
            for r in rows
        ]

    def append_certification(self, decision: CertificationDecision) -> None:
        db.session.add(
            EiCertificationRecord(
                decision_id=decision.decision_id,
                chain_id=decision.chain_id,
                snapshot_id=decision.snapshot_id,
                outcome=decision.outcome.value,
                quality_score=decision.quality_score,
                confidence=decision.confidence,
                coverage=decision.coverage,
                hierarchy_score=decision.hierarchy_score,
                granularity_score=decision.granularity_score,
                warnings_json=_dumps(list(decision.warnings)),
                hard_gate_failures_json=_dumps(list(decision.hard_gate_failures)),
                evidence_quality=decision.evidence_quality,
                reasoning_confidence=decision.reasoning_confidence,
                decision_quality=decision.decision_quality,
                failure_reasons_json=_dumps(
                    list(decision.failure_reasons or decision.hard_gate_failures)
                ),
                created_at=_parse_dt(decision.created_at_iso),
            )
        )
        db.session.flush()

    def get_certification(self, snapshot_id: str) -> CertificationDecision | None:
        row = EiCertificationRecord.query.filter_by(snapshot_id=snapshot_id).first()
        if row is None:
            return None
        return CertificationDecision(
            decision_id=row.decision_id,
            chain_id=row.chain_id,
            snapshot_id=row.snapshot_id,
            outcome=CertificationOutcome(row.outcome),
            quality_score=row.quality_score,
            confidence=row.confidence,
            coverage=row.coverage,
            hierarchy_score=row.hierarchy_score,
            granularity_score=row.granularity_score,
            warnings=tuple(_loads(row.warnings_json, [])),
            hard_gate_failures=tuple(_loads(row.hard_gate_failures_json, [])),
            created_at_iso=_iso(row.created_at),
            evidence_quality=float(getattr(row, "evidence_quality", 0.0) or 0.0),
            reasoning_confidence=float(
                getattr(row, "reasoning_confidence", 0.0) or 0.0
            ),
            decision_quality=float(getattr(row, "decision_quality", 0.0) or 0.0),
            failure_reasons=tuple(
                _loads(getattr(row, "failure_reasons_json", None), [])
            ),
        )

    def append_decision(self, entry: DecisionLedgerEntry) -> None:
        existing = EiDecisionLedgerEntry.query.filter_by(
            decision_id=entry.decision_id
        ).first()
        if existing is not None:
            raise LineageAppendError(
                f"Decision {entry.decision_id!r} already recorded on the ledger."
            )
        db.session.add(
            EiDecisionLedgerEntry(
                decision_id=entry.decision_id,
                chain_id=entry.chain_id,
                generation_index=entry.generation_index,
                generation_id=entry.generation_id,
                agent_id=entry.agent_id,
                policy_id=entry.policy_id,
                evidence_refs_json=_dumps(list(entry.evidence_refs)),
                evidence_grade=entry.evidence_grade.value,
                confidence=entry.confidence,
                reasoning_confidence=entry.reasoning_confidence,
                affected_node_ids_json=_dumps(list(entry.affected_node_ids)),
                decision_type=entry.decision_type.value,
                decision_outcome=entry.decision_outcome.value,
                reason=entry.reason[:1024],
                detail=entry.detail,
                snapshot_id=entry.snapshot_id,
                created_at=_parse_dt(entry.created_at_iso),
            )
        )
        db.session.flush()

    def list_decisions(self, chain_id: str) -> list[DecisionLedgerEntry]:
        rows = (
            EiDecisionLedgerEntry.query.filter_by(chain_id=chain_id)
            .order_by(EiDecisionLedgerEntry.id.asc())
            .all()
        )
        return [
            DecisionLedgerEntry(
                decision_id=r.decision_id,
                chain_id=r.chain_id,
                generation_index=r.generation_index,
                generation_id=r.generation_id,
                agent_id=r.agent_id,
                policy_id=r.policy_id,
                evidence_refs=tuple(_loads(r.evidence_refs_json, [])),
                evidence_grade=EvidenceGrade(r.evidence_grade),
                confidence=r.confidence,
                reasoning_confidence=r.reasoning_confidence,
                affected_node_ids=tuple(_loads(r.affected_node_ids_json, [])),
                decision_type=DecisionType(r.decision_type),
                created_at_iso=_iso(r.created_at),
                decision_outcome=DecisionOutcome(r.decision_outcome),
                reason=r.reason,
                detail=r.detail,
                snapshot_id=r.snapshot_id,
            )
            for r in rows
        ]

    def save_calibration_profile(self, profile: CalibrationProfile) -> None:
        row = EiCalibrationProfile.query.filter_by(
            profile_id=profile.profile_id
        ).first()
        if row is None:
            row = EiCalibrationProfile(profile_id=profile.profile_id)
            db.session.add(row)
        row.workspace_id = profile.workspace_id
        row.granularity = profile.granularity.value
        row.hierarchy = profile.hierarchy.value
        row.topic_density = profile.topic_density.value
        row.difficulty_bias = profile.difficulty_bias.value
        row.created_at = _parse_dt(profile.created_at_iso)
        db.session.flush()

    def get_calibration_profile(self, profile_id: str) -> CalibrationProfile | None:
        row = EiCalibrationProfile.query.filter_by(profile_id=profile_id).first()
        if row is None:
            return None
        return CalibrationProfile(
            profile_id=row.profile_id,
            workspace_id=row.workspace_id,
            granularity=GranularityStyle(row.granularity),
            hierarchy=HierarchyStyle(row.hierarchy),
            topic_density=TopicDensityStyle(row.topic_density),
            difficulty_bias=DifficultyBiasStyle(row.difficulty_bias),
            created_at_iso=_iso(row.created_at),
        )

    def _generation_from_row(self, row: EiGeneration) -> Generation:
        return Generation(
            generation_id=row.generation_id,
            chain_id=row.chain_id,
            generation_index=row.generation_index,
            purpose=row.purpose,
            parent_generation_ids=tuple(_loads(row.parent_generation_ids_json, [])),
            source_document_ids=tuple(_loads(row.source_document_ids_json, [])),
            workspace_id=row.workspace_id,
            created_at_iso=_iso(row.created_at),
            calibration_profile_id=row.calibration_profile_id,
        )

    def _hydrate_snapshot(
        self, row: EiGenerationSnapshot
    ) -> CurriculumGenerationSnapshot:
        generation = self.get_generation(row.generation_id)
        if generation is None:
            raise SnapshotNotFoundError(
                f"Generation {row.generation_id!r} missing "
                f"for snapshot {row.snapshot_id}."
            )
        node_rows = EiEducationalNode.query.filter_by(snapshot_id=row.snapshot_id).all()
        nodes: list[EducationalNode] = []
        rejected: list[RejectedNode] = []
        for n in node_rows:
            provenance = (
                _provenance_from_dict(_loads(n.provenance_json, {}))
                if n.provenance_json
                else None
            )
            attrs_raw = _loads(n.attributes_json, {})
            grade_raw = attrs_raw.pop("_evidence_grade", None)
            policy_raw = attrs_raw.pop("_policy_id", None)
            attributes = tuple((str(k), str(v)) for k, v in attrs_raw.items())
            evidence_grade = None
            if grade_raw:
                try:
                    evidence_grade = EvidenceGrade(str(grade_raw))
                except ValueError:
                    evidence_grade = None
            node = EducationalNode(
                node_id=n.node_id,
                generation_local_id=n.generation_local_id,
                title=n.title,
                kind=n.kind,
                role=n.role,
                parent_node_id=n.parent_node_id,
                confidence=_confidence_from_dict(_loads(n.confidence_json, {})),
                lineage=_lineage_from_dict(_loads(n.lineage_json, {})),
                active=n.active,
                provenance_id=n.provenance_id,
                provenance=provenance,
                body=n.body,
                attributes=attributes,
                evidence_grade=evidence_grade,
                policy_id=str(policy_raw) if policy_raw else None,
            )
            nodes.append(node)
            if n.is_rejected_record and not n.active:
                rejected.append(
                    RejectedNode(
                        node=node,
                        rejected_at_generation=n.rejected_at_generation or "",
                        reason_code=n.rejection_reason_code or "",
                        reason_label=n.rejection_reason_label or "",
                        confidence=float(n.rejection_confidence or 0.0),
                    )
                )
        return CurriculumGenerationSnapshot(
            snapshot_id=row.snapshot_id,
            generation=generation,
            nodes=tuple(nodes),
            rejected_nodes=tuple(rejected),
            metrics=_quality_from_dict(_loads(row.metrics_json, {})),
            provenance_bundle_id=row.provenance_bundle_id,
            created_at_iso=_iso(row.created_at),
            status=SnapshotStatus(row.status),
            generation_hash=getattr(row, "generation_hash", "") or "",
            agent_id=getattr(row, "agent_id", "") or "",
            agent_version=getattr(row, "agent_version", "") or "",
        )
