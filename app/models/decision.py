"""Decision model for the Decision Journal.

Records user decisions about recommendations, tracking acceptance,
completion, and outcomes over time.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class Decision(db.Model):
    """A decision records whether a user accepted or rejected a recommendation.

    The Decision Journal provides a complete audit trail of what recommendations
    were offered, whether they were accepted, completed, and what the outcome was.
    This enables analysis of recommendation effectiveness and user behaviour patterns.
    """

    __tablename__ = "decisions"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # The recommendation that triggered this decision
    recommendation_title: str = db.Column(db.String(255), nullable=False)
    recommendation_category: str = db.Column(db.String(100), nullable=False)
    recommendation_priority: str = db.Column(db.String(50), nullable=False)
    recommendation_reason: str = db.Column(db.Text, nullable=False)
    recommendation_expected_benefit: str = db.Column(db.Text, nullable=False)
    recommendation_generated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    # Decision outcome
    accepted: bool = db.Column(db.Boolean, default=False, nullable=False)
    completed: bool = db.Column(db.Boolean, default=False, nullable=False)
    outcome_summary: str = db.Column(db.Text, nullable=True)

    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    user = db.relationship("User", back_populates="decisions")

    def __repr__(self) -> str:
        return f"<Decision {self.recommendation_title} accepted={self.accepted}>"

    def to_dict(self) -> dict:
        """Convert decision to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "recommendation_title": self.recommendation_title,
            "recommendation_category": self.recommendation_category,
            "recommendation_priority": self.recommendation_priority,
            "recommendation_reason": self.recommendation_reason,
            "recommendation_expected_benefit": self.recommendation_expected_benefit,
            "accepted": self.accepted,
            "completed": self.completed,
            "outcome_summary": self.outcome_summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }