"""Stateless routing rules for the Mission Adapter.

Deterministic only — no educational reasoning, no randomness.
"""

from __future__ import annotations

import hashlib

from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.dto.routing_decision import (
    RoutingDecision,
    RoutingMode,
    SelectedEngine,
)
from app.application.mission_adapter.exceptions import RoutingError
from app.application.mission_adapter.migration_manager import MigrationPhase


class RoutingPolicy:
    """Deterministic routing rules (stateless)."""

    # Stable A/B bucket labels.
    BUCKET_A = "a"
    BUCKET_B = "b"

    @staticmethod
    def mode_for_phase(phase: MigrationPhase) -> RoutingMode:
        """Map migration phase onto a default routing mode."""
        mapping = {
            MigrationPhase.LEGACY_ONLY: RoutingMode.LEGACY,
            MigrationPhase.PARALLEL_VALIDATION: RoutingMode.PARALLEL,
            MigrationPhase.LIMITED_V2: RoutingMode.A_B,
            MigrationPhase.FULL_V2: RoutingMode.V2_ONLY,
            MigrationPhase.RETIRED_V1: RoutingMode.V2_ONLY,
        }
        try:
            return mapping[phase]
        except KeyError as exc:
            raise RoutingError(f"Unknown migration phase: {phase!r}") from exc

    @staticmethod
    def ab_bucket(learner_id: str, *, salt: str = "mission-adapter-ab") -> str:
        """Deterministic A/B bucket from learner identity.

        Same learner_id + salt always yields the same bucket.
        """
        digest = hashlib.sha256(f"{salt}:{learner_id}".encode()).hexdigest()
        return (
            RoutingPolicy.BUCKET_A
            if int(digest[:8], 16) % 2 == 0
            else RoutingPolicy.BUCKET_B
        )

    @staticmethod
    def decide(
        *,
        mode: RoutingMode,
        request: AdapterRequest,
        v2_enabled: bool,
        v1_available: bool,
        v2_available: bool,
        ab_salt: str = "mission-adapter-ab",
    ) -> RoutingDecision:
        """Produce a deterministic routing decision.

        Raises:
            RoutingError: When the mode cannot be satisfied.
        """
        if mode == RoutingMode.LEGACY:
            if not v1_available:
                raise RoutingError("LEGACY mode requires V1 engine")
            return RoutingDecision(
                mode=mode,
                primary_engine=SelectedEngine.V1,
                shadow_engine=None,
                compare=False,
                expose_v2=False,
                reason="legacy_only",
                fallback_engine=None,
            )

        if mode == RoutingMode.V2_ONLY:
            if not v2_enabled:
                raise RoutingError("V2_ONLY mode requires V2 feature gate")
            if not v2_available:
                raise RoutingError("V2_ONLY mode requires V2 engine")
            fallback = SelectedEngine.V1 if v1_available else None
            return RoutingDecision(
                mode=mode,
                primary_engine=SelectedEngine.V2,
                shadow_engine=None,
                compare=False,
                expose_v2=True,
                reason="v2_only",
                fallback_engine=fallback,
            )

        if mode == RoutingMode.SHADOW:
            if not v1_available:
                raise RoutingError("SHADOW mode requires V1 engine")
            shadow = SelectedEngine.V2 if (v2_enabled and v2_available) else None
            return RoutingDecision(
                mode=mode,
                primary_engine=SelectedEngine.V1,
                shadow_engine=shadow,
                compare=shadow is not None,
                expose_v2=False,
                reason="shadow_v1_primary",
                fallback_engine=None,
            )

        if mode == RoutingMode.PARALLEL:
            if not v1_available:
                raise RoutingError("PARALLEL mode requires V1 engine")
            if not (v2_enabled and v2_available):
                # Degrade to legacy when V2 cannot participate.
                return RoutingDecision(
                    mode=mode,
                    primary_engine=SelectedEngine.V1,
                    shadow_engine=None,
                    compare=False,
                    expose_v2=False,
                    reason="parallel_degraded_v1",
                    fallback_engine=None,
                )
            return RoutingDecision(
                mode=mode,
                primary_engine=SelectedEngine.V1,
                shadow_engine=SelectedEngine.V2,
                compare=True,
                expose_v2=False,
                reason="parallel_validate",
                fallback_engine=None,
            )

        if mode == RoutingMode.A_B:
            if not v2_enabled:
                if not v1_available:
                    raise RoutingError("A_B without V2 requires V1 engine")
                return RoutingDecision(
                    mode=mode,
                    primary_engine=SelectedEngine.V1,
                    shadow_engine=None,
                    compare=False,
                    expose_v2=False,
                    reason="ab_v2_disabled",
                    fallback_engine=None,
                    ab_bucket=None,
                )
            bucket = RoutingPolicy.ab_bucket(request.learner_id, salt=ab_salt)
            if bucket == RoutingPolicy.BUCKET_B and v2_available:
                return RoutingDecision(
                    mode=mode,
                    primary_engine=SelectedEngine.V2,
                    shadow_engine=None,
                    compare=False,
                    expose_v2=True,
                    reason="ab_bucket_b_v2",
                    fallback_engine=(
                        SelectedEngine.V1 if v1_available else None
                    ),
                    ab_bucket=bucket,
                )
            if not v1_available:
                raise RoutingError("A_B bucket A requires V1 engine")
            return RoutingDecision(
                mode=mode,
                primary_engine=SelectedEngine.V1,
                shadow_engine=None,
                compare=False,
                expose_v2=False,
                reason="ab_bucket_a_v1",
                fallback_engine=None,
                ab_bucket=bucket,
            )

        raise RoutingError(f"Unsupported routing mode: {mode!r}")
