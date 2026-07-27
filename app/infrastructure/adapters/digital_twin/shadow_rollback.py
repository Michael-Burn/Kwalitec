"""Rollback verification for Twin Shadow Validation (MS-004 T6).

Verifies that disabling KWALITEC_DIGITAL_TWIN immediately removes Twin
participation while preserving existing Experience behaviour.
Observational only — no Experience UX authority cutover.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.digital_twin import (
    shadow_telemetry as telemetry,
)
from app.infrastructure.events.registry import EventRegistry

CompositionFactory = Callable[..., tuple[Any, Any]]


@dataclass(frozen=True)
class TwinRollbackVerificationResult:
    """Outcome of an observational Twin flag rollback drill."""

    ok: bool
    twin_disabled_removes_participation: bool
    experience_twin_port_preserved: bool
    adaptive_flags_unchanged: bool
    feature_flag_isolation_ok: bool
    details: tuple[str, ...] = ()

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_flags_unchanged": self.adaptive_flags_unchanged,
            "details": list(self.details),
            "experience_twin_port_preserved": self.experience_twin_port_preserved,
            "feature_flag_isolation_ok": self.feature_flag_isolation_ok,
            "ok": self.ok,
            "twin_disabled_removes_participation": (
                self.twin_disabled_removes_participation
            ),
        }


class TwinRollbackVerifier:
    """Verify Digital Twin flag OFF removes Twin DI while Experience continues."""

    VERIFIER_ID = "twin_rollback_verifier"
    VERIFIER_VERSION = "1.0.0-t6"

    def __init__(
        self,
        *,
        events: EventRegistry | None = None,
        composition_factory: CompositionFactory | None = None,
        health: Any | None = None,
    ) -> None:
        self._events = events or EventRegistry()
        self._composition_factory = composition_factory
        self._health = health

    def verify(
        self,
        *,
        base_environ: dict[str, str] | None = None,
    ) -> TwinRollbackVerificationResult:
        """Run KWALITEC_DIGITAL_TWIN OFF drill and report Twin removal.

        Does not mutate Runtime A. Does not enable Experience Twin authority.
        """
        factory = self._composition_factory
        if factory is None:
            from app.infrastructure.adapters.twin_rollback_defaults import (
                default_composition_factory,
            )

            factory = default_composition_factory
        base = dict(base_environ or {})
        details: list[str] = []

        # Twin ON baseline — Twin DI present; Experience Twin port remains UX SoT.
        on_env = {
            **base,
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_ADAPTIVE_ENGINE": base.get("KWALITEC_ADAPTIVE_ENGINE", "0"),
            "KWALITEC_ADAPTIVE_SHADOW": base.get("KWALITEC_ADAPTIVE_SHADOW", "0"),
            "KWALITEC_ADAPTIVE_AUTHORITY": base.get(
                "KWALITEC_ADAPTIVE_AUTHORITY", "0"
            ),
        }
        on_flags = resolve_v2_feature_flags(environ=on_env)
        on_comp, on_service = factory(flags=on_flags)
        twin_on = (
            getattr(on_comp, "twin_snapshot_builder", None) is not None
            and getattr(on_comp, "student_twin_projection_port", None) is not None
            and getattr(on_comp, "twin_shadow", None) is not None
        )
        experience_on = getattr(on_comp, "twin", None) is not None
        if twin_on:
            details.append("twin_di_present_when_flag_on")
        else:
            details.append("FAIL:twin_di_missing_when_flag_on")
        if experience_on:
            details.append("experience_twin_adapter_present_when_flag_on")
        else:
            details.append("FAIL:experience_twin_adapter_missing_when_flag_on")

        # Twin OFF — Twin participation removed; Experience Twin adapter remains.
        off_env = {
            **base,
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_ADAPTIVE_ENGINE": on_env["KWALITEC_ADAPTIVE_ENGINE"],
            "KWALITEC_ADAPTIVE_SHADOW": on_env["KWALITEC_ADAPTIVE_SHADOW"],
            "KWALITEC_ADAPTIVE_AUTHORITY": on_env["KWALITEC_ADAPTIVE_AUTHORITY"],
        }
        off_flags = resolve_v2_feature_flags(environ=off_env)
        off_comp, off_service = factory(flags=off_flags)
        twin_off = (
            getattr(off_comp, "digital_twin", None) is None
            and getattr(off_comp, "twin_facet_assembler", None) is None
            and getattr(off_comp, "twin_snapshot_builder", None) is None
            and getattr(off_comp, "twin_explainability", None) is None
            and getattr(off_comp, "twin_input_adapter", None) is None
            and getattr(off_comp, "student_twin_projector", None) is None
            and getattr(off_comp, "student_twin_projection_port", None) is None
            and getattr(off_comp, "twin_shadow", None) is None
        )
        experience_off = getattr(off_comp, "twin", None) is not None
        if twin_off:
            details.append("twin_participation_removed_when_flag_off")
        else:
            details.append("FAIL:twin_participation_still_present_when_flag_off")
        if experience_off:
            details.append("experience_twin_adapter_preserved_when_flag_off")
        else:
            details.append("FAIL:experience_twin_adapter_missing_when_flag_off")

        # Adaptive flags must be independent of Twin OFF.
        adaptive_unchanged = (
            off_flags.ENABLE_ADAPTIVE_ENGINE == on_flags.ENABLE_ADAPTIVE_ENGINE
            and off_flags.ENABLE_ADAPTIVE_ENGINE_SHADOW
            == on_flags.ENABLE_ADAPTIVE_ENGINE_SHADOW
            and off_flags.ENABLE_ADAPTIVE_AUTHORITY
            == on_flags.ENABLE_ADAPTIVE_AUTHORITY
        )
        if adaptive_unchanged:
            details.append("adaptive_flags_independent_of_twin")
        else:
            details.append("FAIL:adaptive_flags_changed_by_twin_rollback")

        # Spot-check Experience service still constructs with Twin OFF.
        service_ok = on_service is not None and off_service is not None
        if service_ok:
            details.append("experience_service_constructed_both_modes")
        else:
            details.append("FAIL:experience_service_construction_failed")

        twin_removed = twin_off
        experience_preserved = experience_on and experience_off and service_ok
        isolation_ok = twin_on and twin_off and adaptive_unchanged
        ok = twin_removed and experience_preserved and isolation_ok

        if self._health is not None:
            self._health.record_rollback(ok=ok)
            self._health.record_feature_flag_isolation(passed=isolation_ok)

        result = TwinRollbackVerificationResult(
            ok=ok,
            twin_disabled_removes_participation=twin_removed,
            experience_twin_port_preserved=experience_preserved,
            adaptive_flags_unchanged=adaptive_unchanged,
            feature_flag_isolation_ok=isolation_ok,
            details=tuple(details),
        )
        telemetry.emit_rollback_verified(
            self._events,
            ok=result.ok,
            details=result.details,
        )
        return result


def build_twin_rollback_verifier(
    *,
    events: EventRegistry | None = None,
    composition_factory: CompositionFactory | None = None,
    health: Any | None = None,
) -> TwinRollbackVerifier:
    """DI helper for TwinRollbackVerifier."""
    return TwinRollbackVerifier(
        events=events,
        composition_factory=composition_factory,
        health=health,
    )


def verify_twin_rollback(
    *,
    events: EventRegistry | None = None,
    base_environ: dict[str, str] | None = None,
    composition_factory: CompositionFactory | None = None,
    health: Any | None = None,
) -> TwinRollbackVerificationResult:
    """Convenience entry point for ops / tests."""
    return build_twin_rollback_verifier(
        events=events,
        composition_factory=composition_factory,
        health=health,
    ).verify(base_environ=base_environ)


__all__ = [
    "TwinRollbackVerificationResult",
    "TwinRollbackVerifier",
    "build_twin_rollback_verifier",
    "verify_twin_rollback",
]
