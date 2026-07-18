"""Repository contract for Curriculum structure persistence.

Interface only — no implementation. Future application / infrastructure
layers provide concrete adapters. Domain remains free of Flask and ORM.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.curriculum.entities.curriculum import Curriculum
from app.domain.curriculum.value_objects.curriculum_id import CurriculumId


class CurriculumRepository(ABC):
    """Persistence port for Curriculum aggregates.

    Implementations belong outside ``app/domain/``. This contract does not
    imply SQLAlchemy models or migrations exist yet.
    """

    @abstractmethod
    def get_by_id(
        self, curriculum_id: str | CurriculumId
    ) -> Curriculum | None:
        """Load a curriculum by identity, or None if absent."""

    @abstractmethod
    def list_all(self) -> list[Curriculum]:
        """List all curricula known to the store."""

    @abstractmethod
    def save(self, curriculum: Curriculum) -> None:
        """Persist a curriculum aggregate (create or replace)."""

    @abstractmethod
    def delete(self, curriculum_id: str | CurriculumId) -> bool:
        """Remove a curriculum by identity. Returns True when removed."""
