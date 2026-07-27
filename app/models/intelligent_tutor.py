"""ORM models for Evidence-Backed Intelligent Tutor (TUTOR-001).

Stores conversations only. Does not duplicate Student Digital Twin state.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class TutorSessionRow(db.Model):
    """Durable Tutor conversation session."""

    __tablename__ = "tutor_sessions"
    __table_args__ = (
        db.Index("ix_tutor_sessions_twin_updated", "twin_id", "updated_at"),
        db.Index("ix_tutor_sessions_student_status", "student_id", "status"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    session_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    student_id: str = db.Column(db.String(128), nullable=False)
    status: str = db.Column(db.String(32), nullable=False, default="active")
    title: str = db.Column(db.String(256), nullable=False, default="")
    active_mission_id: str = db.Column(db.String(64), nullable=False, default="")
    memory_json: str = db.Column(db.Text, nullable=False, default="{}")
    version: int = db.Column(db.Integer, nullable=False, default=1)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return f"<TutorSessionRow {self.session_id} status={self.status}>"


class TutorMessageRow(db.Model):
    """Single message in a Tutor conversation (student or tutor)."""

    __tablename__ = "tutor_messages"
    __table_args__ = (
        db.Index("ix_tutor_messages_session_created", "session_id", "created_at"),
        db.Index("ix_tutor_messages_twin_role", "twin_id", "role"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    message_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    session_id: str = db.Column(
        db.String(64),
        db.ForeignKey("tutor_sessions.session_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    role: str = db.Column(db.String(16), nullable=False)
    kind: str = db.Column(db.String(64), nullable=False, default="general")
    body: str = db.Column(db.Text, nullable=False, default="")
    concept_id: str = db.Column(db.String(64), nullable=False, default="")
    mission_id: str = db.Column(db.String(64), nullable=False, default="")
    context_id: str = db.Column(db.String(64), nullable=False, default="")
    evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class TutorExplanationRow(db.Model):
    """Persisted educational explanation attached to a Tutor response."""

    __tablename__ = "tutor_explanations"
    __table_args__ = (
        db.Index("ix_tutor_explanations_twin_created", "twin_id", "created_at"),
        db.Index("ix_tutor_explanations_session", "session_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    explanation_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    session_id: str = db.Column(
        db.String(64),
        db.ForeignKey("tutor_sessions.session_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    response_id: str = db.Column(db.String(64), nullable=False, default="")
    kind: str = db.Column(db.String(64), nullable=False, default="general")
    summary: str = db.Column(db.Text, nullable=False, default="")
    detail: str = db.Column(db.Text, nullable=False, default="")
    evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    concept_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    reasoning_run_id: str = db.Column(db.String(64), nullable=False, default="")
    mission_id: str = db.Column(db.String(64), nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class TutorFeedbackRow(db.Model):
    """Optional student / founder feedback on a Tutor response."""

    __tablename__ = "tutor_feedback"
    __table_args__ = (
        db.Index("ix_tutor_feedback_twin_created", "twin_id", "created_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    feedback_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    session_id: str = db.Column(
        db.String(64),
        db.ForeignKey("tutor_sessions.session_id"),
        nullable=False,
    )
    response_id: str = db.Column(db.String(64), nullable=False, default="")
    rating: int = db.Column(db.Integer, nullable=False, default=0)
    comment: str = db.Column(db.Text, nullable=False, default="")
    helpful: bool | None = db.Column(db.Boolean, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
