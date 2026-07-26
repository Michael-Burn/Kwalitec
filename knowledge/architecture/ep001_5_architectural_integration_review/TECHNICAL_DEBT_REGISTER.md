# EP-001.5 — Technical Debt Register

**Milestone:** EP-001.5  
**Date:** 2026-07-26

Priority: P0 blocking · P1 near-term · P2 planned · P3 backlog

---

## Architectural debt

| ID | Priority | Item | Evidence | Remediation |
|---|---|---|---|---|
| TD-ARCH-01 | P1 | Multiple Twin stacks coexist (Epic / V2 / EOS / MS-004 / Experience) | EP-001.1 discovery; packages still present | Quarantine non-authority stacks in docs + import guidance; never merge blindly |
| TD-ARCH-02 | P1 | Dual presentation authority: EP-001.4 vs `EducationalExplainabilityService` | EP-001.4 completion report | Explicit cutover milestone choosing one SoT for student-facing narrative |
| TD-ARCH-03 | P2 | `MissionOptimizer` canonical path orphaned (no production callers) | Grep: only `mission_optimizer.py` defines `generate_balanced_mission` | Wire into a deliberate surface or remove dead API |
| TD-ARCH-04 | P2 | Foundation per-call construction in Runtime A services (not shared composition DI) | `_resolve_twin_foundation` in planning/readiness/recommendation services | Inject composition Foundation |
| TD-ARCH-05 | P2 | Collector still depends on legacy readiness getters (permanent until refactor) | `ReadinessCollector` → `get_overall_readiness` | Optional future: collectors read ORM/facts without service recursion surface |
| TD-ARCH-06 | P3 | Doc/code drift on Shadow / Adaptive-input separate flags | Architecture docs vs `v2_flags.py` | Align documentation |

---

## Operational debt

| ID | Priority | Item | Evidence | Remediation |
|---|---|---|---|---|
| TD-OPS-01 | P1 | Twin-gated `build_*` APIs unused by HTTP — no production observability of EP-001 consumer chain | No route callers | Observability milestone: shadow metrics on `build_*` even before UX cutover |
| TD-OPS-02 | P1 | Authority ON not soaked in production-like env | Default OFF; readiness report historically holds T7 | Soak plan with rollback drills |
| TD-OPS-03 | P2 | Duplicate collector work when Insight → Readiness → Planner → Foundation each assemble | Nested `_resolve_*` calls | Pass shared assembled state / plan / readiness down the chain |
| TD-OPS-04 | P2 | Shadow bundled with Twin ON — cannot observe Shadow without enabling Foundation DI | Composition wires both under Twin | Accept or split flags |

---

## Product debt

| ID | Priority | Item | Evidence | Remediation |
|---|---|---|---|---|
| TD-PROD-01 | P1 | Students never see EP-001.2–4 outputs under default config | Flags OFF; no HTTP wiring | Product cutover epic after soak |
| TD-PROD-02 | P2 | Mock performance unavailable — cannot inform plan/readiness/insight | Foundation `REASON_MOCK_NOT_DISTINGUISHED` | Runtime A distinguish mock evidence |
| TD-PROD-03 | P2 | Confidence bands are evidence-density heuristics, not self-report confidence | EP-001.3 known limitations | Product decision on Capability 2.7 |
| TD-PROD-04 | P3 | Available study time still from StudyPlan minutes; Foundation only preference hints | EP-001.2 debt | Optional Twin enrichment later |

---

## Prioritised remediation sequence

1. **P1 observability** (TD-OPS-01) — measure Foundation/build_* without UX change  
2. **P1 Twin stack narrative quarantine** (TD-ARCH-01) — reduce ownership confusion  
3. **P1 Experience Authority soak** (TD-OPS-02) — before HTTP cutover  
4. **P1 presentation SoT decision** (TD-ARCH-02)  
5. **P2 DI sharing + nested assemble cost** (TD-ARCH-04, TD-OPS-03)  
6. **P2 MissionOptimizer fate** (TD-ARCH-03)  
7. **P2 mock evidence** (TD-PROD-02) when product needs it  
8. **P3 docs alignment** (TD-ARCH-06)

---

## Debt introduced by EP-001 itself vs inherited

| Category | Introduced by EP-001 | Inherited / pre-existing |
|---|---|---|
| Architectural | Thin consumer packages + dual API surfaces (`build_*` vs legacy) | Multi-Twin stacks; Epic write pipeline gap |
| Operational | Nested resolve cost; unused HTTP | Shadow/Authority soak incomplete (MS-004) |
| Product | New guidance not yet surfaced | Mock distinction; self-report confidence |

**C:** EP-001 traded additive dual-path complexity for safe cutover. That debt is **intentional and manageable**, not accidental architecture failure.
