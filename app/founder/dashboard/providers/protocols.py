"""Provider protocols for Founder Dashboard live integration (FSI-002).

The dashboard consumes only these provider interfaces. Providers wrap
Founder public services; tests inject stubs so no repository access is required.
"""

from __future__ import annotations

from typing import Protocol

from app.founder.briefing import FounderWeeklyBrief
from app.founder.operational_state import FounderOperationalState
from app.founder.recommendations import RecommendationSet


class OperationalStateGate(Protocol):
    """Public read surface for Founder Operational State (FOS-005)."""

    def get_state(self) -> FounderOperationalState | None:
        """Return the current operational snapshot, or None if unavailable."""


class RecommendationGate(Protocol):
    """Public read surface for the Recommendation Engine (FOS-006)."""

    def get_recommendations(
        self, state: FounderOperationalState
    ) -> RecommendationSet | None:
        """Return recommendations for ``state``, or None if unavailable."""


class WeeklyBriefGate(Protocol):
    """Public read surface for Weekly Briefing (FOS-007)."""

    def get_brief(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
    ) -> FounderWeeklyBrief | None:
        """Return the latest weekly brief, or None if unavailable."""
