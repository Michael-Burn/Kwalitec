"""MissionPublisher — publish MissionPlan results outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.education.mission_generation.models.mission_plan import MissionPlan


class MissionPublisher(ABC):
    """Outbound port for publishing a completed mission plan.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning or mission composition.
    """

    @abstractmethod
    def publish_missions(self, mission_plan: MissionPlan) -> None:
        """Publish ``mission_plan`` to downstream consumers.

        Raises:
            application.errors.ApplicationError: On coordination failure.
        """
