"""Unit tests for RecommendationEngine (FOS-006)."""

from __future__ import annotations

from app.founder.recommendations.config import (
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    STATUS_ATTENTION,
    STATUS_CRITICAL,
    STATUS_HEALTHY,
    TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH,
    TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES,
    TEMPLATE_SELECT_ROADMAP_CAPABILITY,
    TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
)
from app.founder.recommendations.dto import RuleOutcome
from app.founder.recommendations.models import RecommendationEvidence
from app.founder.recommendations.rules import NoInternalAlphaFeedbackRule
from app.founder.recommendations.tests.helpers import (
    RECOMMENDATION_NOW,
    make_engine,
    make_healthy_state,
    make_state,
)


class TestRecommendationEngine:
    def test_healthy_state_returns_empty_healthy_set(self) -> None:
        result = make_engine().evaluate(make_healthy_state())
        assert result.recommendations == ()
        assert result.overall_status == STATUS_HEALTHY
        assert result.snapshot_version == "1.0"
        assert result.generated_at == RECOMMENDATION_NOW

    def test_runs_all_registered_rules(self) -> None:
        state = make_state(
            knowledge_overrides={"tests_pass": False},
            capability_overrides={
                "archive_inconsistencies": 1,
                "active_count": 0,
                "completed_count": 1,
                "total_count": 1,
            },
            alpha_overrides={"feedback_count": 0, "duplicate_count": 0},
        )
        result = make_engine().evaluate(state)
        ids = {r.id for r in result.recommendations}
        assert TEMPLATE_WAIT_FOR_INTERNAL_ALPHA in ids
        assert TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES in ids
        assert TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH in ids
        assert TEMPLATE_SELECT_ROADMAP_CAPABILITY in ids
        assert result.overall_status == STATUS_CRITICAL

    def test_renders_template_wording(self) -> None:
        state = make_state(alpha_overrides={"feedback_count": 0, "duplicate_count": 0})
        result = make_engine().evaluate(state)
        assert len(result.recommendations) == 1
        rec = result.recommendations[0]
        assert rec.id == TEMPLATE_WAIT_FOR_INTERNAL_ALPHA
        assert "Internal Alpha" in rec.title
        assert rec.explanation
        assert rec.rationale
        assert rec.evidence

    def test_custom_rules_only(self) -> None:
        state = make_state(alpha_overrides={"feedback_count": 0, "duplicate_count": 0})
        result = make_engine(rules=(NoInternalAlphaFeedbackRule(),)).evaluate(state)
        assert len(result.recommendations) == 1
        assert result.overall_status == STATUS_ATTENTION

    def test_sort_outcomes_by_priority(self) -> None:
        outcomes = [
            RuleOutcome(
                rule_id="a",
                template_id="select_roadmap_capability",
                category="roadmap",
                priority=PRIORITY_MEDIUM,
                evidence=(
                    RecommendationEvidence(source="c", metric="m", value=0),
                ),
            ),
            RuleOutcome(
                rule_id="b",
                template_id="resolve_archive_inconsistencies",
                category="archive",
                priority=PRIORITY_CRITICAL,
                evidence=(
                    RecommendationEvidence(source="c", metric="m", value=1),
                ),
            ),
            RuleOutcome(
                rule_id="c",
                template_id="wait_for_internal_alpha",
                category="release",
                priority=PRIORITY_HIGH,
                evidence=(
                    RecommendationEvidence(source="c", metric="m", value=0),
                ),
            ),
        ]
        sorted_outcomes = make_engine()._sort_outcomes(outcomes)
        assert [o.priority for o in sorted_outcomes] == [
            PRIORITY_CRITICAL,
            PRIORITY_HIGH,
            PRIORITY_MEDIUM,
        ]
