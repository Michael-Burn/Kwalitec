"""SQLAlchemy adapter for EvidenceRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import EvidenceRepository
from domain.education.evidence import EvidenceRecord
from domain.education.foundation.ids import EvidenceId
from infrastructure.persistence.dto.evidence import EvidenceRecordDTO
from infrastructure.persistence.mappers.evidence_mapper import EvidenceMapper
from infrastructure.persistence.sqlalchemy.models.evidence import EvidenceModel
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


class SqlAlchemyEvidenceRepository(EvidenceRepository):
    """Persist EvidenceRecord aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, evidence_id: EvidenceId) -> EvidenceRecord | None:
        row = get_by_pk(self._session, EvidenceModel, evidence_id.value)
        if row is None:
            return None
        return EvidenceMapper.to_domain(dto_from_model(EvidenceRecordDTO, row))

    def list_by_student(self, student_id: str) -> list[EvidenceRecord]:
        rows = list_by_student(self._session, EvidenceModel, student_id)
        return [
            EvidenceMapper.to_domain(dto_from_model(EvidenceRecordDTO, row))
            for row in rows
        ]

    def save(self, evidence: EvidenceRecord) -> None:
        self._on_save(evidence)
        dto = EvidenceMapper.to_persistence(evidence)
        upsert(self._session, model_from_dto(EvidenceModel, dto))
