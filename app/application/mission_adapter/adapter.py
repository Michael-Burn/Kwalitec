"""MissionAdapter — sole public entry point for mission generation.

Responsible only for routing, comparison, auditing, and migration safety.
Contains NO educational logic. Depends only on injected engine contracts —
never instantiates Mission Engine V1 or Mission Engine V2 directly.
"""

from __future__ import annotations

import time
from types import MappingProxyType

from app.application.mission_adapter.audit_service import AuditService
from app.application.mission_adapter.comparison_service import ComparisonService
from app.application.mission_adapter.contracts import MissionEnginePort
from app.application.mission_adapter.dto.adapter_request import AdapterRequest
from app.application.mission_adapter.dto.adapter_result import AdapterResult
from app.application.mission_adapter.dto.comparison_result import ComparisonResult
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot
from app.application.mission_adapter.dto.routing_decision import (
    RoutingDecision,
    SelectedEngine,
)
from app.application.mission_adapter.exceptions import (
    ComparisonFailure,
    EngineUnavailable,
    MissionAdapterError,
)
from app.application.mission_adapter.feature_gate import FeatureGate
from app.application.mission_adapter.health_monitor import HealthMonitor
from app.application.mission_adapter.migration_manager import MigrationManager
from app.application.mission_adapter.router import MissionRouter

_LIFECYCLE_OPS = frozenset(
    {
        "generate_mission",
        "resume_mission",
        "pause_mission",
        "skip_mission",
        "archive_mission",
    }
)


class MissionAdapter:
    """Single public interface for mission operations.

    Dashboard and future APIs must call this adapter — never Mission
    Engine V1 or Mission Engine 2.0 directly.
    """

    ADAPTER_VERSION = "mission-adapter-1"

    def __init__(
        self,
        *,
        router: MissionRouter,
        feature_gate: FeatureGate,
        migration_manager: MigrationManager,
        comparison_service: ComparisonService | None = None,
        audit_service: AuditService | None = None,
        health_monitor: HealthMonitor | None = None,
        clock=None,
    ) -> None:
        self._router = router
        self._gate = feature_gate
        self._migration = migration_manager
        self._comparison = comparison_service or ComparisonService()
        self._audit = audit_service or AuditService(clock=clock)
        self._health = health_monitor or HealthMonitor(clock=clock)

    # ------------------------------------------------------------------
    # Construction helper
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        *,
        v1_engine: MissionEnginePort | None = None,
        v2_engine: MissionEnginePort | None = None,
        global_v2_enabled: bool = False,
        migration_manager: MigrationManager | None = None,
        allowed_cohorts: frozenset[str] | set[str] | None = None,
        allowed_organisations: frozenset[str] | set[str] | None = None,
        allowed_environments: frozenset[str] | set[str] | None = None,
        clock=None,
        ab_salt: str = "mission-adapter-ab",
    ) -> MissionAdapter:
        """Build an adapter with default collaborators (DI-friendly).

        Engines are injected — never constructed here.
        """
        migration = migration_manager or MigrationManager()
        gate = FeatureGate(
            migration_manager=migration,
            global_enabled=global_v2_enabled,
            allowed_cohorts=allowed_cohorts,
            allowed_organisations=allowed_organisations,
            allowed_environments=allowed_environments,
        )
        router = MissionRouter(
            migration_manager=migration,
            feature_gate=gate,
            v1_engine=v1_engine,
            v2_engine=v2_engine,
            ab_salt=ab_salt,
        )
        return cls(
            router=router,
            feature_gate=gate,
            migration_manager=migration,
            audit_service=AuditService(clock=clock),
            health_monitor=HealthMonitor(clock=clock),
            clock=clock,
        )

    # ------------------------------------------------------------------
    # Public operations
    # ------------------------------------------------------------------

    def generate_mission(self, request: AdapterRequest) -> AdapterResult:
        """Generate a mission via the routed engine(s)."""
        return self._execute("generate_mission", request)

    def resume_mission(self, request: AdapterRequest) -> AdapterResult:
        """Resume a mission via the routed engine(s)."""
        return self._execute("resume_mission", request)

    def pause_mission(self, request: AdapterRequest) -> AdapterResult:
        """Pause a mission via the routed engine(s)."""
        return self._execute("pause_mission", request)

    def skip_mission(self, request: AdapterRequest) -> AdapterResult:
        """Skip a mission via the routed engine(s)."""
        return self._execute("skip_mission", request)

    def archive_mission(self, request: AdapterRequest) -> AdapterResult:
        """Archive a mission via the routed engine(s)."""
        return self._execute("archive_mission", request)

    def health_status(self) -> dict[str, object]:
        """Return health monitor status (never alters routing)."""
        return self._health.status(
            v1_available=self._router.v1_available(),
            v2_available=self._router.v2_available(),
            routing_mode=self._router.resolve_mode(),
            migration_phase=self._migration.phase.value,
        )

    def comparison_summary(self) -> dict[str, float | int | bool]:
        """Aggregate structural comparison statistics."""
        return self._comparison.summary()

    # ------------------------------------------------------------------
    # Accessors (for tests / operators — not educational APIs)
    # ------------------------------------------------------------------

    @property
    def migration_manager(self) -> MigrationManager:
        return self._migration

    @property
    def feature_gate(self) -> FeatureGate:
        return self._gate

    @property
    def router(self) -> MissionRouter:
        return self._router

    @property
    def audit_service(self) -> AuditService:
        return self._audit

    @property
    def comparison_service(self) -> ComparisonService:
        return self._comparison

    @property
    def health_monitor(self) -> HealthMonitor:
        return self._health

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _execute(self, operation: str, request: AdapterRequest) -> AdapterResult:
        if operation not in _LIFECYCLE_OPS:
            raise MissionAdapterError(f"Unsupported operation: {operation}")
        # Prefer explicit operation on the request when provided; otherwise
        # stamp the method name for audit consistency.
        if request.operation != operation:
            request = AdapterRequest(
                operation=operation,
                learner_id=request.learner_id,
                mission_id=request.mission_id,
                journey_id=request.journey_id,
                topic_id=request.topic_id,
                session_id=request.session_id,
                organisation_id=request.organisation_id,
                cohort_id=request.cohort_id,
                environment=request.environment,
                correlation_id=request.correlation_id,
                context=request.context,
            )

        started = time.perf_counter()
        decision = self._router.decide(request)
        fallbacks: list[str] = []
        fallback_used = False
        shadow_executed = False
        shadow_unavailable = False
        comparison: ComparisonResult | None = None
        comparison_failed = False
        comparison_diverged = False
        error_type: str | None = None
        success = True
        mission: MissionSnapshot | None = None
        selected = decision.primary_engine
        audit = None  # assigned in finally

        try:
            primary = self._invoke(decision.primary_engine, operation, request)
            mission = primary

            secondary: MissionSnapshot | None = None
            if decision.shadow_engine is not None:
                try:
                    secondary = self._invoke(
                        decision.shadow_engine, operation, request
                    )
                    shadow_executed = True
                except EngineUnavailable:
                    # Shadow failure must not break primary path.
                    comparison_failed = True
                    shadow_unavailable = True

            if decision.compare and secondary is not None:
                try:
                    comparison = self._comparison.compare(primary, secondary)
                    comparison_diverged = not comparison.matched
                except ComparisonFailure:
                    comparison_failed = True
                    raise

        except EngineUnavailable as exc:
            if decision.fallback_engine is not None:
                try:
                    mission = self._invoke(
                        decision.fallback_engine, operation, request
                    )
                    fallbacks.append(decision.fallback_engine.value)
                    fallback_used = True
                    selected = decision.fallback_engine
                except Exception as fallback_exc:  # noqa: BLE001
                    success = False
                    error_type = type(fallback_exc).__name__
                    raise EngineUnavailable(
                        f"Primary and fallback engines failed: {exc}; "
                        f"{fallback_exc}"
                    ) from fallback_exc
            else:
                success = False
                error_type = type(exc).__name__
                raise
        except MissionAdapterError as exc:
            success = False
            error_type = type(exc).__name__
            raise
        except Exception as exc:  # noqa: BLE001 — engine port may raise anything
            success = False
            error_type = type(exc).__name__
            raise MissionAdapterError(
                f"Engine operation {operation} failed: {exc}"
            ) from exc
        finally:
            duration_ms = (time.perf_counter() - started) * 1000.0
            versions = self._engine_versions()
            audit = self._audit.record(
                operation=operation,
                learner_id=request.learner_id,
                routing_mode=decision.mode,
                selected_engine=selected,
                fallbacks=tuple(fallbacks),
                duration_ms=duration_ms,
                comparison_executed=comparison is not None,
                comparison_id=(
                    comparison.comparison_id if comparison else None
                ),
                engine_versions=versions,
                success=success,
                error_type=error_type,
                correlation_id=request.correlation_id,
                organisation_id=request.organisation_id,
                metadata={
                    "adapter_version": self.ADAPTER_VERSION,
                    "reason": decision.reason,
                },
            )
            self._health.note_invocation(
                mode=decision.mode,
                success=success,
                fallback_used=fallback_used,
                comparison_executed=comparison is not None,
                comparison_failed=comparison_failed,
                comparison_diverged=comparison_diverged,
                error_type=error_type,
                v1_unavailable=(
                    decision.primary_engine == SelectedEngine.V1
                    and error_type == "EngineUnavailable"
                    and not fallback_used
                ),
                v2_unavailable=(
                    (
                        decision.primary_engine == SelectedEngine.V2
                        and error_type == "EngineUnavailable"
                        and not fallback_used
                    )
                    or shadow_unavailable
                ),
            )

        # Expose only what routing permits.
        exposed = mission
        if (
            exposed is not None
            and exposed.engine_id == "v2"
            and not decision.expose_v2
            and decision.primary_engine != SelectedEngine.V2
        ):
            # Defensive: never leak shadow V2 as the public mission.
            exposed = None

        return AdapterResult(
            mission=exposed,
            routing=decision,
            audit=audit,
            comparison=comparison,
            fallback_used=fallback_used,
            shadow_executed=shadow_executed,
        )

    def _invoke(
        self,
        selected: SelectedEngine,
        operation: str,
        request: AdapterRequest,
    ) -> MissionSnapshot:
        engine = self._router.engine_for(selected)
        method = getattr(engine, operation)
        return method(request)

    def _engine_versions(self) -> MappingProxyType:
        data: dict[str, str] = {"adapter": self.ADAPTER_VERSION}
        if self._router.v1_engine is not None:
            data["v1"] = self._router.v1_engine.engine_version
        if self._router.v2_engine is not None:
            data["v2"] = self._router.v2_engine.engine_version
        return MappingProxyType(data)

    def preview_routing(self, request: AdapterRequest) -> RoutingDecision:
        """Inspect routing without executing engines (operator / tests)."""
        return self._router.decide(request)
