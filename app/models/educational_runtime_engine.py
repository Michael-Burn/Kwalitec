"""ORM models for the curriculum-driven Educational Runtime Engine (PI-001C).

Stores only student-runtime facts that cannot be deterministically re-derived:
enrolment, study-plan instance pointers, open/completed mission instances, and
immutable educational events. Curriculum structure remains in the published
package; progress is derived from events + the PI-001B progress model.
"""

from __future__ import annotations

from datetime import UTC, date, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class RuntimeEnrolment(db.Model):
    """Student enrolment against a published curriculum identity."""

    __tablename__ = "runtime_enrolments"
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "curriculum_identity",
            name="uq_runtime_enrolments_user_curriculum",
        ),
        db.Index(
            "ix_runtime_enrolments_user_subject",
            "user_id",
            "subject_code",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    enrolment_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    subject_code: str = db.Column(db.String(64), nullable=False, index=True)
    curriculum_identity: str = db.Column(db.String(128), nullable=False, index=True)
    published_package_id: int = db.Column(
        db.Integer,
        db.ForeignKey("published_curriculum_packages.id"),
        nullable=False,
        index=True,
    )
    version_label: str = db.Column(db.String(64), nullable=False)
    status: str = db.Column(db.String(32), nullable=False, default="active")
    exam_date: date | None = db.Column(db.Date, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return (
            f"<RuntimeEnrolment {self.enrolment_id} "
            f"{self.curriculum_identity} status={self.status}>"
        )


class RuntimeStudyPlanInstance(db.Model):
    """Student study-plan instance bound to a published study-plan template.

    Does not duplicate topic titles or minutes — those remain in the derived
    immutable template snapshot from PI-001B.
    """

    __tablename__ = "runtime_study_plan_instances"
    __table_args__ = (
        db.Index(
            "ix_runtime_study_plan_user_status",
            "user_id",
            "status",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    plan_instance_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    enrolment_id: str = db.Column(
        db.String(64),
        db.ForeignKey("runtime_enrolments.enrolment_id"),
        nullable=False,
        index=True,
    )
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    subject_code: str = db.Column(db.String(64), nullable=False)
    curriculum_identity: str = db.Column(db.String(128), nullable=False, index=True)
    version_label: str = db.Column(db.String(64), nullable=False)
    status: str = db.Column(db.String(32), nullable=False, default="active")
    # Reconciled projection of derive_progress(...).current_topic_id
    current_topic_id: str | None = db.Column(db.String(128), nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self) -> str:
        return (
            f"<RuntimeStudyPlanInstance {self.plan_instance_id} "
            f"status={self.status} topic={self.current_topic_id}>"
        )


class RuntimeMissionInstance(db.Model):
    """Curriculum-bound daily mission instantiated from a mission template."""

    __tablename__ = "runtime_mission_instances"
    __table_args__ = (
        db.UniqueConstraint(
            "plan_instance_id",
            "mission_date",
            name="uq_runtime_mission_plan_date",
        ),
        db.Index(
            "ix_runtime_mission_user_date",
            "user_id",
            "mission_date",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    mission_instance_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    plan_instance_id: str = db.Column(
        db.String(64),
        db.ForeignKey("runtime_study_plan_instances.plan_instance_id"),
        nullable=False,
        index=True,
    )
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    curriculum_identity: str = db.Column(db.String(128), nullable=False)
    template_id: str = db.Column(db.String(128), nullable=False)
    topic_id: str = db.Column(db.String(128), nullable=False, index=True)
    topic_code: str = db.Column(db.String(64), nullable=False, default="")
    title: str = db.Column(db.String(512), nullable=False, default="")
    task_descriptions_json: str = db.Column(db.Text, nullable=False, default="[]")
    mission_date: date = db.Column(db.Date, nullable=False)
    status: str = db.Column(db.String(32), nullable=False, default="generated")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    completed_at: datetime | None = db.Column(db.DateTime, nullable=True)
    # Phase 1 evidence-companion: SQL Mission substrate for StudyAttempt FK.
    # Never used for topic selection or Home "today's mission" surfacing.
    sql_mission_id: int | None = db.Column(
        db.Integer,
        db.ForeignKey("missions.id"),
        nullable=True,
        unique=True,
        index=True,
    )

    def __repr__(self) -> str:
        return (
            f"<RuntimeMissionInstance {self.mission_instance_id} "
            f"{self.mission_date} status={self.status}>"
        )


class RuntimeEducationalEvent(db.Model):
    """Append-only educational event — immutable after insert."""

    __tablename__ = "runtime_educational_events"
    __table_args__ = (
        db.Index(
            "ix_runtime_events_user_curriculum",
            "user_id",
            "curriculum_identity",
        ),
        db.Index(
            "ix_runtime_events_plan_type",
            "plan_instance_id",
            "event_type",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    event_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    event_type: str = db.Column(db.String(64), nullable=False, index=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    enrolment_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    plan_instance_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    curriculum_identity: str = db.Column(db.String(128), nullable=False)
    topic_id: str | None = db.Column(db.String(128), nullable=True)
    mission_instance_id: str | None = db.Column(db.String(64), nullable=True)
    payload_json: str = db.Column(db.Text, nullable=False, default="{}")
    occurred_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    def __repr__(self) -> str:
        return (
            f"<RuntimeEducationalEvent {self.event_id} type={self.event_type}>"
        )
