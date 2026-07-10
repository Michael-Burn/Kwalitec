"""Study Plan models for organizing and scheduling study."""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class StudyPlan(db.Model):
    """A study plan represents a personalized learning schedule for a specific exam.
    
    Study plans organize the approach to exam preparation, including timing,
    study preferences, and target grades. They form the foundation for
    automatic mission generation.
    """

    __tablename__ = "study_plans"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    curriculum_id: int = db.Column(
        db.Integer,
        db.ForeignKey("curricula.id"),
        nullable=True,
        comment="Associated curriculum for structured syllabus",
    )
    exam_name: str = db.Column(db.String(255), nullable=False)
    exam_sitting: str = db.Column(db.String(100), nullable=False)  # e.g., "June 2026"
    exam_date: datetime = db.Column(db.Date, nullable=False)
    weekday_study_minutes: int = db.Column(db.Integer, nullable=False)  # Minutes per weekday
    weekend_study_minutes: int = db.Column(db.Integer, nullable=False)  # Minutes per weekend day
    current_stage: str = db.Column(db.String(255), nullable=False)  # e.g., "Chapter 1", "Revision"
    study_preference: str = db.Column(
        db.String(50),
        default="Mixed",
        nullable=False,
        comment="Reading First, Questions First, or Mixed",
    )
    target_grade: str = db.Column(db.String(50), nullable=False)  # e.g., "A", "B", "Pass"
    preferred_session_minutes: int = db.Column(
        db.Integer,
        default=60,
        nullable=False,
        comment="Preferred study session length in minutes (30/45/60/90/120)",
    )
    curriculum_version: str = db.Column(
        db.String(20),
        nullable=True,
        default=None,
        comment="Curriculum version this plan was created against",
    )
    curriculum_topic_code: str = db.Column(
        db.String(50),
        nullable=True,
        default=None,
        comment="Official curriculum topic code currently being studied (e.g., 'CS1-A')",
    )
    active: bool = db.Column(db.Boolean, default=False, nullable=False)
    archived: bool = db.Column(db.Boolean, default=False, nullable=False, comment="Archived plans are hidden from active scheduling but preserved")
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="study_plans")
    curriculum = db.relationship("Curriculum", back_populates="study_plans")
    week_plans = db.relationship(
        "WeekPlan",
        back_populates="study_plan",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="WeekPlan.week_number",
    )

    def __repr__(self) -> str:
        return f"<StudyPlan {self.exam_name}>"

    def get_total_weeks(self) -> int:
        """Get the total number of weeks in this study plan.
        
        Returns:
            int: Number of weeks planned
        """
        return len(self.week_plans)

    def get_weeks_remaining(self) -> int:
        """Get the number of weeks remaining until exam date.
        
        Returns:
            int: Number of weeks remaining
        """
        from datetime import date, timedelta

        today = date.today()
        exam_date = self.exam_date
        days_remaining = (exam_date - today).days
        weeks_remaining = max(0, days_remaining // 7)
        return weeks_remaining


class WeekPlan(db.Model):
    """A week plan represents a specific week within a study plan.
    
    Week plans mark the time boundaries and organization points for
    mission generation and tracking.
    """

    __tablename__ = "week_plans"

    id: int = db.Column(db.Integer, primary_key=True)
    study_plan_id: int = db.Column(db.Integer, db.ForeignKey("study_plans.id"), nullable=False)
    week_number: int = db.Column(db.Integer, nullable=False)
    start_date: datetime = db.Column(db.Date, nullable=False)
    end_date: datetime = db.Column(db.Date, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    study_plan = db.relationship("StudyPlan", back_populates="week_plans")

    def __repr__(self) -> str:
        return f"<WeekPlan Week {self.week_number}>"

    def is_current_week(self) -> bool:
        """Check if this is the current week.
        
        Returns:
            bool: True if today falls within this week
        """
        from datetime import date

        today = date.today()
        return self.start_date <= today <= self.end_date

    def is_past(self) -> bool:
        """Check if this week is in the past.
        
        Returns:
            bool: True if the end date has passed
        """
        from datetime import date

        today = date.today()
        return self.end_date < today