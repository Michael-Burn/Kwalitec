"""AssessmentPublisher — publish MasteryAssessment results outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)


class AssessmentPublisher(ABC):
    """Outbound port for publishing a completed mastery assessment.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning.
    """

    @abstractmethod
    def publish_assessment(self, assessment: MasteryAssessment) -> None:
        """Publish ``assessment`` to downstream consumers.

        Raises:
            application.errors.ApplicationError: On coordination failure.
        """
