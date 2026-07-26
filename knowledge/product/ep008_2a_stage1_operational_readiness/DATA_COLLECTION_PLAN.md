# EP-008.2A — Data Collection Plan

**Programme:** EP-008.2A — Stage 1 Operational Readiness  
**Date:** 2026-07-26  
**Status:** Plan COMPLETE — collection **not started** (enrollment HOLD)  
**Governing metrics:** EP-003 `EDUCATIONAL_METRICS.md` · EP-007.3 `COHORT_DESIGN.md` §4  
**Evidence law:** P-003.5 Evidence Hierarchy / Claim Standard  
**Does not:** Redefine M1–M9; claim C-EDU; change emit schemas beyond documenting what exists  

---

## 1. Purpose

Define **what** Stage 1 will collect, **how**, **retention / privacy**, and **which claims** each dataset may support — so the Product Board knows the evidence path before participants enroll.

---

## 2. Populations and IDs

| Population | ID scheme | Counts toward Stage 1 N? |
|---|---|---|
| Stage 0 internal | `BETA-INT-*` | **No** |
| Stage 1 pilot | `BETA-PIL-001` … `010` | **Yes** |
| Stage 2 expanded | `BETA-EXT-*` | Later; not this plan |

Knowledge artefacts: **pseudonymous IDs only** — no emails, names, or raw PII.

---

## 3. Consent gates for inclusion

| Dataset | Requires |
|---|---|
| Productive study access | Invite account + applicable privacy notice |
| M1–M9 KPI numerators | Measurement consent |
| Analytics event rows (flag ON) | Invite-only + privacy notice covering first-party learning analytics |
| Interview notes / themes | Interview consent (optional) |
| Anonymous quotes in internal reports | Quote consent (optional) |
| After measurement withdrawal | Exclude from numerators; honour export/delete |

---

## 4. Collection streams

### 4.1 Operational / reliability (C-REL)

| Data | Source | Cadence | Storage |
|---|---|---|---|
| Monitoring snapshot | `flask analytics-metrics` | Weekly (daily first week flag ON) | Ops notes (dated); optional knowledge annex without PII |
| P0/P1/P2 tickets | Support / issue tracker | Continuous | Tracker tagged `private-beta` |
| Onboarding status | Cohort registry fields | Per participant | `BETA_COHORT.md` status only |
| Analytics enable log | `ANALYTICS_ACTIVATION.md` | On change | Knowledge |
| Privacy request log | Support + audit CLI | On request | Audit log (36 months policy) |

### 4.2 Behavioural educational metrics (directional → later G1.9 path)

| ID | Metric | Cadence | Stage 1 directional target | Claim class until floors |
|---|---|---|---|---|
| M1 | Weekly Active Learners among accepted | Weekly | ≥60% WAL by personal week 3 | Exploratory / directional |
| M2 | Sessions per WAL | Weekly | Median ≥1.5 / week early | Same |
| M3 | Reflection completion | Weekly | ≥70% when required | Same |
| M4 | Session completion | Weekly | ≥70% (relaxed vs 75%) | Same |
| M5 | Journey / progress engagement | Bi-weekly | Trend; **provisional** if Journey emit gated | Label provisional |
| M6 | Study consistency | Weekly | Mean ≥0.50 | Same |
| M7 | Continuity WoW | Weekly | ≥60% post week 1 | Same |
| M8 | Time-to-readiness proxy | Window end | Baseline only; no Exam Ready claim | Watch |
| M9 | Curriculum completion trend | Window end | Exam-dated interpretation only | Watch |

**Sources:** productive Session / Reflection domain records; analytics events when Pilot ON; manual ops count if flag OFF (must label method).

**Forbidden vanity:** raw login counts, streaks-as-success, engagement without productive Session definition.

### 4.3 Observational commitment / follow-through (research only)

| Event / derived | Source | Use |
|---|---|---|
| `commitment_confirmed` | EP-008.3A emit / preference record | Observational rate |
| `commitment_deferred` | Same | Honest agency signal |
| `commitment_completed` / session-linked complete | Same | Follow-through research |
| Accept / dismiss marketing KPIs | **Out of scope** unless separate Approved PRD lifts freeze | Frozen (DR-036) |

**Hard rule:** these metrics must **not** feed ranking, readiness, or Twin authority. Not C-EDU; not Strong-band K2 alone.

### 4.4 Qualitative research

| Instrument | When | Output | Codes |
|---|---|---|---|
| Week-1 check-in | Personal week 1 | Short notes | Activation / P1 themes |
| Week 2–3 check-in | Mid window | Short notes | M3/M6/clarity |
| Structured interview (~30 min) | Week 4+ | Coded notes | M / O / Q / surface IDs |
| Continuous feedback / issues | Always | Feedback register | Defect vs Never-Build |

Stage 1 ops exit target: **≥3** coded interviews (full educational GO still wants ≥8 or 25% active — C6).

### 4.5 Privacy fulfilment evidence

| Action | Tool | SLA (beta) |
|---|---|---|
| Export | `flask analytics-export-user` | ≤14 days |
| Delete analytics | `flask analytics-delete-user` | ≤30 days request path |
| Consent verify | `flask analytics-verify-consent` | Before KPI inclusion disputes |
| Retention | `flask analytics-retention` | Daily when flag ON external |

---

## 5. Weekly scorecard filing procedure

1. Freeze claim window dates (personal starts may stagger — report both calendar week and N at risk).  
2. Compute M1–M4, M6–M7 per Educational Metrics formulae.  
3. Record **N accepted**, **N WAL**, **N with measurement consent**, method (analytics ON vs manual).  
4. Status cells: `On track` | `Watch` | `Off track` | `Baseline` | `N/A` | `Excluded` | `exploratory` | `insufficient N`.  
5. File under EP-004 scorecard location or successor Stage 1 ops folder — **no PII**.  
6. Review P0/P1 open count same day.

Template values remain empty until collection starts — do not invent.

---

## 6. Export pack for analysis (end of window or on Board request)

Produce a **research export pack** (internal Board / measurement only):

| Artefact | Contents |
|---|---|
| `scorecards/` | Weekly CSV or markdown tables (pseudonymous aggregates) |
| `events_summary/` | Aggregated event counts by type / week (no raw reflection text) |
| `commitment_observational/` | Confirm / defer / complete rates with N |
| `interviews/` | Coded theme matrix (M/Q IDs); quotes only if quote-consented |
| `ops/` | Monitoring verdicts; incident list; privacy request outcomes |
| `limitations.md` | N, missing emit, provisional M5, confidence band |

**Delivery:** secure channel; not public; not marketing site.

**Student-level JSON exports:** fulfil per-user via Privacy Ops on request — separate from aggregate research pack.

---

## 7. Evidence → claim mapping

| Collected evidence | Minimum hierarchy | Permitted claim | Forbidden claim |
|---|---|---|---|
| Ops GREEN + closed P0 | E2 ops | C-REL for Stage 1 pilot class | C-V1 |
| Tier B prior packs | E3 | Bounded perception (already filed) | C-VAL-E; C-EDU |
| Stage 1 M-series N 5–10 ≥2–4 weeks | E4 path (partial) | Directional behavioural description with N | Educational GO; G1.9 PASS alone |
| Interviews ≥3 coded | Supporting E4 | Theme support for Q1–Q3 | Substitute for M floors |
| Full C5–C6 floors + Q1–Q5 Yes | E5 + Go | C-EDU path / G1.9 reconsideration | Pass-rate north star without methodology |

Prefer-lower: if uncertain, under-claim.

---

## 8. Integrity and anti-patterns

| Do | Do not |
|---|---|
| Label insufficient N | Greenwash empty KPIs |
| Keep Stage 0 separate | Count dogfood as Stage 1 N |
| Keep commitment observational | Feed ranking from commitment rates |
| Observation-only analysis without PRD | Silent A/B on recommendations / readiness |
| Pseudonymise knowledge artefacts | Paste emails into git |

---

## 9. Dependencies before first event / first scorecard

1. OR-01 Privacy Review signed.  
2. OR-02/OR-06 Pilot analytics path **or** explicit manual-measurement decision.  
3. OR-03/OR-04 Notice + consent capture.  
4. At least one `BETA-PIL` Accepted with measurement consent.

Until then this plan is **rehearsal-only**.

---

## 10. Success of *this* plan (EP-008.2A)

| Criterion | Status |
|---|---|
| Streams defined | Met |
| Claim mapping explicit | Met |
| Export pack specified | Met |
| Live collection started | **Not met** (blocked — documented) |

---

**End of DATA_COLLECTION_PLAN**
