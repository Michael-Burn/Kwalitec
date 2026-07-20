"""DashboardReadModel — aggregate dashboard projection for UI consumption."""

from __future__ import annotations

from dataclasses import dataclass

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


@dataclass(frozen=True, slots=True)
class DashboardReadModel:
    """Closed dashboard presentation artefact for one composition pass.

    Sparse sections are lawful. Fabricated educational certainty is not.
    Never carries domain aggregates.
    """

    student_id: str
    recommendation: RecommendationReadModel | None
    todays_mission: TodaysMissionReadModel | None
    progress: ProgressSummaryReadModel | None
    timeline: TimelineReadModel | None
    warnings: tuple[str, ...] = ()
    empty_states: tuple[str, ...] = ()
    composed_at: str | None = None
