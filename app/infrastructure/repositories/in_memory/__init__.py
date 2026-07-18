"""In-memory repository implementations for infrastructure foundation."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from app.infrastructure.persistence.evidence_store import EvidenceStore
from app.infrastructure.persistence.optimistic_locking import (
    OptimisticLockGuard,
)
from app.infrastructure.persistence.snapshot_store import SnapshotStore
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.infrastructure.repositories.contracts import (
    AggregateRepository,
    EvidenceRepository,
    SnapshotRepository,
)


class InMemorySnapshotRepository(SnapshotRepository):
    """SnapshotRepository backed by SnapshotStore."""

    def __init__(
        self,
        store: SnapshotStore | None = None,
        *,
        uow: UnitOfWork | None = None,
    ) -> None:
        self._store = store or SnapshotStore()
        self._uow = uow
        self._available = True

    @property
    def repository_id(self) -> str:
        return "snapshot_repository"

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
        record = self._store.save(
            aggregate_name,
            aggregate_id,
            payload,
            schema_version=schema_version,
            correlation_id=correlation_id,
        )
        if self._uow is not None and self._uow.is_active:
            self._uow.register(
                self.repository_id,
                "save_snapshot",
                {"snapshot_id": record.snapshot_id},
            )
        return {
            "snapshot_id": record.snapshot_id,
            "aggregate_name": record.aggregate_name,
            "aggregate_id": record.aggregate_id,
            "schema_version": record.schema_version,
            "correlation_id": record.correlation_id,
        }

    def load_latest(
        self, aggregate_name: str, aggregate_id: str
    ) -> dict[str, Any] | None:
        record = self._store.latest(aggregate_name, aggregate_id)
        if record is None:
            return None
        return {
            "snapshot_id": record.snapshot_id,
            "aggregate_name": record.aggregate_name,
            "aggregate_id": record.aggregate_id,
            "schema_version": record.schema_version,
            "payload": dict(record.payload),
            "created_at": record.created_at.isoformat(),
            "correlation_id": record.correlation_id,
            "metadata": dict(record.metadata),
        }


class InMemoryEvidenceRepository(EvidenceRepository):
    """EvidenceRepository backed by EvidenceStore."""

    def __init__(
        self,
        store: EvidenceStore | None = None,
        *,
        uow: UnitOfWork | None = None,
    ) -> None:
        self._store = store or EvidenceStore()
        self._uow = uow
        self._available = True

    @property
    def repository_id(self) -> str:
        return "evidence_repository"

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available

    def append_evidence(
        self,
        *,
        learner_id: str,
        subject_id: str,
        evidence_type: str,
        payload: dict[str, Any] | None = None,
        correlation_id: str = "",
        causation_id: str = "",
    ) -> dict[str, Any]:
        record = self._store.append(
            learner_id=learner_id,
            subject_id=subject_id,
            evidence_type=evidence_type,
            payload=payload,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )
        if self._uow is not None and self._uow.is_active:
            self._uow.register(
                self.repository_id,
                "append_evidence",
                {"record_id": record.record_id},
            )
        return {
            "record_id": record.record_id,
            "learner_id": record.learner_id,
            "subject_id": record.subject_id,
            "evidence_type": record.evidence_type,
            "recorded_at": record.recorded_at.isoformat(),
            "correlation_id": record.correlation_id,
            "causation_id": record.causation_id,
        }

    def list_evidence(
        self, learner_id: str, *, subject_id: str | None = None
    ) -> tuple[dict[str, Any], ...]:
        records = self._store.list_for_learner(
            learner_id, subject_id=subject_id
        )
        return tuple(
            {
                "record_id": r.record_id,
                "learner_id": r.learner_id,
                "subject_id": r.subject_id,
                "evidence_type": r.evidence_type,
                "payload": dict(r.payload),
                "recorded_at": r.recorded_at.isoformat(),
                "correlation_id": r.correlation_id,
                "causation_id": r.causation_id,
                "source": r.source,
                "metadata": dict(r.metadata),
            }
            for r in records
        )


class InMemoryAggregateRepository(AggregateRepository):
    """Generic in-memory aggregate document repository with optimistic locking."""

    def __init__(
        self,
        *,
        repository_id: str = "aggregate_repository",
        aggregate_name: str = "Aggregate",
        uow: UnitOfWork | None = None,
        lock: OptimisticLockGuard | None = None,
    ) -> None:
        self._repository_id = repository_id
        self._aggregate_name = aggregate_name
        self._docs: dict[str, dict[str, Any]] = {}
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
        doc = self._docs.get(aggregate_id)
        return None if doc is None else dict(doc)

    def save(
        self,
        aggregate_id: str,
        document: dict[str, Any],
        *,
        expected_version: int | None = None,
    ) -> dict[str, Any]:
        token = self._lock.bump(
            self._aggregate_name,
            aggregate_id,
            expected=expected_version,
        )
        stored = dict(document)
        stored["_version"] = token.version
        self._docs[aggregate_id] = stored
        if self._uow is not None and self._uow.is_active:
            self._uow.register(
                self.repository_id,
                "save",
                {"aggregate_id": aggregate_id, "version": token.version},
            )
        return {
            "aggregate_id": aggregate_id,
            "version": token.version,
            "ok": True,
        }

    def delete(self, aggregate_id: str) -> bool:
        existed = aggregate_id in self._docs
        self._docs.pop(aggregate_id, None)
        if existed and self._uow is not None and self._uow.is_active:
            self._uow.register(
                self.repository_id,
                "delete",
                {"aggregate_id": aggregate_id},
            )
        return existed

    def list_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._docs))


def snapshot_as_dict(record: Any) -> dict[str, Any]:
    """Helper for tests — convert dataclass records to dicts."""
    if hasattr(record, "__dataclass_fields__"):
        return asdict(record)
    return dict(record)
