"""ORM models for Curriculum Knowledge Graph (EI-001).

Normalised persistence for the educational structure SoT:

Subject → Topic → Section → Subsection → Learning Objective
plus educational objects, LO reference links, typed edges, and id aliases.

No PDF bytes, extraction jobs, Twin FKs, or student runtime tables.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class CkgGraphEdition(db.Model):
    """Edition metadata root tying a subject code to an edition label."""

    __tablename__ = "ckg_graph_editions"
    __table_args__ = (
        db.UniqueConstraint(
            "subject_code",
            "edition_label",
            name="uq_ckg_graph_editions_subject_edition",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    edition_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    subject_code: str = db.Column(db.String(32), nullable=False, index=True)
    edition_label: str = db.Column(db.String(64), nullable=False)
    provider: str = db.Column(db.String(64), nullable=False, default="IFoA")
    title: str = db.Column(db.String(255), nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    subjects = db.relationship(
        "CkgSubject",
        back_populates="graph_edition",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<CkgGraphEdition {self.subject_code} {self.edition_label}>"


class CkgSubject(db.Model):
    """Subject root node."""

    __tablename__ = "ckg_subjects"

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(128), nullable=False, unique=True, index=True)
    graph_edition_id: str = db.Column(
        db.String(64),
        db.ForeignKey("ckg_graph_editions.edition_id"),
        nullable=False,
        index=True,
    )
    code: str = db.Column(db.String(32), nullable=False)
    title: str = db.Column(db.String(255), nullable=False, default="")
    provider: str = db.Column(db.String(64), nullable=False, default="IFoA")
    edition_label: str = db.Column(db.String(64), nullable=False)
    sequence_index: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    graph_edition = db.relationship("CkgGraphEdition", back_populates="subjects")
    topics = db.relationship(
        "CkgTopic",
        back_populates="subject",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="CkgTopic.subject_stable_id",
    )

    def __repr__(self) -> str:
        return f"<CkgSubject {self.stable_id}>"


class CkgTopic(db.Model):
    """Topic within a subject."""

    __tablename__ = "ckg_topics"
    __table_args__ = (
        db.Index("ix_ckg_topics_subject_order", "subject_stable_id", "display_order"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(128), nullable=False, unique=True, index=True)
    subject_stable_id: str = db.Column(
        db.String(128),
        db.ForeignKey("ckg_subjects.stable_id"),
        nullable=False,
        index=True,
    )
    code: str = db.Column(db.String(64), nullable=False, default="")
    title: str = db.Column(db.String(512), nullable=False, default="")
    display_order: int = db.Column(db.Integer, nullable=False, default=0)
    difficulty: str = db.Column(db.String(32), nullable=False, default="foundational")
    estimated_study_minutes: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    subject = db.relationship(
        "CkgSubject",
        back_populates="topics",
        foreign_keys=[subject_stable_id],
    )
    sections = db.relationship(
        "CkgSection",
        back_populates="topic",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="CkgSection.topic_stable_id",
    )

    def __repr__(self) -> str:
        return f"<CkgTopic {self.stable_id}>"


class CkgSection(db.Model):
    """Section within a topic."""

    __tablename__ = "ckg_sections"
    __table_args__ = (
        db.Index("ix_ckg_sections_topic_order", "topic_stable_id", "display_order"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(160), nullable=False, unique=True, index=True)
    topic_stable_id: str = db.Column(
        db.String(128),
        db.ForeignKey("ckg_topics.stable_id"),
        nullable=False,
        index=True,
    )
    code: str = db.Column(db.String(64), nullable=False, default="")
    title: str = db.Column(db.String(512), nullable=False, default="")
    display_order: int = db.Column(db.Integer, nullable=False, default=0)
    difficulty: str = db.Column(db.String(32), nullable=False, default="foundational")
    estimated_study_minutes: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    topic = db.relationship(
        "CkgTopic",
        back_populates="sections",
        foreign_keys=[topic_stable_id],
    )
    subsections = db.relationship(
        "CkgSubsection",
        back_populates="section",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="CkgSubsection.section_stable_id",
    )

    def __repr__(self) -> str:
        return f"<CkgSection {self.stable_id}>"


class CkgSubsection(db.Model):
    """Subsection within a section."""

    __tablename__ = "ckg_subsections"
    __table_args__ = (
        db.Index(
            "ix_ckg_subsections_section_order",
            "section_stable_id",
            "display_order",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(192), nullable=False, unique=True, index=True)
    section_stable_id: str = db.Column(
        db.String(160),
        db.ForeignKey("ckg_sections.stable_id"),
        nullable=False,
        index=True,
    )
    code: str = db.Column(db.String(64), nullable=False, default="")
    title: str = db.Column(db.String(512), nullable=False, default="")
    display_order: int = db.Column(db.Integer, nullable=False, default=0)
    difficulty: str = db.Column(db.String(32), nullable=False, default="foundational")
    estimated_study_minutes: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    section = db.relationship(
        "CkgSection",
        back_populates="subsections",
        foreign_keys=[section_stable_id],
    )
    learning_objectives = db.relationship(
        "CkgLearningObjective",
        back_populates="subsection",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="CkgLearningObjective.subsection_stable_id",
    )

    def __repr__(self) -> str:
        return f"<CkgSubsection {self.stable_id}>"


class CkgLearningObjective(db.Model):
    """Learning objective within a subsection."""

    __tablename__ = "ckg_learning_objectives"
    __table_args__ = (
        db.Index(
            "ix_ckg_los_subsection_order",
            "subsection_stable_id",
            "display_order",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(224), nullable=False, unique=True, index=True)
    subsection_stable_id: str = db.Column(
        db.String(192),
        db.ForeignKey("ckg_subsections.stable_id"),
        nullable=False,
        index=True,
    )
    code: str = db.Column(db.String(64), nullable=False, default="")
    statement: str = db.Column(db.Text, nullable=False, default="")
    cognitive_level: str = db.Column(
        db.String(32), nullable=False, default="understand"
    )
    learning_type: str = db.Column(db.String(32), nullable=False, default="concept")
    display_order: int = db.Column(db.Integer, nullable=False, default=0)
    difficulty: str = db.Column(db.String(32), nullable=False, default="foundational")
    estimated_study_minutes: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    subsection = db.relationship(
        "CkgSubsection",
        back_populates="learning_objectives",
        foreign_keys=[subsection_stable_id],
    )
    links = db.relationship(
        "CkgLoLink",
        back_populates="learning_objective",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="CkgLoLink.lo_stable_id",
    )

    def __repr__(self) -> str:
        return f"<CkgLearningObjective {self.stable_id}>"


class CkgDefinition(db.Model):
    """Definition educational object."""

    __tablename__ = "ckg_definitions"
    __table_args__ = (db.Index("ix_ckg_definitions_owner", "owner_stable_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(256), nullable=False, unique=True, index=True)
    owner_stable_id: str = db.Column(db.String(224), nullable=False)
    title: str = db.Column(db.String(512), nullable=False, default="")
    body: str = db.Column(db.Text, nullable=False, default="")
    cmp_locator: str | None = db.Column(db.String(255), nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CkgFormula(db.Model):
    """Formula educational object."""

    __tablename__ = "ckg_formulas"
    __table_args__ = (db.Index("ix_ckg_formulas_owner", "owner_stable_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(256), nullable=False, unique=True, index=True)
    owner_stable_id: str = db.Column(db.String(224), nullable=False)
    title: str = db.Column(db.String(512), nullable=False, default="")
    notation: str = db.Column(db.Text, nullable=False, default="")
    latex: str | None = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CkgWorkedExample(db.Model):
    """Worked example educational object."""

    __tablename__ = "ckg_worked_examples"
    __table_args__ = (db.Index("ix_ckg_worked_examples_owner", "owner_stable_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(256), nullable=False, unique=True, index=True)
    owner_stable_id: str = db.Column(db.String(224), nullable=False)
    title: str = db.Column(db.String(512), nullable=False, default="")
    summary: str = db.Column(db.Text, nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CkgPracticeExercise(db.Model):
    """Practice exercise educational object (structure only)."""

    __tablename__ = "ckg_practice_exercises"
    __table_args__ = (db.Index("ix_ckg_practice_exercises_owner", "owner_stable_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(256), nullable=False, unique=True, index=True)
    owner_stable_id: str = db.Column(db.String(224), nullable=False)
    title: str = db.Column(db.String(512), nullable=False, default="")
    difficulty: str = db.Column(db.String(32), nullable=False, default="foundational")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CkgReadingReference(db.Model):
    """CMP / reading citation (no PDF bytes)."""

    __tablename__ = "ckg_reading_references"
    __table_args__ = (db.Index("ix_ckg_reading_references_owner", "owner_stable_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(256), nullable=False, unique=True, index=True)
    owner_stable_id: str = db.Column(db.String(224), nullable=False)
    title: str = db.Column(db.String(512), nullable=False, default="")
    document_kind: str = db.Column(db.String(64), nullable=False, default="cmp")
    locator: str = db.Column(db.String(255), nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CkgSyllabusOutcome(db.Model):
    """Official syllabus outcome reference."""

    __tablename__ = "ckg_syllabus_outcomes"
    __table_args__ = (db.Index("ix_ckg_syllabus_outcomes_owner", "owner_stable_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    stable_id: str = db.Column(db.String(256), nullable=False, unique=True, index=True)
    owner_stable_id: str = db.Column(db.String(224), nullable=False)
    outcome_code: str = db.Column(db.String(64), nullable=False, default="")
    statement_ref: str = db.Column(db.Text, nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CkgLoLink(db.Model):
    """Learning-objective reference link to an educational object."""

    __tablename__ = "ckg_lo_links"
    __table_args__ = (
        db.UniqueConstraint(
            "lo_stable_id",
            "target_kind",
            "target_stable_id",
            name="uq_ckg_lo_links_lo_target",
        ),
        db.Index("ix_ckg_lo_links_target", "target_stable_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    link_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    lo_stable_id: str = db.Column(
        db.String(224),
        db.ForeignKey("ckg_learning_objectives.stable_id"),
        nullable=False,
        index=True,
    )
    target_kind: str = db.Column(db.String(64), nullable=False)
    target_stable_id: str = db.Column(db.String(256), nullable=False)
    relationship_type: str = db.Column(
        db.String(64), nullable=False, default="references"
    )
    sequence_index: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    learning_objective = db.relationship(
        "CkgLearningObjective",
        back_populates="links",
        foreign_keys=[lo_stable_id],
    )


class CkgEdge(db.Model):
    """Directed typed edge (requires, cross_references, contains, …)."""

    __tablename__ = "ckg_edges"
    __table_args__ = (
        db.UniqueConstraint(
            "from_stable_id",
            "to_stable_id",
            "relationship_type",
            name="uq_ckg_edges_from_to_type",
        ),
        db.Index("ix_ckg_edges_from", "from_stable_id"),
        db.Index("ix_ckg_edges_to", "to_stable_id"),
        db.Index("ix_ckg_edges_type", "relationship_type"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    edge_id: str = db.Column(db.String(128), nullable=False, unique=True, index=True)
    from_stable_id: str = db.Column(db.String(256), nullable=False)
    to_stable_id: str = db.Column(db.String(256), nullable=False)
    relationship_type: str = db.Column(db.String(64), nullable=False)
    sequence_index: int = db.Column(db.Integer, nullable=False, default=0)
    rationale: str | None = db.Column(db.String(512), nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CkgIdAlias(db.Model):
    """Maps retired stable ids to their successors across curriculum updates."""

    __tablename__ = "ckg_id_aliases"
    __table_args__ = (
        db.UniqueConstraint("old_stable_id", name="uq_ckg_id_aliases_old"),
        db.Index("ix_ckg_id_aliases_new", "new_stable_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    old_stable_id: str = db.Column(db.String(256), nullable=False)
    new_stable_id: str = db.Column(db.String(256), nullable=False)
    reason: str = db.Column(db.String(255), nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
