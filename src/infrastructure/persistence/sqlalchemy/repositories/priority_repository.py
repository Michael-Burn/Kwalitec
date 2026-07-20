"""SQLAlchemy adapter for PriorityRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import PriorityRepository
from domain.education.foundation.ids import PriorityId
from domain.education.priority import EducationalPriority
from infrastructure.persistence.dto.priority import PriorityDTO
from infrastructure.persistence.mappers.priority_mapper import PriorityMapper
from infrastructure.persistence.sqlalchemy.models.priority import PriorityModel
from infrastructure.persistence.sqlalchemy.repositories._ops import (
    AggregateTracker,
    _noop_tracker,
    get_by_pk,
    list_by_student,
    upsert,
)
from infrastructure.persistence.sqlalchemy.repositories.row_codec import (
    dto_from_model,
    model_from_dto,
)


class SqlAlchemyPriorityRepository(PriorityRepository):
    """Persist EducationalPriority aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, priority_id: PriorityId) -> EducationalPriority | None:
        row = get_by_pk(self._session, PriorityModel, priority_id.value)
        if row is None:
            return None
        return PriorityMapper.to_domain(dto_from_model(PriorityDTO, row))

    def list_by_student(self, student_id: str) -> list[EducationalPriority]:
        rows = list_by_student(self._session, PriorityModel, student_id)
        return [
            PriorityMapper.to_domain(dto_from_model(PriorityDTO, row))
            for row in rows
        ]

    def save(self, priority: EducationalPriority) -> None:
        self._on_save(priority)
        dto = PriorityMapper.to_persistence(priority)
        upsert(self._session, model_from_dto(PriorityModel, dto))
