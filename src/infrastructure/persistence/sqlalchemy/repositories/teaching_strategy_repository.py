"""SQLAlchemy adapter for TeachingStrategyRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import TeachingStrategyRepository
from domain.education.foundation.ids import TeachingStrategyId
from domain.education.teaching_strategy import TeachingStrategy
from infrastructure.persistence.dto.teaching_strategy import TeachingStrategyDTO
from infrastructure.persistence.mappers.teaching_strategy_mapper import (
    TeachingStrategyMapper,
)
from infrastructure.persistence.sqlalchemy.models.teaching_strategy import (
    TeachingStrategyModel,
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


class SqlAlchemyTeachingStrategyRepository(TeachingStrategyRepository):
    """Persist TeachingStrategy aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, strategy_id: TeachingStrategyId) -> TeachingStrategy | None:
        row = get_by_pk(self._session, TeachingStrategyModel, strategy_id.value)
        if row is None:
            return None
        return TeachingStrategyMapper.to_domain(
            dto_from_model(TeachingStrategyDTO, row)
        )

    def list_by_student(self, student_id: str) -> list[TeachingStrategy]:
        rows = list_by_student(self._session, TeachingStrategyModel, student_id)
        return [
            TeachingStrategyMapper.to_domain(
                dto_from_model(TeachingStrategyDTO, row)
            )
            for row in rows
        ]

    def save(self, strategy: TeachingStrategy) -> None:
        self._on_save(strategy)
        dto = TeachingStrategyMapper.to_persistence(strategy)
        upsert(self._session, model_from_dto(TeachingStrategyModel, dto))
