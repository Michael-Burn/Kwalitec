"""Rollback verification for Strategy Shadow Validation (MS-005 S3).

Verifies that disabling KWALITEC_STRATEGY_ENGINE immediately removes Strategy
Engine participation while preserving Runtime A, Twin, Adaptive Engine, and
Experience behaviour. Observational only — no Experience UX authority cutover.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.strategy_engine import (
    shadow_telemetry as telemetry,
)
from app.infrastructure.events.registry import EventRegistry

CompositionFactory = Callable[..., tuple[Any, Any]]


@dataclass(frozen=True)
class StrategyShadowRollbackResult:
    """Outcome of an observational Strategy flag rollback drill."""

    ok: bool
    strategy_disabled_removes_participation: bool
    runtime_a_unchanged: bool
    twin_flags_unchanged: bool
    adaptive_flags_unchanged: bool
    experience_preserved: bool
    feature_flag_isolation_ok: bool
    details: tuple[str, ...] = ()

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_flags_unchanged": self.adaptive_flags_unchanged,
            "details": list(self.details),
            "experience_preserved": self.experience_preserved,
            "feature_flag_isolation_ok": self.feature_flag_isolation_ok,
            "ok": self.ok,
            "runtime_a_unchanged": self.runtime_a_unchanged,
            "strategy_disabled_removes_participation": (
                self.strategy_disabled_removes_participation
            ),
            "twin_flags_unchanged": self.twin_flags_unchanged,
        }


class StrategyShadowRollback:
    """Verify Strategy flag OFF removes Strategy DI while Experience continues."""

    VERIFIER_ID = "strategy_shadow_rollback"
    VERIFIER_VERSION = "1.0.0-s3"

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
    ) -> StrategyShadowRollbackResult:
        """Run KWALITEC_STRATEGY_ENGINE OFF drill and report Strategy removal.

        Does not mutate Runtime A. Does not enable Experience Strategy authority.
        Does not alter Twin or Adaptive participation flags.
        """
        from app.infrastructure.adapters.student_experience.composition import (
            build_production_experience,
        )

        factory = self._composition_factory or build_production_experience
        base = dict(base_environ or {})
        details: list[str] = []

        on_env = {
            **base,
            "KWALITEC_STRATEGY_ENGINE": "1",
            "KWALITEC_DIGITAL_TWIN": base.get("KWALITEC_DIGITAL_TWIN", "0"),
            "KWALITEC_ADAPTIVE_ENGINE": base.get("KWALITEC_ADAPTIVE_ENGINE", "0"),
            "KWALITEC_ADAPTIVE_SHADOW": base.get("KWALITEC_ADAPTIVE_SHADOW", "0"),
            "KWALITEC_ADAPTIVE_AUTHORITY": base.get(
                "KWALITEC_ADAPTIVE_AUTHORITY", "0"
            ),
        }
        on_flags = resolve_v2_feature_flags(environ=on_env)
        on_comp, on_service = factory(flags=on_flags)
        strategy_on = (
            getattr(on_comp, "strategy_engine", None) is not None
            and getattr(on_comp, "strategy_explainability", None) is not None
            and getattr(on_comp, "strategy_projector", None) is not None
            and getattr(on_comp, "strategy_projection_port", None) is not None
            and getattr(on_comp, "strategy_shadow", None) is not None
        )
        experience_on = getattr(on_comp, "twin", None) is not None
        if strategy_on:
            details.append("strategy_di_present_when_flag_on")
        else:
            details.append("FAIL:strategy_di_missing_when_flag_on")
        if experience_on:
            details.append("experience_adapters_present_when_flag_on")
        else:
            details.append("FAIL:experience_adapters_missing_when_flag_on")

        off_env = {
            **base,
            "KWALITEC_STRATEGY_ENGINE": "0",
            "KWALITEC_DIGITAL_TWIN": on_env["KWALITEC_DIGITAL_TWIN"],
            "KWALITEC_ADAPTIVE_ENGINE": on_env["KWALITEC_ADAPTIVE_ENGINE"],
            "KWALITEC_ADAPTIVE_SHADOW": on_env["KWALITEC_ADAPTIVE_SHADOW"],
            "KWALITEC_ADAPTIVE_AUTHORITY": on_env["KWALITEC_ADAPTIVE_AUTHORITY"],
        }
        off_flags = resolve_v2_feature_flags(environ=off_env)
        off_comp, off_service = factory(flags=off_flags)
        strategy_off = (
            getattr(off_comp, "strategy_engine", None) is None
            and getattr(off_comp, "strategy_explainability", None) is None
            and getattr(off_comp, "strategy_projector", None) is None
            and getattr(off_comp, "strategy_projection_port", None) is None
            and getattr(off_comp, "strategy_shadow", None) is None
        )
        experience_off = getattr(off_comp, "twin", None) is not None
        if strategy_off:
            details.append("strategy_participation_removed_when_flag_off")
        else:
            details.append(
                "FAIL:strategy_participation_still_present_when_flag_off"
            )
        if experience_off:
            details.append("experience_adapters_preserved_when_flag_off")
        else:
            details.append("FAIL:experience_adapters_missing_when_flag_off")

        twin_unchanged = (
            off_flags.ENABLE_DIGITAL_TWIN == on_flags.ENABLE_DIGITAL_TWIN
        )
        if twin_unchanged:
            details.append("twin_flags_independent_of_strategy")
        else:
            details.append("FAIL:twin_flags_changed_by_strategy_rollback")

        adaptive_unchanged = (
            off_flags.ENABLE_ADAPTIVE_ENGINE == on_flags.ENABLE_ADAPTIVE_ENGINE
            and off_flags.ENABLE_ADAPTIVE_ENGINE_SHADOW
            == on_flags.ENABLE_ADAPTIVE_ENGINE_SHADOW
            and off_flags.ENABLE_ADAPTIVE_AUTHORITY
            == on_flags.ENABLE_ADAPTIVE_AUTHORITY
        )
        if adaptive_unchanged:
            details.append("adaptive_flags_independent_of_strategy")
        else:
            details.append("FAIL:adaptive_flags_changed_by_strategy_rollback")

        # Runtime A bridge flags must be independent of Strategy OFF.
        runtime_a_unchanged = (
            off_flags.ENABLE_MISSION_READ_BRIDGE
            == on_flags.ENABLE_MISSION_READ_BRIDGE
            and off_flags.ENABLE_MISSION_START_BRIDGE
            == on_flags.ENABLE_MISSION_START_BRIDGE
            and off_flags.ENABLE_RECOMMENDATION_BRIDGE
            == on_flags.ENABLE_RECOMMENDATION_BRIDGE
            and off_flags.ENABLE_JOURNEY_BRIDGE == on_flags.ENABLE_JOURNEY_BRIDGE
            and off_flags.ENABLE_HISTORY_BRIDGE == on_flags.ENABLE_HISTORY_BRIDGE
        )
        if runtime_a_unchanged:
            details.append("runtime_a_flags_independent_of_strategy")
        else:
            details.append("FAIL:runtime_a_flags_changed_by_strategy_rollback")

        service_ok = on_service is not None and off_service is not None
        if service_ok:
            details.append("experience_service_constructed_both_modes")
        else:
            details.append("FAIL:experience_service_construction_failed")

        strategy_removed = strategy_off
        experience_preserved = experience_on and experience_off and service_ok
        isolation_ok = (
            strategy_on
            and strategy_off
            and twin_unchanged
            and adaptive_unchanged
            and runtime_a_unchanged
        )
        ok = (
            strategy_removed
            and experience_preserved
            and isolation_ok
            and runtime_a_unchanged
        )

        if self._health is not None:
            self._health.record_rollback(ok=ok)
            self._health.record_feature_flag_isolation(passed=isolation_ok)

        result = StrategyShadowRollbackResult(
            ok=ok,
            strategy_disabled_removes_participation=strategy_removed,
            runtime_a_unchanged=runtime_a_unchanged,
            twin_flags_unchanged=twin_unchanged,
            adaptive_flags_unchanged=adaptive_unchanged,
            experience_preserved=experience_preserved,
            feature_flag_isolation_ok=isolation_ok,
            details=tuple(details),
        )
        telemetry.emit_rollback_verified(
            self._events,
            ok=result.ok,
            details=result.details,
        )
        return result


def build_strategy_shadow_rollback(
    *,
    events: EventRegistry | None = None,
    composition_factory: CompositionFactory | None = None,
    health: Any | None = None,
) -> StrategyShadowRollback:
    """DI helper for StrategyShadowRollback."""
    return StrategyShadowRollback(
        events=events,
        composition_factory=composition_factory,
        health=health,
    )


def verify_strategy_shadow_rollback(
    *,
    events: EventRegistry | None = None,
    base_environ: dict[str, str] | None = None,
    composition_factory: CompositionFactory | None = None,
    health: Any | None = None,
) -> StrategyShadowRollbackResult:
    """Convenience entry point for ops / tests."""
    return build_strategy_shadow_rollback(
        events=events,
        composition_factory=composition_factory,
        health=health,
    ).verify(base_environ=base_environ)


__all__ = [
    "StrategyShadowRollback",
    "StrategyShadowRollbackResult",
    "build_strategy_shadow_rollback",
    "verify_strategy_shadow_rollback",
]
