"""RecommendationPublisher — publish RecommendationSet results outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)


class RecommendationPublisher(ABC):
    """Outbound port for publishing a completed recommendation set.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning.
    """

    @abstractmethod
    def publish_recommendations(
        self, recommendation_set: RecommendationSet
    ) -> None:
        """Publish ``recommendation_set`` to downstream consumers.

        Raises:
            application.errors.ApplicationError: On coordination failure.
        """
