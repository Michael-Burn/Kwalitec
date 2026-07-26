# Weekly Educational Scorecard

**Programme:** EP-004 — Workstream 4  
**Metrics authority:** [`../ep003_educational_effectiveness/EDUCATIONAL_METRICS.md`](../ep003_educational_effectiveness/EDUCATIONAL_METRICS.md) — **M1–M9 unchanged**  
**Scorecard layout:** [`../ep003_educational_effectiveness/PRODUCT_SCORECARD.md`](../ep003_educational_effectiveness/PRODUCT_SCORECARD.md)  
**Updated:** 2026-07-24  
**Rule:** Below sample thresholds → label **exploratory** / **insufficient N**. Never greenwash.

---

## Measurement window policy

| Window | Population | Claim level |
|---|---|---|
| Week 0 (Stage 0) | Internal participants only | Exploratory — not product claims |
| Weeks 1+ Stage 1 | External pilot after privacy | Directional only until N≥10 / ≥2 weeks |
| Weeks ≥4 with N≥20 | Stage 2 active | Product-decision threshold (Metrics §4) |

Cadence: **weekly** during private beta for M1–M4, M6–M7; bi-weekly M5; monthly M8–M9 / Go–No-Go.

---

## Week 0 — Stage 0 baseline (2026-07-24)

**Population:** BETA-INT-001 … 003 (N_external = 0; N_internal_participant = 3)  
**Analytics:** Production default OFF; internal ON authorized only  
**Claim level:** **exploratory / insufficient N**

### Educational KPIs (M1–M9)

| ID | Metric | Target (EP-003) | Value | Status | Notes |
|---|---|---|---|---|---|
| M1 | Weekly Active Learners | ≥70% retain WAL weeks 3–6 (N≥20) | Internal dogfood only | **Baseline / exploratory** | External WAL = 0 |
| M2 | Sessions per WAL | Median ≥2 / week by week 4 | Not reported | **Insufficient N** | No external WAL denominator |
| M3 | Reflection completion | ≥80% | Not reported | **Insufficient N** | Measure when flag ON + reflections required |
| M4 | Session completion (completed/started) | ≥75% by week 4 | Not reported | **Insufficient N** | Abandon rate TBD Stage 1 |
| M5 | Curriculum progress velocity | Baseline weeks 1–2 | Provisional N/A | **Baseline** | Prefer `journey.progressed` when emit live (ADR-026); else provisional label |
| M6 | Study consistency (4-week) | ≥0.60 | Not reported | **Insufficient N** | Needs ≥4 weeks external |
| M7 | Learning continuity (WoW) | ≥70% post week 1 | Not reported | **Insufficient N** | Needs multi-week external WAL |
| M8 | Time to readiness | Baseline only; no marketing | Censored / N/A | **Baseline** | Twin authority; no claim |
| M9 | Curriculum completion | Trend / exam-dated plan | N/A | **Baseline** | Requires exam-scoped plans |

### Activation (scorecard companions)

| KPI | Target | Value | Status |
|---|---|---|---|
| Invite → first Session (7d) | ≥70% | N/A (no external invites) | Baseline |
| Time to first Session (median days) | ≤3 | N/A | Baseline |

### Ops companions (context only)

| KPI | Value | Status |
|---|---|---|
| Support P1 open >48h | 0 | On track |
| Analytics flag (prod default) | OFF | Expected |
| Stage monitoring | GREEN | See OPERATIONS_MONITORING |

### Decisions from Week 0 review

1. **Do not** claim educational effectiveness.  
2. **Hold** Stage 1 until Privacy Review signed.  
3. Continue Stage 0 dogfood; enable analytics **internal-only** when operator completes activation log.  
4. Next scorecard: file Week 1 only after first external productive Sessions **or** note “no external activity.”

---

## Week 1+ template (copy per ISO week)

**ISO week:** ____  
**Stage:** 0 / 1 / 2  
**N invited / N accepted / WAL:** ____ / ____ / ____  
**Claim level:** exploratory | directional | product-decision  

| ID | Value | Status | Evidence path |
|---|---|---|---|
| M1 | | | |
| M2 | | | |
| M3 | | | |
| M4 | | | |
| M5 | | | |
| M6 | | | |
| M7 | | | |
| M8 | | | |
| M9 | | | |

**Abandon rate (M4 companion):** ____  
**Interview tally this week:** ____  
**Ops GREEN/AMBER/RED:** ____  
**Product decisions:** ____  

---

## Exit criteria (WS4)

| Criterion | Status |
|---|---|
| M1–M9 applied without formula change | COMPLETE |
| Weekly cadence defined | COMPLETE |
| Week 0 scorecard filed (honest labels) | COMPLETE |
| Multi-week external fill | OPEN — Stage 1+ |
