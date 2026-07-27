"""ORM models for Adaptive Mission Engine (AME-001).

Stores mission plans, steps, progress, history, feedback, and completion.
Does not duplicate Student Digital Twin mastery / gap / recommendation rows.
"""

from __future__ import annotations

from datetime import UTC, date, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class AmeAdaptiveMission(db.Model):
    """Durable adaptive mission root — at most one ACTIVE per twin."""

    __tablename__ = "adaptive_missions"
    __table_args__ = (
        db.Index("ix_ame_missions_twin_date", "twin_id", "mission_date"),
        db.Index("ix_ame_missions_student_status", "student_id", "status"),
        db.Index("ix_ame_missions_twin_status", "twin_id", "status"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    mission_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    student_id: str = db.Column(db.String(128), nullable=False)
    mission_date: date = db.Column(db.Date, nullable=False)
    status: str = db.Column(db.String(32), nullable=False, default="draft")
    goal: str = db.Column(db.String(512), nullable=False, default="")
    priority: str = db.Column(db.String(32), nullable=False, default="medium")
    educational_objective: str = db.Column(db.Text, nullable=False, default="")
    primary_concept_id: str = db.Column(db.String(64), nullable=False, default="")
    concepts_json: str = db.Column(db.Text, nullable=False, default="[]")
    estimated_duration_minutes: int = db.Column(db.Integer, nullable=False, default=30)
    reason_summary: str = db.Column(db.Text, nullable=False, default="")
    educational_explanation: str = db.Column(db.Text, nullable=False, default="")
    expected_outcome: str = db.Column(db.Text, nullable=False, default="")
    success_criteria_json: str = db.Column(db.Text, nullable=False, default="[]")
    reflection_prompt: str = db.Column(db.Text, nullable=False, default="")
    evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    source_recommendation_ids_json: str = db.Column(
        db.Text, nullable=False, default="[]"
    )
    source_gap_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    recovery_path_json: str = db.Column(db.Text, nullable=False, default="[]")
    reasoning_run_id: str = db.Column(db.String(64), nullable=False, default="")
    schedule_json: str = db.Column(db.Text, nullable=False, default="{}")
    plan_json: str = db.Column(db.Text, nullable=False, default="{}")
    reason_json: str = db.Column(db.Text, nullable=False, default="{}")
    outcome_json: str = db.Column(db.Text, nullable=False, default="{}")
    validation_passed: bool = db.Column(db.Boolean, nullable=False, default=False)
    validation_summary: str = db.Column(db.Text, nullable=False, default="")
    version: int = db.Column(db.Integer, nullable=False, default=1)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return f"<AmeAdaptiveMission {self.mission_id} status={self.status}>"


class AmeMissionStep(db.Model):
    """Ordered abstract activity step within an adaptive mission."""

    __tablename__ = "mission_steps"
    __table_args__ = (
        db.UniqueConstraint("mission_id", "step_id", name="uq_ame_step_id"),
        db.Index("ix_ame_steps_mission_order", "mission_id", "step_order"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    step_id: str = db.Column(db.String(64), nullable=False, index=True)
    mission_id: str = db.Column(
        db.String(64),
        db.ForeignKey("adaptive_missions.mission_id"),
        nullable=False,
    )
    step_order: int = db.Column(db.Integer, nullable=False, default=1)
    activity_type: str = db.Column(db.String(64), nullable=False)
    concept_id: str = db.Column(db.String(64), nullable=False, default="")
    title: str = db.Column(db.String(512), nullable=False, default="")
    estimated_minutes: int = db.Column(db.Integer, nullable=False, default=10)
    reason: str = db.Column(db.Text, nullable=False, default="")
    success_criterion: str = db.Column(db.Text, nullable=False, default="")
    evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    completed: bool = db.Column(db.Boolean, nullable=False, default=False)


class AmeMissionProgress(db.Model):
    """Latest progress snapshot for an adaptive mission."""

    __tablename__ = "mission_progress"
    __table_args__ = (
        db.UniqueConstraint("mission_id", name="uq_ame_progress_mission"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    progress_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    mission_id: str = db.Column(
        db.String(64),
        db.ForeignKey("adaptive_missions.mission_id"),
        nullable=False,
    )
    steps_total: int = db.Column(db.Integer, nullable=False, default=0)
    steps_completed: int = db.Column(db.Integer, nullable=False, default=0)
    percent_complete: float = db.Column(db.Float, nullable=False, default=0.0)
    last_step_id: str = db.Column(db.String(64), nullable=False, default="")
    note: str = db.Column(db.Text, nullable=False, default="")
    updated_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class AmeMissionHistory(db.Model):
    """Append-only history of adaptive mission lifecycle events."""

    __tablename__ = "mission_history"
    __table_args__ = (
        db.Index("ix_ame_history_mission_created", "mission_id", "created_at"),
        db.Index("ix_ame_history_twin_created", "twin_id", "created_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    history_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    mission_id: str = db.Column(
        db.String(64),
        db.ForeignKey("adaptive_missions.mission_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    event_type: str = db.Column(db.String(64), nullable=False)
    summary: str = db.Column(db.Text, nullable=False, default="")
    payload_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class AmeMissionFeedback(db.Model):
    """Optional learner / founder feedback on an adaptive mission."""

    __tablename__ = "mission_feedback"
    __table_args__ = (
        db.Index("ix_ame_feedback_mission", "mission_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    feedback_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    mission_id: str = db.Column(
        db.String(64),
        db.ForeignKey("adaptive_missions.mission_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    rating: int | None = db.Column(db.Integer, nullable=True)
    comment: str = db.Column(db.Text, nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class AmeMissionCompletion(db.Model):
    """Immutable completion record for an adaptive mission."""

    __tablename__ = "mission_completion"
    __table_args__ = (
        db.UniqueConstraint("mission_id", name="uq_ame_completion_mission"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    completion_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    mission_id: str = db.Column(
        db.String(64),
        db.ForeignKey("adaptive_missions.mission_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    completed_at: datetime = db.Column(db.DateTime, nullable=False)
    steps_completed: int = db.Column(db.Integer, nullable=False, default=0)
    steps_total: int = db.Column(db.Integer, nullable=False, default=0)
    outcome_achieved: bool = db.Column(db.Boolean, nullable=False, default=False)
    reflection_response: str = db.Column(db.Text, nullable=False, default="")
    feedback_summary: str = db.Column(db.Text, nullable=False, default="")
