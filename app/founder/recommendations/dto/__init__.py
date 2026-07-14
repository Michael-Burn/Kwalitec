"""DTOs for Founder Recommendation Engine (FOS-006)."""

from __future__ import annotations

from app.founder.recommendations.dto.outcome import RuleOutcome
from app.founder.recommendations.dto.validation import (
    RecommendationValidationError,
    ValidationIssue,
    ValidationReport,
)

__all__ = [
    "RecommendationValidationError",
    "RuleOutcome",
    "ValidationIssue",
    "ValidationReport",
]
