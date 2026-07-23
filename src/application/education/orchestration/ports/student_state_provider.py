"""StudentStateProvider — load StudentEducationalState for orchestration."""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.education.student_state.aggregates.student_educational_state import (
    StudentEducationalState,
)


class StudentStateProvider(ABC):
    """Outbound port for reading a student's current educational state.

    Implementations live in infrastructure. This package defines the
    interface only — no SQLAlchemy, no repositories here.
    """

    @abstractmethod
    def get_student_state(self, student_id: str) -> StudentEducationalState:
        """Return the current ``StudentEducationalState`` for ``student_id``.

        Raises:
            application.errors.NotFoundError: When no state exists.
            application.errors.ApplicationError: On coordination failure.
        """
