# EP-006.5 — Readiness Perception Methodology

**Programme:** EP-006.5 — Readiness Perception Validation (Tier B)  
**Date:** 2026-07-26  
**Implements:** REM-05 / RC-04 (EP-005.2); PERC-01 clearance measurement (EP-006.3)  
**Upstream method:** [`../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md`](../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md) Tier B  
**Sibling method:** [`../ep006_3_mes_perception_validation/PERCEPTION_METHODOLOGY.md`](../ep006_3_mes_perception_validation/PERCEPTION_METHODOLOGY.md)  
**Does not:** Change runtime, UI, Twin algorithms, ReadinessService authority, or educational reasoning  

---

## 1. Claim window

**W-PROD** production defaults after EP-006.4 Home readiness MES delivery. Personalisation / feedback flags remain OFF — no W-GATED credit. ReadinessService remains sole author of readiness judgements.

---

## 2. Dimensions measured

| Dimension | Operational definition | Primary signal |
|---|---|---|
| Readiness explanation visibility | L1 why + next visible without expand; L2 drivers / evidence / confidence / review ≤1 disclosure when present | Surface pack + reviewer observation |
| Driver comprehension | Student can name / restate what drives the estimate (coverage, knowledge, review discipline, etc.) | Blind re-review codes |
| Confidence understanding | Confidence label + basis understood as provisional vs certain | Calibration / confidence codes |
| Next-action clarity | Student knows what to do next from the readiness card (not only mission) | Affirmative next-action codes |
| Review-point usefulness | Review / reassess cue noticed and judged helpful when shown | Review-point codes |
| Student trust | Readiness believed enough to inform study choices **without** treating it as exam-sit advice | Trust / calibration scores |

---

## 3. Evidence methods

| Method | Role |
|---|---|
| Post-change blind re-review (N≥8 readiness-relevant personas) | Tier B student perception |
| Pre-change EP-004 corpus + EP-006.3 Tier B (Home drivers empty) | Tier C baseline / falsifier |
| EP-006.4 automated delivery + Explainability Review Pass | Tier A structural eligibility |
| Surface render captures (schema-complete + cold-start) | What students see |

**Archive rule:** Write Tier B transcripts to `tier_b_reviews/` — do **not** overwrite `ep004_private_beta/blind_reviews/` or `ep006_3_mes_perception_validation/tier_b_reviews/`.

---

## 4. Success / fail signals

| Signal | Pass | Fail |
|---|---|---|
| Home readiness drivers visible (schema-complete) | Majority observe named drivers | Drivers still empty / unnoticed |
| Driver comprehension | ≥ majority can restate drivers in own words | Unpackability theme remains Near-Universal |
| Confidence understanding | Majority read Suggested + basis as provisional | Overclaim / certainty theatre majority |
| Next-action clarity (readiness card) | ≥80% affirmative on schema-complete path | Majority unsure what readiness implies next |
| Student trust (bounded) | Conditional trust for study decisions; refusal of sit advice preserved | Blind sit reliance **or** total distrust of estimate |
| Unsupported claims | Mark explicitly | Treat estimate stacks as validated |

---

## 5. Scoring rules for K3 revalidation

1. Prefer **lower** score when schema-complete and cold-start evidence conflict.  
2. Credit perception lifts only where Tier B observes them on **student-visible Home** readiness surfaces.  
3. Do **not** credit Analytics-only driver bindings as Home perception (that residual was PERC-01).  
4. Do not claim KSI ≥ 80, K3 ≥ 70 Strong mid-band, or educational-effectiveness GO from this pack alone when external N=0 and residuals remain.  
5. Composite confidence remains ≤ Medium unless external Stage 1 N floors are met (they are not).  
6. Preserve ReadinessService authority — scoring changes are measurement only.

---

**End of PERCEPTION_METHODOLOGY**
