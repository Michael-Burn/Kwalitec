"""Educational Feedback Loop persistence (ILE-005).

Internal Sensei educational review records. Never exposed as a student
surface. Append-only relative to Decision Journal history.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class EducationalFeedbackReview(db.Model):
    """One internal Sensei educational review of a journal recommendation.

    Observation → Original recommendation → Later evidence →
    Educational assessment → Future learning.

    ``learner_visible`` is always False for rows written by ILE-005.
    """

    __tablename__ = "educational_feedback_reviews"

    id: int = db.Column(db.Integer, primary_key=True)
    review_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    journal_entry_id: str = db.Column(
        db.String(64), nullable=False, index=True
    )

    observation: str = db.Column(db.Text, nullable=False, default="")
    original_recommendation: str = db.Column(
        db.Text, nullable=False, default=""
    )
    later_evidence: str = db.Column(db.Text, nullable=False, default="")
    educational_assessment: str = db.Column(
        db.Text, nullable=False, default=""
    )
    future_learning: str = db.Column(db.Text, nullable=False, default="")

    review_state: str = db.Column(db.String(64), nullable=False, index=True)
    evidence_quality: str = db.Column(db.String(32), nullable=False)
    assessment_focus: str = db.Column(db.String(64), nullable=False)
    rationale_summary: str = db.Column(db.Text, nullable=False, default="")

    # Hard invariant: Sensei reviews are governance-only.
    learner_visible: bool = db.Column(
        db.Boolean, nullable=False, default=False
    )

    recorded_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    created_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref("educational_feedback_reviews", lazy=True),
    )

    def __repr__(self) -> str:
        return (
            f"<EducationalFeedbackReview {self.review_id} "
            f"state={self.review_state} entry={self.journal_entry_id}>"
        )
