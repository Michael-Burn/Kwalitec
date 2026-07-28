"""Runtime inventory and retirement gate tests (RI-002)."""

from __future__ import annotations

from app.application.runtime_integration.adoption_metrics import AdoptionMetricsService
from app.application.runtime_integration.dto import (
    AdoptionMetricsReport,
    CoverageMetric,
    FallbackReason,
    IntegrationSurface,
    InventoryStatus,
    RetirementGateId,
    TelemetrySnapshot,
)
from app.application.runtime_integration.readiness_service import (
    RuntimeReadinessService,
)
from app.application.runtime_integration.retirement_gates import (
    RETIREMENT_GATES,
    RetirementGateEvaluator,
    gates_catalogue,
)
from app.application.runtime_integration.runtime_inventory import (
    RuntimeInventoryService,
)
from app.application.runtime_integration.telemetry import RuntimeIntegrationTelemetry


def _coverage(metric_id: str, num: int, den: int) -> CoverageMetric:
    return CoverageMetric(
        metric_id=metric_id,
        label=metric_id,
        numerator=num,
        denominator=den,
        definition="test",
    )


def _metrics(
    *,
    sci: tuple[int, int] = (19, 20),
    published: tuple[int, int] = (2, 2),
    decisions: tuple[int, int] = (18, 20),
    ei_count: int = 95,
    fallback_count: int = 5,
) -> AdoptionMetricsReport:
    total = ei_count + fallback_count
    snap = TelemetrySnapshot(
        total_requests=total,
        educational_intelligence_count=ei_count,
        fallback_count=fallback_count,
        migrated_users=frozenset({1}),
        fallback_users=frozenset({2}),
        fallback_by_reason={"no_active_sci": fallback_count},
    )
    return AdoptionMetricsReport(
        sci_coverage=_coverage("sci_coverage", *sci),
        published_curriculum_coverage=_coverage(
            "published_curriculum_coverage", *published
        ),
        educational_decision_coverage=_coverage(
            "educational_decision_coverage", *decisions
        ),
        experience_model_generation_rate=(
            0.0 if total <= 0 else ei_count / total
        ),
        runtime_a_fallback_rate=(0.0 if total <= 0 else fallback_count / total),
        educational_intelligence_request_pct=(
            0.0 if total <= 0 else 100.0 * ei_count / total
        ),
        route_level_usage=(),
        fallback_by_reason=dict(snap.fallback_by_reason),
        telemetry=snap,
        computed_at="2026-07-28T12:00:00Z",
    )


def test_inventory_is_machine_readable_and_classified() -> None:
    report = RuntimeInventoryService().build_report()
    payload = report.to_dict()
    assert "entries" in payload
    assert "counts_by_status" in payload
    assert payload["counts_by_status"]["active"] >= 1
    statuses = {e.status for e in report.entries}
    assert InventoryStatus.ACTIVE in statuses
    assert InventoryStatus.DEPRECATED in statuses
    assert InventoryStatus.REMOVABLE in statuses
    ids = {e.entry_id for e in report.entries}
    assert "rec-service" in ids
    assert "mission-optimizer" in ids
    # RecommendationService still blocks retirement while active.
    rec = next(e for e in report.entries if e.entry_id == "rec-service")
    assert rec.status is InventoryStatus.ACTIVE
    assert rec.blocks_retirement is True


def test_retirement_gates_catalogue_is_documented() -> None:
    catalogue = gates_catalogue()
    assert len(catalogue) == len(RETIREMENT_GATES)
    gate_ids = {g["gate_id"] for g in catalogue}
    assert RetirementGateId.SCI_COVERAGE.value in gate_ids
    assert RetirementGateId.FALLBACK_RATE.value in gate_ids
    assert RetirementGateId.INTEGRATION_TESTS.value in gate_ids


def test_gates_fail_when_coverage_insufficient() -> None:
    inventory = RuntimeInventoryService().build_report()
    evaluations = RetirementGateEvaluator().evaluate(
        _metrics(sci=(1, 10), ei_count=50, fallback_count=50),
        inventory,
        integration_tests_passed=True,
    )
    by_id = {e.gate.gate_id: e for e in evaluations}
    assert by_id[RetirementGateId.SCI_COVERAGE].passed is False
    assert by_id[RetirementGateId.FALLBACK_RATE].passed is False
    assert by_id[RetirementGateId.INTEGRATION_TESTS].passed is True
    assert by_id[RetirementGateId.NO_ACTIVE_RUNTIME_A_AUTHORITY].passed is False


def test_gates_pass_with_synthetic_ready_state() -> None:
    """Gates are testable: a fully migrated metric snapshot can pass coverage gates."""
    inventory = RuntimeInventoryService().build_report()
    # Force inventory entries that block retirement to non-active for this unit test.
    cleared = type(inventory)(
        generated_at=inventory.generated_at,
        entries=tuple(
            type(e)(
                entry_id=e.entry_id,
                component=e.component,
                path=e.path,
                category=e.category,
                status=(
                    InventoryStatus.DEPRECATED
                    if e.blocks_retirement
                    else e.status
                ),
                notes=e.notes,
                blocks_retirement=e.blocks_retirement,
            )
            for e in inventory.entries
        ),
    )
    evaluations = RetirementGateEvaluator().evaluate(
        _metrics(sci=(20, 20), published=(3, 3), decisions=(20, 20)),
        cleared,
        integration_tests_passed=True,
    )
    assert all(e.passed for e in evaluations)


def test_readiness_service_payload_shape(app, db, ctx) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    telemetry.record_fallback(
        student_id=9,
        subject=None,
        reason=FallbackReason.NO_EDUCATIONAL_DECISIONS,
        surface=IntegrationSurface.HOME,
    )
    payload = RuntimeReadinessService(telemetry=telemetry).health_dashboard_payload(
        integration_tests_passed=True,
    )
    assert "ei_request_pct" in payload
    assert "fallback_pct" in payload
    assert "fallback_by_reason" in payload
    assert "route_level_usage" in payload
    assert "gates" in payload
    assert "inventory_entries" in payload
    assert payload["ready_for_retirement"] is False
    assert AdoptionMetricsService(telemetry=telemetry).build_report().to_dict()
