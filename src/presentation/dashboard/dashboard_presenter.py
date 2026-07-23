"""DashboardPresenter — assemble Student Dashboard decision surface (PX-003).

Presentation orchestration only. Assembles Design System chrome around
already-decided Educational OS outputs and optional XP snapshots. Never
diagnoses, recommends, persists, orchestrates learning, or calls AI.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from presentation.dashboard.achievement_mapper import AchievementMapper
from presentation.dashboard.dashboard_mapper import DashboardMapper
from presentation.dashboard.dashboard_view_model import (
    CoachInsightView,
    DashboardViewModel,
    JourneyStoryView,
    MilestoneView,
    MissionHeroView,
    ReadinessSummaryView,
    StreakView,
)
from presentation.dashboard.mission_card_mapper import MissionCardMapper
from presentation.dashboard.progress_mapper import ProgressMapper
from presentation.dashboard.statistics_mapper import StatisticsMapper
from presentation.dashboard.xp_mapper import XpProjectionMapper
from presentation.design_system import Card, CardVariant, ContainerWidth
from presentation.mission_workspace.workspace_presenter import WorkspacePresenter
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)
from presentation.provenance import ProvenanceMapper


class DashboardPresenter:
    """Present the student decision screen from Educational OS / XP inputs."""

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
        experience: Any = None,
    ) -> DashboardViewModel:
        """Map dashboard inputs into an immutable ``DashboardViewModel``.

        Args:
            result: Optional ``PipelineResult`` (structural duck-typing accepted).
            workspace: Optional ``MissionWorkspaceViewModel``. When omitted and
                ``result`` is provided, a workspace is derived via
                ``WorkspacePresenter``.
            twin: Optional StudentTwin / digital-twin display projection.
            evidence_history: Optional evidence history projection.
            statistics: Optional StudyStatistics display projection (not shown
                as a metric grid on the decision screen).
            achievements: Optional achievements collection; kept for
                compatibility but not rendered as a primary dashboard band.
            experience: Optional XP journey / snapshot bundle (preferred when
                present — reuses already-composed XP projections).

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
        action_key = DashboardMapper.primary_action_key(resolved)
        progress_summary = ProgressMapper.map_progress_card(
            resolved,
            statistics=statistics,
        )
        progress_bar = ProgressMapper.map_progress_bar(
            resolved,
            statistics=statistics,
        )
        # Streak remains available for journey fallback / compatibility.
        # Learning statistics are intentionally not mapped onto the decision
        # screen (no metric grids).
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
        pipeline_quick_actions = DashboardMapper.map_quick_actions(
            resolved, result=result
        )

        if XpProjectionMapper.has_experience_cargo(experience):
            hero = XpProjectionMapper.map_hero(
                experience,
                fallback_greeting=greeting_text,
                fallback_mission=mission_card,
                fallback_cta_label=primary_action.label,
                fallback_action_key=action_key,
            )
            readiness = XpProjectionMapper.map_readiness(experience)
            journey = XpProjectionMapper.map_journey(experience)
            coach = XpProjectionMapper.map_coach(experience)
            milestones = XpProjectionMapper.map_milestones(experience)
            quick_actions = XpProjectionMapper.map_quick_actions(
                experience,
                fallback=pipeline_quick_actions,
            )
        else:
            hero = cls._hero_from_pipeline(
                greeting_text=greeting_text,
                mission_card=mission_card,
                mission_reason=mission_reason,
                primary_action=primary_action,
                action_key=action_key,
            )
            readiness = cls._readiness_from_pipeline(
                progress_summary=progress_summary,
                current_streak=current_streak,
                twin=twin,
                result=result,
            )
            journey = cls._journey_from_pipeline(
                progress_summary=progress_summary,
                current_streak=current_streak,
                result=result,
            )
            coach = cls._coach_from_pipeline(
                mission_reason=mission_reason,
                result=result,
            )
            milestones = cls._milestones_from_sessions(upcoming_sessions)
            quick_actions = pipeline_quick_actions

        header = DashboardMapper.map_header(
            greeting=hero.greeting,
            mission_title=hero.mission_title,
        )

        # RR-001: attach presentation-only provenance from existing evidence.
        hero = replace(
            hero,
            provenance=ProvenanceMapper.for_dashboard_hero(
                workspace=resolved,
                result=result,
                experience=experience,
                hero=hero,
            ),
        )
        readiness = replace(
            readiness,
            provenance=ProvenanceMapper.for_readiness(
                experience, result=result
            ),
        )
        journey = replace(
            journey,
            provenance=ProvenanceMapper.for_journey(experience, result=result),
        )
        coach = replace(
            coach,
            provenance=ProvenanceMapper.for_coach(experience, result=result),
        )
        revision_provenance = ProvenanceMapper.for_revision(
            experience=experience, result=result
        )

        return DashboardViewModel(
            header=header,
            hero=hero,
            readiness=readiness,
            journey=journey,
            coach=coach,
            upcoming_milestones=milestones,
            quick_actions=quick_actions,
            container_width=ContainerWidth.WIDE,
            greeting=greeting,
            greeting_text=hero.greeting or greeting_text,
            mission_card=hero.mission_card or mission_card,
            mission_reason=mission_reason,
            primary_action=hero.primary_action or primary_action,
            progress_summary=progress_summary,
            progress_bar=progress_bar,
            learning_statistics=(),  # decision screen — no metric grids
            current_streak=current_streak,
            achievements=achievement_views,
            upcoming_sessions=upcoming_sessions,
            revision_provenance=revision_provenance,
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

    @classmethod
    def _hero_from_pipeline(
        cls,
        *,
        greeting_text: str,
        mission_card: Any,
        mission_reason: Any,
        primary_action: Any,
        action_key: str,
    ) -> MissionHeroView:
        purpose = _text(mission_card.body) or _text(mission_reason.body)
        return MissionHeroView(
            greeting=greeting_text,
            mission_title=_text(mission_card.title, fallback="Today's Mission"),
            duration_label=_text(
                mission_card.duration_label, fallback="Duration not available"
            ),
            purpose=purpose or "Your mission purpose will appear when available.",
            cta_label=_text(primary_action.label, fallback="Continue"),
            action_key=action_key or "begin_session",
            status_label=_text(mission_card.status_label),
            mission_card=mission_card,
            primary_action=primary_action,
        )

    @classmethod
    def _readiness_from_pipeline(
        cls,
        *,
        progress_summary: Any,
        current_streak: StreakView | None,
        twin: Any,
        result: Any,
    ) -> ReadinessSummaryView:
        category = _text(getattr(progress_summary, "title", None), fallback="Readiness")
        trend = _text(
            getattr(progress_summary, "trend_label", None)
            or (current_streak.detail if current_streak else None),
            fallback="Trend not available yet",
        )
        reason = _text(
            getattr(progress_summary, "body", None),
            fallback="Readiness detail will appear as you study.",
        )
        percent_label = ""
        if twin is not None:
            readiness = getattr(twin, "exam_readiness", None) or getattr(
                twin, "readiness", None
            )
            percent_label = _percent_from(readiness)
        available = bool(reason and reason != "No progress detail is available yet.")
        card = Card(
            title=category,
            body=f"{trend} {reason}".strip(),
            eyebrow="Readiness",
            variant=CardVariant.PROGRESS,
        )
        return ReadinessSummaryView(
            category_label=category,
            trend_label=trend,
            reason=reason,
            action_label="Continue learning",
            action_key="begin_session",
            percent_label=percent_label,
            available=available,
            card=card,
        )

    @classmethod
    def _journey_from_pipeline(
        cls,
        *,
        progress_summary: Any,
        current_streak: StreakView | None,
        result: Any,
    ) -> JourneyStoryView:
        parts: list[str] = []
        for candidate in (
            getattr(progress_summary, "body", None),
            current_streak.detail if current_streak else None,
            getattr(
                getattr(result, "student_experience", None),
                "presentation_narrative",
                None,
            ),
        ):
            text = _first_sentence(_text(candidate))
            if text and text not in parts:
                parts.append(text)
            if len(parts) >= 3:
                break
        if not parts:
            story = (
                "Your learning story will appear here as you complete sessions."
            )
            available = False
        else:
            story = " ".join(parts)
            available = True
        return JourneyStoryView(
            story=story,
            available=available,
            card=Card(
                title="Learning journey",
                body=story,
                eyebrow="Journey",
                variant=CardVariant.DEFAULT,
            ),
        )

    @classmethod
    def _coach_from_pipeline(
        cls,
        *,
        mission_reason: Any,
        result: Any,
    ) -> CoachInsightView:
        experience = getattr(result, "student_experience", None) if result else None
        motivation = getattr(experience, "motivation", None) if experience else None
        insight = _clip_sentences(
            _text(
                getattr(motivation, "message", None)
                or getattr(mission_reason, "body", None)
                or getattr(getattr(result, "explanation", None), "summary", None)
            ),
            3,
        )
        if not insight:
            insight = (
                "Your coach insight will appear after your next study session."
            )
            available = False
        else:
            available = True
        return CoachInsightView(
            insight=insight,
            available=available,
            card=Card(
                title="Coach",
                body=insight,
                eyebrow="Coach",
                variant=CardVariant.RECOMMENDATION,
            ),
        )

    @classmethod
    def _milestones_from_sessions(
        cls,
        sessions: tuple[Any, ...],
    ) -> tuple[MilestoneView, ...]:
        views: list[MilestoneView] = []
        for session in sessions[:3]:
            title = _text(getattr(session, "label", None), fallback="Upcoming")
            detail = _text(getattr(session, "detail", None))
            views.append(
                MilestoneView(
                    title=title,
                    detail=detail,
                    days_label=_text(getattr(session, "day_label", None)),
                    card=getattr(session, "card", None)
                    or Card(
                        title=title,
                        body=detail or "Upcoming milestone",
                        eyebrow="Upcoming",
                        variant=CardVariant.DEFAULT,
                    ),
                )
            )
        if not views:
            empty = "Upcoming milestones will appear when a study plan is available."
            views.append(
                MilestoneView(
                    title="No upcoming milestones",
                    detail=empty,
                    card=Card(
                        title="No upcoming milestones",
                        body=empty,
                        eyebrow="Upcoming",
                        variant=CardVariant.DEFAULT,
                    ),
                )
            )
        return tuple(views)


def _text(value: Any, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback


def _first_sentence(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    for separator in (". ", "! ", "? "):
        index = cleaned.find(separator)
        if index != -1:
            return cleaned[: index + 1].strip()
    return cleaned


def _clip_sentences(text: str, maximum: int) -> str:
    cleaned = " ".join(text.split()).strip()
    if not cleaned or maximum < 1:
        return cleaned
    sentences: list[str] = []
    remainder = cleaned
    while remainder and len(sentences) < maximum:
        cut = -1
        for separator in (". ", "! ", "? "):
            index = remainder.find(separator)
            if index != -1 and (cut == -1 or index < cut):
                cut = index + 1
        if cut == -1:
            sentences.append(remainder.strip())
            break
        sentences.append(remainder[:cut].strip())
        remainder = remainder[cut:].lstrip()
    return " ".join(sentences)


def _percent_from(value: Any) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if hasattr(value, "percent") or hasattr(value, "value"):
        value = getattr(value, "percent", None) or getattr(value, "value", None)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if number <= 1.0:
        number *= 100.0
    return f"{int(round(number))}%"
