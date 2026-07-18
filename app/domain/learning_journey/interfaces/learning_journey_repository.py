"""Repository contract for Learning Journey persistence.

Interface only — no implementation. Future application / infrastructure
layers provide concrete adapters. Domain remains free of Flask and ORM.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.learning_journey.entities.learning_journey import LearningJourney


class LearningJourneyRepository(ABC):
    """Persistence port for LearningJourney aggregates.

    Implementations belong outside ``app/domain/``. This contract does not
    imply SQLAlchemy models or migrations exist yet.
    """

    @abstractmethod
    def get_by_id(self, journey_id: str) -> LearningJourney | None:
        """Load a journey by identity, or None if absent."""

    @abstractmethod
    def get_by_learner_and_topic(
        self,
        learner_id: str,
        topic_id: str,
        *,
        curriculum_id: str | None = None,
    ) -> LearningJourney | None:
        """Load the active or latest journey for a learner + topic pair."""

    @abstractmethod
    def list_for_learner(
        self,
        learner_id: str,
        *,
        curriculum_id: str | None = None,
    ) -> list[LearningJourney]:
        """List journeys owned by the learner (optionally curriculum-scoped)."""

    @abstractmethod
    def save(self, journey: LearningJourney) -> None:
        """Persist a journey aggregate (create or replace)."""

    @abstractmethod
    def delete(self, journey_id: str) -> bool:
        """Remove a journey by identity. Returns True when a row was removed."""
