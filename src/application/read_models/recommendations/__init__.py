"""Recommendation read models and projection builders."""

from __future__ import annotations

from application.read_models.recommendations.projection_builder import (
    RecommendationProjectionBuilder,
)
from application.read_models.recommendations.recommendation_read_model import (
    RecommendationReadModel,
)

__all__ = [
    "RecommendationProjectionBuilder",
    "RecommendationReadModel",
]
