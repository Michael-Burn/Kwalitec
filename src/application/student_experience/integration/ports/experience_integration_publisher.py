"""Outbound ports for Experience Integration publishing."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
    ExperienceSnapshotBundle,
)


class ExperienceIntegrationPublisher(ABC):
    """Publish continuous-journey compositions for downstream surfaces."""

    @abstractmethod
    def publish_journey(self, journey: ExperienceJourneyViewModel) -> None:
        """Publish a full experience journey view model."""

    @abstractmethod
    def publish_bundle(self, bundle: ExperienceSnapshotBundle) -> None:
        """Publish a compact cross-module snapshot bundle."""
