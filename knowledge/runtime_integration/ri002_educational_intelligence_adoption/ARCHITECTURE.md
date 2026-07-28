# RI-002 — Educational Intelligence Adoption & Readiness Architecture

**Programme:** RI-002 — Educational Intelligence Adoption & Readiness  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/application/runtime_integration/` (adoption / inventory / gates / readiness)  
**Depends on:** [RI-001](../ri001_educational_runtime_integration/ARCHITECTURE.md)

---

## 1. Capability statement

> Kwalitec can measure and govern the migration from legacy educational runtime to the Educational Intelligence Core.

---

## 2. Philosophy

RI-002 is **observational governance**. It does not:

- invent educational recommendations
- modify Educational Decisions or Experience Models
- remove Runtime A
- change student-facing behaviour

It measures whether Preferred Authority (RI-001) is being adopted and whether documented retirement gates for Runtime A recommendation authority are met (input to RI-005).

---

## 3. Component map

```
DB coverage queries ──┐
                      ├─→ AdoptionMetricsService ──┐
RIS telemetry ────────┘                            │
                                                   ├─→ RuntimeReadinessService
Static inventory catalogue ─→ RuntimeInventoryService ─┤
                                                   │
Retirement gate definitions ─→ RetirementGateEvaluator ─┘
                                                   │
                                                   ▼
                                    Founder Runtime Health dashboard
                                    (/console/runtime-health)
```

| Module | Responsibility |
|--------|----------------|
| `adoption_metrics.py` | SCI / published curriculum / decision coverage + telemetry rates |
| `telemetry.py` | Process-scoped EI vs fallback events, surface + daily trends |
| `runtime_inventory.py` | Machine-readable remaining Runtime A / legacy dependencies |
| `retirement_gates.py` | Documented, code-evaluable exit criteria |
| `readiness_service.py` | Combines metrics + inventory + gates for operators |

---

## 4. Adoption metrics

| Metric | Definition |
|--------|------------|
| SCI coverage | Active-plan students with ≥1 active SCI |
| Published curriculum coverage | Subject codes with ≥1 published CKG edition / all CKG subject codes |
| Educational Decision coverage | Active SCIs with ≥1 persisted EI-007 decision |
| Experience Model generation rate | EI path RIS requests / total RIS requests |
| Runtime A fallback rate | Fallback RIS requests / total RIS requests |
| Route-level EI usage | Per-`IntegrationSurface` EI vs fallback counts |

All definitions are explainable numerators and denominators — no opaque scores.

---

## 5. Runtime Health dashboard

Operator-only Console page at `/console/runtime-health` (Founder / Console access).

Shows:

- EI vs Runtime A request mix
- Fallback reasons
- Coverage metrics
- Adoption trends (daily buckets from process telemetry)
- Migration progress by surface
- Retirement gate pass/fail with evidence
- Inventory status counts and rows

No student recommendation payloads are stored or rendered.

---

## 6. Runtime inventory

Canonical catalogue in `RuntimeInventoryService`, serialisable via `to_dict()` / `to_json_dict()`.

Statuses: `active` · `deprecated` · `removable` · `blocked`

Entries that both `blocks_retirement=true` and `status=active` keep the NO_ACTIVE_RUNTIME_A_AUTHORITY gate failing until RI-005 remediates them.

Human-readable mirror: [`RUNTIME_INVENTORY.md`](RUNTIME_INVENTORY.md) · JSON: [`runtime_inventory.json`](runtime_inventory.json)

---

## 7. Retirement gates

Full criteria: [`RETIREMENT_GATES.md`](RETIREMENT_GATES.md).

Gates are evaluated by `RetirementGateEvaluator` against live metrics and inventory. Passing **all** gates is a necessary input for RI-005; RI-002 never performs removal.

---

## 8. Explicit non-goals

- Modifying EI-007 / EX-001 / Twin / Evidence / CKG
- Deleting `RecommendationService` / `PlanningService`
- Changing Preferred Authority routing behaviour
- Student-facing UI changes

---

## 9. Verification

```bash
python3 -m pytest tests/application/runtime_integration/ \
  tests/test_console_001_kwalitec_console.py -q
python3 -m ruff check app/application/runtime_integration \
  app/founder/dashboard/routes.py app/founder/dashboard/nav.py \
  tests/application/runtime_integration
```
