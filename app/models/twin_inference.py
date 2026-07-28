"""ORM model for Twin Inference Engine beliefs (EI-006).

Derived educational beliefs keyed to Student Curriculum Instance nodes.
Evidence rows are never mutated; beliefs may be deleted and rebuilt.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class TieNodeBelief(db.Model):
    """Persisted explainable Twin belief for one curriculum node.

    ``supporting_evidence_json`` and ``explanation_json`` store references and
    explainability payloads — not duplicated evidence observation bodies.
    """

    __tablename__ = "tie_node_beliefs"
    __table_args__ = (
        db.UniqueConstraint(
            "instance_id",
            "node_stable_id",
            name="uq_tie_node_beliefs_instance_node",
        ),
        db.Index(
            "ix_tie_beliefs_instance_state",
            "instance_id",
            "learning_state",
        ),
        db.Index("ix_tie_beliefs_version", "inference_version"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    belief_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    instance_id: str = db.Column(
        db.String(64),
        db.ForeignKey("sci_student_curriculum_instances.instance_id"),
        nullable=False,
        index=True,
    )
    node_stable_id: str = db.Column(db.String(256), nullable=False, index=True)
    mastery_level: float = db.Column(db.Float, nullable=False, default=0.0)
    confidence_score: float = db.Column(db.Float, nullable=False, default=0.0)
    learning_state: str = db.Column(db.String(32), nullable=False, default="unknown")
    supporting_evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    rationale_summary: str = db.Column(db.Text, nullable=False, default="")
    explanation_json: str = db.Column(db.Text, nullable=False, default="{}")
    inference_timestamp: datetime = db.Column(db.DateTime, nullable=False)
    inference_version: str = db.Column(db.String(32), nullable=False, default="tie.v1")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return (
            f"<TieNodeBelief {self.belief_id} "
            f"node={self.node_stable_id} state={self.learning_state}>"
        )
