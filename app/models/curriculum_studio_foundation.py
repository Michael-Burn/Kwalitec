"""ORM models for Founder Curriculum Studio foundation (PI-001A).

Durable subject / version / document / processing / audit / published
package tables. Students may only consume PublishedCurriculumPackage rows.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class StudioFoundationSubject(db.Model):
    """Educational product created by a Founder (subject-agnostic)."""

    __tablename__ = "studio_foundation_subjects"

    id: int = db.Column(db.Integer, primary_key=True)
    subject_code: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    title: str = db.Column(db.String(255), nullable=False, default="")
    created_by: str = db.Column(db.String(128), nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    versions = db.relationship(
        "StudioFoundationVersion",
        back_populates="subject",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<StudioFoundationSubject {self.subject_code}>"


class StudioFoundationVersion(db.Model):
    """Curriculum version under Founder workflow (draft until published)."""

    __tablename__ = "studio_foundation_versions"
    __table_args__ = (
        db.UniqueConstraint(
            "subject_id",
            "version_label",
            name="uq_studio_foundation_versions_subject_label",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    subject_id: int = db.Column(
        db.Integer,
        db.ForeignKey("studio_foundation_subjects.id"),
        nullable=False,
        index=True,
    )
    version_label: str = db.Column(db.String(64), nullable=False)
    stage: str = db.Column(db.String(64), nullable=False, default="create_subject")
    publication_state: str = db.Column(
        db.String(64), nullable=False, default="draft", index=True
    )
    processing_state: str = db.Column(db.String(64), nullable=True)
    ingestion_job_id: str = db.Column(db.String(128), nullable=True, index=True)
    parsed_structure_json: str = db.Column(db.Text, nullable=True)
    validation_report_json: str = db.Column(db.Text, nullable=True)
    review_notes: str = db.Column(db.Text, nullable=True)
    reviewed_by: str = db.Column(db.String(128), nullable=True)
    reviewed_at: datetime = db.Column(db.DateTime, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    subject = db.relationship("StudioFoundationSubject", back_populates="versions")
    documents = db.relationship(
        "StudioFoundationDocument",
        back_populates="version",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<StudioFoundationVersion {self.version_label} "
            f"state={self.publication_state}>"
        )


class StudioFoundationDocument(db.Model):
    """Uploaded curriculum document reference (CMP / syllabus / supporting).

    Stores references and abstract structure payloads — never PDF bytes.
    """

    __tablename__ = "studio_foundation_documents"
    __table_args__ = (
        db.Index(
            "ix_studio_foundation_documents_version_kind",
            "version_id",
            "kind",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    version_id: int = db.Column(
        db.Integer,
        db.ForeignKey("studio_foundation_versions.id"),
        nullable=False,
        index=True,
    )
    kind: str = db.Column(db.String(64), nullable=False)
    reference: str = db.Column(db.String(1024), nullable=False)
    title: str = db.Column(db.String(255), nullable=False, default="")
    structure_json: str = db.Column(db.Text, nullable=True)
    uploaded_by: str = db.Column(db.String(128), nullable=False, default="")
    uploaded_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    version = db.relationship("StudioFoundationVersion", back_populates="documents")

    def __repr__(self) -> str:
        return f"<StudioFoundationDocument kind={self.kind} id={self.id}>"


class StudioFoundationAuditEvent(db.Model):
    """Append-only audit trail for every foundation lifecycle stage."""

    __tablename__ = "studio_foundation_audit_events"
    __table_args__ = (
        db.Index(
            "ix_studio_foundation_audit_subject_version",
            "subject_code",
            "version_id",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    event_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    subject_code: str = db.Column(db.String(64), nullable=False, index=True)
    version_id: int | None = db.Column(db.Integer, nullable=True, index=True)
    stage: str = db.Column(db.String(64), nullable=False, index=True)
    event_type: str = db.Column(db.String(64), nullable=False)
    actor_id: str = db.Column(db.String(128), nullable=False, default="")
    message: str = db.Column(db.String(512), nullable=False, default="")
    payload_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    def __repr__(self) -> str:
        return (
            f"<StudioFoundationAuditEvent {self.event_id} "
            f"stage={self.stage} type={self.event_type}>"
        )


class PublishedCurriculumPackage(db.Model):
    """Immutable published curriculum package — student-facing SSOT candidate.

    Only rows in this table may be exposed to student consumption paths.
    Draft / processing / review versions never appear here.
    """

    __tablename__ = "published_curriculum_packages"
    __table_args__ = (
        db.UniqueConstraint(
            "subject_code",
            "version_label",
            name="uq_published_curriculum_packages_code_label",
        ),
        db.Index(
            "ix_published_curriculum_packages_active",
            "subject_code",
            "is_active",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    subject_code: str = db.Column(db.String(64), nullable=False, index=True)
    version_id: int = db.Column(db.Integer, nullable=False, unique=True)
    version_label: str = db.Column(db.String(64), nullable=False)
    package_json: str = db.Column(db.Text, nullable=False)
    is_active: bool = db.Column(db.Boolean, nullable=False, default=True, index=True)
    published_by: str = db.Column(db.String(128), nullable=False, default="")
    published_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    source_ingestion_job_id: str = db.Column(db.String(128), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<PublishedCurriculumPackage {self.subject_code} "
            f"{self.version_label} active={self.is_active}>"
        )
