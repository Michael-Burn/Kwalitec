"""ORM models for the canonical curriculum identity layer.

Maps the three existing topic identity schemes (published-content,
Stage A database, study-event) onto opaque canonical UUIDs. Identity
resolution only: no mastery, readiness, coverage, or scheduling.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class CanonicalCurriculumTopic(db.Model):
    """Opaque canonical curriculum topic identity for one curriculum version."""

    __tablename__ = "canonical_curriculum_topic"
    __table_args__ = (
        db.Index(
            "ix_canonical_curriculum_topic_version",
            "curriculum_version",
        ),
    )

    canonical_id: str = db.Column(db.String(36), primary_key=True)
    curriculum_version: str = db.Column(db.String(128), nullable=False)
    title: str = db.Column(db.String(512), nullable=False)
    status: str = db.Column(db.String(32), nullable=False, default="active")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return (
            f"<CanonicalCurriculumTopic {self.canonical_id} "
            f"{self.curriculum_version} status={self.status}>"
        )


class CurriculumTopicIdentityMap(db.Model):
    """Alias from one existing identity scheme to a canonical topic id."""

    __tablename__ = "curriculum_topic_identity_map"
    __table_args__ = (
        db.UniqueConstraint(
            "source_system",
            "source_id",
            "source_version",
            name="uq_curriculum_topic_identity_map_source",
        ),
        db.Index(
            "ix_curriculum_topic_identity_map_canonical",
            "canonical_id",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    canonical_id: str | None = db.Column(
        db.String(36),
        db.ForeignKey("canonical_curriculum_topic.canonical_id"),
        nullable=True,
    )
    source_system: str = db.Column(db.String(64), nullable=False)
    source_id: str = db.Column(db.String(128), nullable=False)
    source_version: str = db.Column(db.String(128), nullable=False)
    mapping_status: str = db.Column(db.String(64), nullable=False)
    mapping_notes: str | None = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return (
            f"<CurriculumTopicIdentityMap {self.source_system}:{self.source_id} "
            f"-> {self.canonical_id} status={self.mapping_status}>"
        )
