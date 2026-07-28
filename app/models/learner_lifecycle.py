"""ORM model for Learner Lifecycle operation checkpoints (LP-001).

Tracks orchestration progress so failed runs can resume without leaving
students in an unrecoverable educational state. Does not store educational
beliefs, decisions, or experience models.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class LlpLifecycleOperation(db.Model):
    """Persisted checkpoint for one learner lifecycle orchestration run."""

    __tablename__ = "llp_lifecycle_operations"
    __table_args__ = (
        db.Index("ix_llp_ops_instance_status", "instance_id", "status"),
        db.Index("ix_llp_ops_student", "student_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    operation_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    operation_type: str = db.Column(db.String(32), nullable=False, index=True)
    status: str = db.Column(db.String(32), nullable=False, index=True)
    student_id: int | None = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True, index=True
    )
    instance_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    correlation_id: str | None = db.Column(db.String(64), nullable=True)
    completed_stages_json: str = db.Column(db.Text, nullable=False, default="[]")
    failed_stage: str | None = db.Column(db.String(64), nullable=True)
    failure_cause: str | None = db.Column(db.Text, nullable=True)
    attempt_count: int = db.Column(db.Integer, nullable=False, default=1)
    orchestrator_version: str = db.Column(db.String(32), nullable=False)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return (
            f"<LlpLifecycleOperation {self.operation_id} "
            f"type={self.operation_type} status={self.status}>"
        )
