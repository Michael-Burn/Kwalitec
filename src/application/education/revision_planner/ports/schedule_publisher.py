"""SchedulePublisher — publish StudySchedule results outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.education.revision_planner.models.study_schedule import StudySchedule


class SchedulePublisher(ABC):
    """Outbound port for publishing a completed study schedule.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning or schedule composition.
    """

    @abstractmethod
    def publish_schedule(self, schedule: StudySchedule) -> None:
        """Publish ``schedule`` to downstream consumers.

        Raises:
            application.errors.ApplicationError: On coordination failure.
        """
