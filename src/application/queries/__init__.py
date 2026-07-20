"""Application queries — read-side intents."""

from __future__ import annotations

from application.queries.get_dashboard import GetDashboard
from application.queries.get_evidence_history import GetEvidenceHistory
from application.queries.get_learner_state import GetLearnerState
from application.queries.get_learning_trajectory import GetLearningTrajectory
from application.queries.get_progress_summary import GetProgressSummary
from application.queries.get_recommendations import GetRecommendations
from application.queries.get_teaching_plan import GetTeachingPlan
from application.queries.get_timeline import GetTimeline
from application.queries.get_todays_mission import GetTodaysMission

__all__ = [
    "GetDashboard",
    "GetEvidenceHistory",
    "GetLearnerState",
    "GetLearningTrajectory",
    "GetProgressSummary",
    "GetRecommendations",
    "GetTeachingPlan",
    "GetTimeline",
    "GetTodaysMission",
]
