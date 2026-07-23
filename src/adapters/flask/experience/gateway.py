"""ExperienceGateway — request-scoped live XP snapshot access (R1-001).

Injects ``ExperienceIntegrationService`` and reuses one composed experience
per request. Adapter concern only — no educational reasoning.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, Protocol

from flask import g, has_request_context

from adapters.flask.experience.inputs_builder import build_integration_inputs
from application.student_experience.integration.enums import IntegrationTrigger
from application.student_experience.integration.experience_integration_service import (
    ExperienceIntegrationService,
)
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
    ExperienceSnapshotBundle,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)

EXPERIENCE_CACHE_G_KEY = "eos_experience_snapshot_cache"
EXPERIENCE_COMPOSE_COUNT_G_KEY = "eos_experience_compose_count"
PRIOR_READINESS_SESSION_KEY = "eos_prior_readiness_snapshot"


class PriorReadinessStore(Protocol):
    """Optional persistence for readiness-change notices across requests."""

    def load(self, student_id: str) -> ReadinessSnapshot | None: ...

    def save(self, student_id: str, snapshot: ReadinessSnapshot) -> None: ...


def _default_as_of() -> datetime:
    return datetime.now(UTC)


class ExperienceGateway:
    """Compose and reuse the continuous experience snapshot for one request.

    Controllers receive this gateway via ``AdapterDependencies`` (DI).
    Snapshot reuse is request-scoped when a Flask request context is active;
    unit tests without Flask reuse an instance-local cache.
    """

    def __init__(
        self,
        *,
        experience_service: ExperienceIntegrationService | None = None,
        as_of_resolver: Callable[[], datetime] | None = None,
        cargo_loader: Callable[[str], Any] | None = None,
        prior_readiness_store: PriorReadinessStore | None = None,
    ) -> None:
        self._service = experience_service or ExperienceIntegrationService()
        self._as_of_resolver = as_of_resolver or _default_as_of
        self._cargo_loader = cargo_loader
        self._prior_store = prior_readiness_store
        self._local_cache: dict[str, ExperienceJourneyViewModel] = {}
        self._local_compose_count = 0

    @property
    def service(self) -> ExperienceIntegrationService:
        return self._service

    @property
    def compose_count(self) -> int:
        """Number of compositions in the active request / instance scope."""
        if has_request_context():
            return int(getattr(g, EXPERIENCE_COMPOSE_COUNT_G_KEY, 0) or 0)
        return self._local_compose_count

    def get(
        self,
        student_id: str,
        *,
        trigger: IntegrationTrigger = IntegrationTrigger.HOME_VIEW,
        force_refresh: bool = False,
        cargo: Any = None,
        evidence_recorded: bool = False,
    ) -> ExperienceJourneyViewModel | None:
        """Return the live experience for ``student_id``, composing at most once.

        Returns ``None`` only when ``student_id`` is empty after strip — callers
        should resolve identity first. Composition failures degrade to ``None``
        so templates never crash on absent projections.
        """
        resolved = (student_id or "").strip()
        if not resolved:
            return None

        cache = self._cache_map()
        if not force_refresh and resolved in cache:
            return cache[resolved]

        try:
            journey = self._compose(
                resolved,
                trigger=trigger,
                cargo=cargo,
                evidence_recorded=evidence_recorded,
                publish=False,
            )
        except Exception:
            return None

        cache[resolved] = journey
        self._remember_readiness(resolved, journey)
        return journey

    def refresh_after_reflection(
        self,
        student_id: str,
        *,
        cargo: Any = None,
    ) -> ExperienceJourneyViewModel | None:
        """Run the post-reflection cascade and replace the request snapshot."""
        resolved = (student_id or "").strip()
        if not resolved:
            return None
        try:
            journey = self._compose(
                resolved,
                trigger=IntegrationTrigger.REFLECTION_SUBMITTED,
                cargo=cargo,
                evidence_recorded=True,
                publish=True,
                use_refresh_after_reflection=True,
            )
        except Exception:
            return None
        self._cache_map()[resolved] = journey
        self._remember_readiness(resolved, journey)
        return journey

    def refresh_after_mission_complete(
        self,
        student_id: str,
        *,
        cargo: Any = None,
        evidence_recorded: bool = True,
    ) -> ExperienceJourneyViewModel | None:
        """Run the post-mission cascade and replace the request snapshot."""
        resolved = (student_id or "").strip()
        if not resolved:
            return None
        try:
            journey = self._compose(
                resolved,
                trigger=IntegrationTrigger.MISSION_COMPLETE,
                cargo=cargo,
                evidence_recorded=evidence_recorded,
                publish=True,
                use_refresh_after_mission=True,
            )
        except Exception:
            return None
        self._cache_map()[resolved] = journey
        self._remember_readiness(resolved, journey)
        return journey

    def snapshot_bundle(
        self,
        student_id: str,
        *,
        force_refresh: bool = False,
    ) -> ExperienceSnapshotBundle | None:
        """Compact snapshot bundle for the current request experience."""
        journey = self.get(student_id, force_refresh=force_refresh)
        if journey is None:
            return None
        return self._service.build_snapshot_bundle(journey)

    def invalidate(self, student_id: str | None = None) -> None:
        """Drop cached experience for one student or the whole request scope."""
        cache = self._cache_map()
        if student_id is None:
            cache.clear()
            return
        cache.pop((student_id or "").strip(), None)

    def _compose(
        self,
        student_id: str,
        *,
        trigger: IntegrationTrigger,
        cargo: Any,
        evidence_recorded: bool,
        publish: bool,
        use_refresh_after_reflection: bool = False,
        use_refresh_after_mission: bool = False,
    ) -> ExperienceJourneyViewModel:
        as_of = self._as_of_resolver()
        resolved_cargo = cargo
        if resolved_cargo is None and self._cargo_loader is not None:
            try:
                resolved_cargo = self._cargo_loader(student_id)
            except Exception:
                resolved_cargo = None

        prior = None
        if self._prior_store is not None:
            try:
                prior = self._prior_store.load(student_id)
            except Exception:
                prior = None

        inputs = build_integration_inputs(
            student_id,
            as_of,
            cargo=resolved_cargo,
            prior_readiness_snapshot=prior,
            evidence_recorded=evidence_recorded,
        )

        if use_refresh_after_reflection:
            journey = self._service.refresh_after_reflection(inputs)
        elif use_refresh_after_mission:
            journey = self._service.refresh_after_mission_complete(
                inputs,
                evidence_recorded=evidence_recorded,
            )
        elif publish:
            journey = self._service.refresh_experience(inputs, trigger=trigger)
        else:
            journey = self._service.build_experience(inputs, trigger=trigger)

        self._bump_compose_count()
        return journey

    def _remember_readiness(
        self,
        student_id: str,
        journey: ExperienceJourneyViewModel,
    ) -> None:
        if self._prior_store is None:
            return
        try:
            self._prior_store.save(student_id, journey.readiness_snapshot)
        except Exception:
            return

    def _cache_map(self) -> dict[str, ExperienceJourneyViewModel]:
        if has_request_context():
            cache = getattr(g, EXPERIENCE_CACHE_G_KEY, None)
            if not isinstance(cache, dict):
                cache = {}
                setattr(g, EXPERIENCE_CACHE_G_KEY, cache)
            return cache
        return self._local_cache

    def _bump_compose_count(self) -> None:
        if has_request_context():
            current = int(getattr(g, EXPERIENCE_COMPOSE_COUNT_G_KEY, 0) or 0)
            setattr(g, EXPERIENCE_COMPOSE_COUNT_G_KEY, current + 1)
        else:
            self._local_compose_count += 1


class MappingPriorReadinessStore:
    """In-memory / session-mapping prior readiness store for adapters."""

    def __init__(self, mapping: dict[str, Any] | None = None) -> None:
        self._mapping = mapping if mapping is not None else {}

    def load(self, student_id: str) -> ReadinessSnapshot | None:
        value = self._mapping.get(_prior_key(student_id))
        if isinstance(value, ReadinessSnapshot):
            return value
        return None

    def save(self, student_id: str, snapshot: ReadinessSnapshot) -> None:
        self._mapping[_prior_key(student_id)] = snapshot


def _prior_key(student_id: str) -> str:
    return f"{PRIOR_READINESS_SESSION_KEY}:{student_id.strip()}"
