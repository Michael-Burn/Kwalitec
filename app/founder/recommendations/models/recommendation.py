"""Immutable recommendation models (FOS-006).

Advisory cargo only — recommendations never authorise releases or mutations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RecommendationEvidence:
    """One metric citation backing a recommendation."""

    source: str
    metric: str
    value: str | int | float | bool


@dataclass(frozen=True)
class Recommendation:
    """A single founder recommendation produced by a rule + template."""

    id: str
    category: str
    priority: str
    title: str
    explanation: str
    rationale: str
    evidence: tuple[RecommendationEvidence, ...]
    created_at: datetime


@dataclass(frozen=True)
class RecommendationSet:
    """Immutable set of recommendations for one operational snapshot."""

    snapshot_version: str
    generated_at: datetime
    recommendations: tuple[Recommendation, ...]
    overall_status: str
