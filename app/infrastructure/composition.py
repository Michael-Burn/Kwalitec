"""Shared Experience store factory for Student + Session compositions."""

from __future__ import annotations

from typing import Any

from app.application.config.v2_flags import (
    Version2FeatureFlags,
    resolve_v2_feature_flags,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.persistence.optimistic_locking import OptimisticLockGuard
from app.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWork,
    UnitOfWork,
)
from app.infrastructure.repositories.contracts import AggregateRepository
from app.infrastructure.repositories.in_memory import InMemoryAggregateRepository
from app.infrastructure.session.store import SessionDocumentStore


def _repo_factory(
    *,
    durable: bool,
    uow: UnitOfWork,
    lock: OptimisticLockGuard,
):
    """Return a callable that builds AggregateRepository instances."""

    def factory(
        *,
        repository_id: str,
        aggregate_name: str,
    ) -> AggregateRepository:
        if durable:
            from app.infrastructure.repositories.sqlalchemy import (
                SqlAlchemyAggregateRepository,
            )

            return SqlAlchemyAggregateRepository(
                repository_id=repository_id,
                aggregate_name=aggregate_name,
                uow=uow,
                lock=lock,
            )
        return InMemoryAggregateRepository(
            repository_id=repository_id,
            aggregate_name=aggregate_name,
            uow=uow,
            lock=lock,
        )

    return factory


def build_experience_projection_store(
    *,
    flags: Version2FeatureFlags | None = None,
    uow: UnitOfWork | None = None,
) -> ExperienceProjectionStore:
    """Build an ExperienceProjectionStore (durable when flagged)."""
    active = flags or resolve_v2_feature_flags()
    lock = OptimisticLockGuard()
    if active.ENABLE_DURABLE_STORE:
        if uow is None:
            from app.extensions import db

            work: UnitOfWork = SqlAlchemyUnitOfWork(db.session)
        else:
            work = uow
    else:
        work = uow or UnitOfWork()
    return ExperienceProjectionStore(
        uow=work,
        lock=lock,
        repository_factory=_repo_factory(
            durable=active.ENABLE_DURABLE_STORE, uow=work, lock=lock
        ),
        durable_snapshots=active.ENABLE_DURABLE_STORE,
    )


def build_session_document_store(
    *,
    flags: Version2FeatureFlags | None = None,
    experience_store: ExperienceProjectionStore | None = None,
) -> SessionDocumentStore:
    """Build a SessionDocumentStore; durable mode uses aggregate repos."""
    active = flags or resolve_v2_feature_flags()
    if not active.ENABLE_DURABLE_STORE:
        return SessionDocumentStore()
    store = experience_store or build_experience_projection_store(flags=active)
    return SessionDocumentStore(backing_repository_factory=_session_repo_factory(store))


def _session_repo_factory(experience_store: ExperienceProjectionStore):
    """Route session namespaces through a dedicated LearningSession aggregate."""

    repo = experience_store.make_repository(
        repository_id="session_document_store",
        aggregate_name="LearningSessionDocument",
    )

    def get_repo() -> AggregateRepository:
        return repo

    return get_repo


def build_opaque_engines(
    *,
    flags: Version2FeatureFlags | None = None,
) -> dict[str, Any]:
    """Construct Phase I opaque engine bridges when injection is enabled."""
    active = flags or resolve_v2_feature_flags()
    if not active.INJECT_PHASE_I_ENGINES:
        return {}
    from app.infrastructure.engines.opaque_bridges import build_default_opaque_engines

    return build_default_opaque_engines()
