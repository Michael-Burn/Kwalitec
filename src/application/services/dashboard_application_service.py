"""DashboardApplicationService — project DTOs into dashboard read models.

Presentation composition only. Does not diagnose, select strategies, persist
state, or load aggregates directly. Sparse sections are lawful.
"""

from __future__ import annotations

from application.dto.teaching_plan import TeachingPlanDTO
from application.errors import ApplicationError, NotFoundError
from application.ports.clock import Clock
from application.queries.get_dashboard import GetDashboard
from application.queries.get_learner_state import GetLearnerState
from application.queries.get_learning_trajectory import GetLearningTrajectory
from application.queries.get_progress_summary import GetProgressSummary
from application.queries.get_recommendations import GetRecommendations
from application.queries.get_teaching_plan import GetTeachingPlan
from application.queries.get_timeline import GetTimeline
from application.queries.get_todays_mission import GetTodaysMission
from application.read_models.dashboard.dashboard_read_model import DashboardReadModel
from application.read_models.dashboard.projection_builder import (
    DashboardProjectionBuilder,
)
from application.read_models.progress.progress_summary_read_model import (
    ProgressSummaryReadModel,
)
from application.read_models.progress.projection_builder import (
    ProgressSummaryProjectionBuilder,
)
from application.read_models.recommendations.projection_builder import (
    RecommendationProjectionBuilder,
)
from application.read_models.recommendations.recommendation_read_model import (
    RecommendationReadModel,
)
from application.read_models.timeline.projection_builder import (
    TimelineProjectionBuilder,
)
from application.read_models.timeline.timeline_read_model import TimelineReadModel
from application.read_models.today.projection_builder import (
    TodaysMissionProjectionBuilder,
)
from application.read_models.today.todays_mission_read_model import (
    TodaysMissionReadModel,
)
from application.services.planning_application_service import PlanningApplicationService
from application.services.twin_application_service import TwinApplicationService


class DashboardApplicationService:
    """Compose immutable dashboard read models from application query DTOs."""

    def __init__(
        self,
        twin: TwinApplicationService,
        planning: PlanningApplicationService,
        clock: Clock,
    ) -> None:
        self._twin = twin
        self._planning = planning
        self._clock = clock

    def get_dashboard(self, query: GetDashboard) -> DashboardReadModel:
        """Compose section projections into one dashboard read model."""
        student_id = _require_student_id(query.student_id)
        empty_states: list[str] = []

        progress = self._optional_progress(student_id, empty_states)
        timeline = self._optional_timeline(student_id, empty_states)
        todays_mission = None
        recommendation = None
        if query.episode_id:
            episode_id = query.episode_id.strip()
            if episode_id:
                todays_mission = self._optional_mission(
                    student_id,
                    episode_id,
                    empty_states,
                )
                recommendation = self._optional_recommendation(
                    student_id,
                    episode_id,
                    empty_states,
                )
        else:
            empty_states.append("no_mission")
            empty_states.append("no_recommendation")

        return DashboardProjectionBuilder.build(
            student_id=student_id,
            recommendation=recommendation,
            todays_mission=todays_mission,
            progress=progress,
            timeline=timeline,
            empty_states=tuple(empty_states),
            composed_at=self._clock.now().isoformat(),
        )

    def get_todays_mission(self, query: GetTodaysMission) -> TodaysMissionReadModel:
        """Project a teaching-plan DTO into today's mission read model."""
        student_id = _require_student_id(query.student_id)
        episode_id = _require_episode_id(query.episode_id)
        plan = self._load_owned_plan(student_id=student_id, episode_id=episode_id)
        return TodaysMissionProjectionBuilder.from_teaching_plan(plan)

    def get_progress(self, query: GetProgressSummary) -> ProgressSummaryReadModel:
        """Project learner state into a progress summary read model."""
        student_id = _require_student_id(query.student_id)
        state = self._twin.get_learner_state(GetLearnerState(student_id=student_id))
        return ProgressSummaryProjectionBuilder.build(state)

    def get_recommendations(
        self, query: GetRecommendations
    ) -> RecommendationReadModel | None:
        """Project already-authored plan packaging into a recommendation card.

        Returns ``None`` when no episode packaging is available. Does not select
        or score educational actions.
        """
        student_id = _require_student_id(query.student_id)
        if not query.episode_id or not query.episode_id.strip():
            return None
        plan = self._load_owned_plan(
            student_id=student_id,
            episode_id=query.episode_id.strip(),
        )
        return _recommendation_from_plan(plan)

    def get_timeline(self, query: GetTimeline) -> TimelineReadModel:
        """Project learning trajectory into a timeline read model."""
        student_id = _require_student_id(query.student_id)
        trajectory = self._twin.get_learning_trajectory(
            GetLearningTrajectory(student_id=student_id)
        )
        return TimelineProjectionBuilder.from_trajectory(trajectory)

    def _load_owned_plan(
        self, *, student_id: str, episode_id: str
    ) -> TeachingPlanDTO:
        plan = self._planning.get_teaching_plan(GetTeachingPlan(episode_id=episode_id))
        if plan.student_id != student_id:
            raise NotFoundError("LearningEpisode", episode_id)
        return plan

    def _optional_progress(
        self, student_id: str, empty_states: list[str]
    ) -> ProgressSummaryReadModel | None:
        try:
            return self.get_progress(GetProgressSummary(student_id=student_id))
        except NotFoundError:
            empty_states.append("no_progress")
            return None

    def _optional_timeline(
        self, student_id: str, empty_states: list[str]
    ) -> TimelineReadModel | None:
        try:
            return self.get_timeline(GetTimeline(student_id=student_id))
        except NotFoundError:
            empty_states.append("no_timeline")
            return None

    def _optional_mission(
        self,
        student_id: str,
        episode_id: str,
        empty_states: list[str],
    ) -> TodaysMissionReadModel | None:
        try:
            return self.get_todays_mission(
                GetTodaysMission(student_id=student_id, episode_id=episode_id)
            )
        except NotFoundError:
            empty_states.append("no_mission")
            return None

    def _optional_recommendation(
        self,
        student_id: str,
        episode_id: str,
        empty_states: list[str],
    ) -> RecommendationReadModel | None:
        try:
            recommendation = self.get_recommendations(
                GetRecommendations(student_id=student_id, episode_id=episode_id)
            )
        except NotFoundError:
            empty_states.append("no_recommendation")
            return None
        if recommendation is None:
            empty_states.append("no_recommendation")
        return recommendation


def _recommendation_from_plan(plan: TeachingPlanDTO) -> RecommendationReadModel:
    """Forward already-authored plan fields into recommendation packaging."""
    can_start = plan.status in {"planned", "in_progress"}
    if plan.status == "in_progress":
        primary_action = "Continue Session"
    else:
        primary_action = "Start Session"
    return RecommendationProjectionBuilder.build(
        title="Continue studying",
        subtitle=plan.teaching_goal_statement,
        primary_action=primary_action if can_start else None,
        reason_summary=None,
        estimated_minutes=None,
        can_start=can_start,
        recommendation_id=plan.plan_id,
    )


def _require_student_id(student_id: str) -> str:
    cleaned = (student_id or "").strip()
    if not cleaned:
        raise ApplicationError("student_id is required")
    return cleaned


def _require_episode_id(episode_id: str) -> str:
    cleaned = (episode_id or "").strip()
    if not cleaned:
        raise ApplicationError("episode_id is required")
    return cleaned
