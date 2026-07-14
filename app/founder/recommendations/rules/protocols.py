"""RecommendationRule protocol (FOS-006).

Each rule independently evaluates FounderOperationalState and optionally
returns a RuleOutcome. No monolithic condition trees in the engine.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.dto import RuleOutcome


@runtime_checkable
class RecommendationRule(Protocol):
    """Evaluate operational state and optionally emit a rule outcome."""

    @property
    def rule_id(self) -> str:
        """Stable identifier for this rule."""

    def evaluate(self, state: FounderOperationalState) -> RuleOutcome | None:
        """Return a RuleOutcome when the rule fires, otherwise None.

        Args:
            state: Immutable Founder Operational State snapshot.

        Returns:
            RuleOutcome with template_id / priority / evidence, or None.
        """
