"""Persistence package — contracts, UoW, stores, locking."""

from __future__ import annotations

from app.infrastructure.persistence.contracts import (
    AGGREGATE_CONTRACTS,
    AggregateContract,
    AggregateOwner,
    contract_for,
    owner_for,
)
from app.infrastructure.persistence.evidence_store import (
    EvidenceRecord,
    EvidenceStore,
)
from app.infrastructure.persistence.optimistic_locking import (
    OptimisticLockError,
    OptimisticLockGuard,
    VersionToken,
)
from app.infrastructure.persistence.snapshot_store import (
    SnapshotRecord,
    SnapshotStore,
)
from app.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWork,
    UnitOfWork,
    UnitOfWorkError,
)

__all__ = [
    "AGGREGATE_CONTRACTS",
    "AggregateContract",
    "AggregateOwner",
    "EvidenceRecord",
    "EvidenceStore",
    "OptimisticLockError",
    "OptimisticLockGuard",
    "SnapshotRecord",
    "SnapshotStore",
    "SqlAlchemyUnitOfWork",
    "UnitOfWork",
    "UnitOfWorkError",
    "VersionToken",
    "contract_for",
    "owner_for",
]
