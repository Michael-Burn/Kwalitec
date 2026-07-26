# EP-006.3 — Perception Methodology

**Programme:** EP-006.3 — MES Perception Validation (Tier B)  
**Date:** 2026-07-26  
**Implements:** MES-09 (EP-006.1) / REM-04 (EP-005.2)  
**Upstream method:** [`../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md`](../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md) Tier B  
**Does not:** Change runtime, UI, Twin algorithms, or educational reasoning  

---

## 1. Claim window

**W-PROD** production defaults after EP-006.2 MES presentation delivery. Personalisation / feedback flags remain OFF — no W-GATED credit.

---

## 2. Dimensions measured

| Dimension | Operational definition | Primary signal |
|---|---|---|
| Explanation visibility | L1 why + next visible without expand; L2 evidence ≤1 disclosure when present | Surface pack + reviewer observation |
| Explanation comprehension | Student can restate why in own words | Blind re-review codes |
| Explanation trust | Guidance believed enough to influence tonight’s choice (without requiring blind obedience) | Trust / credibility scores |
| Explanation usefulness | Why adds instructional value beyond restating the mission title | Usefulness codes |
| Next-action clarity | Student knows what to do next from Home path | Affirmative next-action codes |
| Review-point usefulness | Review / reassess cue noticed and judged helpful when shown | Review-point codes |
| Confidence understanding | Confidence label + basis understood as provisional vs certain | Calibration / confidence codes |

---

## 3. Evidence methods

| Method | Role |
|---|---|
| Post-change blind re-review (N=8 explainability-relevant personas) | Tier B student perception |
| Pre-change EP-004 corpus (SV-001–020) | Tier C baseline / falsifier only |
| EP-006.2 automated contract + template smoke | Tier A structural eligibility (already landed) |
| Dogfood checklist criteria (EP-006.1 §6.1) | Structural visibility cross-check via render capture |

**Archive rule:** Write Tier B transcripts to `tier_b_reviews/` — do **not** overwrite `ep004_private_beta/blind_reviews/` baseline.

---

## 4. Success / fail signals (from EP-006.1 §6.2)

| Signal | Pass | Fail |
|---|---|---|
| Coach opacity theme | Cleared or **minority** on schema-complete Home | Remains Near-Universal |
| K8 validated | ≥ 70 | Still &lt; 70 |
| Next-action clarity | ≥80% of Tier B pack affirmative on Home schema-complete path | Majority still unsure |
| Unsupported claims | Mark explicitly | Treat estimate stacks as validated |

---

## 5. Scoring rules for K8 revalidation

1. Prefer **lower** score when schema-complete and cold-start evidence conflict.  
2. Credit perception lifts only where Tier B observes them on **student-visible** surfaces.  
3. Do not credit Home readiness drivers (still empty in `home_vm`).  
4. Do not claim KSI ≥ 80 or educational-effectiveness GO from this pack.  
5. Composite confidence remains ≤ Medium unless external Stage 1 N floors are met (they are not).

---

**End of PERCEPTION_METHODOLOGY**
