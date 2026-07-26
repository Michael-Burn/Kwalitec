"""Rollback verification for Adaptive Shadow Soak (MS-003 A6).

Verifies that disabling KWALITEC_ADAPTIVE_ENGINE or
KWALITEC_ADAPTIVE_AUTHORITY immediately restores RecommendationService as
the sole Experience recommendation authority. Observational only.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    soak_telemetry as telemetry,
)
from app.infrastructure.adapters.adaptive_engine.port_cutover import (
    adaptive_experience_cutover_active,
)
from app.infrastructure.events.registry import EventRegistry

CompositionFactory = Callable[..., tuple[Any, Any]]


@dataclass(frozen=True)
class RollbackVerificationResult:
    """Outcome of an observational rollback drill."""

    ok: bool
    engine_disabled_restores_recommendation: bool
    authority_disabled_restores_recommendation: bool
    cutover_inactive_when_engine_off: bool
    cutover_inactive_when_authority_off: bool
    details: tuple[str, ...] = ()

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority_disabled_restores_recommendation": (
                self.authority_disabled_restores_recommendation
            ),
            "cutover_inactive_when_authority_off": (
                self.cutover_inactive_when_authority_off
            ),
            "cutover_inactive_when_engine_off": (
                self.cutover_inactive_when_engine_off
            ),
            "details": list(self.details),
            "engine_disabled_restores_recommendation": (
                self.engine_disabled_restores_recommendation
            ),
            "ok": self.ok,
        }


class RollbackVerifier:
    """Verify adaptive flag rollback restores RecommendationService authority."""

    VERIFIER_ID = "adaptive_rollback_verifier"
    VERIFIER_VERSION = "1.0.0-a6"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        composition_factory: CompositionFactory | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._composition_factory = composition_factory

    def verify(
        self,
        *,
        base_environ: dict[str, str] | None = None,
    ) -> RollbackVerificationResult:
        """Run flag-off drills and report whether Experience authority reverts.

        Does not mutate Runtime A. Does not enable Authority in production —
        only constructs compositions for observation.
        """
        from app.infrastructure.adapters.student_experience.composition import (
            build_production_experience,
        )

        factory = self._composition_factory or build_production_experience
        base = dict(base_environ or {})
        details: list[str] = []

        # Engine OFF (Shadow may remain conceptually; Engine off kills cutover).
        engine_off_env = {
            **base,
            "KWALITEC_ADAPTIVE_ENGINE": "0",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
            "KWALITEC_ADAPTIVE_AUTHORITY": "1",
        }
        engine_flags = resolve_v2_feature_flags(environ=engine_off_env)
        cutover_engine_off = adaptive_experience_cutover_active(
            engine_enabled=engine_flags.ENABLE_ADAPTIVE_ENGINE,
            shadow_enabled=engine_flags.ENABLE_ADAPTIVE_ENGINE_SHADOW,
            authority_enabled=engine_flags.ENABLE_ADAPTIVE_AUTHORITY,
        )
        engine_comp, _ = factory(flags=engine_flags)
        engine_router = getattr(engine_comp, "adaptive_port_router", None)
        engine_restored = (
            engine_router is None
            or not getattr(engine_router, "cutover_active", False)
        )
        if not cutover_engine_off:
            details.append("cutover_inactive_when_engine_off")
        else:
            details.append("FAIL:cutover_still_active_when_engine_off")
        if engine_restored:
            details.append("composition_router_inactive_when_engine_off")
        else:
            details.append("FAIL:composition_router_active_when_engine_off")

        # Authority OFF (Engine + Shadow ON) — RecommendationService sole authority.
        auth_off_env = {
            **base,
            "KWALITEC_ADAPTIVE_ENGINE": "1",
            "KWALITEC_ADAPTIVE_SHADOW": "1",
            "KWALITEC_ADAPTIVE_AUTHORITY": "0",
        }
        auth_flags = resolve_v2_feature_flags(environ=auth_off_env)
        cutover_auth_off = adaptive_experience_cutover_active(
            engine_enabled=auth_flags.ENABLE_ADAPTIVE_ENGINE,
            shadow_enabled=auth_flags.ENABLE_ADAPTIVE_ENGINE_SHADOW,
            authority_enabled=auth_flags.ENABLE_ADAPTIVE_AUTHORITY,
        )
        auth_comp, _ = factory(flags=auth_flags)
        auth_router = getattr(auth_comp, "adaptive_port_router", None)
        auth_restored = (
            auth_router is None
            or not getattr(auth_router, "cutover_active", False)
        )
        if not cutover_auth_off:
            details.append("cutover_inactive_when_authority_off")
        else:
            details.append("FAIL:cutover_still_active_when_authority_off")
        if auth_restored:
            details.append("composition_router_inactive_when_authority_off")
        else:
            details.append("FAIL:composition_router_active_when_authority_off")

        # Experience adaptive adapter must not expose adaptive_engine authority
        # when cutover is inactive (spot-check via router presence).
        engine_ok = (not cutover_engine_off) and engine_restored
        authority_ok = (not cutover_auth_off) and auth_restored
        ok = engine_ok and authority_ok

        result = RollbackVerificationResult(
            ok=ok,
            engine_disabled_restores_recommendation=engine_ok,
            authority_disabled_restores_recommendation=authority_ok,
            cutover_inactive_when_engine_off=not cutover_engine_off,
            cutover_inactive_when_authority_off=not cutover_auth_off,
            details=tuple(details),
        )
        telemetry.emit_rollback_verified(
            self._events,
            ok=result.ok,
            details=result.details,
        )
        return result


def build_rollback_verifier(
    *,
    events: EventRegistry | None = None,
    composition_factory: CompositionFactory | None = None,
) -> RollbackVerifier:
    """DI helper for RollbackVerifier."""
    return RollbackVerifier(
        events=events,
        composition_factory=composition_factory,
    )


def verify_adaptive_rollback(
    *,
    events: EventRegistry | None = None,
    base_environ: dict[str, str] | None = None,
    composition_factory: CompositionFactory | None = None,
) -> RollbackVerificationResult:
    """Convenience entry point for ops / tests."""
    return build_rollback_verifier(
        events=events,
        composition_factory=composition_factory,
    ).verify(base_environ=base_environ)


__all__ = [
    "RollbackVerificationResult",
    "RollbackVerifier",
    "build_rollback_verifier",
    "verify_adaptive_rollback",
]
