"""Shared builders for Founder Recommendation Engine tests (FOS-006).

Mock Operational State only — no filesystem, no Dashboard.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from app.founder.operational_state.models import FounderOperationalState
from app.founder.operational_state.tests.helpers import (
    FIXED_NOW,
    make_alpha_dto,
    make_builder,
    make_capability_dto,
    make_knowledge_dto,
)
from app.founder.recommendations.evaluators import RecommendationEngine
from app.founder.recommendations.services import FounderRecommendationService

RECOMMENDATION_NOW = datetime(2026, 7, 14, 15, 0, 0, tzinfo=UTC)


def make_state(**section_overrides) -> FounderOperationalState:
    """Build a valid FounderOperationalState with optional section tweaks.

    Keyword args may include:
    - knowledge / capability / alpha DTO field overrides via
      ``knowledge_overrides``, ``capability_overrides``, ``alpha_overrides``
    - or direct section replaces via ``engineering``, ``capability``, etc.
    """
    knowledge_overrides = section_overrides.pop("knowledge_overrides", {})
    capability_overrides = section_overrides.pop("capability_overrides", {})
    alpha_overrides = section_overrides.pop("alpha_overrides", {})

    state = make_builder().build(
        make_knowledge_dto(**knowledge_overrides),
        make_capability_dto(**capability_overrides),
        make_alpha_dto(**alpha_overrides),
        generated_at=FIXED_NOW,
        validate=True,
    )
    if section_overrides:
        state = replace(state, **section_overrides)
    return state


def make_healthy_state() -> FounderOperationalState:
    """State that should fire no Version 1 recommendations."""
    return make_state(
        # Default helpers: feedback=7, duplicates=2 (below threshold),
        # archive_inconsistencies=0, tests_pass=True, active_count=1.
    )


def make_engine(**kwargs) -> RecommendationEngine:
    return RecommendationEngine(clock=lambda: RECOMMENDATION_NOW, **kwargs)


def make_service(**kwargs) -> FounderRecommendationService:
    return FounderRecommendationService(clock=lambda: RECOMMENDATION_NOW, **kwargs)
