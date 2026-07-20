"""SQLAlchemy adapter for TeachingPlanRepository."""

from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from application.ports.repositories import TeachingPlanRepository
from domain.education.foundation.ids import LearningEpisodeId
from infrastructure.persistence.sqlalchemy.models.teaching_plan import TeachingPlanModel
from infrastructure.persistence.sqlalchemy.repositories._ops import get_by_pk, upsert


class SqlAlchemyTeachingPlanRepository(TeachingPlanRepository):
    """Persist plan ↔ episode coordination bindings via SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_episode_id(self, plan_id: str) -> LearningEpisodeId | None:
        row = get_by_pk(self._session, TeachingPlanModel, plan_id)
        if row is None:
            return None
        return LearningEpisodeId(row.episode_id)

    def get_plan_id(self, episode_id: LearningEpisodeId) -> str | None:
        statement = select(TeachingPlanModel).where(
            TeachingPlanModel.episode_id == episode_id.value
        )
        row = self._session.scalars(statement).first()
        if row is None:
            return None
        return row.plan_id

    def save(self, plan_id: str, episode_id: LearningEpisodeId) -> None:
        self._session.execute(
            delete(TeachingPlanModel).where(
                TeachingPlanModel.episode_id == episode_id.value,
                TeachingPlanModel.plan_id != plan_id,
            )
        )
        upsert(
            self._session,
            TeachingPlanModel(plan_id=plan_id, episode_id=episode_id.value),
        )
