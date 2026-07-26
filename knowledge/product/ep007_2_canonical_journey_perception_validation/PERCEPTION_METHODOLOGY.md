# EP-007.2 — Journey Perception Methodology

**Programme:** EP-007.2 — Canonical Journey Perception Validation (Tier B)  
**Date:** 2026-07-26  
**Implements:** REM-04 measurement for REM-02 / REM-03 (EP-005.2); clears dual-home residual themes from EP-006.3 / EP-006.5  
**Upstream method:** [`../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md`](../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md) Tier B  
**Sibling methods:** [`../ep006_3_mes_perception_validation/PERCEPTION_METHODOLOGY.md`](../ep006_3_mes_perception_validation/PERCEPTION_METHODOLOGY.md), [`../ep006_5_readiness_perception_validation/PERCEPTION_METHODOLOGY.md`](../ep006_5_readiness_perception_validation/PERCEPTION_METHODOLOGY.md)  
**Does not:** Change runtime, UI, Twin algorithms, PlanningService / RecommendationService / ReadinessService authority, or educational reasoning  

---

## 1. Claim window

**W-PROD** production defaults after EP-007.1 with `KWALITEC_V2_SOLE_RUNTIME=ON` (as in `render.yaml`). Personalisation / feedback flags remain OFF — no W-GATED credit. Runtime A remains sole educational authority.

Dual-run (`SOLE_RUNTIME=OFF`) is **out of claim window** for dual-home clearance — logged as residual for Internal Alpha / soak only.

---

## 2. Dimensions measured

| Dimension | Operational definition | Primary signal |
|---|---|---|
| Entry-point discoverability | After login, student finds one obvious home without choosing Dashboard vs Student Home | Blind re-review codes |
| Session-start clarity | Student knows how to start / resume tonight’s study from Home in one step | Affirmative start-path codes |
| Navigation confidence | Student trusts they are on the right path through today’s study without second-guessing chrome | Confidence / orientation codes |
| Duration consistency | Same planned minutes on Home and Session Overview for the same day (preferred minutes) | Duration Pass/Fail codes |
| Continuity through today’s study | Login → Home → Session → Complete → Home feels one loop | Continuity codes |
| Perceived cognitive load | Organisational mental effort falls vs pre-consolidation dual-home / duration reconciliation | Cognitive-load codes |

---

## 3. Evidence methods

| Method | Role |
|---|---|
| Post-change blind re-review (N≥8 journey / workflow-relevant personas) | Tier B student perception |
| Pre-change EP-004 corpus + EP-005.2 journey review + EP-006.3/5 dual-home residuals | Tier C baseline / falsifier |
| EP-007.1 automated canonical journey tests | Tier A structural eligibility |
| Surface / navigation / duration captures | What students see on W-PROD path |

**Archive rule:** Write Tier B transcripts to `tier_b_reviews/` — do **not** overwrite `ep004_private_beta/blind_reviews/` or prior EP-006.x `tier_b_reviews/`.

---

## 4. Success / fail signals

| Signal | Pass | Fail |
|---|---|---|
| Dual-home friction (sole runtime) | Majority report single home / no Dashboard choice | Dual-home theme remains Near-Universal on W-PROD |
| Duration consistency | ≥ majority observe matching Home ↔ Session minutes when preferred set | 30-vs-90 Universal theme persists |
| Session-start clarity | ≥80% affirmative on canonical Home CTA | Majority unsure where to start |
| Continuity | Majority complete today’s loop without competing continue paths | Split continue / resume fatigue majority |
| Cognitive load | Majority report less reconciliation tax than baseline | Management burden unchanged |
| Unsupported claims | Mark explicitly | Treat dual-run Alpha as W-PROD clearance |

---

## 5. Scoring rules for K1 revalidation

1. Prefer **lower** score when sole-runtime Pass conflicts with dual-run residual (do not deny W-PROD Pass; deny High confidence and mid-Strong inflation).  
2. Credit perception lifts only where Tier B observes them on **student-visible sole-runtime** journey surfaces.  
3. Do **not** credit PlanningService schema alone as dual-home clearance (that was already structural).  
4. Do not claim KSI ≥ 80, educational-effectiveness GO, or overall G1 PASS from this pack.  
5. Composite confidence remains ≤ Medium unless external Stage 1 N floors are met (they are not).  
6. Preserve Runtime A ownership — scoring changes are measurement only.  
7. Secondary K5 micro-lift only if cognitive-load / continuity codes Pass majority; prefer-lower.

---

**End of PERCEPTION_METHODOLOGY**
