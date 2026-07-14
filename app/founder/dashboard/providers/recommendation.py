"""Recommendation provider — wraps FOS-006 public service (FSI-002)."""

from __future__ import annotations

import logging
from typing import Protocol

from app.founder.operational_state import FounderOperationalState
from app.founder.recommendations import (
    FounderRecommendationService,
    RecommendationSet,
)

logger = logging.getLogger(__name__)


class RecommendationServiceGate(Protocol):
    """Minimal surface required from FounderRecommendationService."""

    def recommend(self, state: FounderOperationalState) -> RecommendationSet:
        """Return a RecommendationSet for ``state``."""


class RecommendationProvider:
    """Retrieve RecommendationSet for dashboard presentation.

    Does not implement rules. Does not score. Presentation gateway only.
    """

    def __init__(
        self, *, service: RecommendationServiceGate | None = None
    ) -> None:
        self._service: RecommendationServiceGate = (
            service or FounderRecommendationService()
        )

    def get_recommendations(
        self, state: FounderOperationalState
    ) -> RecommendationSet | None:
        """Return recommendations for ``state``, or None on failure."""
        try:
            return self._service.recommend(state)
        except Exception:
            logger.exception(
                "Founder Dashboard: recommendation set unavailable"
            )
            return None
