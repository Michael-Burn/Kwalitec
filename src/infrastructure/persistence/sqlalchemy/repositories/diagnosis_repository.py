"""SQLAlchemy adapter for DiagnosisRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import DiagnosisRepository
from domain.education.diagnosis import EducationalDiagnosis
from domain.education.foundation.ids import DiagnosisId
from infrastructure.persistence.dto.diagnosis import DiagnosisDTO
from infrastructure.persistence.mappers.diagnosis_mapper import DiagnosisMapper
from infrastructure.persistence.sqlalchemy.models.diagnosis import DiagnosisModel
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


class SqlAlchemyDiagnosisRepository(DiagnosisRepository):
    """Persist EducationalDiagnosis aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, diagnosis_id: DiagnosisId) -> EducationalDiagnosis | None:
        row = get_by_pk(self._session, DiagnosisModel, diagnosis_id.value)
        if row is None:
            return None
        return DiagnosisMapper.to_domain(dto_from_model(DiagnosisDTO, row))

    def list_by_student(self, student_id: str) -> list[EducationalDiagnosis]:
        rows = list_by_student(self._session, DiagnosisModel, student_id)
        return [
            DiagnosisMapper.to_domain(dto_from_model(DiagnosisDTO, row))
            for row in rows
        ]

    def save(self, diagnosis: EducationalDiagnosis) -> None:
        self._on_save(diagnosis)
        dto = DiagnosisMapper.to_persistence(diagnosis)
        upsert(self._session, model_from_dto(DiagnosisModel, dto))
