"""Shared builders for Founder Dashboard tests (FSI-002).

Mocked live Founder services only — no filesystem scanning, no Flask app.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.founder.briefing import FounderWeeklyBrief
from app.founder.briefing.tests.helpers import (
    BRIEFING_NOW,
    make_recommendation,
    make_recommendation_set,
)
from app.founder.briefing.tests.helpers import (
    make_service as make_briefing_service,
)
from app.founder.dashboard.providers import (
    OperationalStateProvider,
    RecommendationProvider,
    WeeklyBriefProvider,
)
from app.founder.dashboard.services import FounderDashboardService
from app.founder.operational_state import FounderOperationalState
from app.founder.recommendations import RecommendationSet
from app.founder.recommendations.tests.helpers import (
    make_healthy_state,
    make_state,
)

FIXED_NOW = datetime(2026, 7, 14, 12, 0, 0, tzinfo=UTC)
_UNSET: Any = object()


class StubOperationalStateService:
    """Injectable Operational State service double."""

    def __init__(self, state: FounderOperationalState | None) -> None:
        self._state = state
        self.calls = 0

    def get_state(self, *, generated_at=None) -> FounderOperationalState:
        self.calls += 1
        if self._state is None:
            raise RuntimeError("operational state unavailable")
        return self._state


class StubRecommendationService:
    """Injectable Recommendation service double."""

    def __init__(self, recommendation_set: RecommendationSet | None) -> None:
        self._recommendation_set = recommendation_set
        self.calls = 0

    def recommend(self, state: FounderOperationalState) -> RecommendationSet:
        self.calls += 1
        if self._recommendation_set is None:
            raise RuntimeError("recommendation set unavailable")
        return self._recommendation_set


class StubWeeklyBriefService:
    """Injectable Weekly Brief service double."""

    def __init__(self, brief: FounderWeeklyBrief | None) -> None:
        self._brief = brief
        self.calls = 0

    def generate_brief(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
        *,
        generated_at=None,
        output_dir=None,
    ) -> FounderWeeklyBrief:
        self.calls += 1
        if self._brief is None:
            raise RuntimeError("weekly brief unavailable")
        return self._brief


def make_attention_bundle() -> tuple[
    FounderOperationalState, RecommendationSet, FounderWeeklyBrief
]:
    """State + recommendations + weekly brief for attention scenarios."""
    state = make_state(
        alpha_overrides={"feedback_count": 0, "duplicate_count": 0},
    )
    recommendation_set = make_recommendation_set(
        state=state,
        recommendations=(make_recommendation(),),
        overall_status="attention",
    )
    brief = make_briefing_service().generate_brief(state, recommendation_set)
    return state, recommendation_set, brief


def make_service(
    *,
    state: Any = _UNSET,
    recommendation_set: Any = _UNSET,
    brief: Any = _UNSET,
) -> FounderDashboardService:
    """Build a dashboard service with stubbed Founder public services.

    Pass ``None`` explicitly for a gate to simulate unavailability.
    Omit a gate argument to use healthy/default fixtures.
    """
    if state is _UNSET:
        state = make_healthy_state()
    if recommendation_set is _UNSET:
        recommendation_set = (
            make_recommendation_set(state=state) if state is not None else None
        )
    if brief is _UNSET:
        if state is not None and recommendation_set is not None:
            brief = make_briefing_service().generate_brief(
                state, recommendation_set
            )
        else:
            brief = None

    return FounderDashboardService(
        operational_state=OperationalStateProvider(
            service=StubOperationalStateService(state)
        ),
        recommendations=RecommendationProvider(
            service=StubRecommendationService(recommendation_set)
        ),
        weekly_brief=WeeklyBriefProvider(
            service=StubWeeklyBriefService(brief)
        ),
    )


__all__ = [
    "BRIEFING_NOW",
    "FIXED_NOW",
    "StubOperationalStateService",
    "StubRecommendationService",
    "StubWeeklyBriefService",
    "make_attention_bundle",
    "make_healthy_state",
    "make_recommendation",
    "make_recommendation_set",
    "make_service",
    "make_state",
]
