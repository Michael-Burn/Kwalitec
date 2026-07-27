"""ORM models for Educational Reasoning Engine metadata (SDT-002).

Persists reasoning metadata only — does not duplicate Student Digital Twin
inference rows (mastery, gaps, recommendations live in SDT-001 tables).
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class EducationalReasoningRun(db.Model):
    """Immutable record of one Educational Reasoning Engine cycle."""

    __tablename__ = "educational_reasoning_runs"
    __table_args__ = (
        db.Index("ix_err_runs_twin_created", "twin_id", "created_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    run_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    twin_id: str = db.Column(db.String(64), nullable=False, index=True)
    triggered_by: str = db.Column(db.String(128), nullable=False, default="")
    observation_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    curriculum_evidence_ids_json: str = db.Column(
        db.Text, nullable=False, default="[]"
    )
    retrieval_log_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    summary: str = db.Column(db.Text, nullable=False, default="")
    engine_version: str = db.Column(db.String(64), nullable=False, default="")
    rule_count: int = db.Column(db.Integer, nullable=False, default=0)
    decision_count: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    def __repr__(self) -> str:
        return f"<EducationalReasoningRun {self.run_id}>"


class EducationalRuleExecution(db.Model):
    """Immutable record of one rule execution within a reasoning run."""

    __tablename__ = "educational_rule_executions"
    __table_args__ = (
        db.Index("ix_err_exec_run", "run_id"),
        db.Index("ix_err_exec_rule", "rule_code"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    execution_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    run_id: str = db.Column(
        db.String(64),
        db.ForeignKey("educational_reasoning_runs.run_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False, index=True)
    rule_code: str = db.Column(db.String(64), nullable=False)
    rule_name: str = db.Column(db.String(128), nullable=False, default="")
    sequence: int = db.Column(db.Integer, nullable=False, default=0)
    inputs_json: str = db.Column(db.Text, nullable=False, default="{}")
    outputs_json: str = db.Column(db.Text, nullable=False, default="{}")
    explanation_summary: str = db.Column(db.Text, nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class ReasoningExplanation(db.Model):
    """Immutable explainability payload linked to a run / rule / decision."""

    __tablename__ = "reasoning_explanations"
    __table_args__ = (
        db.Index("ix_err_expl_run", "run_id"),
        db.Index("ix_err_expl_rule", "rule_code"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    explanation_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    run_id: str = db.Column(
        db.String(64),
        db.ForeignKey("educational_reasoning_runs.run_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False, index=True)
    rule_code: str = db.Column(db.String(64), nullable=False, default="")
    decision_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    summary: str = db.Column(db.Text, nullable=False, default="")
    detail: str = db.Column(db.Text, nullable=False, default="")
    observation_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    curriculum_evidence_ids_json: str = db.Column(
        db.Text, nullable=False, default="[]"
    )
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class DecisionRecord(db.Model):
    """Immutable educational decision metadata (not Twin inference rows)."""

    __tablename__ = "decision_records"
    __table_args__ = (
        db.Index("ix_err_dec_run", "run_id"),
        db.Index("ix_err_dec_twin", "twin_id"),
        db.Index("ix_err_dec_kind", "kind"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    decision_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    run_id: str = db.Column(
        db.String(64),
        db.ForeignKey("educational_reasoning_runs.run_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    kind: str = db.Column(db.String(64), nullable=False)
    rule_code: str = db.Column(db.String(64), nullable=False, default="")
    subject_ref: str = db.Column(db.String(128), nullable=False, default="")
    value: float = db.Column(db.Float, nullable=False, default=0.0)
    explanation_summary: str = db.Column(db.Text, nullable=False, default="")
    observation_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    curriculum_evidence_ids_json: str = db.Column(
        db.Text, nullable=False, default="[]"
    )
    payload_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
