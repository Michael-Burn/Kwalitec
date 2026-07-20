"""RecommendationReadModel — presentation projection of today's recommendation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecommendationReadModel:
    """UI-ready recommendation card. Never carries domain aggregates."""

    title: str
    subtitle: str | None
    primary_action: str | None
    reason_summary: str | None
    estimated_minutes: int | None
    can_start: bool
    decision_id: str | None = None
    recommendation_id: str | None = None
