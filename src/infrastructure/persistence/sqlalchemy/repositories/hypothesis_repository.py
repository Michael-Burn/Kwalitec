"""SQLAlchemy adapter for HypothesisRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import HypothesisRepository
from domain.education.foundation.ids import HypothesisId
from domain.education.hypothesis import EducationalHypothesis
from infrastructure.persistence.dto.hypothesis import HypothesisDTO
from infrastructure.persistence.mappers.hypothesis_mapper import HypothesisMapper
from infrastructure.persistence.sqlalchemy.models.hypothesis import HypothesisModel
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


class SqlAlchemyHypothesisRepository(HypothesisRepository):
    """Persist EducationalHypothesis aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, hypothesis_id: HypothesisId) -> EducationalHypothesis | None:
        row = get_by_pk(self._session, HypothesisModel, hypothesis_id.value)
        if row is None:
            return None
        return HypothesisMapper.to_domain(dto_from_model(HypothesisDTO, row))

    def list_by_student(self, student_id: str) -> list[EducationalHypothesis]:
        rows = list_by_student(self._session, HypothesisModel, student_id)
        return [
            HypothesisMapper.to_domain(dto_from_model(HypothesisDTO, row))
            for row in rows
        ]

    def save(self, hypothesis: EducationalHypothesis) -> None:
        self._on_save(hypothesis)
        dto = HypothesisMapper.to_persistence(hypothesis)
        upsert(self._session, model_from_dto(HypothesisModel, dto))
