# RI-002 — Runtime A Retirement Gates

**Programme:** RI-002 — Educational Intelligence Adoption & Readiness  
**Date:** 2026-07-28  
**Status:** Active (measurement) — hard removal deferred to RI-005  
**Code:** `app/application/runtime_integration/retirement_gates.py`

---

## 1. Purpose

Define **measurable, testable** exit criteria for retiring Runtime A as educational recommendation authority. RI-002 evaluates these gates; it does not remove Runtime A.

Mission ORM persistence (`PlanningService` / `MissionService`) may remain after recommendation-authority retirement — persistence is not educational selection.

---

## 2. Gate catalogue

| Gate ID | Title | Operator | Threshold | Unit |
|---------|-------|----------|-----------|------|
| `sci_coverage` | SCI coverage | `>=` | `0.95` | ratio |
| `published_curriculum_coverage` | Published curriculum coverage | `>=` | `1.0` | ratio |
| `educational_decision_coverage` | Educational Decision coverage | `>=` | `0.90` | ratio |
| `fallback_rate` | Runtime A fallback rate | `<=` | `0.05` | ratio |
| `experience_model_rate` | Experience Model generation rate | `>=` | `0.95` | ratio |
| `integration_tests` | Integration test pass requirement | `==` | `1.0` | boolean |
| `no_active_runtime_a_authority` | No active Runtime A recommendation authority | `==` | `0.0` | count of blocking-active inventory entries |

Constants in code must match this table (`SCI_COVERAGE_MIN`, etc.).

---

## 3. Definitions

### SCI coverage ≥ 95%

Distinct students with an **active** study plan who also have ≥1 **active** Student Curriculum Instance, divided by distinct students with an active study plan.

### Published curriculum coverage = 100%

Distinct CKG subject codes with ≥1 `publication_state=published` edition, divided by distinct subject codes that have any CKG edition.

### Educational Decision coverage ≥ 90%

Active SCIs with ≥1 persisted `ere_educational_decisions` row, divided by active SCI count.

### Fallback rate ≤ 5%

Process-scoped `RuntimeIntegrationTelemetry` fallback events / total RIS events.

### Experience Model generation rate ≥ 95%

Process-scoped EI path events / total RIS events (complement of fallback rate when every request is classified).

### Integration tests

Preferred-authority selection, fallback telemetry emission, and no-bypass AST/import guards under `tests/application/runtime_integration/` must pass in CI / local verification. The evaluator accepts an explicit `integration_tests_passed` boolean (set true when the suite is green).

### No active Runtime A recommendation authority

Inventory contains **zero** entries where `blocks_retirement=true` **and** `status=active`. Today this intentionally fails while Temporary compatibility modules remain.

---

## 4. Evaluation API

```python
from app.application.runtime_integration import (
    RuntimeReadinessService,
    RetirementGateEvaluator,
)

report = RuntimeReadinessService().assess(integration_tests_passed=True)
assert isinstance(report.ready_for_retirement, bool)
```

`ready_for_retirement` is true only when **every** gate passes.

---

## 5. Relationship to RI-005

RI-005 may hard-remove Runtime A recommendation authority only when:

1. All retirement gates pass under production-representative telemetry windows
2. Inventory blocking-active entries have been remapped to deprecated/removable
3. Engineering + product owners accept residual mission-persistence debt explicitly

Until then, Runtime A remains Temporary compatibility under Preferred Authority.
