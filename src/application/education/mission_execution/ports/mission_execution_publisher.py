"""MissionExecutionPublisher — publish execution results outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.education.mission_execution.events import MissionExecutionEvent
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)


class MissionExecutionPublisher(ABC):
    """Outbound port for publishing mission execution state / events.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning.
    """

    @abstractmethod
    def publish_execution(self, execution: MissionExecution) -> None:
        """Publish the current execution aggregate."""

    @abstractmethod
    def publish_event(self, event: MissionExecutionEvent) -> None:
        """Publish a single immutable execution event."""
