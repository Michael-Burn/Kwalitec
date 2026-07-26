"""Rollback verification for Twin & Authority soak (EP-002.3).

Demonstrates Twin OFF → Authority OFF restores pre-soak composition
without behavioural regressions. Extends Twin shadow rollback with
explicit Authority OFF belt-and-braces checks.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain import soak_telemetry as telemetry
from app.infrastructure.adapters.consumer_chain.authority_matrix import (
    classify_twin_port,
)
from app.infrastructure.adapters.consumer_chain.soak_contracts import (
    TWINPORT_EXPERIENCE,
    TWINPORT_FOUNDATION_AUTHORITY,
)
from app.infrastructure.adapters.digital_twin.shadow_rollback import (
    verify_twin_rollback,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry

CompositionFactory = Callable[..., tuple[Any, Any]]


@dataclass(frozen=True)
class TwinAuthoritySoakRollbackResult:
    """Outcome of Twin OFF → Authority OFF rollback drill."""

    ok: bool
    twin_off_removes_participation: bool
    authority_off_restores_experience_port: bool
    flags_match_pre_soak: bool
    adaptive_flags_unchanged: bool
    behavioural_regressions: int
    details: tuple[str, ...] = ()

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_flags_unchanged": self.adaptive_flags_unchanged,
            "authority_off_restores_experience_port": (
                self.authority_off_restores_experience_port
            ),
            "behavioural_regressions": self.behavioural_regressions,
            "details": list(self.details),
            "flags_match_pre_soak": self.flags_match_pre_soak,
            "ok": self.ok,
            "twin_off_removes_participation": (
                self.twin_off_removes_participation
            ),
        }


class TwinAuthoritySoakRollbackVerifier:
    """Verify soak peak → Twin OFF → Authority OFF restores pre-soak."""

    VERIFIER_ID = "twin_authority_soak_rollback_verifier"
    VERIFIER_VERSION = "ep002.3.0"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        structured: StructuredLogger | None = None,
        composition_factory: CompositionFactory | None = None,
        health: Any | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._structured = structured or StructuredLogger(
            "kwalitec.consumer_chain.soak"
        )
        self._composition_factory = composition_factory
        self._health = health

    def verify(
        self,
        *,
        base_environ: dict[str, str] | None = None,
    ) -> TwinAuthoritySoakRollbackResult:
        """Run Twin OFF → Authority OFF drill from soak peak (both ON)."""
        from app.infrastructure.adapters.student_experience.composition import (
            build_production_experience,
        )

        factory = self._composition_factory or build_production_experience
        base = dict(base_environ or {})
        details: list[str] = []
        regressions = 0

        # Peak soak: Twin ON + Authority ON.
        peak_env = {
            **base,
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1",
            "KWALITEC_ADAPTIVE_ENGINE": base.get("KWALITEC_ADAPTIVE_ENGINE", "0"),
            "KWALITEC_ADAPTIVE_SHADOW": base.get("KWALITEC_ADAPTIVE_SHADOW", "0"),
            "KWALITEC_ADAPTIVE_AUTHORITY": base.get(
                "KWALITEC_ADAPTIVE_AUTHORITY", "0"
            ),
        }
        peak_flags = resolve_v2_feature_flags(environ=peak_env)
        peak_comp, peak_service = factory(flags=peak_flags)
        peak_port = classify_twin_port(getattr(peak_comp, "twin", None))
        if (
            peak_flags.ENABLE_DIGITAL_TWIN
            and peak_flags.ENABLE_DIGITAL_TWIN_AUTHORITY
            and peak_port == TWINPORT_FOUNDATION_AUTHORITY
        ):
            details.append("peak_authority_port_active")
        elif peak_flags.ENABLE_DIGITAL_TWIN:
            details.append("peak_twin_on_authority_routing_observed")
        else:
            details.append("FAIL:peak_twin_not_enabled")
            regressions += 1

        # Step 1: Twin OFF (Authority env may still be 1 — must resolve OFF).
        twin_off_env = {
            **peak_env,
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1",
        }
        twin_off_flags = resolve_v2_feature_flags(environ=twin_off_env)
        twin_off_comp, twin_off_service = factory(flags=twin_off_flags)
        twin_removed = (
            getattr(twin_off_comp, "digital_twin", None) is None
            and getattr(twin_off_comp, "twin_foundation", None) is None
            and getattr(twin_off_comp, "twin_shadow", None) is None
        )
        authority_cleared = (
            twin_off_flags.ENABLE_DIGITAL_TWIN_AUTHORITY is False
            and not bool(getattr(twin_off_comp, "twin_authority_enabled", True))
        )
        twin_off_port = classify_twin_port(getattr(twin_off_comp, "twin", None))
        experience_preserved = twin_off_port == TWINPORT_EXPERIENCE

        if twin_removed:
            details.append("twin_participation_removed")
        else:
            details.append("FAIL:twin_participation_still_present")
            regressions += 1
        if authority_cleared:
            details.append("authority_auto_cleared_when_twin_off")
        else:
            details.append("FAIL:authority_still_resolved_when_twin_off")
            regressions += 1
        if experience_preserved:
            details.append("experience_twin_port_restored_after_twin_off")
        else:
            details.append("FAIL:experience_twin_port_missing_after_twin_off")
            regressions += 1

        # Step 2: Explicit Authority OFF (belt-and-braces pre-soak).
        pre_soak_env = {
            **twin_off_env,
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_DIGITAL_TWIN_AUTHORITY": "0",
        }
        pre_flags = resolve_v2_feature_flags(environ=pre_soak_env)
        pre_comp, pre_service = factory(flags=pre_flags)
        flags_match = (
            pre_flags.ENABLE_DIGITAL_TWIN is False
            and pre_flags.ENABLE_DIGITAL_TWIN_AUTHORITY is False
        )
        pre_port = classify_twin_port(getattr(pre_comp, "twin", None))
        authority_off_ok = (
            flags_match
            and pre_port == TWINPORT_EXPERIENCE
            and not bool(getattr(pre_comp, "twin_authority_enabled", True))
        )
        if authority_off_ok:
            details.append("authority_off_restores_pre_soak")
        else:
            details.append("FAIL:pre_soak_not_restored")
            regressions += 1

        adaptive_unchanged = (
            pre_flags.ENABLE_ADAPTIVE_ENGINE == peak_flags.ENABLE_ADAPTIVE_ENGINE
            and pre_flags.ENABLE_ADAPTIVE_ENGINE_SHADOW
            == peak_flags.ENABLE_ADAPTIVE_ENGINE_SHADOW
            and pre_flags.ENABLE_ADAPTIVE_AUTHORITY
            == peak_flags.ENABLE_ADAPTIVE_AUTHORITY
        )
        if adaptive_unchanged:
            details.append("adaptive_flags_independent")
        else:
            details.append("FAIL:adaptive_flags_changed")
            regressions += 1

        services_ok = all(
            s is not None
            for s in (peak_service, twin_off_service, pre_service)
        )
        if services_ok:
            details.append("experience_services_constructed")
        else:
            details.append("FAIL:experience_service_construction")
            regressions += 1

        twin_rollback = verify_twin_rollback(
            events=self._events,
            base_environ=base,
            composition_factory=factory,
        )
        if twin_rollback.ok:
            details.append("twin_shadow_rollback_ok")
        else:
            details.append("FAIL:twin_shadow_rollback")
            regressions += 1

        ok = (
            twin_removed
            and authority_cleared
            and experience_preserved
            and authority_off_ok
            and adaptive_unchanged
            and twin_rollback.ok
            and services_ok
            and regressions == 0
        )

        result = TwinAuthoritySoakRollbackResult(
            ok=ok,
            twin_off_removes_participation=twin_removed and twin_rollback.ok,
            authority_off_restores_experience_port=authority_off_ok,
            flags_match_pre_soak=flags_match,
            adaptive_flags_unchanged=adaptive_unchanged,
            behavioural_regressions=regressions,
            details=tuple(details),
        )
        if self._health is not None:
            self._health.record_rollback(ok=result.ok)
        telemetry.emit_rollback_verified(
            structured=self._structured,
            events=self._events,
            ok=result.ok,
            details=result.details,
        )
        return result


def build_twin_authority_soak_rollback_verifier(
    *,
    events: EventRegistry | None = None,
    structured: StructuredLogger | None = None,
    composition_factory: CompositionFactory | None = None,
    health: Any | None = None,
) -> TwinAuthoritySoakRollbackVerifier:
    """DI helper for soak rollback verifier."""
    return TwinAuthoritySoakRollbackVerifier(
        events=events,
        structured=structured,
        composition_factory=composition_factory,
        health=health,
    )


def verify_twin_authority_soak_rollback(
    *,
    events: EventRegistry | None = None,
    structured: StructuredLogger | None = None,
    base_environ: dict[str, str] | None = None,
    composition_factory: CompositionFactory | None = None,
    health: Any | None = None,
) -> TwinAuthoritySoakRollbackResult:
    """Convenience entry point for ops / tests."""
    return build_twin_authority_soak_rollback_verifier(
        events=events,
        structured=structured,
        composition_factory=composition_factory,
        health=health,
    ).verify(base_environ=base_environ)


__all__ = [
    "TwinAuthoritySoakRollbackResult",
    "TwinAuthoritySoakRollbackVerifier",
    "build_twin_authority_soak_rollback_verifier",
    "verify_twin_authority_soak_rollback",
]
