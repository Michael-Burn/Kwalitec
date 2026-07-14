"""Unit tests for FounderWeeklyBriefBuilder (FOS-007)."""

from __future__ import annotations

import pytest

from app.founder.briefing.config import REPORT_VERSION, REQUIRED_SECTION_TITLES
from app.founder.briefing.models import FounderWeeklyBrief
from app.founder.briefing.tests.helpers import (
    BRIEFING_NOW,
    make_attention_inputs,
    make_builder,
    make_recommendation_set,
)
from app.founder.recommendations.tests.helpers import make_healthy_state


class TestFounderWeeklyBriefBuilder:
    def test_build_returns_immutable_brief(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        brief = make_builder().build(state, recommendation_set)
        assert isinstance(brief, FounderWeeklyBrief)
        assert brief.generated_at == BRIEFING_NOW
        assert brief.snapshot_version == state.snapshot_version
        assert brief.metadata.report_version == REPORT_VERSION
        with pytest.raises(Exception):
            brief.week = "mutated"  # type: ignore[misc]

    def test_week_comes_from_internal_alpha(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        brief = make_builder().build(state, recommendation_set)
        assert brief.week == state.internal_alpha.current_week

    def test_sections_cover_required_titles(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(state, recommendation_set)
        titles = tuple(section.title for section in brief.ordered_sections())
        assert titles == REQUIRED_SECTION_TITLES

    def test_orders_are_ascending(self) -> None:
        state, recommendation_set = make_attention_inputs()
        brief = make_builder().build(state, recommendation_set)
        orders = [section.order for section in brief.ordered_sections()]
        assert orders == list(range(1, 10))

    def test_validate_false_skips_raise(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        brief = make_builder().build(state, recommendation_set, validate=False)
        assert isinstance(brief, FounderWeeklyBrief)
