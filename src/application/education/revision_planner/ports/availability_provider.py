"""AvailabilityProvider — supply student availability windows."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from application.education.revision_planner.student_availability import (
    StudentAvailability,
)


class AvailabilityProvider(ABC):
    """Outbound port for loading student availability.

    Implementations live in infrastructure. Availability lookup is never
    educational reasoning or schedule composition.
    """

    @abstractmethod
    def get_availability(
        self,
        student_id: str,
        *,
        start: date,
        end: date,
    ) -> StudentAvailability:
        """Return availability for ``student_id`` across ``[start, end]``."""
