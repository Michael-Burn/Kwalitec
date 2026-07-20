"""SQLAlchemy adapter for DigitalTwinRepository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from application.ports.repositories import DigitalTwinRepository
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.foundation.ids import DigitalTwinId
from infrastructure.persistence.dto.digital_twin import DigitalTwinDTO
from infrastructure.persistence.mappers.digital_twin_mapper import DigitalTwinMapper
from infrastructure.persistence.sqlalchemy.models.digital_twin import DigitalTwinModel
from infrastructure.persistence.sqlalchemy.repositories._ops import (
    AggregateTracker,
    _noop_tracker,
    get_by_pk,
    upsert,
)
from infrastructure.persistence.sqlalchemy.repositories.row_codec import (
    dto_from_model,
    model_from_dto,
)


class SqlAlchemyDigitalTwinRepository(DigitalTwinRepository):
    """Persist EducationalDigitalTwin aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, twin_id: DigitalTwinId) -> EducationalDigitalTwin | None:
        row = get_by_pk(self._session, DigitalTwinModel, twin_id.value)
        if row is None:
            return None
        return DigitalTwinMapper.to_domain(dto_from_model(DigitalTwinDTO, row))

    def get_by_student(self, student_id: str) -> EducationalDigitalTwin | None:
        statement = select(DigitalTwinModel).where(
            DigitalTwinModel.student_id == student_id
        )
        row = self._session.scalars(statement).first()
        if row is None:
            return None
        return DigitalTwinMapper.to_domain(dto_from_model(DigitalTwinDTO, row))

    def save(self, twin: EducationalDigitalTwin) -> None:
        self._on_save(twin)
        dto = DigitalTwinMapper.to_persistence(twin)
        upsert(self._session, model_from_dto(DigitalTwinModel, dto))
