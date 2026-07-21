"""SQLAlchemy Session Runtime checkpoint repository (BR-004)."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import update
from sqlalchemy.orm import Session

from infrastructure.persistence.dto.onboarding import SessionCheckpointDTO
from infrastructure.persistence.mappers.checkpoint_mapper import CheckpointMapper
from infrastructure.persistence.sqlalchemy.models.session_checkpoint import (
    SessionCheckpointModel,
)
from infrastructure.persistence.sqlalchemy.repositories.row_codec import (
    dto_from_model,
    model_from_dto,
)
from infrastructure.persistence.user_repository import ConcurrentUpdateError


class SqlAlchemyCheckpointRepository:
    """Persist serialized session event logs via SQLAlchemy.

    Implements the CheckpointStore protocol used by Session Runtime adapters.
    """

    def __init__(self, session: Session) -> None:
        self._session = session
        self._row_versions: dict[str, int] = {}

    def load(self, session_id: str) -> list[dict[str, object]] | None:
        key = (session_id or "").strip()
        if not key:
            return None
        row = self._session.get(SessionCheckpointModel, key)
        if row is None:
            return None
        dto = dto_from_model(SessionCheckpointDTO, row)
        self._row_versions[key] = int(dto.row_version)
        return CheckpointMapper.events_from_dto(dto)

    def save(self, session_id: str, events: list[dict[str, object]]) -> None:
        key = (session_id or "").strip()
        if not key:
            return
        existing = self._session.get(SessionCheckpointModel, key)
        if existing is None:
            dto = CheckpointMapper.to_persistence(key, events, row_version=1)
            self._session.add(model_from_dto(SessionCheckpointModel, dto))
            self._row_versions[key] = 1
            return

        expected = self._row_versions.get(key)
        if expected is None:
            expected = int(existing.row_version)
        now = datetime.now(UTC)
        dto = CheckpointMapper.to_persistence(
            key,
            events,
            row_version=expected + 1,
            updated_at=now,
        )
        result = self._session.execute(
            update(SessionCheckpointModel)
            .where(
                SessionCheckpointModel.session_id == key,
                SessionCheckpointModel.row_version == expected,
            )
            .values(
                events=list(dto.events),
                updated_at=now,
                row_version=dto.row_version,
            )
        )
        if result.rowcount != 1:
            raise ConcurrentUpdateError(
                f"checkpoint {key} was updated concurrently"
            )
        existing.events = list(dto.events)
        existing.updated_at = now
        existing.row_version = dto.row_version
        self._row_versions[key] = dto.row_version

    def clear(self, session_id: str) -> None:
        key = (session_id or "").strip()
        if not key:
            return
        row = self._session.get(SessionCheckpointModel, key)
        if row is not None:
            self._session.delete(row)
