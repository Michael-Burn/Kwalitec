"""Opaque learner projection store for Student Experience adapters.

Persists Twin / Adaptive / Journey / Mission / Activity projection documents.
Never computes readiness, recommendations, mastery, or journey progression.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.persistence.optimistic_locking import OptimisticLockGuard
from app.infrastructure.persistence.snapshot_store import SnapshotStore
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.infrastructure.repositories.in_memory import InMemoryAggregateRepository


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
    ) -> None:
        self.uow = uow or UnitOfWork()
        self.snapshots = snapshots or SnapshotStore()
        self.lock = lock or OptimisticLockGuard()
        self.twin = InMemoryAggregateRepository(
            repository_id="experience_twin",
            aggregate_name=self.TWIN,
            uow=self.uow,
            lock=self.lock,
        )
        self.adaptive = InMemoryAggregateRepository(
            repository_id="experience_adaptive",
            aggregate_name=self.ADAPTIVE,
            uow=self.uow,
            lock=self.lock,
        )
        self.journey = InMemoryAggregateRepository(
            repository_id="experience_journey",
            aggregate_name=self.JOURNEY,
            uow=self.uow,
            lock=self.lock,
        )
        self.mission = InMemoryAggregateRepository(
            repository_id="experience_mission",
            aggregate_name=self.MISSION,
            uow=self.uow,
            lock=self.lock,
        )
        self.activity = InMemoryAggregateRepository(
            repository_id="experience_activity",
            aggregate_name=self.ACTIVITY,
            uow=self.uow,
            lock=self.lock,
        )
        self.workspaces = InMemoryAggregateRepository(
            repository_id="experience_workspace",
            aggregate_name=self.WORKSPACE,
            uow=self.uow,
            lock=self.lock,
        )
        self.sessions = InMemoryAggregateRepository(
            repository_id="experience_session",
            aggregate_name=self.SESSION,
            uow=self.uow,
            lock=self.lock,
        )

    def get(self, repo: InMemoryAggregateRepository, key: str) -> dict[str, Any] | None:
        """Load an opaque document."""
        return repo.get(key)

    def save(
        self,
        repo: InMemoryAggregateRepository,
        key: str,
        document: dict[str, Any],
        *,
        expected_version: int | None = None,
        snapshot: bool = True,
    ) -> dict[str, Any]:
        """Persist an opaque document; optionally append a snapshot."""
        ack = repo.save(key, document, expected_version=expected_version)
        if snapshot:
            self.snapshots.save(
                repo.aggregate_name,
                key,
                deepcopy(document),
                schema_version=1,
                correlation_id=str(document.get("correlation_id") or ""),
            )
        return ack
