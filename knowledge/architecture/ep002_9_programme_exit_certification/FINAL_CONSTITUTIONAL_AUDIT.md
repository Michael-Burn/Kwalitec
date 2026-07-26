# EP-002.9 — Final Constitutional Audit

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26  
**Nature:** Assurance — no runtime changes

Legend: **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Audit scope

| In scope | Out of scope |
|---|---|
| EP-002.1–EP-002.8 constitutional claims | Redesign of EP-001.1–4 |
| Ownership / fail-open / V1–V2 / no fourth Twin | Product effectiveness trials |
| Programme success criteria vs delivered evidence | Declaring Twin Ready (T7) |
| Residual drift from EP-002.8 | Experience `SOLE_RUNTIME` product cutover |

---

## 2. Constitutional invariants — programme roll-up

| Invariant | EP-002 result | Primary evidence |
|---|---|---|
| Twin owns learner-state read model only | **Hold** | Foundation DI; quarantine note; no Twin writes |
| Planner owns plans / mission persistence | **Hold** | EP-002.7 ORM anchor; MissionOptimizer quarantined |
| Readiness owns evaluation | **Hold** | Collectors stay on legacy getters; no getter wrap |
| Insight owns Twin communication only | **Hold** | Cutover projections; presentation pass-through |
| Consumer Chain owns orchestration / gates only | **Hold** | Observability / dual-run / cutover modules |
| Presentation owns presentation selection | **Hold** | `RuntimeAPresentationAdapter` (EP-002.8) |
| Runtime A owns educational writes | **Hold** | No EP-002 schema / educational write paths |
| Curriculum V1/V2 traversal preserved | **Hold** | No curriculum engine diffs in EP-002 milestones |
| Fail-open Twin / Cutover OFF restores legacy | **Hold** | Rollback plans + drills EP-002.3–8 |
| No fourth Twin stack | **Hold** | Package inventory; quarantine |
| EP-001.1–4 not redesigned | **Hold** | Contracts extended via hosts / gates only |
| No production-wide activation by default | **Hold** | Flags default OFF; production hard-ineligible |

**C:** Constitutional ownership was preserved across the programme. No STOP condition remains open from EP-002.1–8.

---

## 3. Programme success criteria audit

Source: [`../ep002_student_intelligence_surface/PROGRAMME_BRIEF.md`](../ep002_student_intelligence_surface/PROGRAMME_BRIEF.md) §7.

| Criterion | Status | Evidence |
|---|---|---|
| Students can receive EP-001.4 insights on a primary Runtime A surface under gated rollout | **Met (gated non-prod)** | EP-002.5 cutover on dashboard/home |
| Ownership matrix unchanged | **Met** | Ownership Certification; milestone audits |
| No new Twin / planner / readiness / recommendation engine | **Met** | Package inventory delta = gates + presentation facade |
| Legacy paths remain; rollback = flags OFF | **Met** | Rollback plans EP-002.3–8; production hard gate |
| Live observability for all three `build_*` | **Met** | EP-002.1 telemetry |
| Dual presentation debt owned retirement path | **Met for Runtime A HTTP** | EP-002.8 Outcome B; residuals tracked |
| V1/V2 curriculum traversal untouched | **Met** | Explicit N/A across milestones |
| EP-001.1–4 not redesigned | **Met** | Diff posture / completion reports |

### Student-impact criteria

| Criterion | Status | Evidence |
|---|---|---|
| Guidance answers focus / risk / next / why without inventing scores | **Met under gated Twin path** | Insight contracts + cutover projection + presentation pass-through |
| Unavailable / limitation cases remain honest | **Met** | Limitation fallbacks; fail-open to legacy |
| Guidance attributable to planner / readiness when present | **Met** | Provenance / field mapping in EP-001.4 + cutover projections |

### Exit ≠ claims (confirmed)

| Forbidden claim | Confirmed non-claim? |
|---|---|
| Twin Ready (T7) by default | **Yes** |
| Recommendations scientifically validated | **Yes** |
| Public launch readiness | **Yes** |

---

## 4. Constitutional drift register (programme-level)

| ID | Drift | Severity | Disposition |
|---|---|---|---|
| CD-01 | EP-002.7A formal Programme Constitutional Review artefact absent | Process | Accepted process debt (`TD-PC-03`); EP-002.7 pack used as surrogate |
| CD-02 | EI Stage A recommendation card remains parallel narrator when orchestrator ON | Accepted residual | `TD-CO-02` — mutual exclusion retained; post-programme |
| CD-03 | Experience `/student` ExplanationService not consolidated | Out of scope | `TD-PC-02` — SOLE_RUNTIME product decision |
| CD-04 | Daily Plan display topic may differ from ORM session topic | Accepted residual | `TD-DP-01` — documented boundary tension |
| CD-05 | Cutover / dual-run health metrics are process-local | Operational | `TD-CO-01` / `TD-RI-01` / `TD-DP-03` / `TD-DR-03` |

No ownership-invention drift introduced by EP-002.

---

## 5. STOP conditions

| STOP condition | Triggered? |
|---|---|
| Ownership invention (new evaluation/planning in Insight/HTTP/templates) | **No** |
| Fourth Twin stack | **No** |
| Collector recursion via Foundation wrap of readiness getters | **No** |
| Production-wide cutover without evidence | **No** (defaults OFF; hard-ineligible) |
| Twin Ready (T7) claimed from EP-002 alone | **No** |

---

## 6. Constitutional sign-off

| Sign-off item | Status |
|---|---|
| EP-002.1–8 accepted as constitutionally compliant | **Yes** |
| Programme success criteria satisfied within gated non-prod scope | **Yes** |
| Fail-open retained until GA decision | **Yes** |
| Authoritative architecture baseline published | **Yes** — [`AUTHORITATIVE_ARCHITECTURE_BASELINE.md`](AUTHORITATIVE_ARCHITECTURE_BASELINE.md) |
| Twin Ready (T7) | **Not claimed** |
| Production GA | **Not claimed** |

**Verdict: EP-002 is constitutionally certified complete.**

**R:** Future activation beyond Controlled Pilot requires staging evidence and a separate go/no-go — not a constitutional re-open of EP-001 ownership.
