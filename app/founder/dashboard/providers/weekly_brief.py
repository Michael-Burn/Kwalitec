"""Weekly Brief provider — wraps FOS-007 public service (FSI-002)."""

from __future__ import annotations

import logging
from typing import Protocol

from app.founder.briefing import (
    FounderWeeklyBrief,
    FounderWeeklyBriefingService,
)
from app.founder.operational_state import FounderOperationalState
from app.founder.recommendations import RecommendationSet

logger = logging.getLogger(__name__)


class WeeklyBriefServiceGate(Protocol):
    """Minimal surface required from FounderWeeklyBriefingService."""

    def generate_brief(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
        *,
        generated_at=None,
        output_dir=None,
    ) -> FounderWeeklyBrief:
        """Return an in-memory FounderWeeklyBrief."""


class WeeklyBriefProvider:
    """Retrieve FounderWeeklyBrief metadata for dashboard presentation.

    Does not export files. Does not author sections. Gateway only.
    """

    def __init__(
        self, *, service: WeeklyBriefServiceGate | None = None
    ) -> None:
        self._service: WeeklyBriefServiceGate = (
            service or FounderWeeklyBriefingService()
        )

    def get_brief(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
    ) -> FounderWeeklyBrief | None:
        """Return the weekly brief, or None on failure.

        Always requests an in-memory brief (no ``output_dir``) so the
        dashboard never writes briefing artefacts.
        """
        try:
            return self._service.generate_brief(state, recommendation_set)
        except Exception:
            logger.exception("Founder Dashboard: weekly brief unavailable")
            return None
