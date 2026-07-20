"""SQLAlchemy adapter for DecisionRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import DecisionRepository
from domain.education.decision import EducationalDecision
from domain.education.foundation.ids import DecisionId
from infrastructure.persistence.dto.decision import DecisionDTO
from infrastructure.persistence.mappers.decision_mapper import DecisionMapper
from infrastructure.persistence.sqlalchemy.models.decision import DecisionModel
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


class SqlAlchemyDecisionRepository(DecisionRepository):
    """Persist EducationalDecision aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, decision_id: DecisionId) -> EducationalDecision | None:
        row = get_by_pk(self._session, DecisionModel, decision_id.value)
        if row is None:
            return None
        return DecisionMapper.to_domain(dto_from_model(DecisionDTO, row))

    def list_by_student(self, student_id: str) -> list[EducationalDecision]:
        rows = list_by_student(self._session, DecisionModel, student_id)
        return [
            DecisionMapper.to_domain(dto_from_model(DecisionDTO, row))
            for row in rows
        ]

    def save(self, decision: EducationalDecision) -> None:
        self._on_save(decision)
        dto = DecisionMapper.to_persistence(decision)
        upsert(self._session, model_from_dto(DecisionModel, dto))
