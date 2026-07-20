"""SQLAlchemy adapter for SubjectKnowledgeRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import SubjectKnowledgeRepository
from domain.education.foundation.ids import ConceptId
from domain.education.subject_knowledge import Concept
from infrastructure.persistence.dto.subject_knowledge import ConceptDTO
from infrastructure.persistence.mappers.subject_knowledge_mapper import (
    SubjectKnowledgeMapper,
)
from infrastructure.persistence.sqlalchemy.models.subject_knowledge import ConceptModel
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


class SqlAlchemySubjectKnowledgeRepository(SubjectKnowledgeRepository):
    """Persist Concept aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get_concept(self, concept_id: ConceptId) -> Concept | None:
        row = get_by_pk(self._session, ConceptModel, concept_id.value)
        if row is None:
            return None
        return SubjectKnowledgeMapper.to_domain(dto_from_model(ConceptDTO, row))

    def save_concept(self, concept: Concept) -> None:
        self._on_save(concept)
        dto = SubjectKnowledgeMapper.to_persistence(concept)
        upsert(self._session, model_from_dto(ConceptModel, dto))

    def exists(self, concept_id: ConceptId) -> bool:
        return get_by_pk(self._session, ConceptModel, concept_id.value) is not None
