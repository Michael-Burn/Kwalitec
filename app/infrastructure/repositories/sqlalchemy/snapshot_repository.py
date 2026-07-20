"""SQLAlchemy SnapshotRepository — durable append-only snapshots."""

from __future__ import annotations

import json
import uuid
from typing import Any

from app.extensions import db
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.infrastructure.repositories.contracts import SnapshotRepository
from app.models.v2_aggregate import V2AggregateSnapshot


class SqlAlchemySnapshotRepository(SnapshotRepository):
    """Persist snapshots in ``v2_aggregate_snapshots``."""

    def __init__(self, *, uow: UnitOfWork | None = None) -> None:
        self._uow = uow
        self._available = True

    @property
    def repository_id(self) -> str:
        return "sqlalchemy_snapshot_repository"

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available

    def save_snapshot(
        self,
        aggregate_name: str,
        aggregate_id: str,
        payload: dict[str, Any],
        *,
        schema_version: int = 1,
        correlation_id: str = "",
    ) -> dict[str, Any]:
        latest = (
            db.session.query(V2AggregateSnapshot)
            .filter_by(aggregate_name=aggregate_name, aggregate_id=aggregate_id)
            .order_by(V2AggregateSnapshot.sequence.desc())
            .first()
        )
        sequence = 1 if latest is None else int(latest.sequence) + 1
        snapshot_id = uuid.uuid4().hex
        row = V2AggregateSnapshot(
            snapshot_id=snapshot_id,
            aggregate_name=aggregate_name,
            aggregate_id=aggregate_id,
            sequence=sequence,
            schema_version=schema_version,
            payload=json.dumps(payload, default=str, sort_keys=True),
            correlation_id=correlation_id or "",
        )
        db.session.add(row)
        if self._uow is not None and self._uow.is_active:
            self._uow.register(
                self.repository_id,
                "save_snapshot",
                {"snapshot_id": snapshot_id},
            )
            db.session.flush()
        else:
            db.session.commit()
        return {
            "snapshot_id": snapshot_id,
            "aggregate_name": aggregate_name,
            "aggregate_id": aggregate_id,
            "schema_version": schema_version,
            "correlation_id": correlation_id or "",
        }

    def load_latest(
        self, aggregate_name: str, aggregate_id: str
    ) -> dict[str, Any] | None:
        row = (
            db.session.query(V2AggregateSnapshot)
            .filter_by(aggregate_name=aggregate_name, aggregate_id=aggregate_id)
            .order_by(V2AggregateSnapshot.sequence.desc())
            .first()
        )
        if row is None:
            return None
        return {
            "snapshot_id": row.snapshot_id,
            "aggregate_name": row.aggregate_name,
            "aggregate_id": row.aggregate_id,
            "schema_version": row.schema_version,
            "payload": json.loads(row.payload),
            "created_at": row.created_at.isoformat(),
            "correlation_id": row.correlation_id,
            "metadata": {},
        }
