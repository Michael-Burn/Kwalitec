"""ORM models for Founder → Student platform integration (PI-002A).

Stores immutable runtime-routing audit rows so every enrolment decision
is reconstructible (Runtime A vs Runtime C, flags, reason).
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class RuntimeEnrolmentRoutingAudit(db.Model):
    """Append-only audit of runtime selection for a student enrolment."""

    __tablename__ = "runtime_enrolment_routing_audits"
    __table_args__ = (
        db.Index(
            "ix_runtime_routing_audit_user",
            "user_id",
            "created_at",
        ),
        db.Index(
            "ix_runtime_routing_audit_subject",
            "subject_code",
            "runtime_authority",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    audit_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    subject_code: str = db.Column(db.String(64), nullable=False, index=True)
    category_code: str = db.Column(db.String(64), nullable=False, default="")
    runtime_authority: str = db.Column(db.String(64), nullable=False, index=True)
    decision_reason: str = db.Column(db.String(128), nullable=False)
    published_package_id: int | None = db.Column(db.Integer, nullable=True)
    curriculum_identity: str | None = db.Column(db.String(128), nullable=True)
    enrolment_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    study_plan_id: int | None = db.Column(db.Integer, nullable=True, index=True)
    flags_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    def __repr__(self) -> str:
        return (
            f"<RuntimeEnrolmentRoutingAudit {self.audit_id} "
            f"{self.subject_code} → {self.runtime_authority}>"
        )
