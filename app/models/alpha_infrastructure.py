"""ORM models for Internal Alpha operational infrastructure (ALPHA-001).

Presentation telemetry and lightweight product feedback only.
Independent of Educational Evidence, Twin state, recommendations,
and Education OS domain models.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class PresentationEvent(db.Model):
    """One presentation/application telemetry event.

    Never stores educational scores, Twin payloads, or recommendation math.
    """

    __tablename__ = "presentation_events"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int | None = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True, index=True
    )
    event_type: str = db.Column(db.String(64), nullable=False, index=True)
    resource_type: str | None = db.Column(db.String(64), nullable=True)
    resource_id: str | None = db.Column(db.String(64), nullable=True)
    path: str | None = db.Column(db.String(255), nullable=True)
    correlation_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    context_json: str | None = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    user = db.relationship(
        "User",
        backref=db.backref("presentation_events", lazy=True),
    )

    def __repr__(self) -> str:
        return (
            f"<PresentationEvent id={self.id} type={self.event_type} "
            f"user={self.user_id}>"
        )


class AlphaFeedbackSubmission(db.Model):
    """Lightweight structured alpha feedback (mission / explanation / report).

    Distinct from RIP-001 Product Check-in — shorter capture for in-flow
    questions. Does not mutate educational state.
    """

    __tablename__ = "alpha_feedback_submissions"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    kind: str = db.Column(db.String(64), nullable=False, index=True)
    rating: str | None = db.Column(db.String(32), nullable=True)
    message: str | None = db.Column(db.String(500), nullable=True)
    mission_id: int | None = db.Column(
        db.Integer, db.ForeignKey("missions.id"), nullable=True, index=True
    )
    surface: str | None = db.Column(db.String(64), nullable=True)
    product_version: str = db.Column(db.String(32), nullable=False)
    correlation_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    status: str = db.Column(db.String(32), nullable=False, default="new", index=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    user = db.relationship(
        "User",
        backref=db.backref("alpha_feedback_submissions", lazy=True),
    )
    mission = db.relationship("Mission", lazy=True)

    def __repr__(self) -> str:
        return (
            f"<AlphaFeedbackSubmission id={self.id} kind={self.kind} "
            f"user={self.user_id}>"
        )
