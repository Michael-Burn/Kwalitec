"""ORM models for Version 2 durable aggregate / snapshot / evidence storage.

Stores opaque JSON documents only. Never interprets educational meaning.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class V2AggregateDocument(db.Model):
    """Versioned opaque aggregate document row."""

    __tablename__ = "v2_aggregate_documents"
    __table_args__ = (
        db.UniqueConstraint(
            "aggregate_name",
            "aggregate_id",
            name="uq_v2_aggregate_documents_name_id",
        ),
        db.Index(
            "ix_v2_aggregate_documents_name_id",
            "aggregate_name",
            "aggregate_id",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    aggregate_name: str = db.Column(db.String(128), nullable=False)
    aggregate_id: str = db.Column(db.String(256), nullable=False)
    version: int = db.Column(db.Integer, nullable=False, default=0)
    payload: str = db.Column(db.Text, nullable=False)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )


class V2AggregateSnapshot(db.Model):
    """Append-only opaque aggregate snapshot row."""

    __tablename__ = "v2_aggregate_snapshots"
    __table_args__ = (
        db.Index(
            "ix_v2_aggregate_snapshots_name_id_seq",
            "aggregate_name",
            "aggregate_id",
            "sequence",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    snapshot_id: str = db.Column(db.String(64), unique=True, nullable=False, index=True)
    aggregate_name: str = db.Column(db.String(128), nullable=False)
    aggregate_id: str = db.Column(db.String(256), nullable=False)
    sequence: int = db.Column(db.Integer, nullable=False)
    schema_version: int = db.Column(db.Integer, nullable=False, default=1)
    payload: str = db.Column(db.Text, nullable=False)
    correlation_id: str = db.Column(db.String(128), nullable=False, default="")
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )


class V2EvidenceEvent(db.Model):
    """Append-only opaque evidence event row."""

    __tablename__ = "v2_evidence_events"
    __table_args__ = (
        db.Index(
            "ix_v2_evidence_events_learner_subject",
            "learner_id",
            "subject_id",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    record_id: str = db.Column(db.String(64), unique=True, nullable=False, index=True)
    learner_id: str = db.Column(db.String(128), nullable=False, index=True)
    subject_id: str = db.Column(db.String(128), nullable=False)
    evidence_type: str = db.Column(db.String(128), nullable=False)
    payload: str = db.Column(db.Text, nullable=False, default="{}")
    correlation_id: str = db.Column(db.String(128), nullable=False, default="")
    causation_id: str = db.Column(db.String(128), nullable=False, default="")
    recorded_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
