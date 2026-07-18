"""Learning Journey Engine port consumed by Mission Engine 2.0."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.application.learning_journey.dto.journey_snapshot import JourneySnapshot
from app.application.learning_journey.dto.recommendation_result import (
    RecommendationResult,
)
from app.application.learning_journey.dto.session_plan import SessionPlan


@runtime_checkable
class JourneyEnginePort(Protocol):
    """Structural contract for Learning Journey Engine reads.

    Mission Engine 2.0 may snapshot, plan sessions, and read recommendations.
    It must never drive journey progression or Topic Complete.
    """

    def snapshot(self, journey_id: str) -> JourneySnapshot:
        """Return an immutable educational snapshot for ``journey_id``."""

    def session_plan_for(self, journey_id: str) -> SessionPlan | None:
        """Return the deterministic next/current session plan, if any."""

    def recommendation_for(self, journey_id: str) -> RecommendationResult | None:
        """Return the latest advisory recommendation, if any."""
