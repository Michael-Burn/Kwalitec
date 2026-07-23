"""CoachContextPublisher — publish composed CoachContext outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.coach.models.coach_context import CoachContext
from application.student_experience.coach.models.coach_snapshot import CoachSnapshot


class CoachContextPublisher(ABC):
    """Outbound port for publishing structured coaching context.

    Implementations live in infrastructure. Downstream LLM adapters may
    consume published context — this package never invokes an LLM.
    """

    @abstractmethod
    def publish_context(self, context: CoachContext) -> None:
        """Publish a composed ``CoachContext``."""

    @abstractmethod
    def publish_snapshot(self, snapshot: CoachSnapshot) -> None:
        """Publish a composed ``CoachSnapshot``."""
