"""Learning models for recording student learning history."""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class StudyAttempt(db.Model):
    """Records a student's engagement with a mission and learning outcome.
    
    A StudyAttempt captures quantitative and qualitative data about a learning
    session, including time spent, performance metrics, and confidence changes.
    This forms the foundation for learning history analytics and future
    adaptive planning.
    """

    __tablename__ = "study_attempts"
    __table_args__ = (
        db.Index("ix_study_attempts_user_study_date", "user_id", "study_date"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mission_id: int = db.Column(db.Integer, db.ForeignKey("missions.id"), nullable=False)
    topic_id: int = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=True,
        comment="Associated topic from curriculum, if any",
    )
    study_date: datetime = db.Column(db.Date, nullable=False)
    duration_minutes: int = db.Column(
        db.Integer,
        nullable=True,
        comment="Time spent studying (reported by student)",
    )
    questions_attempted: int = db.Column(
        db.Integer,
        nullable=True,
        comment="Total questions/problems attempted",
    )
    questions_correct: int = db.Column(
        db.Integer,
        nullable=True,
        comment="Number of questions answered correctly",
    )
    confidence_before: str = db.Column(
        db.String(50),
        nullable=True,
        comment="Confidence level before studying",
    )
    confidence_after: str = db.Column(
        db.String(50),
        nullable=True,
        comment="Confidence level after studying",
    )
    notes: str = db.Column(
        db.Text,
        nullable=True,
        comment="Student's reflection on the learning session",
    )
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="study_attempts")
    mission = db.relationship("Mission", back_populates="study_attempts")
    mistakes = db.relationship(
        "Mistake",
        back_populates="study_attempt",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<StudyAttempt user={self.user_id} mission={self.mission_id}>"

    def get_accuracy_percentage(self) -> float | None:
        """Calculate accuracy as percentage correct.
        
        Returns:
            float: Percentage correct (0-100), or None if data missing.
        """
        if (
            self.questions_attempted is None
            or self.questions_correct is None
            or self.questions_attempted == 0
        ):
            return None
        return (self.questions_correct / self.questions_attempted) * 100


class LearningObjective(db.Model):
    """Defines specific learning outcomes for a topic.
    
    Learning objectives describe what students should learn about a topic.
    They provide granular learning targets that can be tracked and measured.
    """

    __tablename__ = "learning_objectives"

    id: int = db.Column(db.Integer, primary_key=True)
    topic_id: int = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    description: str = db.Column(
        db.Text,
        nullable=False,
        comment="What students should be able to do (full official syllabus text)",
    )
    order: int = db.Column(
        db.Integer,
        default=0,
        nullable=False,
        comment="Display and priority order",
    )
    active: bool = db.Column(db.Boolean, default=True, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    topic = db.relationship("Topic", back_populates="learning_objectives")

    def __repr__(self) -> str:
        return f"<LearningObjective {self.description[:30]}>"


class Mistake(db.Model):
    """Records an error or misconception identified during learning.
    
    Mistakes capture specific learning gaps or errors made during a study
    session. This allows targeted remediation and misconception analysis.
    """

    __tablename__ = "mistakes"

    id: int = db.Column(db.Integer, primary_key=True)
    study_attempt_id: int = db.Column(
        db.Integer,
        db.ForeignKey("study_attempts.id"),
        nullable=False,
    )
    topic_id: int = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=True,
        comment="Associated topic for analysis",
    )
    mistake_type: str = db.Column(
        db.String(100),
        nullable=True,
        comment="Category: Calculation, Concept, Misconception, Careless, etc.",
    )
    description: str = db.Column(
        db.Text,
        nullable=False,
        comment="What the student did wrong",
    )
    correct_solution: str = db.Column(
        db.Text,
        nullable=True,
        comment="The correct approach or answer",
    )
    resolved: bool = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        comment="Whether student understands the correct solution",
    )
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    study_attempt = db.relationship("StudyAttempt", back_populates="mistakes")
    topic = db.relationship("Topic", back_populates="mistakes")

    def __repr__(self) -> str:
        return f"<Mistake {self.mistake_type}>"
