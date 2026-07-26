"""Analytics blueprint routes."""

from __future__ import annotations

import json

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.presentation.intelligence_surface import RuntimeAPresentationAdapter
from app.services.analytics_service import AnalyticsService
from app.services.readiness_service import ReadinessService

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.get("/")
@login_required
def index():
    """Render the analytics dashboard with charts and performance data.

    READY FOR MIGRATION: under sole runtime, learners use Student Analytics.
    """
    from app.presentation.consolidation import redirect_if_sole_runtime

    sole = redirect_if_sole_runtime("student.history")
    if sole is not None:
        return sole

    user_id = current_user.id

    # Readiness (EP-002.6 gated cutover — legacy fail-open)
    readiness_surface = ReadinessService.get_dashboard_readiness_surface(
        user_id, weak_limit=5, strong_limit=5
    )
    readiness = readiness_surface.get("readiness") or {}
    # EP-002.8: unified presentation selection by source_authority
    weakest_topics, strongest_topics = RuntimeAPresentationAdapter.topic_rows(
        readiness_surface
    )
    readiness_narrative = RuntimeAPresentationAdapter.readiness_narrative(
        readiness_surface
    )
    curriculum_coverage = ReadinessService.get_curriculum_coverage(user_id)
    review_backlog = ReadinessService.get_review_backlog(user_id)
    review_completion = ReadinessService.get_review_completion_rate(user_id)
    current_streak = ReadinessService.get_current_streak(user_id)
    longest_streak = ReadinessService.get_longest_streak(user_id)

    # Time-series analytics
    readiness_trend = AnalyticsService.get_readiness_over_time(user_id, weeks=12)
    mastery_trend = AnalyticsService.get_mastery_over_time(user_id, weeks=12)
    accuracy_trend = AnalyticsService.get_accuracy_trend(user_id, weeks=12)
    weekly_hours = AnalyticsService.get_weekly_study_hours(user_id, weeks=12)
    mission_trend = AnalyticsService.get_mission_completion_trend(user_id, weeks=12)
    review_trend = AnalyticsService.get_review_completion_trend(user_id, weeks=12)
    lifetime = AnalyticsService.get_lifetime_summary(user_id)

    # Weekly report
    weekly_report = AnalyticsService.generate_weekly_report(user_id)

    # Serialize for JavaScript charts
    chart_data = {
        "readiness": readiness_trend,
        "mastery": mastery_trend,
        "accuracy": accuracy_trend,
        "weeklyHours": weekly_hours,
        "missionCompletion": mission_trend,
        "reviewCompletion": review_trend,
    }

    return render_template(
        "analytics/index.html",
        title="Analytics",
        readiness=readiness,
        readiness_narrative=readiness_narrative,
        curriculum_coverage=curriculum_coverage,
        review_backlog=review_backlog,
        review_completion=review_completion,
        current_streak=current_streak,
        longest_streak=longest_streak,
        weakest_topics=weakest_topics,
        strongest_topics=strongest_topics,
        chart_data=json.dumps(chart_data),
        lifetime=lifetime,
        weekly_report=weekly_report,
    )
