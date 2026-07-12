"""Application TwinRepository — durable immutable Twin snapshot persistence.

Stores and retrieves Birth / Successor Twin snapshots via SQLAlchemy.
Never creates Twins, never mutates snapshots in place, never reasons
educationally. Contract types remain free of educational judgement.

InMemoryTwinRepository remains available for process-local unit tests.
"""

from __future__ import annotations

from app.application.twin_repository.in_memory import InMemoryTwinRepository
from app.application.twin_repository.shared import (
    get_shared_twin_repository,
    reset_shared_twin_repository,
)
from app.application.twin_repository.twin_repository import TwinRepository
from app.application.twin_repository.types import (
    SNAPSHOT_FORMAT_VERSION_1_0,
    CurrentSnapshotRef,
    PersistAcknowledgement,
    SnapshotHistory,
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    TwinScope,
    TwinSnapshotIdentity,
    TwinSnapshotRecord,
)

__all__ = [
    "SNAPSHOT_FORMAT_VERSION_1_0",
    "CurrentSnapshotRef",
    "InMemoryTwinRepository",
    "PersistAcknowledgement",
    "SnapshotHistory",
    "TwinAuthorship",
    "TwinPersistenceFailure",
    "TwinPersistenceFailureReason",
    "TwinRepository",
    "TwinScope",
    "TwinSnapshotIdentity",
    "TwinSnapshotRecord",
    "get_shared_twin_repository",
    "reset_shared_twin_repository",
]
