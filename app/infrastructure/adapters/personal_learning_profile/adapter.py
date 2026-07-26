"""Personal Learning Profile adapter / DI surface (EP-004.1)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from app.infrastructure.adapters.personal_learning_profile.aggregator import (
    PersonalLearningProfileAggregator,
    build_personal_learning_profile_aggregator,
)
from app.infrastructure.adapters.personal_learning_profile.contracts import (
    PersonalLearningProfile,
    PersonalLearningProfilePort,
    ProfileResolveResult,
)
from app.infrastructure.adapters.personal_learning_profile.store import (
    PersonalLearningProfileStore,
    build_personal_learning_profile_store,
)


class PersonalLearningProfileAdapter:
    """Port implementation wrapping the process-local store.

    Runtime A services should prefer ``PersonalLearningProfilePort`` typing
    so they do not depend on store/aggregator internals.
    """

    def __init__(self, store: PersonalLearningProfileStore) -> None:
        self._store = store

    @property
    def enabled(self) -> bool:
        return self._store.enabled

    def resolve(
        self,
        student_id: str | int,
        *,
        events: Sequence[Any] | None = None,
        declared_session_minutes: int | None = None,
        as_of: str | None = None,
    ) -> ProfileResolveResult:
        return self._store.resolve(
            student_id,
            events=events,
            declared_session_minutes=declared_session_minutes,
            as_of=as_of,
        )

    def get_cached(
        self, student_id: str | int
    ) -> PersonalLearningProfile | None:
        return self._store.get_cached(student_id)


def build_personal_learning_profile_adapter(
    *,
    enabled: bool,
    aggregator: PersonalLearningProfileAggregator | None = None,
) -> PersonalLearningProfileAdapter | None:
    """DI helper — construct adapter only when ENABLE_PERSONAL_LEARNING_PROFILE."""
    store = build_personal_learning_profile_store(
        enabled=enabled,
        aggregator=aggregator or build_personal_learning_profile_aggregator(),
    )
    if store is None:
        return None
    return PersonalLearningProfileAdapter(store)


def as_profile_port(
    adapter: PersonalLearningProfileAdapter | None,
) -> PersonalLearningProfilePort | None:
    """Cast helper for Protocol-typed injection."""
    return adapter
