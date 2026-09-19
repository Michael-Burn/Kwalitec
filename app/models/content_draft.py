"""ORM model for Founder Console educational content drafts.

Draft rows are founder-authoring state only. They are never loaded by the
student educational package resolution path (on-disk
``educational_packages/`` + publication_approved status). APPROVED on this
table is distinct from PUBLISHED live inventory.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db

# Lifecycle statuses for content drafts. No ``published`` token: APPROVED
# and PUBLISHED remain conceptually distinct (publish is a later mechanism).
CONTENT_DRAFT_STATUS_DRAFT = "draft"
CONTENT_DRAFT_STATUS_READY_FOR_REVIEW = "ready_for_review"
CONTENT_DRAFT_STATUS_APPROVED = "approved"
CONTENT_DRAFT_STATUS_REJECTED = "rejected"

CONTENT_DRAFT_STATUSES: tuple[str, ...] = (
    CONTENT_DRAFT_STATUS_DRAFT,
    CONTENT_DRAFT_STATUS_READY_FOR_REVIEW,
    CONTENT_DRAFT_STATUS_APPROVED,
    CONTENT_DRAFT_STATUS_REJECTED,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class ContentDraft(db.Model):
    """One revision of an educational content draft (Founder Console).

    ``content_id`` is the stable identity across revisions. ``revision``
    increments when an approved (or published-linked) artifact is edited.
    ``payload_json`` holds the educational package JSON shape shared with
    ``CertifiedEducationalPackage`` / the on-disk loader.
    """

    __tablename__ = "content_drafts"
    __table_args__ = (
        db.UniqueConstraint(
            "content_id",
            "revision",
            name="uq_content_drafts_content_revision",
        ),
        db.Index("ix_content_drafts_content_id", "content_id"),
        db.Index("ix_content_drafts_lifecycle_status", "lifecycle_status"),
        db.Index("ix_content_drafts_subject_id", "subject_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)

    content_id: str = db.Column(db.String(36), nullable=False)
    revision: int = db.Column(db.Integer, nullable=False, default=1)

    subject_id: str = db.Column(db.String(64), nullable=False)
    canonical_topic_id: str | None = db.Column(
        db.String(36),
        db.ForeignKey("canonical_curriculum_topic.canonical_id"),
        nullable=True,
        index=True,
    )
    topic_code: str = db.Column(db.String(128), nullable=False, default="")
    objective_id: str = db.Column(db.String(128), nullable=False, default="")

    payload_json: str = db.Column(db.Text, nullable=False, default="{}")

    lifecycle_status: str = db.Column(
        db.String(32),
        nullable=False,
        default=CONTENT_DRAFT_STATUS_DRAFT,
    )

    created_by: str = db.Column(db.String(128), nullable=False, default="")
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now
    )
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    ai_assisted: bool = db.Column(db.Boolean, nullable=False, default=False)
    ai_proposed_json: str | None = db.Column(db.Text, nullable=True)
    human_edited_json: str | None = db.Column(db.Text, nullable=True)

    approved_by: str | None = db.Column(db.String(128), nullable=True)
    approved_at: datetime | None = db.Column(db.DateTime, nullable=True)

    # Reference to a live on-disk package id only. Never a serving join path.
    live_package_id: str | None = db.Column(db.String(256), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<ContentDraft content_id={self.content_id} "
            f"rev={self.revision} status={self.lifecycle_status}>"
        )
