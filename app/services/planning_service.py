"""Service for automatic mission planning and generation from study plans."""

from __future__ import annotations

import logging
from datetime import date
from enum import Enum

from app.extensions import db
from app.models.curriculum import Topic
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.curriculum_service import CurriculumService
from app.services.mission_service import MissionService
from app.services.study_plan_service import StudyPlanService

logger = logging.getLogger(__name__)


class DayType(Enum):
    """Enumeration of day types for mission generation."""

    WEEKDAY = "weekday"
    WEEKEND = "weekend"


class PlanningService:
    """Service for automatic mission planning from study plans.
    
    This service handles deterministic, idempotent mission generation based on
    a user's active study plan. It ensures that missions are generated only for
    the current day and that refreshing never creates duplicates.
    """

    @staticmethod
    def generate_today_mission(user_id: int, today: date | None = None) -> Mission | None:
        """Generate today's mission if it doesn't already exist.
        
        This method is idempotent - calling it multiple times on the same day
        will not create duplicate missions. If a mission already exists for today,
        it will be returned without modification.
        
        Args:
            user_id: The ID of the user.
            today: The date to generate the mission for (defaults to today).
        
        Returns:
            Mission: The generated or existing mission for today, or None if no
                    active study plan exists or today is outside the study window.
        """
        if today is None:
            today = date.today()

        # Get active study plan
        active_plan = StudyPlanService.get_user_active_plan(user_id)
        if not active_plan:
            logger.info("No active study plan for user %s; skipping mission generation", user_id)
            return None

        # Check if mission already exists for today (idempotency)
        existing_mission = Mission.query.filter_by(
            user_id=user_id,
            mission_date=today,
        ).first()

        if existing_mission:
            logger.debug("Mission already exists for user %s on %s", user_id, today)
            return existing_mission

        # Get current week plan
        current_week = StudyPlanService.get_current_week_plan(active_plan)
        if not current_week:
            # Today is outside the study plan date range
            logger.warning(
                "Today %s is outside study plan %s date range; no mission generated",
                today, active_plan.id,
            )
            return None

        # Generate new mission
        mission = PlanningService._generate_mission_for_date(
            user_id=user_id,
            active_plan=active_plan,
            target_date=today,
        )

        logger.info("Generated mission %d for user %s on %s", mission.id, user_id, today)
        return mission

    @staticmethod
    def _generate_mission_for_date(
        user_id: int,
        active_plan: StudyPlan,
        target_date: date,
    ) -> Mission:
        """Generate a mission for a specific date.
        
        This is the core mission generation logic that creates missions based on
        the study plan configuration and deterministic rules. If a curriculum
        is associated with the study plan, the next incomplete topic is used
        to guide task generation. Otherwise, falls back to generic tasks.
        
        Args:
            user_id: The ID of the user.
            active_plan: The active study plan.
            target_date: The date to generate the mission for.
        
        Returns:
            Mission: The created mission with tasks.
        """
        # Determine day type (weekday or weekend)
        day_type = PlanningService._get_day_type(target_date)
        
        # Get study minutes for this day type
        study_minutes = (
            active_plan.weekday_study_minutes
            if day_type == DayType.WEEKDAY
            else active_plan.weekend_study_minutes
        )

        # Determine the best topic for today using priority-based selection
        next_topic = PlanningService._select_topic_for_today(
            user_id=user_id,
            active_plan=active_plan,
            target_date=target_date,
        )

        # Generate mission title and tasks based on day type and topic
        mission_title = PlanningService._generate_mission_title(
            day_type=day_type,
            target_date=target_date,
            topic=next_topic,
        )
        tasks_data = PlanningService._generate_mission_tasks(
            day_type=day_type,
            study_minutes=study_minutes,
            current_stage=active_plan.current_stage,
            study_preference=active_plan.study_preference,
            topic=next_topic,
        )

        # Use a default subject for all automatically generated missions
        subject_id = PlanningService._get_or_create_default_subject(user_id)

        # Create mission via service
        mission = MissionService.create_mission(
            user_id=user_id,
            subject_id=subject_id,
            mission_date=target_date,
            title=mission_title,
            tasks=tasks_data,
        )

        return mission

    @staticmethod
    def _get_day_type(target_date: date) -> DayType:
        """Determine if a date is a weekday or weekend.
        
        Args:
            target_date: The date to check.
        
        Returns:
            DayType: WEEKDAY (Monday-Friday) or WEEKEND (Saturday-Sunday).
        """
        # weekday() returns 0-6 (Monday-Sunday)
        weekday_num = target_date.weekday()
        return DayType.WEEKEND if weekday_num >= 5 else DayType.WEEKDAY

    @staticmethod
    def _generate_mission_title(
        day_type: DayType,
        target_date: date,
        topic: Topic | None = None,
    ) -> str:
        """Generate a descriptive mission title based on day type and topic.
        
        Args:
            day_type: The type of day (WEEKDAY or WEEKEND).
            target_date: The date of the mission.
            topic: Optional topic to include in the title.
        
        Returns:
            str: A descriptive mission title.
        """
        day_name = target_date.strftime("%A")
        date_str = target_date.strftime("%b %d")
        
        if topic:
            if day_type == DayType.WEEKDAY:
                return f"Learn: {topic.name} - {day_name}, {date_str}"
            else:
                return f"Practice: {topic.name} - {day_name}, {date_str}"
        else:
            if day_type == DayType.WEEKDAY:
                return f"Daily Study - {day_name}, {date_str}"
            else:
                return f"Weekend Review - {day_name}, {date_str}"

    @staticmethod
    def _generate_mission_tasks(
        day_type: DayType,
        study_minutes: int,
        current_stage: str,
        study_preference: str,
        topic: Topic | None = None,
    ) -> list[dict]:
        """Generate mission tasks based on day type and study time.
        
        This is the deterministic task generation algorithm. The number and type
        of tasks are always the same for the same inputs, making this testable
        and predictable.
        
        Args:
            day_type: Type of day (WEEKDAY or WEEKEND).
            study_minutes: Total available study minutes.
            current_stage: Current study stage (e.g., "Chapter 3").
            study_preference: Study preference (Reading First, Questions First, Mixed).
            topic: Optional curriculum topic to use in task descriptions.
        
        Returns:
            list[dict]: List of task dictionaries with title, description, and order.
        """
        tasks = []

        if day_type == DayType.WEEKDAY:
            tasks.extend(
                PlanningService._generate_weekday_tasks(
                    study_minutes=study_minutes,
                    current_stage=current_stage,
                    study_preference=study_preference,
                    topic=topic,
                )
            )
        else:
            tasks.extend(
                PlanningService._generate_weekend_tasks(
                    study_minutes=study_minutes,
                    current_stage=current_stage,
                    topic=topic,
                )
            )

        return tasks

    @staticmethod
    def _generate_weekday_tasks(
        study_minutes: int,
        current_stage: str,
        study_preference: str,
        topic: Topic | None = None,
    ) -> list[dict]:
        """Generate tasks for a weekday.
        
        Weekday structure depends on study preference and topic.
        
        Args:
            study_minutes: Total available study minutes.
            current_stage: Current study position (used if no topic).
            study_preference: User's study preference.
            topic: Optional curriculum topic to reference in tasks.
        
        Returns:
            list[dict]: List of task dictionaries.
        """
        tasks = []
        order = 0

        # Allocate time across three tasks
        reading_mins = max(10, int(study_minutes * 0.35))
        practice_mins = max(10, int(study_minutes * 0.40))
        review_mins = max(10, int(study_minutes * 0.25))

        study_subject = topic.name if topic else current_stage

        if study_preference == "Reading First":
            tasks.append({
                "title": f"Read: {study_subject}",
                "description": f"Study the material for {reading_mins} minutes. Focus on understanding key concepts and definitions. Refer to your textbook or notes on {study_subject}.",
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Practice Questions",
                "description": f"Complete practice questions for {practice_mins} minutes. Test your understanding of {study_subject} with worked examples.",
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Review & Consolidate",
                "description": f"Review your answers for {review_mins} minutes. Identify any gaps in your understanding of {study_subject} and note key points.",
                "order": order,
            })
        elif study_preference == "Questions First":
            tasks.append({
                "title": "Practice Questions",
                "description": f"Start with practice questions for {practice_mins} minutes. Test your current knowledge of {study_subject}. This helps identify what you need to learn.",
                "order": order,
            })
            order += 1
            tasks.append({
                "title": f"Read: {study_subject}",
                "description": f"Study relevant material for {reading_mins} minutes. Based on the questions, focus on areas where you need improvement.",
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Review & Learn",
                "description": f"Review for {review_mins} minutes. Connect the theory you just learned to the practice questions. Reinforce your understanding.",
                "order": order,
            })
        else:  # Mixed
            tasks.append({
                "title": f"Study: {study_subject}",
                "description": f"Study and practice {study_subject} for {reading_mins} minutes. Alternate between reading concepts and solving problems.",
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Practice & Apply",
                "description": f"Apply your learning for {practice_mins} minutes. Work through more questions on {study_subject}. Deepen your understanding.",
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Reflect & Review",
                "description": f"Reflect for {review_mins} minutes. Consolidate all learning from {study_subject} today. Note any remaining questions.",
                "order": order,
            })

        return tasks

    @staticmethod
    def _generate_weekend_tasks(
        study_minutes: int,
        current_stage: str,
        topic: Topic | None = None,
    ) -> list[dict]:
        """Generate tasks for a weekend day.
        
        Args:
            study_minutes: Total available study minutes.
            current_stage: Current study position (used if no topic).
            topic: Optional curriculum topic to reference in tasks.
        
        Returns:
            list[dict]: List of task dictionaries.
        """
        tasks = []
        order = 0

        practice_mins = max(15, int(study_minutes * 0.50))
        review_mins = max(10, int(study_minutes * 0.30))
        formula_mins = max(10, int(study_minutes * 0.20))

        study_subject = topic.name if topic else current_stage

        tasks.append({
            "title": "Timed Practice",
            "description": f"Complete a full practice paper or substantial problem set on {study_subject} in {practice_mins} minutes. Time yourself to simulate exam conditions.",
            "order": order,
        })
        order += 1
        tasks.append({
            "title": "Review & Analyze",
            "description": f"Review your answers thoroughly for {review_mins} minutes. Analyze your mistakes on {study_subject}. Understand where you went wrong.",
            "order": order,
        })
        order += 1
        tasks.append({
            "title": "Concept Consolidation",
            "description": f"Consolidate key concepts and formulas for {formula_mins} minutes. Focus on areas revealed by your practice on {study_subject}.",
            "order": order,
        })

        return tasks

    @staticmethod
    def _select_topic_for_today(
        user_id: int,
        active_plan: StudyPlan,
        target_date: date,
    ) -> Topic | None:
        """Select the best topic for today's mission using priority-based ordering.

        Priority order:
        1. Topics due for review today (next_review_date <= today)
        2. Weak topics (mastery < 60) that need attention
        3. Continue curriculum sequence (next incomplete topic)

        This method is deterministic - given the same inputs, it always returns
        the same topic.

        Args:
            user_id: The ID of the user.
            active_plan: The active study plan.
            target_date: The date to select a topic for.

        Returns:
            Topic: The selected topic, or None if no curriculum/no topics available.
        """
        # If no curriculum is associated, fall back to generic topic selection
        if not active_plan.curriculum_id:
            curriculum = None
        else:
            curriculum = CurriculumService.get_curriculum_by_id(active_plan.curriculum_id)

        if not curriculum:
            return None

        # --- Priority 1: Topics due for review today ---
        due_reviews = AdaptiveLearningService.get_topics_due_for_review(
            user_id=user_id,
            target_date=target_date,
        )
        if due_reviews:
            # Pick the first topic due for review (by next_review_date ascending)
            selected_progress = due_reviews[0]
            topic = selected_progress.topic
            logger.debug(
                "Priority 1: Selected review topic %s (due %s, mastery=%.1f)",
                topic.name, selected_progress.next_review_date, selected_progress.mastery_score,
            )
            return topic

        # --- Priority 2: Weak topics that need attention ---
        weak_topics = AdaptiveLearningService.get_weak_topics(
            user_id=user_id,
            threshold=60.0,
        )
        if weak_topics:
            # Weakest topic first (already ordered by mastery ascending)
            selected_progress = weak_topics[0]
            topic = selected_progress.topic
            logger.debug(
                "Priority 2: Selected weak topic %s (mastery=%.1f)",
                topic.name, selected_progress.mastery_score,
            )
            return topic

        # --- Priority 3: Continue curriculum sequence ---
        next_topic = CurriculumService.get_next_incomplete_topic(
            user_id=user_id,
            curriculum=curriculum,
        )
        if next_topic:
            logger.debug("Priority 3: Selected next curriculum topic %s", next_topic.name)
            return next_topic

        # All topics complete
        logger.info("All curriculum topics completed for user %s", user_id)
        return None

    @staticmethod
    def _get_or_create_default_subject(user_id: int) -> int:
        """Get or create a default subject for mission generation.
        
        Creates or returns a "Study Plan" subject to serve as the default
        organizational category for auto-generated missions.
        
        Args:
            user_id: The ID of the user.
        
        Returns:
            int: The subject ID.
        """
        from app.models.subject import Subject

        default_subject = Subject.query.filter_by(
            user_id=user_id,
            name="Study Plan",
            active=True,
        ).first()

        if default_subject:
            return default_subject.id

        default_subject = Subject(
            user_id=user_id,
            name="Study Plan",
            colour="#007bff",
            active=True,
        )
        db.session.add(default_subject)
        db.session.commit()
        logger.info("Created default subject 'Study Plan' for user %s", user_id)
        return default_subject.id