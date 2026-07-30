"""ORM models for Private Beta Validation (PB-001).

Evidence capture only — no educational architecture, AI systems, or
curriculum reasoning. Complements ALPHA-001 telemetry and RIP-001 check-ins.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


# Student-facing feedback categories (PB-001).
FEEDBACK_CATEGORIES: tuple[str, ...] = (
    "bug",
    "suggestion",
    "confusing_screen",
    "missing_feature",
    "incorrect_recommendation",
    "general",
)

# Auto / founder severity ladder (PB-001).
FEEDBACK_SEVERITIES: tuple[str, ...] = (
    "critical",
    "major",
    "minor",
    "enhancement",
    "question",
)

OBSERVATION_FIELDS: tuple[str, ...] = (
    "understood_onboarding",
    "knew_where_to_click",
    "understood_todays_mission",
    "understood_progress",
    "understood_tutor",
    "understood_knowledge_map",
    "became_stuck",
)


class PrivateBetaParticipant(db.Model):
    """Enrolled private-beta cohort member."""

    __tablename__ = "private_beta_participants"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    enrolled_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )
    cohort_label: str = db.Column(db.String(64), nullable=False, default="pb001")
    device_preference: str | None = db.Column(db.String(32), nullable=True)
    is_active: bool = db.Column(db.Boolean, nullable=False, default=True)
    notes: str | None = db.Column(db.String(500), nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now
    )

    user = db.relationship(
        "User",
        backref=db.backref("private_beta_participant", uselist=False, lazy=True),
    )

    def __repr__(self) -> str:
        return (
            f"<PrivateBetaParticipant id={self.id} user={self.user_id} "
            f"cohort={self.cohort_label}>"
        )


class PrivateBetaFeedback(db.Model):
    """Student feedback / bug report for private beta validation."""

    __tablename__ = "private_beta_feedback"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    category: str = db.Column(db.String(64), nullable=False, index=True)
    severity: str = db.Column(db.String(32), nullable=False, index=True)
    message: str = db.Column(db.String(1000), nullable=False)
    current_screen: str | None = db.Column(db.String(128), nullable=True)
    subject_code: str | None = db.Column(db.String(64), nullable=True)
    browser: str | None = db.Column(db.String(64), nullable=True)
    device: str | None = db.Column(db.String(64), nullable=True)
    product_version: str = db.Column(db.String(32), nullable=False)
    user_agent: str | None = db.Column(db.String(512), nullable=True)
    path: str | None = db.Column(db.String(255), nullable=True)
    mission_id: int | None = db.Column(
        db.Integer, db.ForeignKey("missions.id"), nullable=True, index=True
    )
    status: str = db.Column(
        db.String(32), nullable=False, default="new", index=True
    )
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    user = db.relationship(
        "User",
        backref=db.backref("private_beta_feedback", lazy=True),
    )
    mission = db.relationship("Mission", lazy=True)

    def __repr__(self) -> str:
        return (
            f"<PrivateBetaFeedback id={self.id} category={self.category} "
            f"severity={self.severity}>"
        )


class PrivateBetaObservation(db.Model):
    """Founder observation checklist for one beta user session."""

    __tablename__ = "private_beta_observations"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    observer_user_id: int | None = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )
    understood_onboarding: bool | None = db.Column(db.Boolean, nullable=True)
    knew_where_to_click: bool | None = db.Column(db.Boolean, nullable=True)
    understood_todays_mission: bool | None = db.Column(db.Boolean, nullable=True)
    understood_progress: bool | None = db.Column(db.Boolean, nullable=True)
    understood_tutor: bool | None = db.Column(db.Boolean, nullable=True)
    understood_knowledge_map: bool | None = db.Column(db.Boolean, nullable=True)
    became_stuck: bool | None = db.Column(db.Boolean, nullable=True)
    stuck_where: str | None = db.Column(db.String(255), nullable=True)
    notes: str | None = db.Column(db.String(1000), nullable=True)
    observed_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref=db.backref("private_beta_observations", lazy=True),
    )
    observer = db.relationship(
        "User",
        foreign_keys=[observer_user_id],
        lazy=True,
    )

    def __repr__(self) -> str:
        return (
            f"<PrivateBetaObservation id={self.id} user={self.user_id} "
            f"at={self.observed_at}>"
        )
