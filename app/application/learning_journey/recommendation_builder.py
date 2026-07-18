"""Build educational recommendations from journey state.

Recommendations never imply unsupported mastery and never complete topics.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import uuid4

from app.application.learning_journey.dto.recommendation_result import (
    RecommendationResult,
)
from app.application.learning_journey.policies.recommendation_policy import (
    RecommendationPolicy,
)
from app.domain.learning_journey.entities.journey_recommendation import (
    JourneyRecommendation,
    RecommendationLifecycle,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney


class RecommendationBuilder:
    """Produce explainable educational recommendations (deterministic)."""

    def __init__(
        self,
        *,
        policy: RecommendationPolicy | None = None,
        id_factory: Callable[[], str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Wire policy and optional identity / time factories for tests.

        Args:
            policy: Recommendation rules (defaults to RecommendationPolicy).
            id_factory: Callable returning recommendation ids.
            clock: Callable returning aware datetimes.
        """
        self._policy = policy or RecommendationPolicy()
        self._id_factory = id_factory or (lambda: f"rec-{uuid4().hex[:12]}")
        self._clock = clock or (lambda: datetime.now(tz=UTC))

    def build(self, journey: LearningJourney) -> RecommendationResult:
        """Generate a RecommendationResult for ``journey``.

        Does not mutate the journey. Caller may attach the recommendation
        artefact via domain ``with_recommendation``.
        """
        decision = self._policy.decide(journey)
        if decision.kind is None:
            return RecommendationResult(
                recommendation=None,
                kind=None,
                reason=decision.reason,
                confidence_explanation=decision.confidence_explanation,
                rationale_tags=decision.rationale_tags,
                certainty=decision.certainty,
            )

        recommendation = JourneyRecommendation.create(
            self._id_factory(),
            journey.journey_id,
            decision.kind,
            lifecycle=RecommendationLifecycle.PROPOSED,
            certainty=decision.certainty,
            rationale_tags=list(decision.rationale_tags),
            session_id=decision.session_id,
            objective_id=decision.objective_id,
            created_at=self._clock(),
        )
        return RecommendationResult(
            recommendation=recommendation,
            kind=decision.kind,
            reason=decision.reason,
            confidence_explanation=decision.confidence_explanation,
            rationale_tags=decision.rationale_tags,
            certainty=decision.certainty,
        )

    def build_and_attach(
        self,
        journey: LearningJourney,
    ) -> tuple[LearningJourney, RecommendationResult]:
        """Build a recommendation and append it to the journey aggregate."""
        result = self.build(journey)
        if result.recommendation is None:
            return journey, result
        updated = journey.with_recommendation(result.recommendation)
        return updated, result
