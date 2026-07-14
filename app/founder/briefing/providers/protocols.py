"""Provider protocols for Founder Weekly Briefing (FOS-007)."""

from __future__ import annotations

from typing import Protocol

from app.founder.briefing.models import BriefSection
from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.models import RecommendationSet


class SectionBuilder(Protocol):
    """Callable that builds one BriefSection from briefing inputs."""

    def __call__(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
        *,
        order: int,
    ) -> BriefSection: ...
