"""StudyConstraintProvider — supply caller study constraints."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.education.mission_generation.planning_constraints import (
    PlanningConstraints,
)


class StudyConstraintProvider(ABC):
    """Inbound port for study/planning constraints for one student.

    Implementations live in infrastructure (profile, preferences, calendar
    settings). This port never reads StudentEducationalState mastery fields
    and never estimates mastery.
    """

    @abstractmethod
    def constraints_for(self, student_id: str) -> PlanningConstraints:
        """Return planning constraints for ``student_id``."""
