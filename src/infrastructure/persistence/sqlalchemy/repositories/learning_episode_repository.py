"""SQLAlchemy adapter for LearningEpisodeRepository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from application.ports.repositories import LearningEpisodeRepository
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.learning_episode import LearningEpisode
from infrastructure.persistence.dto.learning_episode import LearningEpisodeDTO
from infrastructure.persistence.mappers.learning_episode_mapper import (
    LearningEpisodeMapper,
)
from infrastructure.persistence.sqlalchemy.models.learning_episode import (
    LearningEpisodeModel,
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


class SqlAlchemyLearningEpisodeRepository(LearningEpisodeRepository):
    """Persist LearningEpisode aggregates via SQLAlchemy."""

    def __init__(
        self,
        session: Session,
        on_save: AggregateTracker = _noop_tracker,
    ) -> None:
        self._session = session
        self._on_save = on_save

    def get(self, episode_id: LearningEpisodeId) -> LearningEpisode | None:
        row = get_by_pk(self._session, LearningEpisodeModel, episode_id.value)
        if row is None:
            return None
        return LearningEpisodeMapper.to_domain(
            dto_from_model(LearningEpisodeDTO, row)
        )

    def list_by_student(self, student_id: str) -> list[LearningEpisode]:
        rows = list_by_student(self._session, LearningEpisodeModel, student_id)
        return [
            LearningEpisodeMapper.to_domain(dto_from_model(LearningEpisodeDTO, row))
            for row in rows
        ]

    def save(self, episode: LearningEpisode) -> None:
        self._on_save(episode)
        dto = LearningEpisodeMapper.to_persistence(episode)
        upsert(self._session, model_from_dto(LearningEpisodeModel, dto))
