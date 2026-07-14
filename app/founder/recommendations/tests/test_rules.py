"""Unit tests for Version 1 recommendation rules (FOS-006)."""

from __future__ import annotations

from app.founder.recommendations.config import (
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH,
    TEMPLATE_PRIORITISE_RECURRING_ISSUES,
    TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES,
    TEMPLATE_SELECT_ROADMAP_CAPABILITY,
    TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
)
from app.founder.recommendations.rules import (
    ArchiveValidationFailedRule,
    EngineeringHealthBelowThresholdRule,
    HighDuplicateFeedbackRule,
    NoActiveCapabilitiesRule,
    NoInternalAlphaFeedbackRule,
)
from app.founder.recommendations.tests.helpers import make_healthy_state, make_state


class TestNoInternalAlphaFeedbackRule:
    def test_fires_when_no_feedback(self) -> None:
        state = make_state(alpha_overrides={"feedback_count": 0, "duplicate_count": 0})
        outcome = NoInternalAlphaFeedbackRule().evaluate(state)
        assert outcome is not None
        assert outcome.template_id == TEMPLATE_WAIT_FOR_INTERNAL_ALPHA
        assert outcome.priority == PRIORITY_HIGH

    def test_silent_when_feedback_present(self) -> None:
        assert NoInternalAlphaFeedbackRule().evaluate(make_healthy_state()) is None


class TestArchiveValidationFailedRule:
    def test_fires_when_inconsistencies_present(self) -> None:
        state = make_state(capability_overrides={"archive_inconsistencies": 2})
        outcome = ArchiveValidationFailedRule().evaluate(state)
        assert outcome is not None
        assert outcome.template_id == TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES
        assert outcome.priority == PRIORITY_CRITICAL

    def test_silent_when_clean(self) -> None:
        assert ArchiveValidationFailedRule().evaluate(make_healthy_state()) is None


class TestEngineeringHealthBelowThresholdRule:
    def test_fires_when_tests_fail(self) -> None:
        state = make_state(knowledge_overrides={"tests_pass": False})
        outcome = EngineeringHealthBelowThresholdRule().evaluate(state)
        assert outcome is not None
        assert outcome.template_id == TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH
        assert outcome.priority == PRIORITY_CRITICAL

    def test_fires_when_validation_errors_above_threshold(self) -> None:
        state = make_state(knowledge_overrides={"validation_errors": 3})
        outcome = EngineeringHealthBelowThresholdRule().evaluate(state)
        assert outcome is not None

    def test_silent_when_healthy(self) -> None:
        assert (
            EngineeringHealthBelowThresholdRule().evaluate(make_healthy_state())
            is None
        )


class TestHighDuplicateFeedbackRule:
    def test_fires_on_absolute_threshold(self) -> None:
        state = make_state(
            alpha_overrides={"feedback_count": 10, "duplicate_count": 3}
        )
        outcome = HighDuplicateFeedbackRule().evaluate(state)
        assert outcome is not None
        assert outcome.template_id == TEMPLATE_PRIORITISE_RECURRING_ISSUES
        assert outcome.priority == PRIORITY_HIGH

    def test_fires_on_ratio_threshold(self) -> None:
        state = make_state(
            alpha_overrides={"feedback_count": 5, "duplicate_count": 2}
        )
        # ratio 0.4 exactly meets threshold
        outcome = HighDuplicateFeedbackRule().evaluate(state)
        assert outcome is not None

    def test_silent_when_below_threshold(self) -> None:
        # defaults: 2/7 ≈ 0.286 < 0.4 and absolute < 3
        assert HighDuplicateFeedbackRule().evaluate(make_healthy_state()) is None

    def test_silent_when_no_feedback(self) -> None:
        state = make_state(alpha_overrides={"feedback_count": 0, "duplicate_count": 0})
        assert HighDuplicateFeedbackRule().evaluate(state) is None


class TestNoActiveCapabilitiesRule:
    def test_fires_when_no_active(self) -> None:
        state = make_state(
            capability_overrides={
                "active_count": 0,
                "completed_count": 2,
                "total_count": 2,
            }
        )
        # completed must match release.completed_capabilities via builder
        outcome = NoActiveCapabilitiesRule().evaluate(state)
        assert outcome is not None
        assert outcome.template_id == TEMPLATE_SELECT_ROADMAP_CAPABILITY
        assert outcome.priority == PRIORITY_MEDIUM

    def test_silent_when_active_present(self) -> None:
        assert NoActiveCapabilitiesRule().evaluate(make_healthy_state()) is None

    def test_includes_recent_capability_evidence(self) -> None:
        state = make_state(
            capability_overrides={
                "active_count": 0,
                "completed_count": 1,
                "total_count": 1,
                "recent_capability_ids": ("FOS-005",),
            }
        )
        outcome = NoActiveCapabilitiesRule().evaluate(state)
        assert outcome is not None
        metrics = {e.metric: e.value for e in outcome.evidence}
        assert metrics["recent_capability_ids"] == "FOS-005"
