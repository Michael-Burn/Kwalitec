"""Runtime A retirement gates — measurable exit criteria (RI-002).

Gates are documentation-backed and code-evaluable. Passing all gates is a
necessary input for RI-005 hard removal; this module never removes Runtime A.
"""

from __future__ import annotations

from app.application.runtime_integration.dto import (
    AdoptionMetricsReport,
    GateEvaluation,
    InventoryStatus,
    RetirementGate,
    RetirementGateId,
    RuntimeInventoryReport,
)

# Thresholds documented in RETIREMENT_GATES.md — keep values in sync.
SCI_COVERAGE_MIN = 0.95
PUBLISHED_CURRICULUM_COVERAGE_MIN = 1.0
EDUCATIONAL_DECISION_COVERAGE_MIN = 0.90
FALLBACK_RATE_MAX = 0.05
EXPERIENCE_MODEL_RATE_MIN = 0.95


RETIREMENT_GATES: tuple[RetirementGate, ...] = (
    RetirementGate(
        gate_id=RetirementGateId.SCI_COVERAGE,
        title="SCI coverage",
        description=(
            "At least 95% of students with an active study plan have an "
            "active Student Curriculum Instance."
        ),
        operator=">=",
        threshold=SCI_COVERAGE_MIN,
        unit="ratio",
    ),
    RetirementGate(
        gate_id=RetirementGateId.PUBLISHED_CURRICULUM_COVERAGE,
        title="Published curriculum coverage",
        description=(
            "Every subject code with a CKG edition has ≥1 published edition "
            "(100% published curriculum coverage)."
        ),
        operator=">=",
        threshold=PUBLISHED_CURRICULUM_COVERAGE_MIN,
        unit="ratio",
    ),
    RetirementGate(
        gate_id=RetirementGateId.EDUCATIONAL_DECISION_COVERAGE,
        title="Educational Decision coverage",
        description=(
            "At least 90% of active SCIs have ≥1 persisted EI-007 Educational "
            "Decision."
        ),
        operator=">=",
        threshold=EDUCATIONAL_DECISION_COVERAGE_MIN,
        unit="ratio",
    ),
    RetirementGate(
        gate_id=RetirementGateId.FALLBACK_RATE,
        title="Runtime A fallback rate",
        description=(
            "Process-scoped RIS fallback rate is at most 5% of educational "
            "surface requests."
        ),
        operator="<=",
        threshold=FALLBACK_RATE_MAX,
        unit="ratio",
    ),
    RetirementGate(
        gate_id=RetirementGateId.EXPERIENCE_MODEL_RATE,
        title="Experience Model generation rate",
        description=(
            "At least 95% of RIS requests produce EX-001 Experience Models "
            "(Educational Intelligence path)."
        ),
        operator=">=",
        threshold=EXPERIENCE_MODEL_RATE_MIN,
        unit="ratio",
    ),
    RetirementGate(
        gate_id=RetirementGateId.INTEGRATION_TESTS,
        title="Integration test pass requirement",
        description=(
            "Preferred-authority, fallback telemetry, and no-bypass "
            "verification suites must pass (enforced by CI / local pytest)."
        ),
        operator="==",
        threshold=1.0,
        unit="boolean",
    ),
    RetirementGate(
        gate_id=RetirementGateId.NO_ACTIVE_RUNTIME_A_AUTHORITY,
        title="No active Runtime A recommendation authority",
        description=(
            "Inventory contains no entries that both block retirement and "
            "remain status=active under runtime_a_recommendation / "
            "runtime_a_planning / compatibility_control categories."
        ),
        operator="==",
        threshold=0.0,
        unit="count",
    ),
)


def _compare(operator: str, observed: float, threshold: float) -> bool:
    if operator == ">=":
        return observed >= threshold
    if operator == "<=":
        return observed <= threshold
    if operator == "==":
        return observed == threshold
    raise ValueError(f"Unsupported gate operator: {operator}")


class RetirementGateEvaluator:
    """Evaluate documented Runtime A retirement gates against live evidence."""

    def evaluate(
        self,
        metrics: AdoptionMetricsReport,
        inventory: RuntimeInventoryReport,
        *,
        integration_tests_passed: bool = True,
    ) -> tuple[GateEvaluation, ...]:
        """Return one evaluation per defined gate (deterministic order)."""
        results: list[GateEvaluation] = []
        for gate in RETIREMENT_GATES:
            observed, evidence = self._observe(
                gate,
                metrics=metrics,
                inventory=inventory,
                integration_tests_passed=integration_tests_passed,
            )
            results.append(
                GateEvaluation(
                    gate=gate,
                    observed=observed,
                    passed=_compare(gate.operator, observed, gate.threshold),
                    evidence=evidence,
                )
            )
        return tuple(results)

    def all_passed(
        self,
        metrics: AdoptionMetricsReport,
        inventory: RuntimeInventoryReport,
        *,
        integration_tests_passed: bool = True,
    ) -> bool:
        return all(
            e.passed
            for e in self.evaluate(
                metrics,
                inventory,
                integration_tests_passed=integration_tests_passed,
            )
        )

    @staticmethod
    def _observe(
        gate: RetirementGate,
        *,
        metrics: AdoptionMetricsReport,
        inventory: RuntimeInventoryReport,
        integration_tests_passed: bool,
    ) -> tuple[float, str]:
        gid = gate.gate_id
        if gid is RetirementGateId.SCI_COVERAGE:
            return (
                metrics.sci_coverage.ratio,
                (
                    f"{metrics.sci_coverage.numerator}/"
                    f"{metrics.sci_coverage.denominator} active-plan students "
                    "with SCI"
                ),
            )
        if gid is RetirementGateId.PUBLISHED_CURRICULUM_COVERAGE:
            return (
                metrics.published_curriculum_coverage.ratio,
                (
                    f"{metrics.published_curriculum_coverage.numerator}/"
                    f"{metrics.published_curriculum_coverage.denominator} "
                    "subject codes published"
                ),
            )
        if gid is RetirementGateId.EDUCATIONAL_DECISION_COVERAGE:
            return (
                metrics.educational_decision_coverage.ratio,
                (
                    f"{metrics.educational_decision_coverage.numerator}/"
                    f"{metrics.educational_decision_coverage.denominator} "
                    "active SCIs with decisions"
                ),
            )
        if gid is RetirementGateId.FALLBACK_RATE:
            return (
                metrics.runtime_a_fallback_rate,
                (
                    f"fallback_rate={metrics.runtime_a_fallback_rate:.4f} "
                    f"({metrics.telemetry.fallback_count}/"
                    f"{metrics.telemetry.total_requests} requests)"
                ),
            )
        if gid is RetirementGateId.EXPERIENCE_MODEL_RATE:
            return (
                metrics.experience_model_generation_rate,
                (
                    f"experience_model_generation_rate="
                    f"{metrics.experience_model_generation_rate:.4f}"
                ),
            )
        if gid is RetirementGateId.INTEGRATION_TESTS:
            value = 1.0 if integration_tests_passed else 0.0
            return (
                value,
                (
                    "integration_tests_passed=true"
                    if integration_tests_passed
                    else "integration_tests_passed=false"
                ),
            )
        if gid is RetirementGateId.NO_ACTIVE_RUNTIME_A_AUTHORITY:
            blocking_active = [
                e
                for e in inventory.entries
                if e.blocks_retirement and e.status is InventoryStatus.ACTIVE
            ]
            return (
                float(len(blocking_active)),
                (
                    "no blocking active inventory entries"
                    if not blocking_active
                    else "blocking="
                    + ",".join(e.entry_id for e in blocking_active)
                ),
            )
        raise ValueError(f"Unhandled gate: {gid}")


def gates_catalogue() -> list[dict]:
    """Serialisable catalogue of retirement gate definitions."""
    return [g.to_dict() for g in RETIREMENT_GATES]
