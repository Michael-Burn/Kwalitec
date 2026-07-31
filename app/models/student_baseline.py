"""ORM model for SB-001A Student Baseline — Twin educational origin.

Baseline is self-declared starting state. Changing baseline never deletes
study history, reflections, revision records, or analytics.
"""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class StudentBaseline(db.Model):
    """Durable Baseline declaration for one student × subject scope."""

    __tablename__ = "student_baselines"
    __table_args__ = (
        db.Index(
            "ix_student_baselines_user_subject_status",
            "user_id",
            "subject_key",
            "status",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    subject_key: str = db.Column(db.String(128), nullable=False)
    category_code: str = db.Column(db.String(64), nullable=False)
    subject_code: str = db.Column(db.String(64), nullable=False)
    runtime_authority: str | None = db.Column(db.String(64), nullable=True)

    status: str = db.Column(
        db.String(32),
        nullable=False,
        default="draft",
        comment="draft | complete | superseded",
    )

    experience: str | None = db.Column(db.String(64), nullable=True)
    position_mode: str | None = db.Column(db.String(64), nullable=True)
    curriculum_topic_code: str | None = db.Column(db.String(64), nullable=True)
    exam_history: str | None = db.Column(db.String(64), nullable=True)
    highest_mark: str | None = db.Column(db.String(64), nullable=True)
    learning_objective: str | None = db.Column(db.String(64), nullable=True)
    confidence: str | None = db.Column(db.String(64), nullable=True)
    curriculum_version: str | None = db.Column(db.String(64), nullable=True)

    study_plan_id: int | None = db.Column(
        db.Integer, db.ForeignKey("study_plans.id"), nullable=True
    )
    enrolment_id: str | None = db.Column(db.String(128), nullable=True)
    twin_snapshot_id: str | None = db.Column(db.String(64), nullable=True)
    supersedes_baseline_id: int | None = db.Column(
        db.Integer, db.ForeignKey("student_baselines.id"), nullable=True
    )

    completed_at: datetime | None = db.Column(db.DateTime, nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: datetime = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return (
            f"<StudentBaseline id={self.id} user={self.user_id} "
            f"subject={self.subject_key} status={self.status}>"
        )
