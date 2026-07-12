"""Dashboard Application assemblers — surface projections of Educational Experience.

Owns presentation shaping for dashboard view models. Does not own educational
reasoning, Decision selection, Recommendation packaging math, or Mission
composition.
"""

from __future__ import annotations

from app.application.dashboard.dashboard_assembler import DashboardAssembler
from app.application.dashboard.dashboard_view_model import (
    DashboardViewModel,
    FeatureVisibilityViewModel,
    MissionCardViewModel,
    NavigationAffordancesViewModel,
    ProgressSummaryViewModel,
    ReadinessSummaryViewModel,
)
from app.application.dashboard.educational_dashboard_composer import (
    DashboardCompositionContext,
    EducationalDashboardComposer,
)
from app.application.dashboard.recommendation_card_builder import (
    RecommendationCardBuilder,
    RecommendationCardViewModel,
)

__all__ = [
    "DashboardAssembler",
    "DashboardCompositionContext",
    "DashboardViewModel",
    "EducationalDashboardComposer",
    "FeatureVisibilityViewModel",
    "MissionCardViewModel",
    "NavigationAffordancesViewModel",
    "ProgressSummaryViewModel",
    "ReadinessSummaryViewModel",
    "RecommendationCardBuilder",
    "RecommendationCardViewModel",
]
