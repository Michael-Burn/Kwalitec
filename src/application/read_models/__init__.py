"""Application read models — presentation projections for dashboard surfaces.

Educational Operating System
        ↓
Application Services
        ↓
Projection Builders
        ↓
Read Models
        ↓
Dashboard JSON

Read models are immutable, presentation-optimized, and never modify aggregates.
They contain no educational reasoning, persistence, or business rules.
"""

from __future__ import annotations

from application.read_models.dashboard import (
    DashboardProjectionBuilder,
    DashboardReadModel,
)
from application.read_models.missions import (
    MissionProjectionBuilder,
    MissionTaskReadModel,
)
from application.read_models.progress import (
    ProgressSummaryProjectionBuilder,
    ProgressSummaryReadModel,
)
from application.read_models.recommendations import (
    RecommendationProjectionBuilder,
    RecommendationReadModel,
)
from application.read_models.serialization import to_dashboard_json
from application.read_models.timeline import (
    TimelineEventReadModel,
    TimelineProjectionBuilder,
    TimelineReadModel,
)
from application.read_models.today import (
    TodaysMissionProjectionBuilder,
    TodaysMissionReadModel,
)

__all__ = [
    "DashboardProjectionBuilder",
    "DashboardReadModel",
    "MissionProjectionBuilder",
    "MissionTaskReadModel",
    "ProgressSummaryProjectionBuilder",
    "ProgressSummaryReadModel",
    "RecommendationProjectionBuilder",
    "RecommendationReadModel",
    "TimelineEventReadModel",
    "TimelineProjectionBuilder",
    "TimelineReadModel",
    "TodaysMissionProjectionBuilder",
    "TodaysMissionReadModel",
    "to_dashboard_json",
]
