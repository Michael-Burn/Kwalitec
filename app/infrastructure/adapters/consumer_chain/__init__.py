"""EP-002.1 — Consumer-chain observability for Twin-gated ``build_*`` APIs.

EP-002.2 adds shared Foundation DI helpers for composition-local CLS reuse.
EP-002.3 adds Twin & Authority non-production soak (observational only).
EP-002.4 adds Study Insights dual-run side-car (legacy remains authoritative).
EP-002.5 adds Study Insights gated HTTP cutover (legacy fail-open fallback).
EP-002.6 adds Readiness Intelligence dual-run + gated HTTP cutover (legacy
fail-open fallback; collectors remain on pure getters).
EP-002.7 adds Daily Plan dual-run + gated HTTP cutover (legacy
``generate_today_mission`` fail-open; MissionOptimizer remains quarantined).

Observational dual-run does not change student-facing behaviour. Cutover may
influence dashboard/home/analytics/missions only when explicitly eligible. Reuses
``StructuredLogger`` / ``EventRegistry``.
"""

from __future__ import annotations

from app.infrastructure.adapters.consumer_chain.authority_matrix import (
    classify_twin_port,
    evaluate_matrix_cell,
    run_authority_matrix,
    verify_authority_fail_open,
)
from app.infrastructure.adapters.consumer_chain.contracts import (
    API_BUILD_DAILY_STUDY_PLAN,
    API_BUILD_READINESS_INTELLIGENCE,
    API_BUILD_STUDY_INSIGHTS,
    CONSUMER_CHAIN_APIS,
    OUTCOME_CATEGORIES,
    OUTCOME_EXCEPTION,
    OUTCOME_LIMITATION,
    OUTCOME_SUCCESS,
    OUTCOME_UNAVAILABLE,
    SERVICE_PLANNING,
    SERVICE_READINESS,
    SERVICE_RECOMMENDATION,
)
from app.infrastructure.adapters.consumer_chain.cutover import (
    assess_semantic_alignment,
    has_blocking_limitation,
    is_cutover_active,
    is_study_insights_cutover_eligible,
    project_study_insights_to_recommendations,
    run_study_insights_http_cutover,
)
from app.infrastructure.adapters.consumer_chain.cutover_health import (
    StudyInsightsCutoverHealthMetrics,
    StudyInsightsCutoverHealthSnapshot,
    build_study_insights_cutover_health_metrics,
    get_study_insights_cutover_health_metrics,
    set_study_insights_cutover_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.daily_plan_cutover import (
    assess_daily_plan_semantic_alignment,
    has_daily_plan_blocking_limitation,
    is_daily_plan_cutover_active,
    is_daily_plan_cutover_eligible,
    project_daily_plan_to_mission_surface,
    run_daily_plan_http_cutover,
)
from app.infrastructure.adapters.consumer_chain.daily_plan_cutover_health import (
    DailyPlanCutoverHealthMetrics,
    DailyPlanCutoverHealthSnapshot,
    build_daily_plan_cutover_health_metrics,
    get_daily_plan_cutover_health_metrics,
    set_daily_plan_cutover_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.daily_plan_dual_run import (
    compare_legacy_vs_daily_study_plan,
    run_daily_plan_dual_run,
)
from app.infrastructure.adapters.consumer_chain.daily_plan_dual_run_health import (
    DailyPlanDualRunHealthMetrics,
    DailyPlanDualRunHealthSnapshot,
    build_daily_plan_dual_run_health_metrics,
    get_daily_plan_dual_run_health_metrics,
    set_daily_plan_dual_run_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.dual_run import (
    compare_legacy_vs_build,
    diagnostic_compare_study_insights,
    fingerprint_payload,
    is_dual_run_diagnostics_eligible,
    run_study_insights_dual_run,
)
from app.infrastructure.adapters.consumer_chain.dual_run_health import (
    StudyInsightsDualRunHealthMetrics,
    StudyInsightsDualRunHealthSnapshot,
    build_study_insights_dual_run_health_metrics,
    get_study_insights_dual_run_health_metrics,
    set_study_insights_dual_run_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.foundation_di import (
    ASSEMBLE_SOURCE_ASSEMBLED,
    ASSEMBLE_SOURCE_INJECTED,
    assemble_shared_canonical_state,
    resolve_enabled_twin_foundation,
)
from app.infrastructure.adapters.consumer_chain.observer import (
    classify_build_result,
    observe_build_api,
)
from app.infrastructure.adapters.consumer_chain.readiness_cutover import (
    assess_readiness_semantic_alignment,
    has_readiness_blocking_limitation,
    is_readiness_cutover_active,
    is_readiness_intelligence_cutover_eligible,
    project_readiness_intelligence_to_surface,
    run_readiness_intelligence_http_cutover,
)
from app.infrastructure.adapters.consumer_chain.readiness_cutover_health import (
    ReadinessCutoverHealthMetrics,
    ReadinessCutoverHealthSnapshot,
    build_readiness_cutover_health_metrics,
    get_readiness_cutover_health_metrics,
    set_readiness_cutover_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.readiness_dual_run import (
    compare_legacy_vs_readiness_intelligence,
    run_readiness_intelligence_dual_run,
)
from app.infrastructure.adapters.consumer_chain.readiness_dual_run_health import (
    ReadinessDualRunHealthMetrics,
    ReadinessDualRunHealthSnapshot,
    build_readiness_dual_run_health_metrics,
    get_readiness_dual_run_health_metrics,
    set_readiness_dual_run_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.soak import (
    TwinAuthoritySoakOrchestrator,
    build_twin_authority_soak_orchestrator,
)
from app.infrastructure.adapters.consumer_chain.soak_contracts import (
    CELL_ROLLBACK,
    CELL_TWIN_OFF_AUTHORITY_ENV,
    CELL_TWIN_OFF_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_ON,
    FlagMatrixCell,
    SoakApiObservation,
    TwinAuthoritySoakReport,
)
from app.infrastructure.adapters.consumer_chain.soak_health import (
    TwinAuthoritySoakHealthMetrics,
    TwinAuthoritySoakHealthSnapshot,
    build_twin_authority_soak_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.soak_rollback import (
    TwinAuthoritySoakRollbackResult,
    TwinAuthoritySoakRollbackVerifier,
    build_twin_authority_soak_rollback_verifier,
    verify_twin_authority_soak_rollback,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    build_consumer_chain_telemetry,
    get_consumer_chain_telemetry,
    set_consumer_chain_telemetry,
)

__all__ = [
    "API_BUILD_DAILY_STUDY_PLAN",
    "API_BUILD_READINESS_INTELLIGENCE",
    "API_BUILD_STUDY_INSIGHTS",
    "ASSEMBLE_SOURCE_ASSEMBLED",
    "ASSEMBLE_SOURCE_INJECTED",
    "CELL_ROLLBACK",
    "CELL_TWIN_OFF_AUTHORITY_ENV",
    "CELL_TWIN_OFF_AUTHORITY_OFF",
    "CELL_TWIN_ON_AUTHORITY_OFF",
    "CELL_TWIN_ON_AUTHORITY_ON",
    "CONSUMER_CHAIN_APIS",
    "ConsumerChainTelemetry",
    "DailyPlanDualRunHealthSnapshot",
    "DailyPlanDualRunHealthMetrics",
    "DailyPlanCutoverHealthSnapshot",
    "DailyPlanCutoverHealthMetrics",
    "FlagMatrixCell",
    "OUTCOME_CATEGORIES",
    "OUTCOME_EXCEPTION",
    "OUTCOME_LIMITATION",
    "OUTCOME_SUCCESS",
    "OUTCOME_UNAVAILABLE",
    "ReadinessCutoverHealthMetrics",
    "ReadinessCutoverHealthSnapshot",
    "ReadinessDualRunHealthMetrics",
    "ReadinessDualRunHealthSnapshot",
    "SERVICE_PLANNING",
    "SERVICE_READINESS",
    "SERVICE_RECOMMENDATION",
    "SoakApiObservation",
    "StudyInsightsCutoverHealthMetrics",
    "StudyInsightsCutoverHealthSnapshot",
    "StudyInsightsDualRunHealthMetrics",
    "StudyInsightsDualRunHealthSnapshot",
    "TwinAuthoritySoakHealthMetrics",
    "TwinAuthoritySoakHealthSnapshot",
    "TwinAuthoritySoakOrchestrator",
    "TwinAuthoritySoakReport",
    "TwinAuthoritySoakRollbackResult",
    "TwinAuthoritySoakRollbackVerifier",
    "assemble_shared_canonical_state",
    "assess_readiness_semantic_alignment",
    "assess_daily_plan_semantic_alignment",
    "assess_semantic_alignment",
    "build_consumer_chain_telemetry",
    "build_daily_plan_cutover_health_metrics",
    "build_daily_plan_dual_run_health_metrics",
    "build_readiness_cutover_health_metrics",
    "build_readiness_dual_run_health_metrics",
    "build_study_insights_cutover_health_metrics",
    "build_study_insights_dual_run_health_metrics",
    "build_twin_authority_soak_health_metrics",
    "build_twin_authority_soak_orchestrator",
    "build_twin_authority_soak_rollback_verifier",
    "classify_build_result",
    "classify_twin_port",
    "compare_legacy_vs_build",
    "compare_legacy_vs_daily_study_plan",
    "compare_legacy_vs_readiness_intelligence",
    "diagnostic_compare_study_insights",
    "evaluate_matrix_cell",
    "fingerprint_payload",
    "get_consumer_chain_telemetry",
    "get_daily_plan_cutover_health_metrics",
    "get_daily_plan_dual_run_health_metrics",
    "get_readiness_cutover_health_metrics",
    "get_readiness_dual_run_health_metrics",
    "get_study_insights_cutover_health_metrics",
    "get_study_insights_dual_run_health_metrics",
    "has_blocking_limitation",
    "has_daily_plan_blocking_limitation",
    "has_readiness_blocking_limitation",
    "is_cutover_active",
    "is_daily_plan_cutover_active",
    "is_daily_plan_cutover_eligible",
    "is_dual_run_diagnostics_eligible",
    "is_readiness_cutover_active",
    "is_readiness_intelligence_cutover_eligible",
    "is_study_insights_cutover_eligible",
    "observe_build_api",
    "project_readiness_intelligence_to_surface",
    "project_daily_plan_to_mission_surface",
    "project_study_insights_to_recommendations",
    "resolve_enabled_twin_foundation",
    "run_authority_matrix",
    "run_daily_plan_dual_run",
    "run_daily_plan_http_cutover",
    "run_readiness_intelligence_dual_run",
    "run_readiness_intelligence_http_cutover",
    "run_study_insights_dual_run",
    "run_study_insights_http_cutover",
    "set_consumer_chain_telemetry",
    "set_daily_plan_cutover_health_metrics",
    "set_daily_plan_dual_run_health_metrics",
    "set_readiness_cutover_health_metrics",
    "set_readiness_dual_run_health_metrics",
    "set_study_insights_cutover_health_metrics",
    "set_study_insights_dual_run_health_metrics",
    "verify_authority_fail_open",
    "verify_twin_authority_soak_rollback",
]
