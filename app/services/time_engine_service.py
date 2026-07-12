"""Time Engine Service — calculates remaining study workload for
curriculum-backed study plans.

All calculations are deterministic.  No AI, heuristics, or external APIs
are used.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from app.extensions import db
from app.models.topic_progress import TopicProgress


@dataclass(frozen=True)
class TimeSummary:
    """Immutable summary of study-time metrics for a curriculum-backed
    study plan.

    Attributes:
        total_curriculum_hours: Total estimated hours from the official
            curriculum.
        completed_hours: Sum of ``estimated_hours`` for completed topics.
        remaining_hours: ``total_curriculum_hours`` minus ``completed_hours``.
        available_study_hours: Remaining days until the exam multiplied by
            planned daily minutes, converted to hours.
        hours_surplus_or_deficit: ``available_study_hours`` minus
            ``remaining_hours``.  Positive = surplus, negative = deficit.
    """

    total_curriculum_hours: float
    completed_hours: float
    remaining_hours: float
    available_study_hours: float
    hours_surplus_or_deficit: float


class TimeEngineService:
    """Service for calculating study-time workload and availability.

    Every public method is a ``@staticmethod`` so the class is stateless.
    All calculations are deterministic.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @staticmethod
    def calculate_time_summary(study_plan: object) -> TimeSummary | None:
        """Calculate a time summary for a curriculum-backed study plan.

        Args:
            study_plan: A ``StudyPlan`` ORM instance.

        Returns:
            A frozen ``TimeSummary``, or ``None`` if the study plan has
            no curriculum backing (missing ``curriculum_id`` or
            ``curriculum_version``, or the curriculum cannot be loaded).
        """
        # ── Guard: no curriculum backing ──────────────────────────
        if not study_plan.curriculum_id or not study_plan.curriculum_version:
            return None

        # ── Parse exam name → (org, paper) ───────────────────────
        from app.services.examination_catalogue import parse_exam_name

        org, paper = parse_exam_name(study_plan.exam_name)
        if not org or not paper:
            return None

        version: str = study_plan.curriculum_version

        # ── Load the engine curriculum ───────────────────────────
        from app.curriculum.repository import CurriculumRepository
        from app.services.curriculum_engine_service import CurriculumEngineService

        repo = CurriculumRepository()
        try:
            engine_curriculum = repo.load_auto(org.lower(), paper.lower(), version)
        except Exception:
            return None

        # ── Map engine topics → DB topics (matched by name/title) ─
        from app.models.curriculum import Topic as DBTopic

        db_topics = DBTopic.query.filter_by(
            curriculum_id=study_plan.curriculum_id,
        ).all()

        engine_topics = CurriculumEngineService.get_topics_flat(engine_curriculum)

        code_to_db_topic: dict[str, DBTopic] = {}
        for engine_topic in engine_topics:
            for db_topic in db_topics:
                if db_topic.name == engine_topic.title:
                    code_to_db_topic[engine_topic.code] = db_topic
                    break

        if not code_to_db_topic:
            return None

        # ── Look up TopicProgress for every mapped DB topic ─────
        db_topic_ids = [t.id for t in code_to_db_topic.values()]
        progress_rows = TopicProgress.query.filter(
            TopicProgress.user_id == study_plan.user_id,
            TopicProgress.topic_id.in_(db_topic_ids),
        ).all()

        topic_id_to_completed: dict[int, bool] = {
            tp.topic_id: tp.completed for tp in progress_rows
        }

        # ── Accumulate hours from the flat canonical topic list ─
        total_curriculum_hours: float = 0.0
        completed_hours: float = 0.0

        for engine_topic in engine_topics:
            if hasattr(engine_topic, "estimated_hours"):
                hours = float(engine_topic.estimated_hours)
            else:
                hours = float(getattr(engine_topic, "estimated_minutes", 0)) / 60.0

            total_curriculum_hours += hours

            db_topic = code_to_db_topic.get(engine_topic.code)
            if db_topic is not None and topic_id_to_completed.get(
                db_topic.id, False
            ):
                completed_hours += hours

        remaining_hours = total_curriculum_hours - completed_hours

        # ── Available study hours ────────────────────────────────
        today = date.today()
        exam_date = study_plan.exam_date
        if isinstance(exam_date, datetime):
            exam_date = exam_date.date()

        remaining_days = max(0, (exam_date - today).days)

        # Weighted average daily minutes (5 weekdays + 2 weekend days)
        weekday = study_plan.weekday_study_minutes
        weekend = study_plan.weekend_study_minutes
        planned_daily_minutes = (weekday * 5 + weekend * 2) / 7.0

        available_study_hours = (remaining_days * planned_daily_minutes) / 60.0

        # ── Surplus / deficit ────────────────────────────────────
        hours_surplus_or_deficit = available_study_hours - remaining_hours

        return TimeSummary(
            total_curriculum_hours=round(total_curriculum_hours, 2),
            completed_hours=round(completed_hours, 2),
            remaining_hours=round(remaining_hours, 2),
            available_study_hours=round(available_study_hours, 2),
            hours_surplus_or_deficit=round(hours_surplus_or_deficit, 2),
        )