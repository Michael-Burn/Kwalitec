"""Analytics blueprint routes."""

from __future__ import annotations

import json

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.services.analytics_service import AnalyticsService
from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)
from app.services.readiness_service import ReadinessService

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.get("/")
@login_required
def index():
    """Render the analytics dashboard with charts and performance data."""
    user_id = current_user.id

    # Readiness
    readiness = ReadinessService.get_overall_readiness(user_id)
    readiness_narrative = EducationalExplainabilityService.explain_composite_readiness(
        readiness
    )
    curriculum_coverage = ReadinessService.get_curriculum_coverage(user_id)
    review_backlog = ReadinessService.get_review_backlog(user_id)
    review_completion = ReadinessService.get_review_completion_rate(user_id)
    current_streak = ReadinessService.get_current_streak(user_id)
    longest_streak = ReadinessService.get_longest_streak(user_id)
    weakest_topics = EducationalExplainabilityService.enrich_topic_rows(
        ReadinessService.get_weakest_topics(user_id, limit=5)
    )
    strongest_topics = EducationalExplainabilityService.enrich_topic_rows(
        ReadinessService.get_strongest_topics(user_id, limit=5)
    )

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
