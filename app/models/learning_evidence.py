"""ORM model for Learning Evidence Engine (EI-005).

Append-only educational observation store keyed to Student Curriculum Instance
and curriculum node. Never mutates CKG content, mastery, confidence, missions,
or recommendations.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class LeeEvidenceEvent(db.Model):
    """Immutable educational evidence event (append-only).

    References SCI by ``instance_id`` and curriculum by ``node_stable_id``.
    Corrections are additional rows linked via ``corrects_evidence_id``.
    """

    __tablename__ = "lee_evidence_events"
    __table_args__ = (
        db.Index(
            "ix_lee_evidence_instance_occurred",
            "instance_id",
            "occurred_at",
        ),
        db.Index(
            "ix_lee_evidence_instance_node_occurred",
            "instance_id",
            "node_stable_id",
            "occurred_at",
        ),
        db.Index(
            "ix_lee_evidence_instance_type",
            "instance_id",
            "evidence_type",
        ),
        db.Index("ix_lee_evidence_student", "student_id", "occurred_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    evidence_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    instance_id: str = db.Column(
        db.String(64),
        db.ForeignKey("sci_student_curriculum_instances.instance_id"),
        nullable=False,
        index=True,
    )
    student_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    node_stable_id: str = db.Column(db.String(256), nullable=False, index=True)
    evidence_type: str = db.Column(db.String(64), nullable=False, index=True)
    occurred_at: datetime = db.Column(db.DateTime, nullable=False, index=True)
    recorded_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    source: str = db.Column(db.String(64), nullable=False)
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")
    corrects_evidence_id: str | None = db.Column(
        db.String(64),
        db.ForeignKey("lee_evidence_events.evidence_id"),
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"<LeeEvidenceEvent {self.evidence_id} "
            f"type={self.evidence_type} node={self.node_stable_id}>"
        )
