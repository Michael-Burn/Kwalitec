"""Immutable domain models for Founder Recommendation Engine (FOS-006)."""

from __future__ import annotations

from app.founder.recommendations.models.recommendation import (
    Recommendation,
    RecommendationEvidence,
    RecommendationSet,
)

__all__ = [
    "Recommendation",
    "RecommendationEvidence",
    "RecommendationSet",
]
