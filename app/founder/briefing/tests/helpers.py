"""Shared builders for Founder Weekly Briefing tests (FOS-007).

Mock Operational State and RecommendationSet only — no filesystem scanning,
no Dashboard, no Knowledge Engine / Capability Archive / Internal Alpha.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.founder.briefing.builders import FounderWeeklyBriefBuilder
from app.founder.briefing.services import FounderWeeklyBriefingService
from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.models import (
    Recommendation,
    RecommendationEvidence,
    RecommendationSet,
)
from app.founder.recommendations.tests.helpers import (
    make_healthy_state,
    make_state,
)

BRIEFING_NOW = datetime(2026, 7, 14, 18, 0, 0, tzinfo=UTC)


def make_recommendation(
    *,
    recommendation_id: str = "wait_for_internal_alpha",
    category: str = "release",
    priority: str = "High",
    title: str = "Wait for Internal Alpha before releasing",
    explanation: str = "No Internal Alpha feedback is present.",
    rationale: str = "Internal Alpha is the primary user-signal gate.",
    created_at: datetime = BRIEFING_NOW,
) -> Recommendation:
    return Recommendation(
        id=recommendation_id,
        category=category,
        priority=priority,
        title=title,
        explanation=explanation,
        rationale=rationale,
        evidence=(
            RecommendationEvidence(
                source="internal_alpha",
                metric="feedback_count",
                value=0,
            ),
        ),
        created_at=created_at,
    )


def make_recommendation_set(
    *,
    state: FounderOperationalState | None = None,
    recommendations: tuple[Recommendation, ...] | None = None,
    overall_status: str = "healthy",
    generated_at: datetime = BRIEFING_NOW,
) -> RecommendationSet:
    resolved_state = state if state is not None else make_healthy_state()
    return RecommendationSet(
        snapshot_version=resolved_state.snapshot_version,
        generated_at=generated_at,
        recommendations=(
            recommendations if recommendations is not None else ()
        ),
        overall_status=overall_status,
    )


def make_attention_inputs() -> tuple[FounderOperationalState, RecommendationSet]:
    """State + recommendation set with one High-priority advisory."""
    state = make_state(
        alpha_overrides={"feedback_count": 0, "duplicate_count": 0},
    )
    recommendation_set = make_recommendation_set(
        state=state,
        recommendations=(make_recommendation(),),
        overall_status="attention",
    )
    return state, recommendation_set


def make_builder(**kwargs) -> FounderWeeklyBriefBuilder:
    return FounderWeeklyBriefBuilder(clock=lambda: BRIEFING_NOW, **kwargs)


def make_service(**kwargs) -> FounderWeeklyBriefingService:
    return FounderWeeklyBriefingService(clock=lambda: BRIEFING_NOW, **kwargs)
