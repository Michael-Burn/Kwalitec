"""Recommendation commitment persistence (EP-008.3).

Preference / intent claim only. Never mastery, readiness, or ranking input.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class RecommendationCommitment(db.Model):
    """One student's conscious commit / defer / complete / reflect cycle."""

    __tablename__ = "recommendation_commitments"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    recommendation_key: str = db.Column(db.String(255), nullable=False, index=True)
    title: str = db.Column(db.String(255), nullable=False, default="")
    state: str = db.Column(db.String(32), nullable=False, default="offered")
    deferred_reason_code: str = db.Column(db.String(64), nullable=False, default="")
    deferred_reason_note: str = db.Column(db.String(140), nullable=False, default="")
    expected_benefit: str = db.Column(db.Text, nullable=False, default="")
    review_point: str = db.Column(db.Text, nullable=False, default="")
    suggested_next_action: str = db.Column(db.Text, nullable=False, default="")
    session_id: str = db.Column(db.String(128), nullable=False, default="")
    decision_id: int = db.Column(db.Integer, nullable=True)
    committed_at: datetime = db.Column(db.DateTime, nullable=True)
    deferred_at: datetime = db.Column(db.DateTime, nullable=True)
    session_started_at: datetime = db.Column(db.DateTime, nullable=True)
    completed_at: datetime = db.Column(db.DateTime, nullable=True)
    reflected_at: datetime = db.Column(db.DateTime, nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: datetime = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref=db.backref("recommendation_commitments", lazy=True),
    )

    def __repr__(self) -> str:
        return (
            f"<RecommendationCommitment user={self.user_id} "
            f"state={self.state} title={self.title!r}>"
        )
