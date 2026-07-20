"""DashboardProjectionBuilder — compose section read models into one dashboard.

Aggregates presentation projections only. Does not run educational reasoning,
persist state, or modify aggregates.
"""

from __future__ import annotations

from application.read_models.dashboard.dashboard_read_model import DashboardReadModel
from application.read_models.progress.progress_summary_read_model import (
    ProgressSummaryReadModel,
)
from application.read_models.recommendations.recommendation_read_model import (
    RecommendationReadModel,
)
from application.read_models.timeline.timeline_read_model import TimelineReadModel
from application.read_models.today.todays_mission_read_model import (
    TodaysMissionReadModel,
)


class DashboardProjectionBuilder:
    """Compose section read models into an immutable ``DashboardReadModel``."""

    @staticmethod
    def build(
        *,
        student_id: str,
        recommendation: RecommendationReadModel | None = None,
        todays_mission: TodaysMissionReadModel | None = None,
        progress: ProgressSummaryReadModel | None = None,
        timeline: TimelineReadModel | None = None,
        warnings: tuple[str, ...] = (),
        empty_states: tuple[str, ...] = (),
        composed_at: str | None = None,
    ) -> DashboardReadModel:
        """Aggregate presentation sections into one dashboard read model."""
        return DashboardReadModel(
            student_id=student_id.strip(),
            recommendation=recommendation,
            todays_mission=todays_mission,
            progress=progress,
            timeline=timeline,
            warnings=tuple(warnings),
            empty_states=tuple(empty_states),
            composed_at=composed_at,
        )
