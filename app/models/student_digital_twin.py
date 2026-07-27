"""ORM models for Student Digital Twin Foundation (SDT-001).

Observations and reasoning history are append-only. Inferences (mastery, gaps,
recommendations, predictions, learning-state snapshots) are replaced per
reasoning cycle while prior snapshots remain in history tables.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class SdtStudentDigitalTwin(db.Model):
    """Durable Twin root row."""

    __tablename__ = "student_digital_twins"
    __table_args__ = (
        db.Index("ix_sdt_twins_student", "student_id"),
        db.UniqueConstraint(
            "student_id", "workspace_id", "subject_code", name="uq_sdt_twin_scope"
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    twin_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    student_id: str = db.Column(db.String(128), nullable=False)
    display_name: str = db.Column(db.String(255), nullable=False, default="")
    subject_code: str = db.Column(db.String(64), nullable=False, default="")
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    external_user_id: str | None = db.Column(db.String(128), nullable=True)
    version: int = db.Column(db.Integer, nullable=False, default=1)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return f"<SdtStudentDigitalTwin {self.twin_id}>"


class SdtObservation(db.Model):
    """Append-only educational fact. Never update or delete."""

    __tablename__ = "student_observations"
    __table_args__ = (
        db.Index("ix_sdt_obs_twin_recorded", "twin_id", "recorded_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    observation_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
        index=True,
    )
    student_id: str = db.Column(db.String(128), nullable=False, index=True)
    kind: str = db.Column(db.String(64), nullable=False)
    recorded_at: datetime = db.Column(db.DateTime, nullable=False)
    curriculum_entity_id: str = db.Column(db.String(64), nullable=False, default="")
    curriculum_entity_kind: str = db.Column(db.String(64), nullable=False, default="")
    evidence_reference: str = db.Column(db.String(255), nullable=False, default="")
    provenance: str = db.Column(db.String(255), nullable=False, default="")
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    def __repr__(self) -> str:
        return f"<SdtObservation {self.observation_id} kind={self.kind}>"


class SdtMasteryRecord(db.Model):
    """Current mastery inference per concept (replaced on reasoning)."""

    __tablename__ = "mastery_records"
    __table_args__ = (
        db.UniqueConstraint("twin_id", "concept_id", name="uq_sdt_mastery_concept"),
        db.Index("ix_sdt_mastery_twin", "twin_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    mastery_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    concept_id: str = db.Column(db.String(64), nullable=False)
    concept_title: str = db.Column(db.String(512), nullable=False, default="")
    mastery_score: float = db.Column(db.Float, nullable=False, default=0.0)
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    trend: str = db.Column(db.String(32), nullable=False, default="unknown")
    evidence_count: int = db.Column(db.Integer, nullable=False, default=0)
    supporting_evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    reason: str = db.Column(db.String(512), nullable=False, default="")
    last_updated: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class SdtKnowledgeGap(db.Model):
    """Current knowledge gaps (replaced on reasoning)."""

    __tablename__ = "knowledge_gaps"
    __table_args__ = (db.Index("ix_sdt_gaps_twin", "twin_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    gap_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    concept_id: str = db.Column(db.String(64), nullable=False)
    concept_title: str = db.Column(db.String(512), nullable=False, default="")
    severity: str = db.Column(db.String(32), nullable=False, default="medium")
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    likely_prerequisite_id: str = db.Column(db.String(64), nullable=False, default="")
    likely_prerequisite_title: str = db.Column(
        db.String(512), nullable=False, default=""
    )
    supporting_evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    retrieval_log_id: str | None = db.Column(db.String(64), nullable=True)
    estimated_recovery_effort: float = db.Column(db.Float, nullable=False, default=0.0)
    reason: str = db.Column(db.String(512), nullable=False, default="")
    identified_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    is_active: bool = db.Column(db.Boolean, nullable=False, default=True)


class SdtLearningStateSnapshot(db.Model):
    """Append-only learning-state snapshots."""

    __tablename__ = "learning_state_snapshots"
    __table_args__ = (
        db.Index("ix_sdt_state_twin_computed", "twin_id", "computed_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    snapshot_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    knowledge: float = db.Column(db.Float, nullable=False, default=0.0)
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    retention: float = db.Column(db.Float, nullable=False, default=0.0)
    consistency: float = db.Column(db.Float, nullable=False, default=0.0)
    momentum: float = db.Column(db.Float, nullable=False, default=0.0)
    exam_readiness: float = db.Column(db.Float, nullable=False, default=0.0)
    evidence_count: int = db.Column(db.Integer, nullable=False, default=0)
    reason: str = db.Column(db.String(512), nullable=False, default="")
    computed_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class SdtRecommendation(db.Model):
    """Current recommendations (replaced on reasoning)."""

    __tablename__ = "recommendations"
    __table_args__ = (db.Index("ix_sdt_rec_twin", "twin_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    recommendation_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    title: str = db.Column(db.String(512), nullable=False)
    reason: str = db.Column(db.Text, nullable=False, default="")
    priority: str = db.Column(db.String(32), nullable=False, default="medium")
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    curriculum_entity_id: str = db.Column(db.String(64), nullable=False, default="")
    supporting_evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    related_gap_id: str | None = db.Column(db.String(64), nullable=True)
    status: str = db.Column(db.String(32), nullable=False, default="active")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    is_active: bool = db.Column(db.Boolean, nullable=False, default=True)


class SdtPrediction(db.Model):
    """Prediction scaffolds (framework; replaced on reasoning)."""

    __tablename__ = "predictions"
    __table_args__ = (db.Index("ix_sdt_pred_twin", "twin_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    prediction_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    kind: str = db.Column(db.String(64), nullable=False)
    value: float = db.Column(db.Float, nullable=False, default=0.0)
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    horizon_days: int = db.Column(db.Integer, nullable=False, default=0)
    supporting_evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    reason: str = db.Column(db.String(512), nullable=False, default="")
    algorithm_version: str = db.Column(
        db.String(64), nullable=False, default="sdt001.scaffold_v1"
    )
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    is_active: bool = db.Column(db.Boolean, nullable=False, default=True)


class SdtReasoningHistory(db.Model):
    """Append-only reasoning audit trail."""

    __tablename__ = "reasoning_history"
    __table_args__ = (
        db.Index("ix_sdt_reason_twin_created", "twin_id", "created_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    reasoning_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    triggered_by: str = db.Column(db.String(128), nullable=False, default="")
    observation_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    steps_json: str = db.Column(db.Text, nullable=False, default="[]")
    summary: str = db.Column(db.Text, nullable=False, default="")
    reasoning_version: str = db.Column(db.String(64), nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
