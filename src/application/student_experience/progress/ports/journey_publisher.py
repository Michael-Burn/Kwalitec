"""JourneyPublisher — publish composed journey artefacts outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.progress.models.learning_journey_view_model import (
    LearningJourneyViewModel,
)


class JourneyPublisher(ABC):
    """Outbound port for publishing composed journey views.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning.
    """

    @abstractmethod
    def publish_journey(self, journey: LearningJourneyViewModel) -> None:
        """Publish a composed ``LearningJourneyViewModel``."""

    @abstractmethod
    def publish_snapshot(self, snapshot: JourneySnapshot) -> None:
        """Publish a composed ``JourneySnapshot``."""
