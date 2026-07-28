"""ORM model for Educational Reasoning Engine decisions (EI-007).

Derived educational decisions keyed to Student Curriculum Instance.
Beliefs, evidence, and curriculum are never mutated; decisions may be
deleted and rebuilt deterministically.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class EreEducationalDecision(db.Model):
    """Persisted explainable educational decision for one SCI target.

    Explainability payloads live in ``explanation_json``. Supporting belief
    and evidence ids are references only — payloads stay in EI-006 / EI-005.
    """

    __tablename__ = "ere_educational_decisions"
    __table_args__ = (
        db.UniqueConstraint(
            "instance_id",
            "decision_type",
            "curriculum_target",
            name="uq_ere_decisions_instance_type_target",
        ),
        db.Index(
            "ix_ere_decisions_instance_rank",
            "instance_id",
            "rank_position",
        ),
        db.Index("ix_ere_decisions_version", "reasoning_version"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    decision_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    instance_id: str = db.Column(
        db.String(64),
        db.ForeignKey("sci_student_curriculum_instances.instance_id"),
        nullable=False,
        index=True,
    )
    decision_type: str = db.Column(db.String(64), nullable=False, index=True)
    curriculum_target: str = db.Column(db.String(256), nullable=False, index=True)
    priority: float = db.Column(db.Float, nullable=False, default=0.0)
    rank_position: int = db.Column(db.Integer, nullable=False, default=1)
    rationale_summary: str = db.Column(db.Text, nullable=False, default="")
    prerequisite_chain_json: str = db.Column(db.Text, nullable=False, default="[]")
    estimated_effort_minutes: int = db.Column(db.Integer, nullable=False, default=30)
    expected_educational_outcome: str = db.Column(
        db.String(64), nullable=False, default="advance_mastery"
    )
    supporting_beliefs_json: str = db.Column(db.Text, nullable=False, default="[]")
    supporting_curriculum_json: str = db.Column(db.Text, nullable=False, default="[]")
    supporting_evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    applied_rules_json: str = db.Column(db.Text, nullable=False, default="[]")
    explanation_json: str = db.Column(db.Text, nullable=False, default="{}")
    reasoned_at: datetime = db.Column(db.DateTime, nullable=False)
    reasoning_version: str = db.Column(
        db.String(32), nullable=False, default="ere.v1"
    )
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return (
            f"<EreEducationalDecision {self.decision_id} "
            f"type={self.decision_type} target={self.curriculum_target}>"
        )
