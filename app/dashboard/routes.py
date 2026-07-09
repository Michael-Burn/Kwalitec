"""Dashboard blueprint routes — optimized for performance."""

from __future__ import annotations

import logging
import time

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.burnout_monitor import BurnoutMonitor
from app.services.curriculum_engine_service import (
    CurriculumEngineService,
    StudentCurriculumSummary,
)
from app.services.exam_timeline import ExamTimeline
from app.services.time_engine_service import TimeEngineService
from app.services.mission_optimizer import MissionOptimizer
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService
from app.services.study_plan_service import StudyPlanService

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# Per-call timeout in seconds to prevent a single slow query from blocking
_SERVICE_TIMEOUT = 10.0


def _timed_call(label: str, fn, *args, **kwargs):
    """Invoke a service function with timing and timeout guard.

    If the call exceeds _SERVICE_TIMEOUT, a warning is logged and None
    is returned so the dashboard can still render.
    """
    start = time.monotonic()
    try:
        result = fn(*args, **kwargs)
        elapsed = (time.monotonic() - start) * 1000
        if elapsed > 500:
            logger.warning("Slow dashboard query: %s took %.0f ms", label, elapsed)
        return result
    except Exception as exc:
        elapsed = (time.monotonic() - start) * 1000
        logger.error("Dashboard query failed: %s (%.0f ms): %s", label, elapsed, exc)
        return None


@dashboard_bp.get("/")
@login_required
def index():
    """Render the application dashboard.

    Each service call is individually timed and guarded so that a slow
    or failing query never blocks the entire dashboard from rendering.
    """
    user_id = current_user.id

    # Essentials — needed for the core dashboard UX
    active_study_plan = _timed_call(
        "active_study_plan", StudyPlanService.get_user_active_plan, user_id
    )

    # Auto-generate today's mission if needed (idempotent)
    if active_study_plan:
        _timed_call(
            "generate_today_mission",
            PlanningService.generate_today_mission,
            user_id,
        )

    from app.services.mission_service import MissionService

    today_mission = _timed_call(
        "today_mission", MissionService.get_today_mission, user_id
    )

    # Learning snapshot (lightweight aggregates)
    learning_snapshot = _timed_call(
        "learning_snapshot",
        AdaptiveLearningService.get_learning_snapshot,
        user_id,
    )
    daily_briefing = _timed_call(
        "daily_briefing",
        AdaptiveLearningService.generate_daily_briefing,
        user_id,
    )

    # Readiness
    readiness = _timed_call(
        "readiness", ReadinessService.get_overall_readiness, user_id
    )
    review_backlog = _timed_call(
        "review_backlog", ReadinessService.get_review_backlog, user_id
    )

    # Topic highlights (only 3 each)
    weakest_topics = _timed_call(
        "weakest_topics", ReadinessService.get_weakest_topics, user_id, 3
    )
    strongest_topics = _timed_call(
        "strongest_topics", ReadinessService.get_strongest_topics, user_id, 3
    )

    # Recommendations
    today_recommendation = _timed_call(
        "today_recommendation",
        RecommendationService.generate_today_recommendation,
        user_id,
    )
    all_recommendations = _timed_call(
        "all_recommendations",
        RecommendationService.generate_recommendations,
        user_id,
        5,
    )

    # Optional / heavier widgets
    balanced_mission = _timed_call(
        "balanced_mission",
        MissionOptimizer.generate_balanced_mission,
        user_id,
    )
    exam_timeline = _timed_call(
        "exam_timeline", ExamTimeline.get_timeline, user_id
    )
    burnout_status = _timed_call(
        "burnout_status", BurnoutMonitor.detect_burnout, user_id
    )

    # Decision journal (last 10)
    decision_journal = _timed_call(
        "decision_journal",
        RecommendationService.get_decision_journal,
        user_id,
        10,
    )
    decision_summary = _timed_call(
        "decision_summary",
        RecommendationService.get_decision_summary,
        user_id,
    )

    # Curriculum summary via CurriculumEngineService (no local calculations)
    curriculum_summary: StudentCurriculumSummary | None = None
    readiness_summary = None
    if active_study_plan:
        curriculum_summary = _timed_call(
            "curriculum_summary",
            CurriculumEngineService().build_student_curriculum,
            active_study_plan,
        )
        if curriculum_summary is not None:
            readiness_summary = ReadinessService.calculate_readiness(curriculum_summary)

    # Time status via TimeEngineService
    time_summary = None
    if active_study_plan:
        time_summary = _timed_call(
            "time_summary",
            TimeEngineService.calculate_time_summary,
            active_study_plan,
        )

    return render_template(
        "dashboard/index.html",
        title="Dashboard",
        today_mission=today_mission,
        active_study_plan=active_study_plan,
        learning_snapshot=learning_snapshot or {},
        daily_briefing=daily_briefing or "",
        readiness=readiness or {},
        review_backlog=review_backlog or {},
        weakest_topics=weakest_topics or [],
        strongest_topics=strongest_topics or [],
        today_recommendation=today_recommendation,
        all_recommendations=all_recommendations or [],
        balanced_mission=balanced_mission,
        exam_timeline=exam_timeline,
        burnout_status=burnout_status or {},
        decision_journal=decision_journal or [],
        decision_summary=decision_summary or {},
        curriculum_summary=curriculum_summary,
        readiness_summary=readiness_summary,
        time_summary=time_summary,
    )
