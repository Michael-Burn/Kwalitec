"""Dashboard Assembler — Application Layer presentation composition.

Converts one Educational Experience into one immutable DashboardViewModel.

Owns widget placement, empty-state / warning forwarding, and feature-flag-aware
inclusion only. Never scores readiness, selects next actions, packages
Recommendations, composes Missions, retrieves Twin, interprets Curriculum, or
imports Flask / routes / templates / ORM.
"""

from __future__ import annotations

from dataclasses import replace

from app.application.config.feature_flags import (
    FEATURE_FLAGS,
    EducationalIntelligenceFeatureFlags,
)
from app.application.dashboard.dashboard_view_model import (
    DashboardViewModel,
    FeatureVisibilityViewModel,
    MissionCardViewModel,
    NavigationAffordancesViewModel,
    ProgressSummaryViewModel,
    ReadinessSummaryViewModel,
)
from app.application.dashboard.recommendation_card_builder import (
    RecommendationCardBuilder,
    RecommendationCardViewModel,
)
from app.application.orchestration.educational_orchestrator import (
    EducationalExperience,
)
from app.domain.decision.action_types import ActionFamily
from app.domain.mission.mission import Mission

# Student-facing Mission task labels — educational intent only.
_FAMILY_HEADLINE: dict[ActionFamily, str] = {
    ActionFamily.STUDY: "Study",
    ActionFamily.REVISE: "Review",
    ActionFamily.ASSESS: "Practice check",
    ActionFamily.DIAGNOSTIC: "Focus check",
    ActionFamily.REST_PROTECT_INTENSITY: "Lighter session",
}


class DashboardAssembler:
    """Compose DashboardViewModel from one Educational Experience.

    Presentation conductor only. Educational Orchestrator remains the educational
    conductor; domains remain educational authority.
    """

    @staticmethod
    def assemble(
        experience: EducationalExperience,
        *,
        flags: EducationalIntelligenceFeatureFlags | None = None,
    ) -> DashboardViewModel:
        """Project Educational Experience into a closed Dashboard ViewModel.

        Args:
            experience: Composed Educational Experience Contract snapshot.
            flags: Optional flag snapshot for tests / staged rollout.
                Defaults to the Application Layer ``FEATURE_FLAGS`` singleton.

        Returns:
            Immutable DashboardViewModel. Sparse when flags omit widgets or
            Experience carries empty-state / warning honesty.
        """
        active = flags if flags is not None else FEATURE_FLAGS

        recommendation_card = _recommendation_card(experience, active)
        mission_card = _mission_card(experience, active)
        readiness_summary = _readiness_summary(experience)
        progress_summary = _progress_summary(experience, active)
        warnings = tuple(experience.warnings)
        empty_states = tuple(experience.empty_state_guidance)
        feature_visibility = FeatureVisibilityViewModel(
            recommendations=active.ENABLE_EI_RECOMMENDATIONS,
            missions=active.ENABLE_EI_MISSIONS,
            explainability=active.ENABLE_EI_EXPLAINABILITY,
            progress=active.ENABLE_EI_PROGRESS,
        )
        navigation = _navigation(
            recommendation_card=recommendation_card,
            mission_card=mission_card,
            readiness_summary=readiness_summary,
            progress_summary=progress_summary,
            experience=experience,
            flags=active,
        )
        return DashboardViewModel(
            recommendation_card=recommendation_card,
            mission_card=mission_card,
            readiness_summary=readiness_summary,
            progress_summary=progress_summary,
            warnings=warnings,
            empty_states=empty_states,
            navigation=navigation,
            feature_visibility=feature_visibility,
        )


def _recommendation_card(
    experience: EducationalExperience,
    flags: EducationalIntelligenceFeatureFlags,
) -> RecommendationCardViewModel | None:
    """Reuse RecommendationCardBuilder; gate explainability affordance by flag."""
    if not flags.ENABLE_EI_RECOMMENDATIONS:
        return None
    card = RecommendationCardBuilder.build(experience, flags=flags)
    if card is None:
        return None
    if not flags.ENABLE_EI_EXPLAINABILITY and card.show_explanation:
        return replace(card, show_explanation=False)
    return card


def _mission_card(
    experience: EducationalExperience,
    flags: EducationalIntelligenceFeatureFlags,
) -> MissionCardViewModel | None:
    """Place Mission card when Twin-first missions are enabled — never invent tasks."""
    if not flags.ENABLE_EI_MISSIONS:
        return None
    mission = experience.todays_mission
    return MissionCardViewModel(
        title=_mission_title(mission),
        summary=_mission_summary(mission),
        task_count=mission.task_count,
        task_headlines=_task_headlines(mission),
        duration_display=_mission_duration(mission),
        warning=_mission_warning(
            experience_warnings=experience.warnings,
            mission=mission,
        ),
        show_open_button=mission.task_count > 0,
    )


def _mission_title(mission: Mission) -> str:
    """Presentation title from Decision-bound task family — no re-selection."""
    if not mission.tasks:
        return "Today's mission"
    family = mission.tasks[0].family
    label = _FAMILY_HEADLINE.get(family, family.value)
    return f"Today's mission · {label}"


def _mission_summary(mission: Mission) -> str | None:
    """Short card summary from task count — display only."""
    count = mission.task_count
    if count == 0:
        return "No tasks in this session window"
    if count == 1:
        return "1 task"
    return f"{count} tasks"


def _task_headlines(mission: Mission) -> tuple[str, ...]:
    """Short educational task headlines — never dump internal entity ids."""
    headlines: list[str] = []
    for task in mission.tasks:
        family_label = _FAMILY_HEADLINE.get(task.family, "Study task")
        headlines.append(family_label)
    return tuple(headlines)


def _mission_duration(mission: Mission) -> str | None:
    """Student-facing duration hint — never dump internal feasibility tags."""
    del mission
    return None


def _mission_warning(
    *,
    experience_warnings: tuple[str, ...],
    mission: Mission,
) -> str | None:
    """Keep thin-warrant honesty internal — do not render diagnostic tags in UI.

    Domain warnings remain on the Experience for explainability consumers. The
    student Mission card must never surface tags such as ``cold_start``.
    """
    del experience_warnings, mission
    return None


def _readiness_summary(
    experience: EducationalExperience,
) -> ReadinessSummaryViewModel:
    """Forward Readiness Summary presentation scalars — never recompute."""
    summary = experience.readiness_summary
    honesty: str | None = None
    if summary.cold_start:
        honesty = "cold_start"
    elif summary.overall_posture.value == "not_yet_knowable":
        honesty = "not_yet_knowable"
    elif summary.overall_warrant.value == "low":
        honesty = "thin_warrant"
    return ReadinessSummaryViewModel(
        overall_posture=summary.overall_posture.value,
        warrant_posture=summary.overall_warrant.value,
        cold_start=summary.cold_start,
        honesty_cue=honesty,
    )


def _progress_summary(
    experience: EducationalExperience,
    flags: EducationalIntelligenceFeatureFlags,
) -> ProgressSummaryViewModel | None:
    """Place Twin-first Progress when enabled — never select next action."""
    if not flags.ENABLE_EI_PROGRESS:
        return None
    snapshot = experience.progress_snapshot
    cues: list[str] = [
        f"posture:{snapshot.overall_posture.value}",
        f"warrant:{snapshot.overall_warrant.value}",
    ]
    if snapshot.cold_start:
        cues.append("cold_start")
    if snapshot.curriculum_id:
        cues.append(f"curriculum:{snapshot.curriculum_id}")
    return ProgressSummaryViewModel(
        overall_posture=snapshot.overall_posture.value,
        warrant_posture=snapshot.overall_warrant.value,
        cold_start=snapshot.cold_start,
        progress_cues=tuple(cues),
    )


def _navigation(
    *,
    recommendation_card: RecommendationCardViewModel | None,
    mission_card: MissionCardViewModel | None,
    readiness_summary: ReadinessSummaryViewModel | None,
    progress_summary: ProgressSummaryViewModel | None,
    experience: EducationalExperience,
    flags: EducationalIntelligenceFeatureFlags,
) -> NavigationAffordancesViewModel:
    """Bind CTA visibility to assembled cargo + flags — no unfinished chrome."""
    can_view_explanation = (
        flags.ENABLE_EI_EXPLAINABILITY
        and experience.explainability.explanation_chain is not None
        and recommendation_card is not None
        and recommendation_card.show_explanation
    )
    return NavigationAffordancesViewModel(
        can_start_recommendation=bool(
            recommendation_card is not None and recommendation_card.show_start_button
        ),
        can_open_mission=bool(
            mission_card is not None and mission_card.show_open_button
        ),
        can_view_explanation=can_view_explanation,
        can_view_readiness=readiness_summary is not None,
        can_view_progress=progress_summary is not None,
    )
