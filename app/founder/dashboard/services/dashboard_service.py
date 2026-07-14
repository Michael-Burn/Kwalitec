"""Founder Dashboard service — live Founder presentation coordinator (FSI-002).

Responsibilities:
1. Request current FounderOperationalState
2. Request current RecommendationSet
3. Request latest FounderWeeklyBrief
4. Build Dashboard DTOs

Coordinator only. No calculations, scoring, repository access, or AI.
"""

from __future__ import annotations

from app.founder.briefing import FounderWeeklyBrief
from app.founder.dashboard.dto.activity import ActivityItem, ActivitySection
from app.founder.dashboard.dto.brief import WeeklyBriefSection
from app.founder.dashboard.dto.capability import CapabilityEntry, CapabilitySection
from app.founder.dashboard.dto.internal_alpha import (
    InternalAlphaSection,
    InternalAlphaWeekSummary,
)
from app.founder.dashboard.dto.knowledge import KnowledgeSection
from app.founder.dashboard.dto.overview import DashboardOverview, DashboardPage
from app.founder.dashboard.dto.recommendation import (
    RecommendationCard,
    RecommendationsSection,
)
from app.founder.dashboard.providers import (
    OperationalStateProvider,
    RecommendationProvider,
    WeeklyBriefProvider,
)
from app.founder.dashboard.providers.protocols import (
    OperationalStateGate,
    RecommendationGate,
    WeeklyBriefGate,
)
from app.founder.operational_state import FounderOperationalState
from app.founder.recommendations import RecommendationSet

FOUNDER_OS_VERSION = "1.0"
DEFAULT_RELEASE = "1.0.0"
MAX_TOP_RECOMMENDATIONS = 5


class FounderDashboardService:
    """Aggregate live Founder services into presentation DTOs."""

    def __init__(
        self,
        *,
        operational_state: OperationalStateGate | None = None,
        recommendations: RecommendationGate | None = None,
        weekly_brief: WeeklyBriefGate | None = None,
        fos_version: str = FOUNDER_OS_VERSION,
        default_release: str = DEFAULT_RELEASE,
        max_top_recommendations: int = MAX_TOP_RECOMMENDATIONS,
    ) -> None:
        self._operational_state = operational_state or OperationalStateProvider()
        self._recommendations = recommendations or RecommendationProvider()
        self._weekly_brief = weekly_brief or WeeklyBriefProvider()
        self._fos_version = fos_version
        self._default_release = default_release
        self._max_top = max_top_recommendations

    def build_overview(self) -> DashboardOverview:
        """Build the executive overview from live Founder providers."""
        return self.build_page().overview

    def build_page(self) -> DashboardPage:
        """Build the full Founder Dashboard page model.

        Missing operational state, recommendations, or briefing are handled
        gracefully — the dashboard always returns a renderable page.
        """
        state = self._operational_state.get_state()
        if state is None:
            return self._empty_page()

        recommendation_set = self._recommendations.get_recommendations(state)
        brief = None
        if recommendation_set is not None:
            brief = self._weekly_brief.get_brief(state, recommendation_set)

        return self._page_from_live(state, recommendation_set, brief)

    def _page_from_live(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet | None,
        brief: FounderWeeklyBrief | None,
    ) -> DashboardPage:
        knowledge = _map_knowledge(state)
        capabilities = _map_capabilities(state)
        internal_alpha = _map_internal_alpha(state)
        activity = _map_activity(state)
        recommendations = _map_recommendations(
            recommendation_set, max_top=self._max_top
        )
        weekly_brief = _map_weekly_brief(brief)
        release = state.release.current_release or self._default_release
        latest = _latest_activity_label(
            capability_ids=state.capability.recent_capability_ids,
            alpha_week=state.internal_alpha.current_week,
            brief_week=weekly_brief.week if weekly_brief.available else "",
        )
        overview = DashboardOverview(
            engineering_health=knowledge.engineering_health,
            architecture_health=knowledge.architecture_health,
            capability_count=capabilities.total_count,
            completed_capabilities=capabilities.completed_count,
            active_capabilities=capabilities.active_count,
            internal_alpha_week=internal_alpha.current_week,
            feedback_count=internal_alpha.feedback_count,
            duplicate_feedback=internal_alpha.duplicate_count,
            current_release=release,
            latest_activity=latest,
            snapshot_version=state.snapshot_version,
            recommendation_count=recommendations.count,
            overall_recommendation_status=recommendations.overall_status,
            brief_week=weekly_brief.week if weekly_brief.available else "",
            brief_available=weekly_brief.available,
        )
        return DashboardPage(
            overview=overview,
            fos_version=self._fos_version,
            knowledge=knowledge,
            capabilities=capabilities,
            internal_alpha=internal_alpha,
            activity=activity,
            recommendations=recommendations,
            weekly_brief=weekly_brief,
        )

    def _empty_page(self) -> DashboardPage:
        """Safe empty page when operational state is unavailable."""
        knowledge = KnowledgeSection(
            engineering_standards=0,
            architecture_documents=0,
            research_documents=0,
            capability_documents=0,
            indexed_artefacts=0,
            engineering_health=0,
            architecture_health=0,
        )
        capabilities = CapabilitySection(
            entries=(),
            total_count=0,
            completed_count=0,
            active_count=0,
        )
        internal_alpha = InternalAlphaSection(
            current_week="",
            feedback_count=0,
            duplicate_count=0,
            category_counts={},
            latest_summary_file="",
            recent_weeks=(),
        )
        activity = ActivitySection(
            recently_indexed=(),
            recently_completed_capabilities=(),
            recent_internal_alpha_weeks=(),
            items=(),
        )
        recommendations = RecommendationsSection(
            available=False,
            overall_status="",
            count=0,
            top=(),
        )
        weekly_brief = WeeklyBriefSection(
            available=False,
            week="",
            generated_at="",
            snapshot_version="",
            recommendation_version="",
            report_version="",
        )
        overview = DashboardOverview(
            engineering_health=0,
            architecture_health=0,
            capability_count=0,
            completed_capabilities=0,
            active_capabilities=0,
            internal_alpha_week="",
            feedback_count=0,
            duplicate_feedback=0,
            current_release=self._default_release,
            latest_activity="",
            snapshot_version="",
            recommendation_count=0,
            overall_recommendation_status="",
            brief_week="",
            brief_available=False,
        )
        return DashboardPage(
            overview=overview,
            fos_version=self._fos_version,
            knowledge=knowledge,
            capabilities=capabilities,
            internal_alpha=internal_alpha,
            activity=activity,
            recommendations=recommendations,
            weekly_brief=weekly_brief,
        )


def _signal_health(*, tests_pass: bool, validation_errors: int) -> int:
    """Map Operational State engineering signals to the Version 1 display percent.

    Presentation projection only — mirrors the prior dashboard health display
    (100 when clean, otherwise 0). Does not introduce new scoring.
    """
    if tests_pass and validation_errors == 0:
        return 100
    return 0


def _map_knowledge(state: FounderOperationalState) -> KnowledgeSection:
    health = _signal_health(
        tests_pass=state.engineering.tests_pass,
        validation_errors=state.engineering.validation_errors,
    )
    return KnowledgeSection(
        engineering_standards=state.knowledge.engineering_standards,
        architecture_documents=state.knowledge.architecture_documents,
        research_documents=state.knowledge.research_documents,
        capability_documents=state.knowledge.capability_documents,
        indexed_artefacts=state.knowledge.indexed_artefacts,
        engineering_health=health,
        architecture_health=health,
    )


def _map_capabilities(state: FounderOperationalState) -> CapabilitySection:
    recent = state.capability.recent_capability_ids
    entries = tuple(
        CapabilityEntry(
            capability_id=cap_id,
            title="",
            status="",
            version="",
            completion_date="",
        )
        for cap_id in recent
    )
    return CapabilitySection(
        entries=entries,
        total_count=state.capability.total_count,
        completed_count=state.capability.completed_count,
        active_count=state.capability.active_count,
        recent_capability_ids=recent,
        archive_inconsistencies=state.capability.archive_inconsistencies,
    )


def _map_internal_alpha(state: FounderOperationalState) -> InternalAlphaSection:
    recent_weeks = tuple(
        InternalAlphaWeekSummary(
            week=label,
            feedback_count=0,
            duplicate_count=0,
        )
        for label in state.internal_alpha.recent_week_labels
    )
    return InternalAlphaSection(
        current_week=state.internal_alpha.current_week,
        feedback_count=state.internal_alpha.feedback_count,
        duplicate_count=state.internal_alpha.duplicate_count,
        category_counts=dict(state.internal_alpha.category_counts),
        latest_summary_file="",
        recent_weeks=recent_weeks,
    )


def _map_activity(state: FounderOperationalState) -> ActivitySection:
    recent_caps = state.capability.recent_capability_ids
    recent_weeks = state.internal_alpha.recent_week_labels
    items: list[ActivityItem] = []
    for cap_id in recent_caps:
        items.append(ActivityItem(kind="capability", label=cap_id))
    for week in recent_weeks:
        items.append(ActivityItem(kind="alpha_week", label=week))
    return ActivitySection(
        recently_indexed=(),
        recently_completed_capabilities=recent_caps,
        recent_internal_alpha_weeks=recent_weeks,
        items=tuple(items),
    )


def _map_recommendations(
    recommendation_set: RecommendationSet | None, *, max_top: int
) -> RecommendationsSection:
    if recommendation_set is None:
        return RecommendationsSection(
            available=False,
            overall_status="",
            count=0,
            top=(),
        )
    top = tuple(
        RecommendationCard(
            recommendation_id=rec.id,
            priority=rec.priority,
            title=rec.title,
            category=rec.category,
            explanation=rec.explanation,
        )
        for rec in recommendation_set.recommendations[:max_top]
    )
    return RecommendationsSection(
        available=True,
        overall_status=recommendation_set.overall_status,
        count=len(recommendation_set.recommendations),
        top=top,
    )


def _map_weekly_brief(brief: FounderWeeklyBrief | None) -> WeeklyBriefSection:
    if brief is None:
        return WeeklyBriefSection(
            available=False,
            week="",
            generated_at="",
            snapshot_version="",
            recommendation_version="",
            report_version="",
        )
    return WeeklyBriefSection(
        available=True,
        week=brief.week,
        generated_at=brief.generated_at.isoformat(),
        snapshot_version=brief.snapshot_version,
        recommendation_version=brief.recommendation_version,
        report_version=brief.metadata.report_version,
    )


def _latest_activity_label(
    *,
    capability_ids: tuple[str, ...],
    alpha_week: str,
    brief_week: str,
) -> str:
    """Pick a single latest-activity label from available lists (no ranking)."""
    if capability_ids:
        return capability_ids[0]
    if brief_week:
        return brief_week
    if alpha_week:
        return alpha_week
    return ""
