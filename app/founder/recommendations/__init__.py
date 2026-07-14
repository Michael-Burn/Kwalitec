"""Founder Recommendation Engine (FOS-006).

Consumes immutable FounderOperationalState snapshots and produces
deterministic, rule-based founder recommendations.

Version 1 is advisory only — no AI, no LLMs, no release automation.
"""

from __future__ import annotations

from app.founder.recommendations.models import (
    Recommendation,
    RecommendationEvidence,
    RecommendationSet,
)
from app.founder.recommendations.services import FounderRecommendationService

__all__ = [
    "FounderRecommendationService",
    "Recommendation",
    "RecommendationEvidence",
    "RecommendationSet",
]
