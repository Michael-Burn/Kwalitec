"""SQLAlchemy AggregateRepository — durable versioned opaque documents."""

from __future__ import annotations

import json
from typing import Any

from app.extensions import db
from app.infrastructure.persistence.optimistic_locking import (
    OptimisticLockError,
    OptimisticLockGuard,
)
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.infrastructure.repositories.contracts import AggregateRepository
from app.models.v2_aggregate import V2AggregateDocument


class SqlAlchemyAggregateRepository(AggregateRepository):
    """Persist aggregate documents in ``v2_aggregate_documents``."""

    def __init__(
        self,
        *,
        repository_id: str = "sqlalchemy_aggregate_repository",
        aggregate_name: str = "Aggregate",
        uow: UnitOfWork | None = None,
        lock: OptimisticLockGuard | None = None,
    ) -> None:
        self._repository_id = repository_id
        self._aggregate_name = aggregate_name
        self._uow = uow
        self._lock = lock or OptimisticLockGuard()
        self._available = True

    @property
    def repository_id(self) -> str:
        return self._repository_id

    @property
    def aggregate_name(self) -> str:
        return self._aggregate_name

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available

    def get(self, aggregate_id: str) -> dict[str, Any] | None:
        row = (
            db.session.query(V2AggregateDocument)
            .filter_by(
                aggregate_name=self._aggregate_name,
                aggregate_id=aggregate_id,
            )
            .one_or_none()
        )
        if row is None:
            return None
        doc = json.loads(row.payload)
        doc["_version"] = row.version
        self._lock.seed(self._aggregate_name, aggregate_id, row.version)
        return doc

    def save(
        self,
        aggregate_id: str,
        document: dict[str, Any],
        *,
        expected_version: int | None = None,
    ) -> dict[str, Any]:
        row = (
            db.session.query(V2AggregateDocument)
            .filter_by(
                aggregate_name=self._aggregate_name,
                aggregate_id=aggregate_id,
            )
            .one_or_none()
        )
        current = 0 if row is None else int(row.version)
        self._lock.seed(self._aggregate_name, aggregate_id, current)
        if expected_version is not None and expected_version != current:
            raise OptimisticLockError(
                f"{self._aggregate_name}:{aggregate_id} expected "
                f"v{expected_version}, got v{current}"
            )
        token = self._lock.bump(
            self._aggregate_name,
            aggregate_id,
            expected=expected_version,
        )
        stored = dict(document)
        stored["_version"] = token.version
        payload = json.dumps(stored, default=str, sort_keys=True)
        if row is None:
            row = V2AggregateDocument(
                aggregate_name=self._aggregate_name,
                aggregate_id=aggregate_id,
                version=token.version,
                payload=payload,
            )
            db.session.add(row)
        else:
            row.version = token.version
            row.payload = payload
        if self._uow is not None and self._uow.is_active:
            self._uow.register(
                self.repository_id,
                "save",
                {"aggregate_id": aggregate_id, "version": token.version},
            )
            db.session.flush()
        else:
            db.session.commit()
        return {
            "aggregate_id": aggregate_id,
            "version": token.version,
            "ok": True,
        }

    def delete(self, aggregate_id: str) -> bool:
        row = (
            db.session.query(V2AggregateDocument)
            .filter_by(
                aggregate_name=self._aggregate_name,
                aggregate_id=aggregate_id,
            )
            .one_or_none()
        )
        if row is None:
            return False
        db.session.delete(row)
        if self._uow is not None and self._uow.is_active:
            self._uow.register(
                self.repository_id,
                "delete",
                {"aggregate_id": aggregate_id},
            )
            db.session.flush()
        else:
            db.session.commit()
        return True

    def list_ids(self) -> tuple[str, ...]:
        rows = (
            db.session.query(V2AggregateDocument.aggregate_id)
            .filter_by(aggregate_name=self._aggregate_name)
            .order_by(V2AggregateDocument.aggregate_id)
            .all()
        )
        return tuple(r[0] for r in rows)
