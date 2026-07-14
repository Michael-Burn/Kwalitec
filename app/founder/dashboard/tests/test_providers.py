"""Unit tests for Founder Dashboard live providers (FSI-002)."""

from __future__ import annotations

from app.founder.dashboard.providers import (
    OperationalStateProvider,
    RecommendationProvider,
    WeeklyBriefProvider,
)
from app.founder.dashboard.tests.helpers import (
    StubOperationalStateService,
    StubRecommendationService,
    StubWeeklyBriefService,
    make_attention_bundle,
    make_healthy_state,
    make_recommendation_set,
)


class TestOperationalStateProvider:
    def test_returns_state_from_service(self) -> None:
        state = make_healthy_state()
        provider = OperationalStateProvider(
            service=StubOperationalStateService(state)
        )
        assert provider.get_state() is state

    def test_returns_none_when_service_fails(self) -> None:
        provider = OperationalStateProvider(
            service=StubOperationalStateService(None)
        )
        assert provider.get_state() is None


class TestRecommendationProvider:
    def test_returns_set_from_service(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        provider = RecommendationProvider(
            service=StubRecommendationService(recommendation_set)
        )
        assert provider.get_recommendations(state) is recommendation_set

    def test_returns_none_when_service_fails(self) -> None:
        state = make_healthy_state()
        provider = RecommendationProvider(
            service=StubRecommendationService(None)
        )
        assert provider.get_recommendations(state) is None


class TestWeeklyBriefProvider:
    def test_returns_brief_from_service(self) -> None:
        state, recommendation_set, brief = make_attention_bundle()
        provider = WeeklyBriefProvider(
            service=StubWeeklyBriefService(brief)
        )
        assert provider.get_brief(state, recommendation_set) is brief

    def test_returns_none_when_service_fails(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        provider = WeeklyBriefProvider(service=StubWeeklyBriefService(None))
        assert provider.get_brief(state, recommendation_set) is None
