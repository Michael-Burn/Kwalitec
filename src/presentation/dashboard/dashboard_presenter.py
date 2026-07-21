"""DashboardPresenter — assemble Student Dashboard 2.0 view model.

Presentation orchestration only. Assembles Design System chrome around
already-decided Educational OS outputs. Never diagnoses, recommends, persists,
orchestrates learning, or calls AI.
"""

from __future__ import annotations

from typing import Any

from presentation.dashboard.achievement_mapper import AchievementMapper
from presentation.dashboard.dashboard_mapper import DashboardMapper
from presentation.dashboard.dashboard_view_model import DashboardViewModel
from presentation.dashboard.mission_card_mapper import MissionCardMapper
from presentation.dashboard.progress_mapper import ProgressMapper
from presentation.dashboard.statistics_mapper import StatisticsMapper
from presentation.design_system import ContainerWidth
from presentation.mission_workspace.workspace_presenter import WorkspacePresenter
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)


class DashboardPresenter:
    """Present the student command centre from Educational OS display inputs."""

    @classmethod
    def present(
        cls,
        result: Any = None,
        workspace: MissionWorkspaceViewModel | None = None,
        *,
        twin: Any = None,
        evidence_history: Any = None,
        statistics: Any = None,
        achievements: Any = None,
    ) -> DashboardViewModel:
        """Map dashboard inputs into an immutable ``DashboardViewModel``.

        Args:
            result: Optional ``PipelineResult`` (structural duck-typing accepted).
            workspace: Optional ``MissionWorkspaceViewModel``. When omitted and
                ``result`` is provided, a workspace is derived via
                ``WorkspacePresenter``.
            twin: Optional StudentTwin / digital-twin display projection.
            evidence_history: Optional evidence history projection.
            statistics: Optional StudyStatistics display projection.
            achievements: Optional achievements collection; falls back to
                ``result.student_experience.achievements`` when omitted.

        Returns:
            Immutable ``DashboardViewModel`` with null-safe Design System chrome.
        """
        resolved = cls._resolve_workspace(result=result, workspace=workspace)

        greeting_text, greeting = DashboardMapper.map_greeting(
            resolved,
            result=result,
            twin=twin,
        )
        mission_card = MissionCardMapper.map_mission_card(resolved, result=result)
        mission_reason = MissionCardMapper.map_mission_reason(resolved, result=result)
        primary_action = DashboardMapper.map_primary_action(resolved)
        progress_summary = ProgressMapper.map_progress_card(
            resolved,
            statistics=statistics,
        )
        progress_bar = ProgressMapper.map_progress_bar(
            resolved,
            statistics=statistics,
        )
        learning_statistics = StatisticsMapper.map_learning_statistics(
            statistics=statistics,
            twin=twin,
            evidence_history=evidence_history,
            workspace=resolved,
            result=result,
        )
        current_streak = StatisticsMapper.map_streak(
            statistics=statistics,
            result=result,
            twin=twin,
        )
        achievement_views = AchievementMapper.map_achievements(
            achievements,
            result=result,
        )
        upcoming_sessions = DashboardMapper.map_upcoming_sessions(
            result=result,
            statistics=statistics,
        )
        quick_actions = DashboardMapper.map_quick_actions(resolved, result=result)
        header = DashboardMapper.map_header(
            greeting=greeting_text,
            mission_title=mission_card.title,
        )

        return DashboardViewModel(
            header=header,
            greeting=greeting,
            mission_card=mission_card,
            mission_reason=mission_reason,
            primary_action=primary_action,
            progress_summary=progress_summary,
            progress_bar=progress_bar,
            learning_statistics=learning_statistics,
            current_streak=current_streak,
            achievements=achievement_views,
            upcoming_sessions=upcoming_sessions,
            quick_actions=quick_actions,
            container_width=ContainerWidth.WIDE,
            greeting_text=greeting_text,
        )

    @classmethod
    def _resolve_workspace(
        cls,
        *,
        result: Any,
        workspace: MissionWorkspaceViewModel | None,
    ) -> MissionWorkspaceViewModel:
        if workspace is not None:
            return workspace
        return WorkspacePresenter.present(result)
