"""Topic progress tracking model."""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class TopicProgress(db.Model):
    """Tracks a user's progress on individual topics.
    
    This model records how users are progressing through curriculum topics,
    including confidence levels, completion status, mastery metrics,
    and review scheduling.
    """

    __tablename__ = "topic_progress"

    # Stage constants
    STAGE_NOT_STARTED = "Not Started"
    STAGE_LEARNING = "Learning"
    STAGE_PRACTISING = "Practising"
    STAGE_MASTERED = "Mastered"
    STAGE_NEEDS_REVIEW = "Needs Review"

    STAGES = [
        STAGE_NOT_STARTED,
        STAGE_LEARNING,
        STAGE_PRACTISING,
        STAGE_MASTERED,
        STAGE_NEEDS_REVIEW,
    ]

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    topic_id: int = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False,
    )
    confidence: str = db.Column(
        db.String(50),
        default="Not Started",
        nullable=False,
        comment="Not Started, Low, Medium, High, Mastered",
    )
    completed: bool = db.Column(db.Boolean, default=False, nullable=False)
    last_reviewed: datetime = db.Column(
        db.DateTime,
        nullable=True,
        comment="Last time this topic was studied",
    )
    revision_count: int = db.Column(
        db.Integer,
        default=0,
        nullable=False,
        comment="Number of times this topic has been reviewed",
    )
    mastery_score: float = db.Column(
        db.Float,
        default=0.0,
        nullable=False,
        comment="Calculated mastery score from 0 to 100",
    )
    average_accuracy: float = db.Column(
        db.Float,
        nullable=True,
        comment="Average accuracy across all study attempts (0-100)",
    )
    average_confidence: float = db.Column(
        db.Float,
        nullable=True,
        comment="Average numeric confidence derived from confidence levels",
    )
    next_review_date: datetime = db.Column(
        db.Date,
        nullable=True,
        comment="Scheduled date for the next review of this topic",
    )
    current_stage: str = db.Column(
        db.String(50),
        default=STAGE_NOT_STARTED,
        nullable=False,
        comment="Learning stage: Not Started, Learning, Practising, Mastered, Needs Review",
    )
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at: datetime = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    user = db.relationship("User", back_populates="topic_progress")
    topic = db.relationship("Topic", back_populates="topic_progress")

    def __repr__(self) -> str:
        return f"<TopicProgress user={self.user_id} topic={self.topic_id}>"

    def mark_reviewed(self) -> None:
        """Mark this topic as reviewed today and increment revision count.
        
        Call this when a mission is completed that involves this topic.
        """
        self.last_reviewed = datetime.utcnow()
        self.revision_count += 1
        self.updated_at = datetime.utcnow()
