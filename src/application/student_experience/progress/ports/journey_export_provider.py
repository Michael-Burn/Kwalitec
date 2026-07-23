"""JourneyExportProvider — export composed journey artefacts."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.progress.models.learning_journey_view_model import (
    LearningJourneyViewModel,
)


class JourneyExportProvider(ABC):
    """Outbound port for exporting journey projections.

    Implementations live in infrastructure. Export is presentation /
    delivery wiring — never educational reasoning.
    """

    @abstractmethod
    def export_journey(self, journey: LearningJourneyViewModel) -> str:
        """Export a composed journey into a transport-safe representation."""

    @abstractmethod
    def export_snapshot(self, snapshot: JourneySnapshot) -> str:
        """Export a journey snapshot into a transport-safe representation."""
