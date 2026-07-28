"""Runtime Integration Service — Preferred Authority orchestration (RI-001).

Detects active SCI + Educational Decisions, invokes EX-001 Experience Engine,
and falls back to Runtime A compatibility only when prerequisites are missing.
No educational reasoning lives here.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from app.application.educational_experience_engine.experience_service import (
    ExperienceTransformationService,
)
from app.application.educational_reasoning_engine.query_service import (
    DecisionQueryService,
)
from app.application.runtime_integration.dto import (
    AuthoritySource,
    FallbackReason,
    IntegrationResult,
    IntegrationSurface,
    SurfaceExperienceBundle,
)
from app.application.runtime_integration.routing import (
    decide_authority,
    resolve_active_instance,
)
from app.application.runtime_integration.telemetry import (
    DEFAULT_TELEMETRY,
    RuntimeIntegrationTelemetry,
)

logger = logging.getLogger(__name__)

RuntimeAFallback = Callable[[int, IntegrationSurface], Any]


class RuntimeIntegrationService:
    """Single integration interface for educational surface consumers.

    Controllers and adapters call this service. They must not perform
    educational ranking, prerequisite logic, or decision generation.
    """

    def __init__(
        self,
        *,
        experience: ExperienceTransformationService | None = None,
        decision_query: DecisionQueryService | None = None,
        telemetry: RuntimeIntegrationTelemetry | None = None,
        runtime_a_fallback: RuntimeAFallback | None = None,
        integration_enabled: bool = True,
    ) -> None:
        self._experience = experience or ExperienceTransformationService()
        self._decision_query = decision_query or DecisionQueryService()
        self._telemetry = telemetry or DEFAULT_TELEMETRY
        self._runtime_a_fallback = runtime_a_fallback
        self._integration_enabled = bool(integration_enabled)

    @property
    def telemetry(self) -> RuntimeIntegrationTelemetry:
        return self._telemetry

    def resolve_for_surface(
        self,
        student_id: int,
        surface: IntegrationSurface | str,
        *,
        subject_code: str | None = None,
        runtime_a_fallback: RuntimeAFallback | None = None,
    ) -> IntegrationResult:
        """Route one surface request to EI→EX-001 or Runtime A compatibility."""
        surface_key = (
            surface
            if isinstance(surface, IntegrationSurface)
            else IntegrationSurface(str(surface).strip().lower())
        )
        sid = int(student_id)
        preferred_subject = (
            None if subject_code is None else str(subject_code).strip().upper() or None
        )

        instance = resolve_active_instance(sid, subject_code=preferred_subject)
        decision_count = 0
        primary_view = None
        if instance is not None:
            views = self._decision_query.highest_value_actions(
                instance.instance_id, limit=1
            )
            decision_count = len(views)
            primary_view = views[0] if views else None

        routing = decide_authority(
            integration_enabled=self._integration_enabled,
            instance=instance,
            decision_count=decision_count,
            preferred_subject=preferred_subject,
        )

        if routing.use_educational_intelligence and primary_view is not None:
            bundle = self._experience.present_decision_view(primary_view)
            experience = SurfaceExperienceBundle(
                instance_id=routing.instance_id or primary_view.decision.instance_id,
                decision_id=primary_view.decision.decision_id,
                surfaces=bundle,
                authority=AuthoritySource.EDUCATIONAL_INTELLIGENCE,
            )
            self._telemetry.record_educational_intelligence(
                student_id=sid,
                subject=routing.subject_code,
                surface=surface_key,
                instance_id=experience.instance_id,
                decision_id=experience.decision_id,
            )
            return IntegrationResult(
                authority=AuthoritySource.EDUCATIONAL_INTELLIGENCE,
                surface=surface_key,
                student_id=sid,
                subject_code=routing.subject_code,
                instance_id=experience.instance_id,
                decision_id=experience.decision_id,
                experience=experience,
            )

        reason = routing.fallback_reason or FallbackReason.NO_ACTIVE_SCI
        self._telemetry.record_fallback(
            student_id=sid,
            subject=routing.subject_code or preferred_subject,
            reason=reason,
            surface=surface_key,
            missing_prerequisite=routing.missing_prerequisite,
            instance_id=routing.instance_id,
        )
        fallback_fn = runtime_a_fallback or self._runtime_a_fallback
        payload = None
        if fallback_fn is not None:
            payload = fallback_fn(sid, surface_key)
        return IntegrationResult(
            authority=AuthoritySource.RUNTIME_A_COMPATIBILITY,
            surface=surface_key,
            student_id=sid,
            subject_code=routing.subject_code or preferred_subject,
            instance_id=routing.instance_id,
            compatibility_payload=payload,
            fallback_reason=reason,
            missing_prerequisite=routing.missing_prerequisite,
        )

    def has_educational_intelligence(
        self,
        student_id: int,
        *,
        subject_code: str | None = None,
    ) -> bool:
        """True when Preferred Authority can serve without recording telemetry.

        Used by presentation forks (e.g. Runtime C) that must not double-count
        adoption metrics before the real surface resolve.
        """
        if not self._integration_enabled:
            return False
        preferred_subject = (
            None if subject_code is None else str(subject_code).strip().upper() or None
        )
        instance = resolve_active_instance(
            int(student_id), subject_code=preferred_subject
        )
        if instance is None:
            return False
        views = self._decision_query.highest_value_actions(
            instance.instance_id, limit=1
        )
        return len(views) > 0

    def resolve_recommendation(
        self,
        student_id: int,
        *,
        subject_code: str | None = None,
        runtime_a_fallback: RuntimeAFallback | None = None,
    ) -> IntegrationResult:
        """Convenience entry for recommendation / Home / Dashboard reads."""
        return self.resolve_for_surface(
            student_id,
            IntegrationSurface.RECOMMENDATION,
            subject_code=subject_code,
            runtime_a_fallback=runtime_a_fallback,
        )

    def adoption_snapshot(self) -> dict[str, Any]:
        """Aggregation payload for RI-005 readiness measurement."""
        return self._telemetry.snapshot().to_dict()
