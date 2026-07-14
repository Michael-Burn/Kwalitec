"""Immutable DTOs for the Founder Dashboard (FOS-004 / FSI-002)."""

from __future__ import annotations

from app.founder.dashboard.dto.activity import ActivityItem, ActivitySection
from app.founder.dashboard.dto.brief import WeeklyBriefSection
from app.founder.dashboard.dto.capability import (
    CapabilityEntry,
    CapabilitySection,
    CapabilitySnapshot,
)
from app.founder.dashboard.dto.internal_alpha import (
    InternalAlphaSection,
    InternalAlphaSnapshot,
    InternalAlphaWeekSummary,
)
from app.founder.dashboard.dto.knowledge import (
    KnowledgeSection,
    KnowledgeSnapshot,
)
from app.founder.dashboard.dto.overview import DashboardOverview, DashboardPage
from app.founder.dashboard.dto.recommendation import (
    RecommendationCard,
    RecommendationsSection,
)

__all__ = [
    "ActivityItem",
    "ActivitySection",
    "CapabilityEntry",
    "CapabilitySection",
    "CapabilitySnapshot",
    "DashboardOverview",
    "DashboardPage",
    "InternalAlphaSection",
    "InternalAlphaSnapshot",
    "InternalAlphaWeekSummary",
    "KnowledgeSection",
    "KnowledgeSnapshot",
    "RecommendationCard",
    "RecommendationsSection",
    "WeeklyBriefSection",
]
