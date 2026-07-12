"""ORM model for durable immutable Digital Twin snapshots.

Stores whole Twin aggregates as JSON payloads with snapshot identity,
scope keys, authorship, and provenance. Never interprets educational meaning.
Never mutates prior rows — successors are new rows (Capability 3.7.1–3.8.2).
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class TwinSnapshot(db.Model):
    """One immutable Twin snapshot row (birth or successor).

    Current designation is the maximum ``sequence`` for a given scope — prior
    rows are never updated when a successor is persisted.
    """

    __tablename__ = "twin_snapshots"
    __table_args__ = (
        db.Index(
            "ix_twin_snapshots_scope_sequence",
            "student_id",
            "sitting_id",
            "curriculum_id",
            "sequence",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    snapshot_id: str = db.Column(db.String(64), unique=True, nullable=False, index=True)

    student_id: str = db.Column(db.String(128), nullable=False, index=True)
    sitting_id: str | None = db.Column(db.String(128), nullable=True)
    curriculum_id: str | None = db.Column(db.String(128), nullable=True)

    sequence: int = db.Column(db.Integer, nullable=False)
    format_version: str = db.Column(db.String(32), nullable=False)
    authorship: str = db.Column(db.String(32), nullable=False)

    twin_payload: str = db.Column(db.Text, nullable=False)
    provenance_payload: str | None = db.Column(db.Text, nullable=True)

    persisted_at: datetime = db.Column(db.DateTime, nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return (
            f"<TwinSnapshot {self.snapshot_id} "
            f"student={self.student_id} seq={self.sequence}>"
        )
