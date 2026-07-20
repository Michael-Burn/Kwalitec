"""Repository package — contracts and in-memory implementations."""

from __future__ import annotations

from app.infrastructure.repositories.contracts import (
    AggregateRepository,
    EvidenceRepository,
    Repository,
    SnapshotRepository,
)
from app.infrastructure.repositories.in_memory import (
    InMemoryAggregateRepository,
    InMemoryEvidenceRepository,
    InMemorySnapshotRepository,
)
from app.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyAggregateRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemySnapshotRepository,
)

__all__ = [
    "AggregateRepository",
    "EvidenceRepository",
    "InMemoryAggregateRepository",
    "InMemoryEvidenceRepository",
    "InMemorySnapshotRepository",
    "Repository",
    "SnapshotRepository",
    "SqlAlchemyAggregateRepository",
    "SqlAlchemyEvidenceRepository",
    "SqlAlchemySnapshotRepository",
]
