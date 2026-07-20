"""Recommendation Engine — deterministic Educational OS recommendations.

EDU-004: Generate RecommendationSpecifications from Digital Twin,
MissionSpecification, StudyPlan, ProgressReport, Diagnosis, Educational
Priority, and Teaching Strategy.

Recommendations are educational decisions, not UI hints.

Pure domain logic only. No AI, no prompting, no randomness, no persistence,
Flask, ORM, HTTP, or DTOs.
"""

from __future__ import annotations

from domain.recommendation.enums import (
    RecommendationCategory,
    RecommendationPriorityBand,
    RecommendationReasonCode,
    SupportingEvidenceCode,
)
from domain.recommendation.ids import RecommendationId, RecommendationSpecificationId
from domain.recommendation.recommendation import (
    Recommendation,
    RecommendationConfidence,
    SupportingEvidence,
)
from domain.recommendation.recommendation_generator import (
    RecommendationGenerator,
    category_rank,
    confidence_from_millipoints,
    map_priority_band,
)
from domain.recommendation.recommendation_priority import RecommendationPriority
from domain.recommendation.recommendation_reason import RecommendationReason
from domain.recommendation.recommendation_specification import (
    RecommendationSpecification,
)

__all__ = [
    # Aggregate / specification
    "RecommendationSpecification",
    "Recommendation",
    "SupportingEvidence",
    "RecommendationConfidence",
    # Value objects
    "RecommendationPriority",
    "RecommendationReason",
    # Identities
    "RecommendationSpecificationId",
    "RecommendationId",
    # Enums
    "RecommendationCategory",
    "RecommendationPriorityBand",
    "RecommendationReasonCode",
    "SupportingEvidenceCode",
    # Generator
    "RecommendationGenerator",
    "map_priority_band",
    "category_rank",
    "confidence_from_millipoints",
]
