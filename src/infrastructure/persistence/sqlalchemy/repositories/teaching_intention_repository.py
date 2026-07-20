"""SQLAlchemy adapter for TeachingIntentionRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import TeachingIntentionRepository
from domain.education.foundation.ids import TeachingIntentionId
from domain.education.teaching_intention import TeachingIntention
from infrastructure.persistence.dto.teaching_intention import TeachingIntentionDTO
from infrastructure.persistence.mappers.teaching_intention_mapper import (
    TeachingIntentionMapper,
)
from infrastructure.persistence.sqlalchemy.models.teaching_intention import (
    TeachingIntentionModel,
)
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


class SqlAlchemyTeachingIntentionRepository(TeachingIntentionRepository):
    """Persist TeachingIntention aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, intention_id: TeachingIntentionId) -> TeachingIntention | None:
        row = get_by_pk(self._session, TeachingIntentionModel, intention_id.value)
        if row is None:
            return None
        return TeachingIntentionMapper.to_domain(
            dto_from_model(TeachingIntentionDTO, row)
        )

    def list_by_student(self, student_id: str) -> list[TeachingIntention]:
        rows = list_by_student(self._session, TeachingIntentionModel, student_id)
        return [
            TeachingIntentionMapper.to_domain(
                dto_from_model(TeachingIntentionDTO, row)
            )
            for row in rows
        ]

    def save(self, intention: TeachingIntention) -> None:
        self._on_save(intention)
        dto = TeachingIntentionMapper.to_persistence(intention)
        upsert(self._session, model_from_dto(TeachingIntentionModel, dto))
