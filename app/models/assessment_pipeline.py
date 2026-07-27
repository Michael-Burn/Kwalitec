"""ORM models for Assessment & Learning Feedback Pipeline (AP-001).

Stores assessment events, results, feedback, attempts, performance summaries,
and mission assessment links. Does not duplicate Student Digital Twin state.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class ApAssessmentEvent(db.Model):
    """Immutable assessment event root."""

    __tablename__ = "assessment_events"
    __table_args__ = (
        db.Index("ix_ap_events_twin_occurred", "twin_id", "occurred_at"),
        db.Index("ix_ap_events_student_type", "student_id", "event_type"),
        db.Index("ix_ap_events_mission", "mission_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    event_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    event_type: str = db.Column(db.String(64), nullable=False)
    twin_id: str = db.Column(
        db.String(64),
        db.ForeignKey("student_digital_twins.twin_id"),
        nullable=False,
    )
    student_id: str = db.Column(db.String(128), nullable=False)
    occurred_at: datetime = db.Column(db.DateTime, nullable=False)
    activity_id: str = db.Column(db.String(128), nullable=False, default="")
    curriculum_entity_id: str = db.Column(db.String(128), nullable=False, default="")
    curriculum_entity_kind: str = db.Column(db.String(64), nullable=False, default="")
    concept_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    mission_id: str = db.Column(db.String(64), nullable=False, default="")
    step_id: str = db.Column(db.String(64), nullable=False, default="")
    source: str = db.Column(db.String(128), nullable=False, default="")
    score: float | None = db.Column(db.Float, nullable=True)
    correct: bool | None = db.Column(db.Boolean, nullable=True)
    duration_seconds: int | None = db.Column(db.Integer, nullable=True)
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    def __repr__(self) -> str:
        return f"<ApAssessmentEvent {self.event_id} type={self.event_type}>"


class ApAssessmentResult(db.Model):
    """Structured assessment result metadata linked to an observation."""

    __tablename__ = "assessment_results"
    __table_args__ = (
        db.Index("ix_ap_results_twin_created", "twin_id", "created_at"),
        db.Index("ix_ap_results_event", "event_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    result_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    event_id: str = db.Column(
        db.String(64),
        db.ForeignKey("assessment_events.event_id"),
        nullable=False,
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    event_type: str = db.Column(db.String(64), nullable=False)
    observation_id: str = db.Column(db.String(64), nullable=False)
    performance_label: str = db.Column(db.String(64), nullable=False, default="")
    evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    concepts_json: str = db.Column(db.Text, nullable=False, default="[]")
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class ApLearningFeedback(db.Model):
    """Deterministic educational learning feedback."""

    __tablename__ = "learning_feedback"
    __table_args__ = (
        db.Index("ix_ap_feedback_twin_ts", "twin_id", "timestamp"),
        db.Index("ix_ap_feedback_event", "event_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    feedback_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    event_id: str = db.Column(
        db.String(64),
        db.ForeignKey("assessment_events.event_id"),
        nullable=False,
    )
    result_id: str = db.Column(db.String(64), nullable=False)
    activity: str = db.Column(db.String(256), nullable=False, default="")
    performance: str = db.Column(db.String(64), nullable=False, default="")
    evidence_json: str = db.Column(db.Text, nullable=False, default="[]")
    concepts_json: str = db.Column(db.Text, nullable=False, default="[]")
    confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    suggested_next_action: str = db.Column(db.Text, nullable=False, default="")
    timestamp: datetime = db.Column(db.DateTime, nullable=False)
    source: str = db.Column(db.String(64), nullable=False, default="")
    observation_id: str = db.Column(db.String(64), nullable=False, default="")
    mission_id: str = db.Column(db.String(64), nullable=False, default="")
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")


class ApMissionAssessmentLink(db.Model):
    """Links adaptive missions to assessment events / observations."""

    __tablename__ = "mission_assessment_links"
    __table_args__ = (
        db.UniqueConstraint(
            "mission_id", "event_id", name="uq_ap_mission_event_link"
        ),
        db.Index("ix_ap_mission_links_twin", "twin_id"),
        db.Index("ix_ap_mission_links_mission", "mission_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    link_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    twin_id: str = db.Column(db.String(64), nullable=False)
    mission_id: str = db.Column(db.String(64), nullable=False)
    event_id: str = db.Column(
        db.String(64),
        db.ForeignKey("assessment_events.event_id"),
        nullable=False,
    )
    observation_id: str = db.Column(db.String(64), nullable=False, default="")
    step_id: str = db.Column(db.String(64), nullable=False, default="")
    link_kind: str = db.Column(db.String(64), nullable=False, default="completion")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class ApActivityAttempt(db.Model):
    """Immutable activity attempt record."""

    __tablename__ = "activity_attempts"
    __table_args__ = (
        db.Index("ix_ap_attempts_twin_at", "twin_id", "attempted_at"),
        db.Index("ix_ap_attempts_activity", "activity_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    attempt_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    student_id: str = db.Column(db.String(128), nullable=False)
    activity_id: str = db.Column(db.String(128), nullable=False)
    activity_kind: str = db.Column(db.String(64), nullable=False, default="")
    attempted_at: datetime = db.Column(db.DateTime, nullable=False)
    event_id: str = db.Column(db.String(64), nullable=False, default="")
    curriculum_entity_id: str = db.Column(db.String(128), nullable=False, default="")
    concept_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    score: float | None = db.Column(db.Float, nullable=True)
    correct: bool | None = db.Column(db.Boolean, nullable=True)
    duration_seconds: int | None = db.Column(db.Integer, nullable=True)
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")


class ApPerformanceSummary(db.Model):
    """Cached performance summary over assessment evidence (not Twin state)."""

    __tablename__ = "performance_summaries"
    __table_args__ = (
        db.Index("ix_ap_perf_twin_generated", "twin_id", "generated_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    summary_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    twin_id: str = db.Column(db.String(64), nullable=False)
    student_id: str = db.Column(db.String(128), nullable=False)
    event_count: int = db.Column(db.Integer, nullable=False, default=0)
    attempt_count: int = db.Column(db.Integer, nullable=False, default=0)
    correct_count: int = db.Column(db.Integer, nullable=False, default=0)
    incorrect_count: int = db.Column(db.Integer, nullable=False, default=0)
    mean_score: float | None = db.Column(db.Float, nullable=True)
    concepts_json: str = db.Column(db.Text, nullable=False, default="[]")
    generated_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    window_start: datetime | None = db.Column(db.DateTime, nullable=True)
    window_end: datetime | None = db.Column(db.DateTime, nullable=True)
