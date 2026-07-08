"""Service for managing study plans and week plans."""

from __future__ import annotations

from datetime import date, timedelta

from app.extensions import db
from app.models.study_plan import StudyPlan, WeekPlan


class StudyPlanService:
    """Service for creating and managing study plans."""

    @staticmethod
    def create_study_plan(
        user_id: int,
        exam_name: str,
        exam_sitting: str,
        exam_date: date,
        weekday_study_minutes: int,
        weekend_study_minutes: int,
        current_stage: str,
        study_preference: str,
        target_grade: str,
    ) -> StudyPlan:
        """Create a new study plan with associated week plans.

        Args:
            user_id: The ID of the user creating the study plan.
            exam_name: Name of the exam (e.g., "A-Level").
            exam_sitting: Exam sitting/session (e.g., "June 2026").
            exam_date: The date of the exam.
            weekday_study_minutes: Minutes per weekday for study.
            weekend_study_minutes: Minutes per weekend day for study.
            current_stage: Current study position (e.g., "Chapter 1").
            study_preference: Study preference (Reading First, Questions First, Mixed).
            target_grade: Target grade to achieve.

        Returns:
            StudyPlan: The created study plan with week plans.

        Raises:
            ValueError: If input validation fails.
        """
        # Validate inputs
        StudyPlanService._validate_study_plan_input(
            exam_date, weekday_study_minutes, weekend_study_minutes
        )

        # Deactivate any existing active study plans for this user
        StudyPlanService.deactivate_user_plans(user_id)

        # Create the study plan
        study_plan = StudyPlan(
            user_id=user_id,
            exam_name=exam_name,
            exam_sitting=exam_sitting,
            exam_date=exam_date,
            weekday_study_minutes=weekday_study_minutes,
            weekend_study_minutes=weekend_study_minutes,
            current_stage=current_stage,
            study_preference=study_preference,
            target_grade=target_grade,
            active=True,
        )

        db.session.add(study_plan)
        db.session.flush()  # Flush to get the study_plan.id

        # Create week plans
        week_plans = StudyPlanService._generate_week_plans(study_plan)
        for week_plan in week_plans:
            db.session.add(week_plan)

        db.session.commit()
        return study_plan

    @staticmethod
    def _validate_study_plan_input(
        exam_date: date,
        weekday_study_minutes: int,
        weekend_study_minutes: int,
    ) -> None:
        """Validate study plan input parameters.

        Args:
            exam_date: The exam date to validate.
            weekday_study_minutes: Weekday study time to validate.
            weekend_study_minutes: Weekend study time to validate.

        Raises:
            ValueError: If any validation fails.
        """
        today = date.today()

        if exam_date <= today:
            raise ValueError("Exam date must be in the future.")

        if weekday_study_minutes < 15 or weekday_study_minutes > 480:
            raise ValueError("Weekday study time must be between 15 and 480 minutes.")

        if weekend_study_minutes < 15 or weekend_study_minutes > 480:
            raise ValueError("Weekend study time must be between 15 and 480 minutes.")

    @staticmethod
    def _generate_week_plans(study_plan: StudyPlan) -> list[WeekPlan]:
        """Generate week plans from study start date to exam date.

        Args:
            study_plan: The study plan to generate weeks for.

        Returns:
            list[WeekPlan]: List of generated week plans.
        """
        today = date.today()
        exam_date = study_plan.exam_date

        # Find the Monday of the current week
        days_since_monday = today.weekday()
        start_of_week = today - timedelta(days=days_since_monday)

        week_plans = []
        week_number = 1
        current_week_start = start_of_week

        while current_week_start < exam_date:
            current_week_end = current_week_start + timedelta(days=6)

            # Clamp the end date to the exam date if necessary
            if current_week_end >= exam_date:
                current_week_end = exam_date - timedelta(days=1)

            week_plan = WeekPlan(
                study_plan_id=study_plan.id,
                week_number=week_number,
                start_date=current_week_start,
                end_date=current_week_end,
            )
            week_plans.append(week_plan)

            current_week_start = current_week_end + timedelta(days=1)
            week_number += 1

        return week_plans

    @staticmethod
    def get_user_active_plan(user_id: int) -> StudyPlan | None:
        """Get the active study plan for a user.

        Args:
            user_id: The user ID.

        Returns:
            StudyPlan | None: The active study plan or None if not found.
        """
        return StudyPlan.query.filter_by(user_id=user_id, active=True).first()

    @staticmethod
    def deactivate_user_plans(user_id: int) -> None:
        """Deactivate all study plans for a user.

        Args:
            user_id: The user ID.
        """
        StudyPlan.query.filter_by(user_id=user_id, active=True).update({"active": False})
        db.session.commit()

    @staticmethod
    def set_active_plan(study_plan_id: int, user_id: int) -> StudyPlan:
        """Set a specific study plan as active for a user.

        Args:
            study_plan_id: The ID of the study plan to activate.
            user_id: The ID of the user (for authorization).

        Returns:
            StudyPlan: The activated study plan.

        Raises:
            ValueError: If the study plan doesn't exist or doesn't belong to the user.
        """
        study_plan = StudyPlan.query.get(study_plan_id)
        if not study_plan:
            raise ValueError(f"Study plan {study_plan_id} not found")

        if study_plan.user_id != user_id:
            raise ValueError(f"Study plan {study_plan_id} does not belong to user {user_id}")

        # Deactivate other plans
        StudyPlanService.deactivate_user_plans(user_id)

        # Activate this plan
        study_plan.active = True
        db.session.commit()
        return study_plan

    @staticmethod
    def get_user_plans(user_id: int) -> list[StudyPlan]:
        """Get all study plans for a user.

        Args:
            user_id: The user ID.

        Returns:
            list[StudyPlan]: List of study plans ordered by creation date (newest first).
        """
        return StudyPlan.query.filter_by(user_id=user_id).order_by(
            StudyPlan.created_at.desc()
        ).all()

    @staticmethod
    def get_current_week_plan(study_plan: StudyPlan) -> WeekPlan | None:
        """Get the current week plan for a study plan.

        Args:
            study_plan: The study plan.

        Returns:
            WeekPlan | None: The current week plan or None if not found.
        """
        today = date.today()
        return WeekPlan.query.filter(
            WeekPlan.study_plan_id == study_plan.id,
            WeekPlan.start_date <= today,
            WeekPlan.end_date >= today,
        ).first()
