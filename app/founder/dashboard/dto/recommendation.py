"""Recommendation presentation DTOs for Founder Dashboard (FSI-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecommendationCard:
    """One recommendation row for dashboard display."""

    recommendation_id: str
    priority: str
    title: str
    category: str
    explanation: str


@dataclass(frozen=True)
class RecommendationsSection:
    """Top recommendations panel (presentation only — no rule evaluation)."""

    available: bool
    overall_status: str
    count: int
    top: tuple[RecommendationCard, ...]
