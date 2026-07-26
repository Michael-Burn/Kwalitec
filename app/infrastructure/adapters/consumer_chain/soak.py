"""Twin & Authority non-production soak orchestrator (EP-002.3).

Exercises Twin-gated ``build_*`` APIs, Authority matrix routing, and
rollback under observational telemetry. Never influences student UX,
HTTP routes, or Runtime A writes.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from typing import Any

from app.infrastructure.adapters.consumer_chain import soak_telemetry as telemetry
from app.infrastructure.adapters.consumer_chain.authority_matrix import (
    run_authority_matrix,
    verify_authority_fail_open,
)
from app.infrastructure.adapters.consumer_chain.contracts import (
    API_BUILD_DAILY_STUDY_PLAN,
    API_BUILD_READINESS_INTELLIGENCE,
    API_BUILD_STUDY_INSIGHTS,
    LOG_FOUNDATION_ASSEMBLE,
    OUTCOME_EXCEPTION,
    OUTCOME_SUCCESS,
    OUTCOME_UNAVAILABLE,
)
from app.infrastructure.adapters.consumer_chain.observer import (
    classify_build_result,
)
from app.infrastructure.adapters.consumer_chain.soak_contracts import (
    CELL_TWIN_ON_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_ON,
    SOAK_ADAPTER_ID,
    SOAK_ADAPTER_VERSION,
    SoakApiObservation,
    TwinAuthoritySoakReport,
)
from app.infrastructure.adapters.consumer_chain.soak_health import (
    TwinAuthoritySoakHealthMetrics,
    build_twin_authority_soak_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.soak_rollback import (
    verify_twin_authority_soak_rollback,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    build_consumer_chain_telemetry,
    set_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry

BuildPlanFn = Callable[..., Any]
BuildReadinessFn = Callable[..., Any]
BuildInsightsFn = Callable[..., Any]


class TwinAuthoritySoakOrchestrator:
    """Observational soak runner for Twin + Authority non-prod validation."""

    ADAPTER_ID = SOAK_ADAPTER_ID
    ADAPTER_VERSION = SOAK_ADAPTER_VERSION

    def __init__(
        self,
        *,
        enabled: bool = True,
        events: EventRegistry | None = None,
        structured: StructuredLogger | None = None,
        chain_telemetry: ConsumerChainTelemetry | None = None,
        health: TwinAuthoritySoakHealthMetrics | None = None,
        composition_factory: Callable[..., tuple[Any, Any]] | None = None,
        build_plan: BuildPlanFn | None = None,
        build_readiness: BuildReadinessFn | None = None,
        build_insights: BuildInsightsFn | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._events = events or EventRegistry()
        self._structured = structured or StructuredLogger(
            "kwalitec.consumer_chain.soak"
        )
        self._chain = chain_telemetry or build_consumer_chain_telemetry(
            structured=StructuredLogger("kwalitec.consumer_chain.soak.chain"),
            events=self._events,
        )
        self._health = health or build_twin_authority_soak_health_metrics()
        self._composition_factory = composition_factory
        self._build_plan = build_plan
        self._build_readiness = build_readiness
        self._build_insights = build_insights

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def health(self) -> TwinAuthoritySoakHealthMetrics:
        return self._health

    def _resolve_builders(
        self,
    ) -> tuple[BuildPlanFn, BuildReadinessFn, BuildInsightsFn]:
        if (
            self._build_plan is not None
            and self._build_readiness is not None
            and self._build_insights is not None
        ):
            return (
                self._build_plan,
                self._build_readiness,
                self._build_insights,
            )
        from app.services.planning_service import PlanningService
        from app.services.readiness_service import ReadinessService
        from app.services.recommendation_service import RecommendationService

        return (
            self._build_plan or PlanningService.build_daily_study_plan,
            self._build_readiness
            or ReadinessService.build_readiness_intelligence,
            self._build_insights or RecommendationService.build_study_insights,
        )

    def _ingest_foundation_records(self) -> None:
        for record in self._chain.records:
            if record.get("message") != LOG_FOUNDATION_ASSEMBLE:
                continue
            assembled = bool(record.get("assembled"))
            source = str(record.get("assemble_source") or "")
            self._health.record_foundation(
                assembled=assembled,
                share_hit=(source == "injected" or not assembled),
            )

    def _observe_call(
        self,
        *,
        api_name: str,
        student_id: str,
        twin_enabled: bool,
        authority_enabled: bool,
        call: Callable[[], Any],
    ) -> SoakApiObservation:
        telemetry.emit_requested(
            structured=self._structured,
            events=self._events,
            student_id=student_id,
            cell_id=(
                CELL_TWIN_ON_AUTHORITY_ON
                if authority_enabled
                else CELL_TWIN_ON_AUTHORITY_OFF
            ),
        )
        started = time.perf_counter()
        try:
            result = call()
        except Exception as exc:  # noqa: BLE001 — soak boundary
            latency_ms = (time.perf_counter() - started) * 1000.0
            self._health.record_execution(
                outcome=OUTCOME_EXCEPTION,
                latency_ms=latency_ms,
                exception=True,
            )
            telemetry.emit_failed(
                structured=self._structured,
                events=self._events,
                student_id=student_id,
                api_name=api_name,
                error_code=type(exc).__name__,
                latency_ms=latency_ms,
            )
            return SoakApiObservation(
                api_name=api_name,
                student_id=student_id,
                twin_enabled=twin_enabled,
                authority_enabled=authority_enabled,
                outcome=OUTCOME_EXCEPTION,
                latency_ms=latency_ms,
                returned_none=True,
                error_code=type(exc).__name__,
                ok=False,
            )

        latency_ms = (time.perf_counter() - started) * 1000.0
        outcome, returned_none, codes, _confidence = classify_build_result(result)
        self._health.record_execution(
            outcome=outcome,
            latency_ms=latency_ms,
            limitation_codes=codes,
        )
        telemetry.emit_completed(
            structured=self._structured,
            events=self._events,
            student_id=student_id,
            api_name=api_name,
            outcome=outcome,
            latency_ms=latency_ms,
            twin_enabled=twin_enabled,
            authority_enabled=authority_enabled,
        )
        return SoakApiObservation(
            api_name=api_name,
            student_id=student_id,
            twin_enabled=twin_enabled,
            authority_enabled=authority_enabled,
            outcome=outcome,
            latency_ms=latency_ms,
            returned_none=returned_none,
            limitation_codes=codes,
            ok=outcome != OUTCOME_EXCEPTION,
        )

    def execute_twin_workload(
        self,
        *,
        student_ids: Sequence[str] | Sequence[int],
        iterations: int = 1,
        twin_enabled: bool = True,
        authority_enabled: bool = False,
        foundation: Any | None = None,
        canonical_state: Any | None = None,
    ) -> tuple[SoakApiObservation, ...]:
        """Exercise build_* APIs under Twin-enabled soak posture."""
        if not self._enabled:
            return ()

        plan_fn, ready_fn, insight_fn = self._resolve_builders()
        previous = set_consumer_chain_telemetry(self._chain)
        observations: list[SoakApiObservation] = []
        try:
            for _ in range(max(1, int(iterations))):
                for raw_id in student_ids:
                    sid = str(raw_id)
                    try:
                        user_id = int(raw_id)
                    except (TypeError, ValueError):
                        user_id = abs(hash(sid)) % (10**6)

                    kwargs: dict[str, Any] = {}
                    if foundation is not None:
                        kwargs["foundation"] = foundation
                    if canonical_state is not None:
                        kwargs["canonical_state"] = canonical_state

                    observations.append(
                        self._observe_call(
                            api_name=API_BUILD_DAILY_STUDY_PLAN,
                            student_id=sid,
                            twin_enabled=twin_enabled,
                            authority_enabled=authority_enabled,
                            call=lambda uid=user_id, kw=dict(kwargs): plan_fn(
                                uid, **kw
                            ),
                        )
                    )
                    ready_kw = dict(kwargs)
                    ready_kw.setdefault("include_planner", True)
                    observations.append(
                        self._observe_call(
                            api_name=API_BUILD_READINESS_INTELLIGENCE,
                            student_id=sid,
                            twin_enabled=twin_enabled,
                            authority_enabled=authority_enabled,
                            call=lambda uid=user_id, kw=dict(ready_kw): ready_fn(
                                uid, **kw
                            ),
                        )
                    )
                    insight_kw = dict(kwargs)
                    insight_kw.setdefault("include_planner", True)
                    insight_kw.setdefault("include_readiness", True)
                    observations.append(
                        self._observe_call(
                            api_name=API_BUILD_STUDY_INSIGHTS,
                            student_id=sid,
                            twin_enabled=twin_enabled,
                            authority_enabled=authority_enabled,
                            call=lambda uid=user_id, kw=dict(insight_kw): insight_fn(
                                uid, **kw
                            ),
                        )
                    )
        finally:
            set_consumer_chain_telemetry(previous)
        return tuple(observations)

    def execute_full_soak(
        self,
        *,
        student_ids: Sequence[str] | Sequence[int],
        iterations: int = 10,
        foundation: Any | None = None,
        canonical_state: Any | None = None,
        base_environ: dict[str, str] | None = None,
        run_matrix: bool = True,
        run_rollback: bool = True,
        fail_open_fallback: Any | None = None,
    ) -> TwinAuthoritySoakReport:
        """Run Twin workload + Authority matrix + rollback; return report."""
        started = time.perf_counter()
        details: list[str] = []
        observations: list[SoakApiObservation] = []
        ownership_violations = 0
        behavioural_regressions = 0

        if not self._enabled:
            return TwinAuthoritySoakReport(
                ok=False,
                soak_duration_ms=0.0,
                requests_exercised=0,
                average_latency_ms=0.0,
                p95_latency_ms=0.0,
                foundation_assemble_count=0,
                share_hit_count=0,
                share_hit_rate=0.0,
                failure_count=0,
                exception_count=0,
                details=("soak_disabled",),
            )

        # Twin ON / Authority OFF workload.
        observations.extend(
            self.execute_twin_workload(
                student_ids=student_ids,
                iterations=iterations,
                twin_enabled=True,
                authority_enabled=False,
                foundation=foundation,
                canonical_state=canonical_state,
            )
        )
        details.append("twin_workload_authority_off_complete")

        # Twin ON / Authority ON workload (same build_* path; flag snapshot).
        observations.extend(
            self.execute_twin_workload(
                student_ids=student_ids,
                iterations=max(1, iterations // 2),
                twin_enabled=True,
                authority_enabled=True,
                foundation=foundation,
                canonical_state=canonical_state,
            )
        )
        details.append("twin_workload_authority_on_complete")
        self._ingest_foundation_records()

        matrix_cells = ()
        if run_matrix:
            matrix_cells = run_authority_matrix(
                composition_factory=self._composition_factory,
                base_environ=base_environ,
                structured=self._structured,
                events=self._events,
            )
            for cell in matrix_cells:
                self._health.record_matrix(ok=cell.ok)
                if not cell.ok:
                    behavioural_regressions += 1
                    details.append(f"FAIL:matrix:{cell.cell_id}")
            if all(c.ok for c in matrix_cells):
                details.append("authority_matrix_ok")

        if fail_open_fallback is not None:
            fo_ok, fo_details = verify_authority_fail_open(
                fallback=fail_open_fallback,
            )
            details.extend(fo_details)
            if not fo_ok:
                behavioural_regressions += 1

        rollback_success = False
        if run_rollback:
            rollback = verify_twin_authority_soak_rollback(
                events=self._events,
                structured=self._structured,
                base_environ=base_environ,
                composition_factory=self._composition_factory,
                health=self._health,
            )
            rollback_success = rollback.ok
            details.extend(rollback.details)
            behavioural_regressions += rollback.behavioural_regressions
            if not rollback.ok:
                details.append("FAIL:rollback")

        snapshot = self._health.snapshot()
        telemetry.emit_health(
            structured=self._structured,
            events=self._events,
            snapshot=snapshot.to_canonical_dict(),
        )

        duration_ms = (time.perf_counter() - started) * 1000.0
        exception_count = sum(
            1 for o in observations if o.outcome == OUTCOME_EXCEPTION
        )
        failure_count = snapshot.failure_count
        # Twin ON soak should not be all-unavailable if foundation injected.
        if foundation is not None:
            unavailable = sum(
                1 for o in observations if o.outcome == OUTCOME_UNAVAILABLE
            )
            if unavailable == len(observations) and observations:
                behavioural_regressions += 1
                details.append("FAIL:all_unavailable_with_foundation")
            successes = sum(
                1
                for o in observations
                if o.outcome in (OUTCOME_SUCCESS, "limitation")
            )
            if successes == 0 and observations:
                details.append("WARN:no_success_or_limitation_outcomes")

        ok = (
            rollback_success
            and behavioural_regressions == 0
            and ownership_violations == 0
            and exception_count == 0
            and (not matrix_cells or all(c.ok for c in matrix_cells))
        )
        if ok:
            details.append("soak_ok")

        return TwinAuthoritySoakReport(
            ok=ok,
            soak_duration_ms=duration_ms,
            requests_exercised=len(observations),
            average_latency_ms=snapshot.average_latency_ms,
            p95_latency_ms=snapshot.p95_latency_ms,
            foundation_assemble_count=snapshot.foundation_assemble_count,
            share_hit_count=snapshot.share_hit_count,
            share_hit_rate=snapshot.share_hit_rate,
            failure_count=failure_count,
            exception_count=exception_count,
            limitation_code_counts=dict(self._health.limitation_code_counts),
            matrix_cells=matrix_cells,
            rollback_success=rollback_success,
            ownership_violations=ownership_violations,
            behavioural_regressions=behavioural_regressions,
            observations=tuple(observations),
            details=tuple(details),
        )


def build_twin_authority_soak_orchestrator(
    *,
    enabled: bool = True,
    events: EventRegistry | None = None,
    structured: StructuredLogger | None = None,
    chain_telemetry: ConsumerChainTelemetry | None = None,
    health: TwinAuthoritySoakHealthMetrics | None = None,
    composition_factory: Callable[..., tuple[Any, Any]] | None = None,
    build_plan: BuildPlanFn | None = None,
    build_readiness: BuildReadinessFn | None = None,
    build_insights: BuildInsightsFn | None = None,
) -> TwinAuthoritySoakOrchestrator:
    """DI helper for Twin & Authority soak orchestrator."""
    return TwinAuthoritySoakOrchestrator(
        enabled=enabled,
        events=events,
        structured=structured,
        chain_telemetry=chain_telemetry,
        health=health,
        composition_factory=composition_factory,
        build_plan=build_plan,
        build_readiness=build_readiness,
        build_insights=build_insights,
    )


__all__ = [
    "TwinAuthoritySoakOrchestrator",
    "build_twin_authority_soak_orchestrator",
]
