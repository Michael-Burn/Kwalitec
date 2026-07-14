"""Unit tests for priority sorting (FOS-006)."""

from __future__ import annotations

from app.founder.recommendations.config import (
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
)
from app.founder.recommendations.tests.helpers import make_engine, make_state


class TestPrioritySorting:
    def test_recommendations_sorted_critical_to_low(self) -> None:
        state = make_state(
            knowledge_overrides={"tests_pass": False},
            capability_overrides={
                "archive_inconsistencies": 1,
                "active_count": 0,
                "completed_count": 1,
                "total_count": 1,
            },
            alpha_overrides={
                "feedback_count": 10,
                "duplicate_count": 5,
            },
        )
        result = make_engine().evaluate(state)
        priorities = [r.priority for r in result.recommendations]
        ranks = {
            PRIORITY_CRITICAL: 0,
            PRIORITY_HIGH: 1,
            PRIORITY_MEDIUM: 2,
            PRIORITY_LOW: 3,
        }
        assert priorities == sorted(priorities, key=lambda p: ranks[p])
        # Critical rules should appear before High / Medium
        assert priorities[0] == PRIORITY_CRITICAL
        assert PRIORITY_MEDIUM in priorities
        assert priorities.index(PRIORITY_MEDIUM) > priorities.index(PRIORITY_HIGH)
