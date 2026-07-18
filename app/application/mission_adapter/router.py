"""MissionRouter — deterministic engine selection for the Mission Adapter."""

from __future__ import annotations

from app.application.mission_adapter.contracts import MissionEnginePort
from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.dto.routing_decision import (
    RoutingDecision,
    RoutingMode,
    SelectedEngine,
)
from app.application.mission_adapter.exceptions import (
    EngineUnavailable,
    RoutingError,
)
from app.application.mission_adapter.feature_gate import FeatureGate
from app.application.mission_adapter.migration_manager import MigrationManager
from app.application.mission_adapter.policies.routing_policy import RoutingPolicy


class MissionRouter:
    """Determines which engine(s) execute for an adapter request.

    Routing decisions are deterministic given the same request, migration
    phase, feature gate, and engine availability. Never performs
    educational reasoning.
    """

    def __init__(
        self,
        *,
        migration_manager: MigrationManager,
        feature_gate: FeatureGate,
        v1_engine: MissionEnginePort | None = None,
        v2_engine: MissionEnginePort | None = None,
        mode_override: RoutingMode | None = None,
        ab_salt: str = "mission-adapter-ab",
    ) -> None:
        self._migration = migration_manager
        self._gate = feature_gate
        self._v1 = v1_engine
        self._v2 = v2_engine
        self._mode_override = mode_override
        self._ab_salt = ab_salt

    @property
    def v1_engine(self) -> MissionEnginePort | None:
        return self._v1

    @property
    def v2_engine(self) -> MissionEnginePort | None:
        return self._v2

    def bind_engines(
        self,
        *,
        v1_engine: MissionEnginePort | None = None,
        v2_engine: MissionEnginePort | None = None,
    ) -> None:
        """Replace injected engine ports (dependency injection)."""
        if v1_engine is not None:
            self._v1 = v1_engine
        if v2_engine is not None:
            self._v2 = v2_engine

    def set_mode_override(self, mode: RoutingMode | None) -> None:
        """Force a routing mode (tests / operator); None restores phase map."""
        self._mode_override = mode

    def resolve_mode(self) -> RoutingMode:
        """Active routing mode (override or migration-derived)."""
        if self._mode_override is not None:
            return self._mode_override
        return RoutingPolicy.mode_for_phase(self._migration.phase)

    def v1_bound(self) -> bool:
        """True when a V1 port is injected and V1 is not retired."""
        if self._migration.v1_retired():
            return False
        return self._v1 is not None

    def v2_bound(self) -> bool:
        """True when a V2 port is injected."""
        return self._v2 is not None

    def v1_available(self) -> bool:
        """True when V1 port is bound and reports available."""
        return self.v1_bound() and self._v1.is_available()  # type: ignore[union-attr]

    def v2_available(self) -> bool:
        """True when V2 port is bound and reports available."""
        return self.v2_bound() and self._v2.is_available()  # type: ignore[union-attr]

    def decide(self, request: AdapterRequest) -> RoutingDecision:
        """Produce a deterministic routing decision for ``request``.

        Presence (bound) drives mode legality. Liveness is checked when
        engines are invoked so failures become ``EngineUnavailable`` with
        an audit trail rather than a pre-invoke routing error.
        """
        mode = self.resolve_mode()
        return RoutingPolicy.decide(
            mode=mode,
            request=request,
            v2_enabled=self._gate.is_v2_enabled(request),
            v1_available=self.v1_bound(),
            v2_available=self.v2_bound(),
            ab_salt=self._ab_salt,
        )

    def engine_for(self, selected: SelectedEngine) -> MissionEnginePort:
        """Resolve a selected engine enum to an injected port.

        Raises:
            EngineUnavailable: When the port is missing or unhealthy.
            RoutingError: When ``selected`` is NONE.
        """
        if selected == SelectedEngine.NONE:
            raise RoutingError("No engine selected")
        if selected == SelectedEngine.V1:
            if not self.v1_available() or self._v1 is None:
                raise EngineUnavailable("V1 mission engine unavailable")
            return self._v1
        if selected == SelectedEngine.V2:
            if not self.v2_available() or self._v2 is None:
                raise EngineUnavailable("V2 mission engine unavailable")
            return self._v2
        raise RoutingError(f"Unknown selected engine: {selected!r}")
