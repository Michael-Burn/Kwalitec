"""Curriculum and Topic models for structuring exam syllabi."""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class Curriculum(db.Model):
    """A curriculum represents a structured exam syllabus.
    
    Curricula contain hierarchical topics that define what should be studied
    for a specific exam. Each curriculum can have multiple versions and can
    be used by multiple study plans.
    """

    __tablename__ = "curricula"

    id: int = db.Column(db.Integer, primary_key=True)
    exam_name: str = db.Column(db.String(255), nullable=False)
    version: str = db.Column(db.String(50), nullable=False)  # e.g., "2024", "2025"
    active: bool = db.Column(db.Boolean, default=True, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    topics = db.relationship(
        "Topic",
        back_populates="curriculum",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="Topic.curriculum_id",
    )
    study_plans = db.relationship(
        "StudyPlan",
        back_populates="curriculum",
        lazy=True,
    )

    def __repr__(self) -> str:
        return f"<Curriculum {self.exam_name} v{self.version}>"

    def get_root_topics(self) -> list[Topic]:
        """Get all top-level topics (no parent).
        
        Returns:
            list[Topic]: Topics ordered by order field.
        """
        return (
            Topic.query.filter_by(
                curriculum_id=self.id,
                parent_topic_id=None,
                active=True,
            )
            .order_by(Topic.order)
            .all()
        )

    def get_all_topics_ordered(self) -> list[Topic]:
        """Get all topics in depth-first order.
        
        This returns topics in a hierarchical order suitable for displaying
        a syllabus tree or for sequential learning.
        
        Returns:
            list[Topic]: All active topics ordered hierarchically.
        """
        all_topics = []

        def collect_topics(parent_id: int | None = None) -> None:
            """Recursively collect topics in order."""
            topics = (
                Topic.query.filter_by(
                    curriculum_id=self.id,
                    parent_topic_id=parent_id,
                    active=True,
                )
                .order_by(Topic.order)
                .all()
            )
            for topic in topics:
                all_topics.append(topic)
                collect_topics(parent_id=topic.id)

        collect_topics()
        return all_topics


class Topic(db.Model):
    """A topic within a curriculum.
    
    Topics represent atomic units of learning content. Topics can be nested
    (parent_topic_id) to represent hierarchical syllabus structures like
    chapters containing sections containing subtopics.
    """

    __tablename__ = "topics"

    id: int = db.Column(db.Integer, primary_key=True)
    curriculum_id: int = db.Column(
        db.Integer,
        db.ForeignKey("curricula.id"),
        nullable=False,
    )
    name: str = db.Column(db.String(255), nullable=False)
    parent_topic_id: int = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=True,
    )
    order: int = db.Column(db.Integer, default=0, nullable=False)
    syllabus_weight: float = db.Column(
        db.Float,
        default=1.0,
        nullable=False,
        comment="Relative importance (0.5 = half, 1.0 = normal, 2.0 = double)",
    )
    recommended_minutes: int = db.Column(
        db.Integer,
        nullable=False,
        comment="Suggested study time in minutes",
    )
    active: bool = db.Column(db.Boolean, default=True, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    curriculum = db.relationship("Curriculum", back_populates="topics")
    parent_topic = db.relationship(
        "Topic",
        remote_side=[id],
        back_populates="subtopics",
    )
    subtopics = db.relationship(
        "Topic",
        back_populates="parent_topic",
        lazy=True,
    )
    topic_progress = db.relationship(
        "TopicProgress",
        back_populates="topic",
        lazy=True,
        cascade="all, delete-orphan",
    )
    learning_objectives = db.relationship(
        "LearningObjective",
        back_populates="topic",
        lazy=True,
        cascade="all, delete-orphan",
    )
    mistakes = db.relationship(
        "Mistake",
        back_populates="topic",
        lazy=True,
    )

    def __repr__(self) -> str:
        return f"<Topic {self.name}>"

    def is_leaf_topic(self) -> bool:
        """Check if this is a leaf topic (no subtopics).
        
        Returns:
            bool: True if this topic has no active subtopics.
        """
        return not self.subtopics

    def get_all_subtopics(self) -> list[Topic]:
        """Get all subtopics recursively in depth-first order.
        
        Returns:
            list[Topic]: All active subtopics ordered hierarchically.
        """
        all_subs = []

        def collect_subs(topic: Topic) -> None:
            """Recursively collect subtopics."""
            for sub in sorted(topic.subtopics, key=lambda t: t.order):
                if sub.active:
                    all_subs.append(sub)
                    collect_subs(sub)

        collect_subs(self)
        return all_subs