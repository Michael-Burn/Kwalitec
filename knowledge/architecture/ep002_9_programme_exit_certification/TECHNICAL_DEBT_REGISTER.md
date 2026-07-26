# EP-002.9 — Technical Debt Register

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26  
**Supersedes programme tracking for:** EP-001.5 debt consumed by EP-002 + EP-002.1–8 residual IDs

Priority: **P0** blocking · **P1** near-term · **P2** planned · **P3** backlog · **Closed**

---

## 1. EP-001.5 debt consumed by EP-002

| ID | Original item | Disposition |
|---|---|---|
| TD-OPS-01 | No live `build_*` observability | **Closed** (EP-002.1) |
| TD-ARCH-01 | Multi-Twin operator confusion | **Closed at operator/docs level** (EP-002.1 quarantine) |
| TD-ARCH-06 | Shadow / Adaptive TwinInput flag-doc drift | **Closed** (EP-002.1 docs alignment) |
| TD-ARCH-04 / TD-OPS-03 / IF-07 | Nested Foundation reassembly | **Closed** for Insight composition path (EP-002.2) |
| TD-ARCH-03 / IF-09 | MissionOptimizer orphan | **Dispositioned** — soft-deprecate / quarantine (EP-002.2); hard-delete deferred |
| TD-OPS-02 | Authority not soaked | **Closed for non-prod harness** (EP-002.3); target-env soak still open for T7 |
| TD-PROD-01 | Students never see EP-001.2–4 under defaults | **Partially closed** — gated non-prod cutovers exist; production still OFF by design |
| TD-ARCH-02 | Dual presentation Insight vs EIP-003 | **Closed for Runtime A HTTP** (EP-002.8 Outcome B) |

---

## 2. Open technical debt (authoritative post-EP-002)

### Architectural

| ID | Priority | Item | Evidence | Remediation |
|---|---|---|---|---|
| TD-DP-01 | P1 | Twin daily-plan display topic may differ from legacy ORM session topic | EP-002.7 | Product decision: align display to ORM, or promote Twin slot into persistence under constitutional review |
| TD-DP-04 | P2 | MissionOptimizer soft-deprecated code remains | EP-002.2 / .7 | Hard-delete after quarantine period + grep gate |
| TD-ARCH-05 | P2 | Collectors depend on legacy readiness getters | EP-001.5 / EP-002.6 | Optional collector refactor (out of EP-002 critical path) |
| TD-PC-02 | P2 | Experience `/student` ExplanationService not consolidated | EP-002.8 | SOLE_RUNTIME product programme |
| TD-CO-02 | P2 | EI Stage A dashboard card remains separate narrator | EP-002.5 / .8 | Product disposition under mutual exclusion; do not invent third narrator |

### Operational

| ID | Priority | Item | Evidence | Remediation |
|---|---|---|---|---|
| TD-OPS-STAGING | P1 | Live staging soak evidence pack across EP-002.5–8 not archived as programme artefact | EP-002.5–8 benches only | Controlled Pilot ops pack: metrics, logs, Foundation P95, rollback drills |
| TD-CO-01 / TD-RI-01 / TD-DP-03 / TD-DR-03 | P2 | Cutover / dual-run health metrics are process-local | Milestone reports | Durable metrics sink / ops dashboard |
| TD-OPS-04 | P3 | Shadow bundled with Twin ON | EP-001.5 | Accept unless independent Shadow rollout required |

### Product / presentation

| ID | Priority | Item | Evidence | Remediation |
|---|---|---|---|---|
| TD-PROD-02 | P2 | Mock performance unavailable on Foundation | EP-001.5 | Runtime A distinguish mock evidence when product needs it |
| TD-PROD-03 | P2 | Confidence bands are evidence-density heuristics | EP-001.3 | Product decision on Capability 2.7 |
| TD-PC-01 | P3 | Twin confidence not a dedicated UI chip | EP-002.8 | Optional UX polish |
| TD-DR-01 / TD-CO-03 / TD-RI-03 | P2 | Alignment / fingerprint heuristics | EP-002.4–6 | Improve topical alignment before production expansion |
| TD-DR-02 | P3 | EI path may skip dual-run coverage | EP-002.4 | Accept or extend diagnostics |

### Process

| ID | Priority | Item | Evidence | Remediation |
|---|---|---|---|---|
| TD-PC-03 | P3 | EP-002.7A formal constitutional review artefact missing | EP-002.8 CD-01 | Do not invent retroactively; cite EP-002.7 pack + this exit audit |
| TD-NAME-01 | P3 | Programme ID collision with EP-002 Analytics | Programme README | Prefer full titles; optional future alias |

---

## 3. Closed in EP-002 (selected)

| ID | Closed by |
|---|---|
| TD-OPS-01 | EP-002.1 |
| TD-ARCH-01 (docs/ops) | EP-002.1 |
| TD-ARCH-06 | EP-002.1 |
| IF-07 / nested CLS | EP-002.2 |
| TD-RI-02 readiness double-narration | EP-002.8 |
| TD-ARCH-02 Runtime A HTTP dual presentation | EP-002.8 |

---

## 4. Prioritised post-programme sequence

1. **P1 staging evidence pack** (`TD-OPS-STAGING`) before expanding Controlled Pilot  
2. **P1 display/persistence alignment decision** (`TD-DP-01`) before Daily Plan production consideration  
3. **P2 durable metrics** (process-local health debt)  
4. **P2 EI Stage A / Experience narrator dispositions** (`TD-CO-02`, `TD-PC-02`)  
5. **P2 MissionOptimizer hard-delete** (`TD-DP-04`)  
6. **P2/P3 product Twin facet gaps** (mock performance, confidence UX)  

---

## 5. Debt statement

**C:** EP-002 intentionally retained dual-path complexity for safe cutover and then burned the Runtime A presentation dual-path. Remaining debt is operational evidence, Experience-scope consolidation, and accepted boundary tensions — not constitutional failure.

**R:** Do not reopen EP-001 ownership to “fix” residual presentation or Experience debt.
