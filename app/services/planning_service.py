"""Service for automatic mission planning and generation from study plans."""

from __future__ import annotations

import logging
from collections import deque
from datetime import date, timedelta
from enum import Enum

from app.extensions import db
from app.models.curriculum import Topic
from app.models.mission import Mission
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


# Leading syllabus command verbs that make awkward mission copy when prefixed
# with "Study" / "Practice" (e.g. "Study Understand and use …").
_TOPIC_TITLE_VERB_PREFIXES: tuple[str, ...] = (
    "understand and use ",
    "understand and apply ",
    "understand and explain ",
    "understand ",
    "describe and use ",
    "describe ",
    "explain ",
    "calculate ",
    "derive ",
    "apply ",
    "define ",
    "identify ",
    "analyse ",
    "analyze ",
    "compare ",
    "discuss ",
    "evaluate ",
    "produce ",
    "construct ",
    "solve ",
    "use ",
)


class PlanningService:
    """Service for automatic mission planning from study plans.
    
    This service handles deterministic, idempotent mission generation based on
    a user's active study plan. It ensures that missions are generated only for
    the current day and that refreshing never creates duplicates.
    """

    @staticmethod
    def _topic_study_label(topic: Topic | None, fallback: str = "today's topic") -> str:
        """Return a natural study label from an official syllabus topic title.

        Official titles are often imperative learning objectives. Mission copy
        should read like a premium learning platform, e.g. ``Generalised Linear
        Models`` rather than ``Understand and use generalised linear models``.
        """
        raw = (topic.name if topic and topic.name else fallback).strip()
        lowered = raw.lower()
        for prefix in _TOPIC_TITLE_VERB_PREFIXES:
            if lowered.startswith(prefix):
                raw = raw[len(prefix):].strip()
                break
        if not raw:
            return fallback
        # Preserve intentional acronyms; otherwise title-case word-wise.
        words = []
        for word in raw.split():
            if word.isupper() or any(ch.isdigit() for ch in word):
                words.append(word)
            else:
                words.append(word[:1].upper() + word[1:] if word else word)
        return " ".join(words)
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
        topic_label = PlanningService._topic_study_label(topic) if topic else None

        if topic_label:
            if day_type == DayType.WEEKDAY:
                return f"Study {topic_label} — {day_name}, {date_str}"
            return f"Practice {topic_label} — {day_name}, {date_str}"
        if day_type == DayType.WEEKDAY:
            return f"Daily Study — {day_name}, {date_str}"
        return f"Weekend Review — {day_name}, {date_str}"

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

        study_subject = PlanningService._topic_study_label(topic, fallback=current_stage)

        if study_preference == "Reading First":
            tasks.append({
                "title": f"Study {study_subject}",
                "description": (
                    f"Read the Core Reading for today's section for about "
                    f"{reading_mins} minutes. Focus on the key ideas in "
                    f"{study_subject}."
                ),
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Complete practice questions",
                "description": (
                    f"Work through the recommended practice questions for about "
                    f"{practice_mins} minutes on {study_subject}."
                ),
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Review and consolidate",
                "description": (
                    f"Spend about {review_mins} minutes reviewing your answers "
                    f"and noting any gaps in {study_subject}."
                ),
                "order": order,
            })
        elif study_preference == "Questions First":
            tasks.append({
                "title": "Complete practice questions",
                "description": (
                    f"Start with practice questions for about {practice_mins} "
                    f"minutes to test your current understanding of "
                    f"{study_subject}."
                ),
                "order": order,
            })
            order += 1
            tasks.append({
                "title": f"Study {study_subject}",
                "description": (
                    f"Read the Core Reading for about {reading_mins} minutes, "
                    f"focusing on the areas the questions highlighted."
                ),
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Review and learn",
                "description": (
                    f"Spend about {review_mins} minutes connecting the theory "
                    f"to the practice questions on {study_subject}."
                ),
                "order": order,
            })
        else:  # Mixed
            tasks.append({
                "title": f"Study {study_subject}",
                "description": (
                    f"Read the Core Reading for today's section and complete "
                    f"the recommended practice questions "
                    f"(about {reading_mins} minutes on {study_subject})."
                ),
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Practice and apply",
                "description": (
                    f"Apply what you have learned for about {practice_mins} "
                    f"minutes with further questions on {study_subject}."
                ),
                "order": order,
            })
            order += 1
            tasks.append({
                "title": "Reflect and review",
                "description": (
                    f"Spend about {review_mins} minutes consolidating today's "
                    f"learning on {study_subject} and noting remaining questions."
                ),
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

        study_subject = PlanningService._topic_study_label(topic, fallback=current_stage)

        tasks.append({
            "title": "Timed practice",
            "description": (
                f"Complete a focused practice set on {study_subject} in about "
                f"{practice_mins} minutes under timed conditions."
            ),
            "order": order,
        })
        order += 1
        tasks.append({
            "title": "Review and analyse",
            "description": (
                f"Review your answers thoroughly for about {review_mins} "
                f"minutes and note where {study_subject} still feels uncertain."
            ),
            "order": order,
        })
        order += 1
        tasks.append({
            "title": "Consolidate key points",
            "description": (
                f"Spend about {formula_mins} minutes consolidating formulas, "
                f"definitions, and key results for {study_subject}."
            ),
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

    # ── Curriculum-backed study plan helpers ──────────────────────────────

    @staticmethod
    def _resolve_curriculum_sequence(study_plan: StudyPlan) -> list[dict] | None:
        """Resolve the official curriculum topic order for a curriculum-backed plan.

        Loads the curriculum from the Curriculum Engine, topologically sorts
        topics respecting prerequisites, and returns the sequence starting
        from the user's selected ``curriculum_topic_code``.  Topics that come
        before the selected topic in the official order are excluded.

        Args:
            study_plan: A study plan with ``curriculum_version`` and
                ``curriculum_topic_code`` set.

        Returns:
            A list of topic dicts with keys ``name``, ``code``, ``hours``,
            ``weighting``, ``prerequisites`` — ordered following the official
            curriculum sequence — or ``None`` if the curriculum cannot be
            resolved or the plan is not curriculum-backed.
        """
        from app.services.curriculum_engine_service import CurriculumEngineService

        version = study_plan.curriculum_version
        topic_code = study_plan.curriculum_topic_code

        if not version or not topic_code:
            return None

        # Parse exam_name — expected format "<Organisation> <Paper>"
        parts = study_plan.exam_name.split(" ", 1)
        if len(parts) != 2:
            logger.debug(
                "Cannot parse exam_name '%s' for curriculum sequence resolution.",
                study_plan.exam_name,
            )
            return None

        organisation, paper = parts
        engine = CurriculumEngineService()

        if not engine.curriculum_exists(organisation, paper, version):
            logger.debug(
                "Curriculum %s/%s/%s not found on disk — falling back to generic sequencing.",
                organisation, paper, version,
            )
            return None

        try:
            curriculum = engine.load_auto(organisation, paper, version)
        except Exception:
            logger.exception(
                "Failed to load curriculum %s/%s/%s for sequence resolution.",
                organisation, paper, version,
            )
            return None

        engine_topics = CurriculumEngineService.get_topics_flat(curriculum)

        if not engine_topics:
            return None

        # ── Topological sort respecting prerequisites ──────────────────
        # V1 topics carry prerequisites; V2 TopicDefinitions are already in
        # official syllabus order and typically have no prerequisite graph.
        topic_map: dict[str, dict] = {}
        for et in engine_topics:
            learning_outcomes = []
            if hasattr(et, "learning_outcomes"):
                learning_outcomes = [
                    {
                        "code": lo.code,
                        "description": lo.description,
                        "suggested_revision_days": lo.suggested_revision_days,
                    }
                    for lo in et.learning_outcomes
                ]
            elif hasattr(et, "learning_objectives"):
                learning_outcomes = [
                    {
                        "code": lo.code,
                        "description": lo.description,
                        "suggested_revision_days": 14,
                    }
                    for lo in et.learning_objectives
                ]

            if hasattr(et, "estimated_hours"):
                hours = float(et.estimated_hours)
            else:
                hours = float(getattr(et, "estimated_minutes", 0)) / 60.0

            topic_map[et.id] = {
                "name": et.title,
                "code": et.code,
                "hours": hours,
                "weighting": float(getattr(et, "weighting", 0.0) or 0.0),
                "prerequisites": list(getattr(et, "prerequisites", []) or []),
                "learning_outcomes": learning_outcomes,
            }

        # Build dependency graph for Kahn's algorithm
        in_degree: dict[str, int] = {tid: 0 for tid in topic_map}
        adj: dict[str, list[str]] = {tid: [] for tid in topic_map}

        for et in engine_topics:
            for prereq_id in getattr(et, "prerequisites", []) or []:
                if prereq_id in topic_map:
                    adj[prereq_id].append(et.id)
                    in_degree[et.id] += 1

        queue: deque[str] = deque(
            tid for tid, deg in in_degree.items() if deg == 0
        )
        sorted_ids: list[str] = []

        while queue:
            current = queue.popleft()
            sorted_ids.append(current)
            for neighbor in adj[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Keep only topics present in the graph
        sorted_ids = [tid for tid in sorted_ids if tid in topic_map]

        # ── Locate the selected starting topic ─────────────────────────
        start_index: int | None = None
        for i, tid in enumerate(sorted_ids):
            if topic_map[tid]["code"] == topic_code:
                start_index = i
                break

        if start_index is None:
            logger.warning(
                "Topic code '%s' not found in curriculum %s/%s/%s — using full sequence.",
                topic_code, organisation, paper, version,
            )
            start_index = 0

        # Build the sequence from the selected topic onwards
        sequence = [
            topic_map[tid] for tid in sorted_ids[start_index:]
        ]

        logger.info(
            "Resolved curriculum sequence for plan %d: %d topics starting from '%s'.",
            study_plan.id, len(sequence), sequence[0]["code"] if sequence else "N/A",
        )
        return sequence

    @staticmethod
    def generate_curriculum_week_plans(
        study_plan: StudyPlan,
    ) -> list[WeekPlan] | None:
        """Generate week plans paced by the official curriculum topic order.

        Each topic is assigned to one or more weeks based on its estimated
        hours and the plan's weekly study minutes.  Topics are paced
        sequentially following the resolved curriculum sequence.

        Args:
            study_plan: A curriculum-backed study plan.

        Returns:
            A list of WeekPlan objects with ``topic_name`` embedded, or
            ``None`` if the curriculum cannot be resolved.
        """
        sequence = PlanningService._resolve_curriculum_sequence(study_plan)
        if sequence is None or not sequence:
            return None

        today = date.today()
        exam_date = study_plan.exam_date

        # Total available study minutes per week
        weekly_minutes = (
            study_plan.weekday_study_minutes * 5
            + study_plan.weekend_study_minutes * 2
        )

        if weekly_minutes <= 0:
            weekly_minutes = 300  # sensible fallback

        # Find the Monday of the current week
        days_since_monday = today.weekday()
        current_week_start = today - timedelta(days=days_since_monday)

        week_plans: list[WeekPlan] = []
        week_number = 1
        topic_index = 0

        while current_week_start < exam_date and topic_index < len(sequence):
            current_week_end = current_week_start + timedelta(days=6)

            # Clamp the end date to the exam date
            if current_week_end >= exam_date:
                current_week_end = exam_date - timedelta(days=1)

            topic_data = sequence[topic_index]
            topic_hours = topic_data["hours"]
            topic_minutes = int(topic_hours * 60)

            # Determine how many weeks this topic should span
            weeks_for_topic = max(
                1, -(-topic_minutes // weekly_minutes)
            )  # ceiling division

            for _ in range(weeks_for_topic):
                if current_week_start >= exam_date:
                    break

                current_week_end = current_week_start + timedelta(days=6)
                if current_week_end >= exam_date:
                    current_week_end = exam_date - timedelta(days=1)

                wp = WeekPlan(
                    study_plan_id=study_plan.id,
                    week_number=week_number,
                    start_date=current_week_start,
                    end_date=current_week_end,
                )
                week_plans.append(wp)

                current_week_start = current_week_end + timedelta(days=1)
                week_number += 1

            topic_index += 1

        # If there are remaining weeks before the exam after all topics
        # have been assigned, fill with revision weeks.
        while current_week_start < exam_date:
            current_week_end = current_week_start + timedelta(days=6)
            if current_week_end >= exam_date:
                current_week_end = exam_date - timedelta(days=1)

            wp = WeekPlan(
                study_plan_id=study_plan.id,
                week_number=week_number,
                start_date=current_week_start,
                end_date=current_week_end,
            )
            week_plans.append(wp)

            current_week_start = current_week_end + timedelta(days=1)
            week_number += 1

        logger.info(
            "Generated %d curriculum-paced week plans for plan %d (%d topics).",
            len(week_plans), study_plan.id, len(sequence),
        )
        return week_plans
