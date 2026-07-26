"""Process-local Personal Learning Profile store (EP-004.1).

Supports incremental replacement of immutable profile snapshots per student.
Never raises into educational control flows.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from threading import Lock
from typing import Any

from app.infrastructure.adapters.personal_learning_profile.aggregator import (
    PersonalLearningProfileAggregator,
    build_personal_learning_profile_aggregator,
)
from app.infrastructure.adapters.personal_learning_profile.contracts import (
    REASON_AGGREGATOR_ERROR,
    REASON_FLAG_OFF,
    REASON_STORE_ERROR,
    RESOLVE_STATUS_FAILED,
    RESOLVE_STATUS_OK,
    RESOLVE_STATUS_SKIPPED,
    PersonalLearningProfile,
    ProfileResolveResult,
)

logger = logging.getLogger(__name__)


class PersonalLearningProfileStore:
    """Incremental profile store keyed by student_id.

    Each update replaces the prior immutable snapshot for that student.
    Fail-open: resolve returns skipped/failed results instead of raising.
    """

    STORE_ID = "personal_learning_profile_store"
    STORE_VERSION = "1.0.0-ep004.1"

    def __init__(
        self,
        *,
        enabled: bool = True,
        aggregator: PersonalLearningProfileAggregator | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._aggregator = aggregator or build_personal_learning_profile_aggregator()
        self._profiles: dict[str, PersonalLearningProfile] = {}
        self._lock = Lock()
        self._resolve_ok_count = 0
        self._resolve_skipped_count = 0
        self._resolve_failed_count = 0
        self._update_count = 0

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def store_id(self) -> str:
        return self.STORE_ID

    def get_cached(
        self, student_id: str | int
    ) -> PersonalLearningProfile | None:
        sid = str(student_id).strip()
        with self._lock:
            return self._profiles.get(sid)

    def upsert(self, profile: PersonalLearningProfile) -> PersonalLearningProfile:
        """Replace the stored snapshot for profile.student_id."""
        with self._lock:
            self._profiles[profile.student_id] = profile
            self._update_count += 1
        return profile

    def resolve(
        self,
        student_id: str | int,
        *,
        events: Sequence[Any] | None = None,
        declared_session_minutes: int | None = None,
        as_of: str | None = None,
    ) -> ProfileResolveResult:
        """Aggregate evidence into a profile snapshot (fail-open)."""
        if not self._enabled:
            self._resolve_skipped_count += 1
            return ProfileResolveResult(
                ok=False,
                status=RESOLVE_STATUS_SKIPPED,
                reason=REASON_FLAG_OFF,
                message="ENABLE_PERSONAL_LEARNING_PROFILE is OFF",
            )
        try:
            profile = self._aggregator.aggregate(
                student_id=student_id,
                events=events,
                declared_session_minutes=declared_session_minutes,
                as_of=as_of,
            )
            self.upsert(profile)
            self._resolve_ok_count += 1
            return ProfileResolveResult(
                ok=True,
                status=RESOLVE_STATUS_OK,
                profile=profile,
                message="personal learning profile resolved",
            )
        except ValueError as exc:
            logger.warning(
                "personal_learning_profile_aggregate_invalid error=%s", exc
            )
            self._resolve_failed_count += 1
            return ProfileResolveResult(
                ok=False,
                status=RESOLVE_STATUS_FAILED,
                reason=REASON_AGGREGATOR_ERROR,
                message=str(exc),
            )
        except Exception as exc:  # noqa: BLE001 — store must not raise
            logger.warning(
                "personal_learning_profile_resolve_failed error=%s", exc
            )
            self._resolve_failed_count += 1
            return ProfileResolveResult(
                ok=False,
                status=RESOLVE_STATUS_FAILED,
                reason=REASON_STORE_ERROR,
                message=str(exc),
            )

    def clear(self) -> None:
        with self._lock:
            self._profiles.clear()

    def stats(self) -> dict[str, Any]:
        with self._lock:
            size = len(self._profiles)
        return {
            "enabled": self._enabled,
            "profile_count": size,
            "update_count": self._update_count,
            "resolve_ok_count": self._resolve_ok_count,
            "resolve_skipped_count": self._resolve_skipped_count,
            "resolve_failed_count": self._resolve_failed_count,
            "store_id": self.STORE_ID,
            "store_version": self.STORE_VERSION,
        }


def build_personal_learning_profile_store(
    *,
    enabled: bool,
    aggregator: PersonalLearningProfileAggregator | None = None,
) -> PersonalLearningProfileStore | None:
    """DI helper — construct store only when flag is ON."""
    if not enabled:
        return None
    return PersonalLearningProfileStore(
        enabled=True, aggregator=aggregator
    )
