"""ORM models for Student Curriculum Binding (EI-004).

Separates immutable published curriculum (CKG) from mutable learner state:

- SciStudentCurriculumInstance — student ↔ published edition binding
- SciCurriculumNodeState — educational state per curriculum node

Does not modify CKG tables, Twin, missions, or recommendation engines.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class SciStudentCurriculumInstance(db.Model):
    """Persistent binding of a student to a Published Curriculum Edition."""

    __tablename__ = "sci_student_curriculum_instances"
    __table_args__ = (
        db.Index(
            "ix_sci_instances_student_subject_active",
            "student_id",
            "subject_code",
            "is_active",
        ),
        db.Index("ix_sci_instances_edition", "edition_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    instance_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    student_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    subject_code: str = db.Column(db.String(32), nullable=False, index=True)
    edition_id: str = db.Column(
        db.String(64),
        db.ForeignKey("ckg_graph_editions.edition_id"),
        nullable=False,
        index=True,
    )
    enrolled_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    is_active: bool = db.Column(db.Boolean, nullable=False, default=True, index=True)
    is_completed: bool = db.Column(db.Boolean, nullable=False, default=False)
    completed_at: datetime | None = db.Column(db.DateTime, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    node_states = db.relationship(
        "SciCurriculumNodeState",
        back_populates="instance",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="SciCurriculumNodeState.instance_id",
    )

    def __repr__(self) -> str:
        return (
            f"<SciStudentCurriculumInstance {self.instance_id} "
            f"student={self.student_id} subject={self.subject_code}>"
        )


class SciCurriculumNodeState(db.Model):
    """Mutable educational state for one curriculum node within an instance.

    References curriculum by ``node_stable_id`` only — never mutates CKG rows.
    """

    __tablename__ = "sci_curriculum_node_states"
    __table_args__ = (
        db.UniqueConstraint(
            "instance_id",
            "node_stable_id",
            name="uq_sci_node_states_instance_stable",
        ),
        db.Index(
            "ix_sci_node_states_completion",
            "instance_id",
            "completion_status",
        ),
        db.Index("ix_sci_node_states_kind", "instance_id", "node_kind"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    instance_id: str = db.Column(
        db.String(64),
        db.ForeignKey("sci_student_curriculum_instances.instance_id"),
        nullable=False,
        index=True,
    )
    node_stable_id: str = db.Column(db.String(256), nullable=False, index=True)
    node_kind: str = db.Column(db.String(64), nullable=False, default="")
    mastery: float = db.Column(db.Float, nullable=False, default=0.0)
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    revision_status: str = db.Column(
        db.String(32), nullable=False, default="not_due"
    )
    attempts: int = db.Column(db.Integer, nullable=False, default=0)
    total_study_time_minutes: int = db.Column(db.Integer, nullable=False, default=0)
    last_interaction_at: datetime | None = db.Column(db.DateTime, nullable=True)
    completion_status: str = db.Column(
        db.String(32), nullable=False, default="not_started", index=True
    )
    evidence_count: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    instance = db.relationship(
        "SciStudentCurriculumInstance",
        back_populates="node_states",
        foreign_keys=[instance_id],
    )

    def __repr__(self) -> str:
        return (
            f"<SciCurriculumNodeState {self.node_stable_id} "
            f"instance={self.instance_id}>"
        )
