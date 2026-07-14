"""Unit tests for briefing section templates (FOS-007)."""

from __future__ import annotations

from app.founder.briefing.config import (
    SECTION_ENGINEERING,
    SECTION_EXECUTIVE_SUMMARY,
    SECTION_RISKS,
)
from app.founder.briefing.templates import (
    build_engineering_overview,
    build_executive_summary,
    build_recommendation_summary,
    build_risks,
    build_top_priorities,
)
from app.founder.briefing.tests.helpers import (
    make_attention_inputs,
    make_recommendation,
    make_recommendation_set,
)
from app.founder.recommendations.tests.helpers import make_healthy_state


class TestSectionTemplates:
    def test_executive_summary_is_deterministic(self) -> None:
        state, recommendation_set = make_attention_inputs()
        first = build_executive_summary(state, recommendation_set, order=1)
        second = build_executive_summary(state, recommendation_set, order=1)
        assert first == second
        assert first.title == SECTION_EXECUTIVE_SUMMARY
        assert "Overall status: attention" in first.content
        assert state.internal_alpha.current_week in first.content

    def test_engineering_overview_uses_state_counts(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        section = build_engineering_overview(state, recommendation_set, order=2)
        assert section.title == SECTION_ENGINEERING
        standards = f"Standards count: {state.engineering.standards_count}"
        assert standards in section.content
        assert "Tests: pass" in section.content

    def test_top_priorities_empty_set(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(state=state)
        section = build_top_priorities(state, recommendation_set, order=6)
        assert "No active priorities" in section.content

    def test_recommendation_summary_lists_ids(self) -> None:
        state, recommendation_set = make_attention_inputs()
        section = build_recommendation_summary(state, recommendation_set, order=7)
        assert "wait_for_internal_alpha" in section.content
        assert "Count: 1" in section.content

    def test_risks_only_critical_and_high(self) -> None:
        state = make_healthy_state()
        recommendation_set = make_recommendation_set(
            state=state,
            recommendations=(
                make_recommendation(
                    recommendation_id="pause_for_engineering_health",
                    priority="Critical",
                    title="Pause new capabilities",
                    explanation="Engineering health is below threshold.",
                ),
                make_recommendation(
                    recommendation_id="select_roadmap_capability",
                    priority="Medium",
                    title="Select roadmap capability",
                    explanation="No capabilities are currently active.",
                ),
            ),
            overall_status="critical",
        )
        section = build_risks(state, recommendation_set, order=8)
        assert section.title == SECTION_RISKS
        assert "Pause new capabilities" in section.content
        assert "Select roadmap capability" not in section.content
