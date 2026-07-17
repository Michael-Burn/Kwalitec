"""Mission and MissionTask models."""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class Mission(db.Model):
    """A mission is a collection of tasks assigned for a specific date and subject.

    Missions represent daily learning objectives organized by subject.
    Each mission contains multiple tasks that need to be completed.
    """

    __tablename__ = "missions"
    __table_args__ = (
        db.Index("ix_missions_status_mission_date", "status", "mission_date"),
        db.Index(
            "ix_missions_user_date_study_plan",
            "user_id",
            "mission_date",
            "study_plan_id",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subject_id: int = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    study_plan_id: int | None = db.Column(
        db.Integer,
        db.ForeignKey("study_plans.id"),
        nullable=True,
        comment="Active study plan this mission was generated for",
    )
    mission_date: datetime = db.Column(db.Date, nullable=False)
    title: str = db.Column(db.String(255), nullable=False)
    status: str = db.Column(
        db.String(50),
        default="Pending",
        nullable=False,
        comment="Pending, In Progress, or Completed",
    )
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="missions")
    subject = db.relationship("Subject", back_populates="missions")
    study_plan = db.relationship("StudyPlan", back_populates="missions")
    study_attempts = db.relationship(
        "StudyAttempt",
        back_populates="mission",
        lazy=True,
        cascade="all, delete-orphan",
    )
    tasks = db.relationship(
        "MissionTask",
        back_populates="mission",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="MissionTask.order",
    )

    def __repr__(self) -> str:
        return f"<Mission {self.title}>"

    def get_completion_percentage(self) -> float:
        """Calculate the completion percentage of this mission's tasks.

        Returns:
            float: Percentage of tasks completed (0-100). Returns 100 if no tasks.
        """
        if not self.tasks:
            return 100.0

        completed_count = sum(1 for task in self.tasks if task.completed)
        return (completed_count / len(self.tasks)) * 100


class MissionTask(db.Model):
    """A single task within a mission.

    Tasks are the atomic units of work that make up a mission.
    Each task can be marked as complete or incomplete.
    """

    __tablename__ = "mission_tasks"

    id: int = db.Column(db.Integer, primary_key=True)
    mission_id: int = db.Column(
        db.Integer, db.ForeignKey("missions.id"), nullable=False, index=True
    )
    title: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.Text, nullable=True)
    order: int = db.Column(db.Integer, default=0, nullable=False)
    completed: bool = db.Column(db.Boolean, default=False, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    mission = db.relationship("Mission", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<MissionTask {self.title}>"
