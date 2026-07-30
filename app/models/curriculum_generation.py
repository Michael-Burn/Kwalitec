"""ORM models for EI-001 Curriculum Intelligence Engine generation store.

Append-only snapshots + lineage. Snapshot content is never updated after insert;
only lifecycle ``status`` may change.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class EiGenerationChain(db.Model):
    """Active pointer for one engine chain / Curriculum Memory scope."""

    __tablename__ = "ei_generation_chains"

    id: int = db.Column(db.Integer, primary_key=True)
    chain_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    workspace_id: str = db.Column(
        db.String(128), nullable=False, default="", index=True
    )
    active_snapshot_id: str | None = db.Column(db.String(64), nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )


class EiGeneration(db.Model):
    """Generation metadata row (one educational purpose)."""

    __tablename__ = "ei_generations"
    __table_args__ = (
        db.Index("ix_ei_gen_chain_index", "chain_id", "generation_index"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    generation_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    chain_id: str = db.Column(db.String(64), nullable=False, index=True)
    generation_index: int = db.Column(db.Integer, nullable=False)
    purpose: str = db.Column(db.String(128), nullable=False, default="")
    parent_generation_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    source_document_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    calibration_profile_id: str | None = db.Column(db.String(64), nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class EiGenerationSnapshot(db.Model):
    """Immutable generation snapshot. Content columns are write-once."""

    __tablename__ = "ei_generation_snapshots"
    __table_args__ = (
        db.Index("ix_ei_snap_chain_status", "chain_id", "status"),
        db.Index("ix_ei_snap_generation", "generation_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    snapshot_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    generation_id: str = db.Column(
        db.String(64),
        db.ForeignKey("ei_generations.generation_id"),
        nullable=False,
    )
    chain_id: str = db.Column(db.String(64), nullable=False, index=True)
    generation_index: int = db.Column(db.Integer, nullable=False)
    provenance_bundle_id: str = db.Column(db.String(64), nullable=False, default="")
    status: str = db.Column(db.String(64), nullable=False, default="accepted")
    metrics_json: str = db.Column(db.Text, nullable=False, default="{}")
    generation_hash: str = db.Column(db.String(64), nullable=False, default="")
    agent_id: str = db.Column(db.String(128), nullable=False, default="")
    agent_version: str = db.Column(db.String(64), nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class EiEducationalNode(db.Model):
    """Educational node frozen into a snapshot (rejected nodes stay inactive)."""

    __tablename__ = "ei_educational_nodes"
    __table_args__ = (
        db.Index("ix_ei_node_snap", "snapshot_id"),
        db.Index("ix_ei_node_stable", "chain_id", "node_id"),
        db.UniqueConstraint(
            "snapshot_id",
            "node_id",
            name="uq_ei_node_snapshot_node",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    snapshot_id: str = db.Column(
        db.String(64),
        db.ForeignKey("ei_generation_snapshots.snapshot_id"),
        nullable=False,
    )
    chain_id: str = db.Column(db.String(64), nullable=False)
    node_id: str = db.Column(db.String(64), nullable=False)
    generation_local_id: str = db.Column(db.String(64), nullable=False, default="")
    title: str = db.Column(db.String(512), nullable=False, default="")
    kind: str = db.Column(db.String(64), nullable=False, default="")
    role: str | None = db.Column(db.String(64), nullable=True)
    parent_node_id: str | None = db.Column(db.String(64), nullable=True)
    active: bool = db.Column(db.Boolean, nullable=False, default=True)
    body: str = db.Column(db.Text, nullable=False, default="")
    provenance_id: str | None = db.Column(db.String(64), nullable=True)
    confidence_json: str = db.Column(db.Text, nullable=False, default="{}")
    lineage_json: str = db.Column(db.Text, nullable=False, default="{}")
    provenance_json: str | None = db.Column(db.Text, nullable=True)
    attributes_json: str = db.Column(db.Text, nullable=False, default="{}")
    is_rejected_record: bool = db.Column(db.Boolean, nullable=False, default=False)
    rejection_reason_code: str | None = db.Column(db.String(128), nullable=True)
    rejection_reason_label: str | None = db.Column(db.String(512), nullable=True)
    rejected_at_generation: str | None = db.Column(db.String(64), nullable=True)
    rejection_confidence: float | None = db.Column(db.Float, nullable=True)


class EiLineageOperation(db.Model):
    """Append-only Curriculum Memory lineage operations."""

    __tablename__ = "ei_lineage_operations"
    __table_args__ = (
        db.Index("ix_ei_lineage_node", "chain_id", "node_id"),
        db.UniqueConstraint("operation_id", name="uq_ei_lineage_operation_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    operation_id: str = db.Column(db.String(64), nullable=False)
    chain_id: str = db.Column(db.String(64), nullable=False)
    node_id: str = db.Column(db.String(64), nullable=False)
    kind: str = db.Column(db.String(32), nullable=False)
    generation_id: str = db.Column(db.String(64), nullable=False)
    generation_index: int = db.Column(db.Integer, nullable=False)
    reason_code: str = db.Column(db.String(128), nullable=False, default="")
    reason_label: str = db.Column(db.String(512), nullable=False, default="")
    related_node_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    evidence_refs_json: str = db.Column(db.Text, nullable=False, default="[]")
    confidence: float | None = db.Column(db.Float, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class EiRegressionReport(db.Model):
    """Persisted regression accept/reject report."""

    __tablename__ = "ei_regression_reports"
    __table_args__ = (db.Index("ix_ei_reg_chain", "chain_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    report_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    chain_id: str = db.Column(db.String(64), nullable=False)
    candidate_generation_id: str = db.Column(db.String(64), nullable=False)
    candidate_snapshot_id: str = db.Column(db.String(64), nullable=False)
    baseline_generation_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    accepted: bool = db.Column(db.Boolean, nullable=False, default=False)
    reason: str = db.Column(db.String(512), nullable=False, default="")
    candidate_metrics_json: str = db.Column(db.Text, nullable=False, default="{}")
    baseline_metrics_json: str = db.Column(db.Text, nullable=False, default="{}")
    gate_failures_json: str = db.Column(db.Text, nullable=False, default="[]")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class EiCertificationRecord(db.Model):
    """Persisted Gen 7 certification decision."""

    __tablename__ = "ei_certification_records"
    __table_args__ = (db.Index("ix_ei_cert_chain", "chain_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    decision_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    chain_id: str = db.Column(db.String(64), nullable=False)
    snapshot_id: str = db.Column(db.String(64), nullable=False, unique=True)
    outcome: str = db.Column(db.String(64), nullable=False)
    quality_score: float = db.Column(db.Float, nullable=False, default=0.0)
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    coverage: float = db.Column(db.Float, nullable=False, default=0.0)
    hierarchy_score: float = db.Column(db.Float, nullable=False, default=0.0)
    granularity_score: float = db.Column(db.Float, nullable=False, default=0.0)
    warnings_json: str = db.Column(db.Text, nullable=False, default="[]")
    hard_gate_failures_json: str = db.Column(db.Text, nullable=False, default="[]")
    evidence_quality: float = db.Column(db.Float, nullable=False, default=0.0)
    reasoning_confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    decision_quality: float = db.Column(db.Float, nullable=False, default=0.0)
    failure_reasons_json: str = db.Column(db.Text, nullable=False, default="[]")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class EiDecisionLedgerEntry(db.Model):
    """Append-only Educational Decision Ledger (EI-001D)."""

    __tablename__ = "ei_decision_ledger"
    __table_args__ = (
        db.Index("ix_ei_decision_chain", "chain_id"),
        db.UniqueConstraint("decision_id", name="uq_ei_decision_ledger_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    decision_id: str = db.Column(db.String(64), nullable=False)
    chain_id: str = db.Column(db.String(64), nullable=False)
    generation_index: int = db.Column(db.Integer, nullable=False)
    generation_id: str = db.Column(db.String(64), nullable=False, default="")
    agent_id: str = db.Column(db.String(128), nullable=False, default="")
    policy_id: str = db.Column(db.String(128), nullable=False, default="")
    evidence_refs_json: str = db.Column(db.Text, nullable=False, default="[]")
    evidence_grade: str = db.Column(db.String(8), nullable=False, default="D")
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    reasoning_confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    affected_node_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    decision_type: str = db.Column(db.String(64), nullable=False, default="other")
    decision_outcome: str = db.Column(db.String(32), nullable=False, default="accepted")
    reason: str = db.Column(db.String(1024), nullable=False, default="")
    detail: str = db.Column(db.Text, nullable=False, default="")
    snapshot_id: str = db.Column(db.String(64), nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class EiCalibrationProfile(db.Model):
    """Founder calibration profile (style settings)."""

    __tablename__ = "ei_calibration_profiles"
    __table_args__ = (db.Index("ix_ei_cal_workspace", "workspace_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    profile_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    granularity: str = db.Column(db.String(64), nullable=False, default="balanced")
    hierarchy: str = db.Column(db.String(64), nullable=False, default="balanced")
    topic_density: str = db.Column(db.String(64), nullable=False, default="balanced")
    difficulty_bias: str = db.Column(db.String(64), nullable=False, default="balanced")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
