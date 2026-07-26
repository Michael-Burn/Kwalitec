# EP-008.3B — Recommendation Commitment Perception Methodology

**Programme:** EP-008.3B — Recommendation Commitment Validation (Tier B)  
**Date:** 2026-07-26  
**Implements:** EP-008.3 [`VALIDATION_PLAN.md`](../ep008_3_recommendation_commitment_followthrough/VALIDATION_PLAN.md) §5; P-004.1 IMP-02 measurement  
**Upstream method:** [`../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md`](../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md) Tier B  
**Sibling methods:** EP-008.1B Recommendation Trust; EP-006.3 / EP-006.5 / EP-007.2 perception programmes  
**Does not:** Change runtime, UI, Twin algorithms, RecommendationService ranking, or educational reasoning  

---

## 1. Claim window

**W-PROD** production defaults after EP-008.3A commitment layer on sole-runtime Student Home (Pattern A). Trust Contract T1–T11 remains. Personalisation / feedback flags remain OFF — no W-GATED credit. Runtime A remains sole educational authority. Ranking unchanged.

---

## 2. Dimensions measured

Approved observables only (VALIDATION_PLAN §2 + §5.2; PSF K2 / K7). No new metrics invented.

| Dimension | Operational definition | Primary signal |
|---|---|---|
| Recommendation commitment (agency) | Student experiences conscious choice to do tonight’s tip | H1 agency codes |
| Honest deferral | Defer feels safe; preferred to fake compliance / ignore | H2 defer codes |
| Session completion intention | Student links commit → session → outcome | Completion codes |
| Reflection usefulness | Can restate what changed / why / what next after completion | H3 reflection codes |
| Recommendation continuity | Plan feels continuous across commit / defer / history | H4 continuity codes |
| Student understanding | Trust why/evidence still restatable (regression watch) | Trust regression codes |
| Student workload / cognitive load | No increase vs EP-008.1B clutter baseline; single primary CTA | H5 load codes |
| Behavioural friction | Shame, streak pressure, dual CTA, Twin theatre | Shame / Twin codes |

### Behavioural metrics (observational only)

Measure when available; do **not** invent rates:

| Metric | Use |
|---|---|
| Commitment rate | Directional baseline |
| Honest deferral rate | Non-zero healthy band |
| Completion rate among committed | Prefer under-claim |
| Reflection viewed / acknowledged | Majority of completions in dogfood |
| Recommendation revisit after defer | Optional continuity signal |

**This programme:** confirms instrumentation exists (Tier A CF-A10) and records dogfood checklist outcomes. Cohort-level rates remain **absent** (external N=0; no Stage 0 aggregate snapshot filed).

---

## 3. Evidence methods

| Method | Role |
|---|---|
| Post-change blind re-review (N≥8 trust / agency / motivation / load personas) | Tier B student perception |
| Pre-change EP-008.1B corpus (K2=68; Strong-band residual) | Tier C baseline / falsifier |
| EP-008.3A contract tests CF-A01–CF-A12 + design checklists | Tier A structural eligibility |
| Surface render captures (offered, committed, deferred, reflection, refusal, history) | What students see |
| UI_SPEC §13 dogfood checklist | Facilitator structural walkthrough |
| Theme coding | Agency / shame / clutter / continuity / Twin theatre |

**Archive rule:** Write Tier B transcripts to `tier_b_reviews/` — do **not** overwrite `ep004_private_beta/blind_reviews/` or prior EP-006/007/008.1B `tier_b_reviews/`.

**Reviewer framework:** `knowledge/product/ep004_private_beta/reviewer_framework/` — personas executed one at a time against the Student Surface Pack.

---

## 4. Perception hypotheses (VALIDATION_PLAN §5.2)

| ID | Hypothesis | Falsifier |
|---|---|---|
| H1 | Students experience conscious choice (“I chose to do it”) | Majority report passive click-through or coercion |
| H2 | Defer feels honest and safe | Students prefer lying / ignoring over defer; or report shame |
| H3 | Reflection clarifies what changed and what next | Students cannot restate change/next after completion |
| H4 | History reads as educational narrative | Students call it clutter / audit log / irrelevant |
| H5 | Cognitive load does not increase vs trust-only baseline | Dual-CTA / overwhelm themes dominate |
| H6 | K8 does not regress | Opacity / overclaim / Twin-learning themes appear |

---

## 5. Success / fail signals

| Signal | Pass | Fail |
|---|---|---|
| H1 agency | Majority describe choice (or Pattern A helper as conscious intent) | Passive click-through / coercion majority |
| H2 defer honesty | Majority prefer honest defer over fake compliance | Shame / avoid defer |
| H3 reflection | Majority restate change + next | Empty / magic coach |
| H4 history | Majority educational narrative | Audit-log / clutter majority |
| H5 load | No dual primary CTA; load not Fail vs EP-008.1B | Overwhelm / ignore Start Session |
| H6 K8 hold | No Twin theatre / opacity regression | Opacity / overclaim dominate |
| Behavioural floors | Directional rates present | Rates absent → Strong-band K2 blocked |
| Unsupported claims | Mark explicitly | Treat estimated ΔKSI or invented rates as validated |

---

## 6. Scoring rules for K2 / K7 / K8 revalidation

1. Prefer **lower** score when perception and behavioural evidence conflict.  
2. Credit perception lifts only where Tier B observes them on **student-visible** commitment surfaces.  
3. Do **not** credit ranking / precision (unchanged).  
4. Strong-band K2 (**≥75**) requires Tier B agency themes **plus** observational commitment evidence — not UI alone (VALIDATION_PLAN §6).  
5. Without cohort behavioural floors, do **not** raise K2 into Strong band (≥70 mid-claim also prefer-capped at Partial upper without rates — align with EP-008.1B lesson).  
6. K7 propose **+2 to +6** only if history/continuity themes support; prefer-lower.  
7. K8 target **hold ≥ 72**; any opacity/overclaim → no K2 inflation.  
8. Composite confidence remains ≤ Medium (external N=0).  
9. Preserve Runtime A ownership — scoring changes are measurement only.

---

## 7. Out of scope

- M1–M9 educational effectiveness (EP-008.2 / EP-007.3)  
- Ranking precision sample (IMP-11)  
- Personalisation ON (EP-009.x)  
- Invented survey instruments beyond approved dimensions  
- Runtime A / recommendation personalisation adaptation  

---

**End of PERCEPTION_METHODOLOGY**
