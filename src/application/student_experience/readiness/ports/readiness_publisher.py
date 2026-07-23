"""ReadinessPublisher — publish composed readiness artefacts outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.readiness.models.exam_readiness_view_model import (
    ExamReadinessViewModel,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)


class ReadinessPublisher(ABC):
    """Outbound port for publishing composed readiness views.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning.
    """

    @abstractmethod
    def publish_readiness(self, readiness: ExamReadinessViewModel) -> None:
        """Publish a composed ``ExamReadinessViewModel``."""

    @abstractmethod
    def publish_snapshot(self, snapshot: ReadinessSnapshot) -> None:
        """Publish a composed ``ReadinessSnapshot``."""
