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
    sections = db.relationship(
        "Section",
        back_populates="curriculum",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="Section.curriculum_id",
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
    # V2 curriculum hierarchy: a Topic may optionally belong to a Section.
    # This field is intentionally nullable during the introduction milestone so
    # that existing topics (and study plans built on them) continue to work
    # unchanged. It is populated in a later milestone.
    section_id: int | None = db.Column(
        db.Integer,
        db.ForeignKey("sections.id"),
        nullable=True,
    )

    # Relationships
    curriculum = db.relationship("Curriculum", back_populates="topics")
    section = db.relationship(
        "Section",
        back_populates="topics",
        foreign_keys=[section_id],
    )
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


class Section(db.Model):
    """A section within a curriculum (V2 curriculum architecture).

    Sections are the top-level organizational units of a curriculum, sitting
    between the :class:`Curriculum` and its :class:`Topic` records. A
    curriculum has many sections; each section belongs to exactly one
    curriculum. A section may contain many topics (linked via
    ``Topic.section_id``), though that link is optional during the
    introduction milestone.
    """

    __tablename__ = "sections"

    id: int = db.Column(db.Integer, primary_key=True)
    curriculum_id: int = db.Column(
        db.Integer,
        db.ForeignKey("curricula.id"),
        nullable=False,
    )
    official_id: str | None = db.Column(
        db.String(100),
        nullable=True,
        comment="Canonical identifier from the official syllabus source",
    )
    code: str | None = db.Column(
        db.String(50),
        nullable=True,
        comment="Short human-readable code for the section (e.g. 'S1')",
    )
    title: str = db.Column(db.String(255), nullable=False)
    description: str | None = db.Column(db.Text(), nullable=True)
    exam_weight: float | None = db.Column(
        db.Float(),
        nullable=True,
        comment="Relative weighting of this section in the exam",
    )
    display_order: int = db.Column(
        db.Integer,
        default=0,
        nullable=False,
        comment="Ordering of the section within the curriculum",
    )
    estimated_hours: float | None = db.Column(
        db.Float(),
        nullable=True,
        comment="Estimated study hours required to cover this section",
    )
    difficulty: str | None = db.Column(
        db.String(50),
        nullable=True,
        comment="Difficulty rating (e.g. 'Easy', 'Medium', 'Hard')",
    )
    created_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    curriculum = db.relationship("Curriculum", back_populates="sections")
    topics = db.relationship(
        "Topic",
        back_populates="section",
        lazy=True,
        foreign_keys="Topic.section_id",
    )

    def __repr__(self) -> str:
        return f"<Section {self.code or self.official_id or self.title}>"