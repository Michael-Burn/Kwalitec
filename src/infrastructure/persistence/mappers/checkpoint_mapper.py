"""Structural mapping for session checkpoints (BR-004)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from infrastructure.persistence.dto.onboarding import SessionCheckpointDTO


class CheckpointMapper:
    """Map checkpoint event lists ↔ SessionCheckpointDTO."""

    @staticmethod
    def to_persistence(
        session_id: str,
        events: list[dict[str, object]],
        *,
        row_version: int = 1,
        updated_at: datetime | None = None,
    ) -> SessionCheckpointDTO:
        return SessionCheckpointDTO(
            session_id=session_id,
            events=[dict(item) for item in events],
            updated_at=updated_at or datetime.now(UTC),
            row_version=row_version,
        )

    @staticmethod
    def events_from_dto(dto: SessionCheckpointDTO) -> list[dict[str, object]]:
        payload: list[Any] = list(dto.events or [])
        return [dict(item) for item in payload if isinstance(item, dict)]
