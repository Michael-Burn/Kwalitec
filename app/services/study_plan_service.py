"""Service for managing study plans and week plans."""

from __future__ import annotations

import logging
from datetime import date, timedelta

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.topic_progress import TopicProgress

logger = logging.getLogger(__name__)


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
        preferred_session_minutes: int = 60,
        curriculum_version: str | None = None,
        curriculum_topic_code: str | None = None,
        completed_curriculum_topics: list[str] | None = None,
    ) -> StudyPlan:
        """Create a new study plan with associated week plans.

        Args:
            user_id: The ID of the user creating the study plan.
            exam_name: Name of the exam (e.g., "IFoA CS1").
            exam_sitting: Exam sitting/session (e.g., "April 2027").
            exam_date: The date of the exam.
            weekday_study_minutes: Minutes per weekday for study.
            weekend_study_minutes: Minutes per weekend day for study.
            current_stage: Current study stage (e.g., "Learning", "Revision").
            study_preference: Study preference (Reading First, Questions First, Mixed).
            target_grade: Target grade to achieve.
            preferred_session_minutes: Preferred study session length in minutes.
            curriculum_version: Optional curriculum version this plan was created against.
            curriculum_topic_code: Optional official curriculum topic code (e.g., "CS1-A").
            completed_curriculum_topics: Optional list of topic codes the user has
                already completed (from the Study Plan Wizard).

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
            preferred_session_minutes=preferred_session_minutes,
            curriculum_version=curriculum_version,
            curriculum_topic_code=curriculum_topic_code,
            active=True,
        )

        db.session.add(study_plan)
        db.session.flush()  # Flush to get the study_plan.id

        # Create week plans
        week_plans = StudyPlanService._generate_week_plans(study_plan)
        for week_plan in week_plans:
            db.session.add(week_plan)

        # Initialize TopicProgress from curriculum if applicable
        StudyPlanService._initialize_topic_progress_from_curriculum(
            study_plan,
            completed_curriculum_topics or [],
        )

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
    def _initialize_topic_progress_from_curriculum(
        study_plan: StudyPlan,
        completed_curriculum_topics: list[str] | None = None,
    ) -> None:
        """Initialize TopicProgress records from the curriculum backing this plan.

        When a study plan is created against a known curriculum, this method
        ensures that every topic in the curriculum has a corresponding
        TopicProgress row for the user.  Existing records are left untouched
        so that progress is preserved across plan changes.

        Topics whose ``code`` appears in ``completed_curriculum_topics`` are
        initialised as *completed* (completed=True, mastery_score=100.0,
        current_stage="Completed").

        The topic identified by ``curriculum_topic_code`` is promoted as the
        student's *current* topic (its ``current_stage`` is set to
        ``Learning``) but is **never** marked completed — even if it
        accidentally appears in ``completed_curriculum_topics``.
        """
        curriculum_version = study_plan.curriculum_version
        curriculum_topic_code = study_plan.curriculum_topic_code

        if curriculum_version is None:
            return  # Not a curriculum-backed plan — nothing to do.

        if completed_curriculum_topics is None:
            completed_curriculum_topics = []

        # Parse exam_name to extract organisation and paper.
        # Expected format: "<Organisation> <Paper>" (e.g. "IFoA CS1").
        parts = study_plan.exam_name.split(" ", 1)
        if len(parts) != 2:
            logger.debug(
                "Cannot parse exam_name '%s' for curriculum initialisation — skipping.",
                study_plan.exam_name,
            )
            return

        organisation, paper = parts

        from app.services.curriculum_engine_service import CurriculumEngineService

        engine = CurriculumEngineService()

        if not engine.curriculum_exists(organisation, paper, curriculum_version):
            logger.debug(
                "Curriculum %s/%s/%s not found — skipping topic progress initialisation.",
                organisation, paper, curriculum_version,
            )
            return

        try:
            curriculum = engine.load_curriculum(organisation, paper, curriculum_version)
        except Exception:
            logger.exception(
                "Failed to load curriculum %s/%s/%s.",
                organisation, paper, curriculum_version,
            )
            return

        engine_topics = curriculum.topics

        # ── Find or create the SQLAlchemy Curriculum row ──────────────────
        db_curriculum = Curriculum.query.filter_by(
            exam_name=f"{organisation} {paper}",
            version=curriculum_version,
        ).first()
        if db_curriculum is None:
            db_curriculum = Curriculum(
                exam_name=f"{organisation} {paper}",
                version=curriculum_version,
                active=True,
            )
            db.session.add(db_curriculum)
            db.session.flush()

        # Link the study plan to its curriculum.
        study_plan.curriculum_id = db_curriculum.id

        # ── Ensure a Topic + TopicProgress row for every engine topic ─────
        for order, engine_topic in enumerate(engine_topics, start=1):
            db_topic = Topic.query.filter_by(
                curriculum_id=db_curriculum.id,
                name=engine_topic.title,
            ).first()
            if db_topic is None:
                db_topic = Topic(
                    curriculum_id=db_curriculum.id,
                    name=engine_topic.title,
                    order=order,
                    recommended_minutes=int(engine_topic.estimated_hours * 60),
                    syllabus_weight=engine_topic.weighting,
                    active=True,
                )
                db.session.add(db_topic)
                db.session.flush()

            # Create TopicProgress only if one does not already exist.
            existing_progress = TopicProgress.query.filter_by(
                user_id=study_plan.user_id,
                topic_id=db_topic.id,
            ).first()
            if existing_progress is not None:
                continue

            # Determine initial state based on completed topics list.
            is_completed = engine_topic.code in completed_curriculum_topics

            tp = TopicProgress(
                user_id=study_plan.user_id,
                topic_id=db_topic.id,
                confidence="Mastered" if is_completed else "Not Started",
                completed=is_completed,
                mastery_score=100.0 if is_completed else 0.0,
                revision_count=0,
                last_reviewed=None,
                current_stage=TopicProgress.STAGE_COMPLETED
                if is_completed
                else TopicProgress.STAGE_NOT_STARTED,
            )
            db.session.add(tp)

        # ── Mark the selected topic as the student's current topic ────────
        if curriculum_topic_code is None:
            return  # No current topic selected — all topics stay "Not Started".

        for engine_topic in engine_topics:
            if engine_topic.code != curriculum_topic_code:
                continue

            db_topic = Topic.query.filter_by(
                curriculum_id=db_curriculum.id,
                name=engine_topic.title,
            ).first()
            if db_topic is None:
                continue

            tp = TopicProgress.query.filter_by(
                user_id=study_plan.user_id,
                topic_id=db_topic.id,
            ).first()
            if tp is None:
                # Should not normally happen, but guard anyway.
                continue

            tp.current_stage = TopicProgress.STAGE_LEARNING
            tp.completed = False
            tp.mastery_score = 0.0
            # Explicitly NOT marking completed.
            break

    @staticmethod
    def _generate_week_plans(study_plan: StudyPlan) -> list[WeekPlan]:
        """Generate week plans from study start date to exam date.
        
        For curriculum-backed study plans (those with both
        ``curriculum_version`` and ``curriculum_topic_code`` set), week
        plans are paced according to the official curriculum topic order
        loaded from the Curriculum Engine.  Otherwise, a simple date-based
        week-plan grid is produced.

        Args:
            study_plan: The study plan to generate weeks for.
        
        Returns:
            list[WeekPlan]: List of generated week plans.
        """
        # ── Try curriculum-backed sequencing first ──────────────────────
        if study_plan.curriculum_version and study_plan.curriculum_topic_code:
            from app.services.planning_service import PlanningService
            curriculum_weeks = PlanningService.generate_curriculum_week_plans(study_plan)
            if curriculum_weeks:
                return curriculum_weeks

        # ── Fall back to simple date-based grid ─────────────────────────
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
    def update_study_plan(
        study_plan_id: int,
        user_id: int,
        **kwargs,
    ) -> StudyPlan:
        """Update an existing study plan's details and regenerate week plans.

        Args:
            study_plan_id: The ID of the study plan to update.
            user_id: The ID of the user (for authorization).
            **kwargs: Fields to update (exam_name, exam_sitting, exam_date,
                weekday_study_minutes, weekend_study_minutes, current_stage,
                study_preference, target_grade, preferred_session_minutes,
                curriculum_topic_code, completed_curriculum_topics).

        Returns:
            StudyPlan: The updated study plan.

        Raises:
            ValueError: If the plan doesn't exist, doesn't belong to the user,
                or validation fails.
        """
        study_plan = StudyPlan.query.get(study_plan_id)
        if not study_plan:
            raise ValueError(f"Study plan {study_plan_id} not found")

        if study_plan.user_id != user_id:
            raise ValueError(f"Study plan {study_plan_id} does not belong to user {user_id}")

        if study_plan.archived:
            raise ValueError("Cannot edit an archived study plan.")

        # List of allowed scalar fields that can be updated
        updatable_fields = {
            "exam_name",
            "exam_sitting",
            "exam_date",
            "weekday_study_minutes",
            "weekend_study_minutes",
            "current_stage",
            "study_preference",
            "target_grade",
            "preferred_session_minutes",
            "curriculum_topic_code",
            "curriculum_version",
        }

        # Validate new values for study minutes if provided
        test_weekday = kwargs.get("weekday_study_minutes", study_plan.weekday_study_minutes)
        test_weekend = kwargs.get("weekend_study_minutes", study_plan.weekend_study_minutes)
        test_exam_date = kwargs.get("exam_date", study_plan.exam_date)
        StudyPlanService._validate_study_plan_input(test_exam_date, test_weekday, test_weekend)

        # Apply scalar updates
        for field in updatable_fields:
            if field in kwargs:
                setattr(study_plan, field, kwargs[field])

        db.session.flush()

        # Regenerate week plans (delete old, create new)
        WeekPlan.query.filter_by(study_plan_id=study_plan.id).delete()
        week_plans = StudyPlanService._generate_week_plans(study_plan)
        for week_plan in week_plans:
            db.session.add(week_plan)

        # Update completed curriculum topics if provided and plan is curriculum-backed
        completed_topics = kwargs.get("completed_curriculum_topics")
        if completed_topics is not None and study_plan.curriculum_version:
            curriculum_topic_code = kwargs.get(
                "curriculum_topic_code", study_plan.curriculum_topic_code
            )
            StudyPlanService._sync_completed_topics(
                study_plan, completed_topics, curriculum_topic_code
            )
        elif (
            completed_topics is not None
            and "curriculum_version" in kwargs
            and kwargs["curriculum_version"]
        ):
            curriculum_topic_code = kwargs.get(
                "curriculum_topic_code", study_plan.curriculum_topic_code
            )
            StudyPlanService._sync_completed_topics(
                study_plan, completed_topics, curriculum_topic_code
            )

        db.session.commit()
        return study_plan

    @staticmethod
    def _sync_completed_topics(
        study_plan: StudyPlan,
        completed_codes: list[str],
        curriculum_topic_code: str | None,
    ) -> None:
        """Synchronise TopicProgress completed status with the supplied list.

        Topics whose engine code appears in *completed_codes* are marked as
        completed (unless they are the current learning topic).  Topics
        NOT in the list that were previously completed are reset to
        ``Not Started`` (so the user can un-check a previously completed
        topic).
        """
        from app.models.curriculum import Topic as DBTopic
        from app.services.curriculum_engine_service import CurriculumEngineService

        if not study_plan.curriculum_id or not study_plan.curriculum_version:
            return

        parts = study_plan.exam_name.split(" ", 1)
        if len(parts) != 2:
            return

        organisation, paper = parts
        engine = CurriculumEngineService()
        if not engine.curriculum_exists(organisation, paper, study_plan.curriculum_version):
            return

        try:
            curriculum = engine.load_curriculum(
                organisation, paper, study_plan.curriculum_version
            )
        except Exception:
            logger.exception("Failed to load curriculum for topic sync.")
            return

        engine_topics = curriculum.topics
        completed_set = set(completed_codes)

        for engine_topic in engine_topics:
            db_topic = DBTopic.query.filter_by(
                curriculum_id=study_plan.curriculum_id,
                name=engine_topic.title,
            ).first()
            if db_topic is None:
                continue

            tp = TopicProgress.query.filter_by(
                user_id=study_plan.user_id,
                topic_id=db_topic.id,
            ).first()
            if tp is None:
                continue

            # Never mark the current learning topic as completed
            is_current = curriculum_topic_code and engine_topic.code == curriculum_topic_code
            should_be_completed = engine_topic.code in completed_set and not is_current

            if should_be_completed:
                tp.completed = True
                tp.mastery_score = 100.0
                tp.confidence = "Mastered"
                tp.current_stage = TopicProgress.STAGE_COMPLETED
            else:
                # If it was previously completed but is no longer in the
                # list (or is the current topic), reset to appropriate stage.
                if is_current:
                    tp.completed = False
                    tp.mastery_score = 0.0
                    tp.current_stage = TopicProgress.STAGE_LEARNING
                elif tp.completed and engine_topic.code not in completed_set:
                    tp.completed = False
                    tp.mastery_score = 0.0
                    tp.confidence = "Not Started"
                    tp.current_stage = TopicProgress.STAGE_NOT_STARTED

    @staticmethod
    def delete_study_plan(study_plan_id: int, user_id: int) -> None:
        """Permanently delete a study plan and cascade through dependent data.

        Deletes the study plan, its week plans, and associated TopicProgress
        records for this user.  Missions and study attempts are preserved
        (they belong to the user, not the plan).

        Args:
            study_plan_id: The ID of the study plan to delete.
            user_id: The ID of the user (for authorization).

        Raises:
            ValueError: If the plan doesn't exist or doesn't belong to the user.
        """
        study_plan = StudyPlan.query.get(study_plan_id)
        if not study_plan:
            raise ValueError(f"Study plan {study_plan_id} not found")

        if study_plan.user_id != user_id:
            raise ValueError(f"Study plan {study_plan_id} does not belong to user {user_id}")

        # Delete associated TopicProgress records for this user/curriculum
        if study_plan.curriculum_id:
            from app.models.curriculum import Topic as DBTopic

            linked_topic_ids = [
                r.id
                for r in db.session.query(DBTopic.id)
                .filter(DBTopic.curriculum_id == study_plan.curriculum_id)
                .all()
            ]
            if linked_topic_ids:
                TopicProgress.query.filter(
                    TopicProgress.user_id == user_id,
                    TopicProgress.topic_id.in_(linked_topic_ids),
                ).delete(synchronize_session="fetch")

        # The study plan's week_plans cascade automatically (delete-orphan)
        db.session.delete(study_plan)
        db.session.commit()

    @staticmethod
    def archive_study_plan(study_plan_id: int, user_id: int) -> StudyPlan:
        """Archive a study plan — preserve history but remove from active scheduling.

        If the plan being archived is currently active, it is deactivated
        so that no new missions are generated from it.

        Args:
            study_plan_id: The ID of the study plan to archive.
            user_id: The ID of the user (for authorization).

        Returns:
            StudyPlan: The archived study plan.

        Raises:
            ValueError: If the plan doesn't exist or doesn't belong to the user.
        """
        study_plan = StudyPlan.query.get(study_plan_id)
        if not study_plan:
            raise ValueError(f"Study plan {study_plan_id} not found")

        if study_plan.user_id != user_id:
            raise ValueError(f"Study plan {study_plan_id} does not belong to user {user_id}")

        study_plan.archived = True
        study_plan.active = False
        db.session.commit()
        return study_plan

    @staticmethod
    def get_user_plans(
        user_id: int, include_archived: bool = False
    ) -> list[StudyPlan]:
        """Get all study plans for a user.

        Args:
            user_id: The user ID.
            include_archived: If True, also return archived plans.

        Returns:
            list[StudyPlan]: List of study plans ordered by creation date (newest first).
        """
        query = StudyPlan.query.filter_by(user_id=user_id)
        if not include_archived:
            query = query.filter_by(archived=False)
        return query.order_by(StudyPlan.created_at.desc()).all()

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