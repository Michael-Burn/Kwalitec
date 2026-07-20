"""SQLAlchemy adapter for OrchestratorRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import OrchestratorRepository
from domain.education.foundation.ids import OrchestratorId
from domain.education.orchestrator import EducationalOrchestrator
from infrastructure.persistence.dto.orchestrator import OrchestratorDTO
from infrastructure.persistence.mappers.orchestrator_mapper import OrchestratorMapper
from infrastructure.persistence.sqlalchemy.models.orchestrator import OrchestratorModel
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


class SqlAlchemyOrchestratorRepository(OrchestratorRepository):
    """Persist EducationalOrchestrator aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, orchestrator_id: OrchestratorId) -> EducationalOrchestrator | None:
        row = get_by_pk(self._session, OrchestratorModel, orchestrator_id.value)
        if row is None:
            return None
        return OrchestratorMapper.to_domain(dto_from_model(OrchestratorDTO, row))

    def list_by_student(self, student_id: str) -> list[EducationalOrchestrator]:
        rows = list_by_student(self._session, OrchestratorModel, student_id)
        return [
            OrchestratorMapper.to_domain(dto_from_model(OrchestratorDTO, row))
            for row in rows
        ]

    def save(self, orchestrator: EducationalOrchestrator) -> None:
        self._on_save(orchestrator)
        dto = OrchestratorMapper.to_persistence(orchestrator)
        upsert(self._session, model_from_dto(OrchestratorModel, dto))
