"""Decision categories — reasoning outputs, not Twin state.

Categories request Twin belief updates. They are not recommendations,
readiness estimates, or Mission priorities.
"""

from __future__ import annotations

from enum import StrEnum


class DecisionCategory(StrEnum):
    """Canonical educational decision categories (AP-002D3)."""

    MASTERY_BELIEF_UPDATE = "mastery_belief_update"
    CONFIDENCE_BELIEF_UPDATE = "confidence_belief_update"
    UNCERTAINTY_PRESERVED = "uncertainty_preserved"
    PROVENANCE_RECORDED = "provenance_recorded"


KNOWN_DECISION_CATEGORIES: frozenset[str] = frozenset(
    category.value for category in DecisionCategory
)


def parse_decision_category(value: str | DecisionCategory) -> DecisionCategory:
    """Parse a category or raise for unknown values (never invent)."""
    if isinstance(value, DecisionCategory):
        return value
    normalised = (value or "").strip()
    if normalised not in KNOWN_DECISION_CATEGORIES:
        from app.domain.reasoning.decisions.errors import UnknownDecisionCategory

        raise UnknownDecisionCategory(f"unknown decision category: {value!r}")
    return DecisionCategory(normalised)
