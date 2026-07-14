"""Intermediate rule outcomes before template rendering (FOS-006)."""

from __future__ import annotations

from dataclasses import dataclass

from app.founder.recommendations.models import RecommendationEvidence


@dataclass(frozen=True)
class RuleOutcome:
    """Signal from a fired rule — wording comes from a template later.

    Rules decide *whether* and *why* to recommend. Templates decide *how*
    to phrase the recommendation. ``template_id`` becomes ``Recommendation.id``.
    """

    rule_id: str
    template_id: str
    category: str
    priority: str
    evidence: tuple[RecommendationEvidence, ...]
