"""ReadinessExportProvider — export composed readiness artefacts."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.readiness.models.exam_readiness_view_model import (
    ExamReadinessViewModel,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)


class ReadinessExportProvider(ABC):
    """Outbound port for exporting readiness projections.

    Implementations live in infrastructure. Export is presentation /
    delivery wiring — never educational reasoning.
    """

    @abstractmethod
    def export_readiness(self, readiness: ExamReadinessViewModel) -> str:
        """Export a composed readiness view into a transport-safe representation."""

    @abstractmethod
    def export_snapshot(self, snapshot: ReadinessSnapshot) -> str:
        """Export a readiness snapshot into a transport-safe representation."""
