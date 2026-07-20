"""Opaque learner projection store for Student Experience adapters.

Persists Twin / Adaptive / Journey / Mission / Activity projection documents.
Never computes readiness, recommendations, mastery, or journey progression.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from app.infrastructure.persistence.optimistic_locking import OptimisticLockGuard
from app.infrastructure.persistence.snapshot_store import SnapshotStore
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.infrastructure.repositories.contracts import AggregateRepository
from app.infrastructure.repositories.in_memory import InMemoryAggregateRepository

RepositoryFactory = Callable[..., AggregateRepository]


class ExperienceProjectionStore:
    """Shared opaque projection + session/workspace persistence for Experience.

    Adapters read and write documents only. Educational engines remain the
    sole authorities for learner-state and next-action law.
    """

    TWIN = "ExperienceTwin"
    ADAPTIVE = "ExperienceAdaptive"
    JOURNEY = "ExperienceJourney"
    MISSION = "ExperienceMission"
    ACTIVITY = "ExperienceActivity"
    WORKSPACE = "ExperienceWorkspace"
    SESSION = "ExperienceSession"

    def __init__(
        self,
        *,
        uow: UnitOfWork | None = None,
        snapshots: SnapshotStore | None = None,
        lock: OptimisticLockGuard | None = None,
        repository_factory: RepositoryFactory | None = None,
        durable_snapshots: bool = False,
    ) -> None:
        self.uow = uow or UnitOfWork()
        self.snapshots = snapshots or SnapshotStore()
        self.lock = lock or OptimisticLockGuard()
        self._repository_factory = repository_factory
        self._durable_snapshots = durable_snapshots
        self.twin = self.make_repository(
            repository_id="experience_twin", aggregate_name=self.TWIN
        )
        self.adaptive = self.make_repository(
            repository_id="experience_adaptive", aggregate_name=self.ADAPTIVE
        )
        self.journey = self.make_repository(
            repository_id="experience_journey", aggregate_name=self.JOURNEY
        )
        self.mission = self.make_repository(
            repository_id="experience_mission", aggregate_name=self.MISSION
        )
        self.activity = self.make_repository(
            repository_id="experience_activity", aggregate_name=self.ACTIVITY
        )
        self.workspaces = self.make_repository(
            repository_id="experience_workspace", aggregate_name=self.WORKSPACE
        )
        self.sessions = self.make_repository(
            repository_id="experience_session", aggregate_name=self.SESSION
        )

    def make_repository(
        self, *, repository_id: str, aggregate_name: str
    ) -> AggregateRepository:
        """Construct an aggregate repository for the given name."""
        if self._repository_factory is not None:
            return self._repository_factory(
                repository_id=repository_id,
                aggregate_name=aggregate_name,
            )
        return InMemoryAggregateRepository(
            repository_id=repository_id,
            aggregate_name=aggregate_name,
            uow=self.uow,
            lock=self.lock,
        )

    def get(self, repo: AggregateRepository, key: str) -> dict[str, Any] | None:
        """Load an opaque document."""
        return repo.get(key)

    def save(
        self,
        repo: AggregateRepository,
        key: str,
        document: dict[str, Any],
        *,
        expected_version: int | None = None,
        snapshot: bool = True,
    ) -> dict[str, Any]:
        """Persist an opaque document; optionally append a snapshot."""
        ack = repo.save(key, document, expected_version=expected_version)
        if snapshot:
            aggregate_name = getattr(repo, "aggregate_name", "Aggregate")
            if self._durable_snapshots:
                from app.infrastructure.repositories.sqlalchemy import (
                    SqlAlchemySnapshotRepository,
                )

                SqlAlchemySnapshotRepository(uow=self.uow).save_snapshot(
                    aggregate_name,
                    key,
                    deepcopy(document),
                    schema_version=1,
                    correlation_id=str(document.get("correlation_id") or ""),
                )
            else:
                self.snapshots.save(
                    aggregate_name,
                    key,
                    deepcopy(document),
                    schema_version=1,
                    correlation_id=str(document.get("correlation_id") or ""),
                )
        return ack
