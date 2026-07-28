"""Runtime readiness assessment for Educational Intelligence adoption (RI-002).

Combines adoption metrics, inventory, and retirement gates into an operator
report. Does not change student-facing behaviour or remove Runtime A.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.runtime_integration.adoption_metrics import AdoptionMetricsService
from app.application.runtime_integration.dto import RetirementReadinessReport
from app.application.runtime_integration.retirement_gates import (
    RetirementGateEvaluator,
)
from app.application.runtime_integration.runtime_inventory import (
    RuntimeInventoryService,
)
from app.application.runtime_integration.telemetry import (
    DEFAULT_TELEMETRY,
    RuntimeIntegrationTelemetry,
)


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class RuntimeReadinessService:
    """Assemble the RI-002 readiness / Runtime Health payload."""

    def __init__(
        self,
        *,
        telemetry: RuntimeIntegrationTelemetry | None = None,
        metrics: AdoptionMetricsService | None = None,
        inventory: RuntimeInventoryService | None = None,
        gates: RetirementGateEvaluator | None = None,
    ) -> None:
        self._telemetry = telemetry or DEFAULT_TELEMETRY
        self._metrics = metrics or AdoptionMetricsService(telemetry=self._telemetry)
        self._inventory = inventory or RuntimeInventoryService()
        self._gates = gates or RetirementGateEvaluator()

    def assess(
        self,
        *,
        integration_tests_passed: bool = True,
    ) -> RetirementReadinessReport:
        """Build the full readiness report for operators."""
        metrics = self._metrics.build_report()
        inventory = self._inventory.build_report()
        evaluations = self._gates.evaluate(
            metrics,
            inventory,
            integration_tests_passed=integration_tests_passed,
        )
        return RetirementReadinessReport(
            metrics=metrics,
            inventory=inventory,
            gate_evaluations=evaluations,
            ready_for_retirement=all(e.passed for e in evaluations),
            assessed_at=_utc_now_iso(),
        )

    def health_dashboard_payload(
        self,
        *,
        integration_tests_passed: bool = True,
    ) -> dict:
        """Template-friendly dict for the Founder Runtime Health page."""
        report = self.assess(
            integration_tests_passed=integration_tests_passed,
        )
        metrics = report.metrics
        telemetry = metrics.telemetry
        trend_days = sorted(
            set(telemetry.daily_ei_counts) | set(telemetry.daily_fallback_counts)
        )
        return {
            "assessed_at": report.assessed_at,
            "ready_for_retirement": report.ready_for_retirement,
            "ei_request_pct": metrics.educational_intelligence_request_pct,
            "fallback_pct": 100.0 * metrics.runtime_a_fallback_rate,
            "fallback_by_reason": metrics.fallback_by_reason,
            "route_level_usage": [s.to_dict() for s in metrics.route_level_usage],
            "sci_coverage": metrics.sci_coverage.to_dict(),
            "published_curriculum_coverage": (
                metrics.published_curriculum_coverage.to_dict()
            ),
            "educational_decision_coverage": (
                metrics.educational_decision_coverage.to_dict()
            ),
            "experience_model_generation_rate": (
                metrics.experience_model_generation_rate
            ),
            "migrated_user_count": len(telemetry.migrated_users),
            "total_requests": telemetry.total_requests,
            "trend_labels": trend_days,
            "trend_ei": [telemetry.daily_ei_counts.get(d, 0) for d in trend_days],
            "trend_fallback": [
                telemetry.daily_fallback_counts.get(d, 0) for d in trend_days
            ],
            "inventory_counts": report.inventory.counts_by_status(),
            "inventory_entries": [e.to_dict() for e in report.inventory.entries],
            "gates": [g.to_dict() for g in report.gate_evaluations],
            "passed_gate_count": sum(1 for g in report.gate_evaluations if g.passed),
            "total_gate_count": len(report.gate_evaluations),
        }
