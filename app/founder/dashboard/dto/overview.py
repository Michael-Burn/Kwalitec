"""Top-level Founder Dashboard overview DTOs (FOS-004 / FSI-002)."""

from __future__ import annotations

from dataclasses import dataclass

from app.founder.dashboard.dto.activity import ActivitySection
from app.founder.dashboard.dto.brief import WeeklyBriefSection
from app.founder.dashboard.dto.capability import CapabilitySection
from app.founder.dashboard.dto.internal_alpha import InternalAlphaSection
from app.founder.dashboard.dto.knowledge import KnowledgeSection
from app.founder.dashboard.dto.recommendation import RecommendationsSection


@dataclass(frozen=True)
class DashboardOverview:
    """Immutable executive summary metrics for the Founder Dashboard.

    Summaries are presentation projections of FounderOperationalState,
    RecommendationSet, and FounderWeeklyBrief — never raw subsystem objects.
    """

    engineering_health: int
    architecture_health: int
    capability_count: int
    completed_capabilities: int
    active_capabilities: int
    internal_alpha_week: str
    feedback_count: int
    duplicate_feedback: int
    current_release: str
    latest_activity: str
    snapshot_version: str
    recommendation_count: int
    overall_recommendation_status: str
    brief_week: str
    brief_available: bool


@dataclass(frozen=True)
class DashboardPage:
    """Full Founder Dashboard page model for template rendering."""

    overview: DashboardOverview
    fos_version: str
    knowledge: KnowledgeSection
    capabilities: CapabilitySection
    internal_alpha: InternalAlphaSection
    activity: ActivitySection
    recommendations: RecommendationsSection
    weekly_brief: WeeklyBriefSection
