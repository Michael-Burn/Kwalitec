"""Dashboard blueprint routes — optimized for performance."""

from __future__ import annotations

import logging
import time
from datetime import date, datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.application.config import (
    build_twin_provider,
    resolve_feature_flags,
)
from app.application.dashboard import (
    DashboardCompositionContext,
    DashboardViewModel,
    EducationalDashboardComposer,
)
from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.burnout_monitor import BurnoutMonitor
from app.services.curriculum_engine_service import (
    CurriculumEngineService,
    StudentCurriculumSummary,
)
from app.services.educational_kpi_status import EducationalKpiStatusService
from app.services.exam_timeline import ExamTimeline
from app.services.mission_optimizer import MissionOptimizer
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService
from app.services.study_plan_service import StudyPlanService
from app.services.time_engine_service import TimeEngineService

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


def _compose_educational_dashboard(
    user_id: int,
    active_study_plan,
) -> DashboardViewModel | None:
    """Request Twin-first dashboard composition via Application Layer only.

    Presentation owns auth / HTTP. Educational coordination lives in
    EducationalDashboardComposer. Returns None for legacy RecommendationService
    fallback — never invents Mid readiness. Internal Alpha wires the interim
    cold-start TwinSource so the Recommendation card is reachable for daily use.
    """
    flags = resolve_feature_flags()
    curriculum_id = None
    available_minutes = None
    if active_study_plan is not None:
        curriculum_id = getattr(active_study_plan, "curriculum_id", None)
        available_minutes = getattr(
            active_study_plan, "preferred_session_minutes", None
        )
    return EducationalDashboardComposer(
        twin_provider=build_twin_provider(flags=flags),
        flags=flags,
    ).compose(
        DashboardCompositionContext(
            student_id=str(user_id),
            curriculum_id=curriculum_id,
            available_minutes=available_minutes,
        )
    )


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

    # Auto-generate today's mission if needed (idempotent, active-plan scoped)
    if active_study_plan:
        _timed_call(
            "generate_today_mission",
            PlanningService.generate_today_mission,
            user_id,
        )

    from app.services.mission_service import MissionService

    today_mission = _timed_call(
        "today_mission",
        MissionService.get_today_mission,
        user_id,
        None,
        active_study_plan.id if active_study_plan else None,
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

    # Educational Intelligence (Stage A / Internal Alpha) — Application only.
    # Flags default off; missing curriculum / composition → None fallback.
    ei_flags = resolve_feature_flags()
    dashboard_view_model = None
    if ei_flags.ENABLE_EDUCATIONAL_ORCHESTRATOR:
        dashboard_view_model = _timed_call(
            "educational_dashboard",
            _compose_educational_dashboard,
            user_id,
            active_study_plan,
        )

    # Legacy recommendations remain default authority and silent fallback when
    # EI cannot produce a truthful Experience. When the EI card is present,
    # legacy recommendation lists stay out of the template (invisible dual path).
    ei_recommendation_active = bool(
        dashboard_view_model is not None
        and dashboard_view_model.recommendation_card is not None
    )
    today_recommendation = None
    all_recommendations = None
    if not ei_recommendation_active:
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

    # Time status via TimeEngineService (single source for hours balance)
    time_summary = None
    if active_study_plan:
        time_summary = _timed_call(
            "time_summary",
            TimeEngineService.calculate_time_summary,
            active_study_plan,
        )

    # Schedule/pace KPI status — same EducationalKpiStatusService as Exam card
    schedule_kpi_status = None
    days_for_status = None
    if exam_timeline is not None:
        days_for_status = exam_timeline["days_remaining"]
    elif (
        active_study_plan is not None
        and getattr(active_study_plan, "exam_date", None)
    ):
        exam_dt = active_study_plan.exam_date
        if isinstance(exam_dt, datetime):
            exam_dt = exam_dt.date()
        days_for_status = (exam_dt - date.today()).days

    if time_summary is not None and days_for_status is not None:
        coverage_pct = None
        if exam_timeline is not None:
            coverage_pct = exam_timeline.get("curriculum_coverage_pct")
        schedule_kpi_status = EducationalKpiStatusService.from_time_summary(
            time_summary,
            days_for_status,
            coverage_pct=coverage_pct,
        )
    elif days_for_status is not None:
        schedule_kpi_status = EducationalKpiStatusService.from_days_remaining(
            days_for_status
        )

    from app.services.study_tips_service import StudyTipsService
    from app.services.welcome_service import WelcomeService

    study_tip = StudyTipsService.tip_for_day()
    show_welcome = WelcomeService.should_show(current_user)

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
        dashboard_view_model=dashboard_view_model,
        balanced_mission=balanced_mission,
        exam_timeline=exam_timeline,
        burnout_status=burnout_status or {},
        decision_journal=decision_journal or [],
        decision_summary=decision_summary or {},
        curriculum_summary=curriculum_summary,
        readiness_summary=readiness_summary,
        time_summary=time_summary,
        schedule_kpi_status=schedule_kpi_status,
        study_tip=study_tip,
        show_welcome=show_welcome,
    )


@dashboard_bp.post("/welcome/dismiss")
@login_required
def dismiss_welcome():
    """Permanently dismiss the first-time welcome modal."""
    from app.services.welcome_service import WelcomeService

    WelcomeService.dismiss(current_user.id)
    next_url = request.form.get("next") or url_for("dashboard.index")
    # Only allow local relative redirects
    if not next_url.startswith("/"):
        next_url = url_for("dashboard.index")
    return redirect(next_url)
