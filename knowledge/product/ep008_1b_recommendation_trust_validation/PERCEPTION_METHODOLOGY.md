# EP-008.1B — Recommendation Trust Perception Methodology

**Programme:** EP-008.1B — Recommendation Trust Validation (Tier B)  
**Date:** 2026-07-26  
**Implements:** EP-008.1 [`VALIDATION_PLAN.md`](../ep008_1_recommendation_trust/VALIDATION_PLAN.md) §4; P-004.1 IMP-01 measurement  
**Upstream method:** [`../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md`](../ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md) Tier B  
**Sibling methods:** EP-006.3 / EP-006.5 / EP-007.2 perception programmes  
**Does not:** Change runtime, UI, Twin algorithms, RecommendationService ranking, or educational reasoning  

---

## 1. Claim window

**W-PROD** production defaults after EP-008.1A trust presentation on sole-runtime Student Home. Personalisation / feedback flags remain OFF — no W-GATED credit. Runtime A remains sole educational authority. Ranking unchanged.

---

## 2. Dimensions measured

Approved observables only (VALIDATION_PLAN §2 + §4.2; PSF K2). No new metrics invented.

| Dimension | Operational definition | Primary signal |
|---|---|---|
| Recommendation clarity | Student can restate why the tip exists and why it matters now | Why / why-now codes |
| Understanding | Student can answer the five success questions on schema-complete nights | Five-question Pass codes |
| Actionability | One clear next action; willingness path to Start Session | Next-action / CTA codes |
| Trust | Tip believed enough to influence tonight’s choice without blind obedience | Trust / credibility scores |
| Confidence | Confidence label + basis understood as provisional vs certain | Confidence codes |
| Acceptance (stated) | Stated willingness to follow tip tonight (H2) | Willingness codes |
| Completion intention | Student understands practice can change future tips (review / loop) | Completion-loop codes |
| Coherence (Q9) | Plan relationship labelled; divergence not silent | Coherence codes |
| Alternatives / refusal (Q10) | Agency via ≤2 alts **or** honest empty preferred to fake tip | H3 / H4 codes |

---

## 3. Evidence methods

| Method | Role |
|---|---|
| Post-change blind re-review (N≥8 trust / recommendation-relevant personas) | Tier B student perception |
| Pre-change EP-004 corpus + EP-006.3 MES Tier B (K2=55 residual) | Tier C baseline / falsifier |
| EP-008.1A contract tests TR-A01–TR-A08 + design checklists | Tier A structural eligibility |
| Surface render captures (schema-complete, honest refusal, cold-start) | What students see |
| Theme coding | Trust gained / still opaque / overclaim / clutter |

**Archive rule:** Write Tier B transcripts to `tier_b_reviews/` — do **not** overwrite `ep004_private_beta/blind_reviews/` or prior EP-006/007 `tier_b_reviews/`.

**Reviewer framework:** `knowledge/product/ep004_private_beta/reviewer_framework/` — personas executed one at a time against the Student Surface Pack (live student-facing experience when package diverges).

---

## 4. Perception hypotheses (VALIDATION_PLAN §4.2)

| ID | Hypothesis | Falsifier |
|---|---|---|
| H1 | Schema-complete Home clears “I don’t know why I should follow this” | ≥50% still cannot state why/evidence |
| H2 | Why-now + benefit raise stated willingness to start session | No change vs pre-trust baseline anecdotes |
| H3 | Refusal state increases honesty trust vs fake tip | Students prefer fabricated confident tip |
| H4 | Alternatives increase agency without decision paralysis | Students report overwhelm / ignore primary CTA |

---

## 5. Success / fail signals

| Signal | Pass | Fail |
|---|---|---|
| Five success questions (schema-complete) | Majority can restate why / why-now / next / benefit / loop | Majority cannot |
| H1 clarity / understanding | ≥50% can state why + evidence | Opacity majority |
| H2 stated acceptance | Majority affirmative willingness on schema-complete | No lift vs baseline hesitation |
| H3 refusal honesty | Majority prefer honest empty over fake certainty | Prefer fabricated tip |
| H4 alternatives | Agency without primary-CTA paralysis | Overwhelm / ignore primary |
| Confidence | Majority read Suggested / Cannot-yet as provisional | Certainty theatre majority |
| Unsupported claims | Mark explicitly | Treat estimate stacks or acceptance rates as validated |

---

## 6. Scoring rules for K2 revalidation

1. Prefer **lower** score when schema-complete and cold-start / refusal evidence conflict.  
2. Credit perception lifts only where Tier B observes them on **student-visible** trust surfaces.  
3. Do **not** credit ranking / precision (unchanged) or acceptance-rate KPIs (EP-008.3).  
4. Strong-band K2 (**≥75**) is **not** claimable from UI trust alone.  
5. Planning band after clean Tier B: **67–73**; apply prefer-lower.  
6. Composite confidence remains ≤ Medium (external N=0).  
7. Preserve Runtime A ownership — scoring changes are measurement only.  
8. Secondary K8 deepen only if structured Coach / refusal / benefit codes support it; prefer-lower.

---

## 7. Out of scope

- M1–M9 educational effectiveness (EP-008.2 / EP-007.3)  
- Acceptance / dismiss rate dashboards (EP-008.3)  
- Recommendation precision sample (IMP-11)  
- Invented survey instruments beyond approved dimensions  

---

**End of PERCEPTION_METHODOLOGY**
