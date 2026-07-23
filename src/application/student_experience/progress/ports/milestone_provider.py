"""MilestoneProvider — projected milestones for the journey surface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from application.student_experience.progress.enums import JourneyMilestoneKind


@dataclass(frozen=True, slots=True)
class ProvidedMilestone:
    """Immutable milestone supplied by an external provider."""

    milestone_id: str
    kind: JourneyMilestoneKind
    title: str
    description: str
    reached_at: datetime | None = None


class MilestoneProvider(ABC):
    """Outbound port for student milestones.

    Implementations live in infrastructure. Never estimates mastery or
    invents educational awards from raw evidence.
    """

    @abstractmethod
    def list_milestones(
        self, student_id: str, *, limit: int = 10
    ) -> tuple[ProvidedMilestone, ...]:
        """Return milestones for ``student_id``."""
