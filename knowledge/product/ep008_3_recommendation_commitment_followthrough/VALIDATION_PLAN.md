# EP-008.3 — Validation Plan

**Programme:** EP-008.3 — Recommendation Commitment & Follow-through  
**Date:** 2026-07-26  
**Status:** Validation contract for design + successor delivery  
**Primary claim target:** K2 Recommendation usefulness ≥ **75** (Strong-band eligibility)  
**Secondary:** K7 improvement; **K8 hold** (no regression from **72**)  
**Also watch:** Cognitive load (must not increase)  
**Rule:** Prefer-lower; estimated ΔKSI ≠ validated progress (DR-026); metrics observational only  

---

## 1. What this plan proves

| Claim | In scope? |
|---|---|
| Students can consciously commit and honestly defer on Home | **Yes** |
| Completion reflection answers what changed / why / what next | **Yes** |
| Lightweight recommendation history is educationally readable | **Yes** |
| Observational commitment / completion / defer / reflection metrics exist | **Yes** |
| Ranking / educational reasoning improved | **No** |
| Exam outcomes / DR-036 freeze lift | **No** — Stage 1 / separate |
| Validated KSI board amended | **Only after** Tier A + behavioural floors + Tier B + prefer-lower re-score |

---

## 2. Success criteria → observables

| Student success criterion | Observable | Pass signal | Fail signal |
|---|---|---|---|
| I understand why this is today’s priority | Trust L1 still bound (regression watch) | Tier B restates why/evidence | Trust speech regresses |
| I chose to do it | Commit affordance + KPI | Student describes conscious choice; commitment rate observable | “I just clicked Start” with no agency; or dark-pattern reports |
| I know what changed afterwards | Reflection fields | Student restates change + next | Magic coach / empty outcome |
| Honest not-today | Defer catalogue | Prefer honest defer over fake compliance | Shame / streak pressure |
| Plan feels continuous | Continuity copy + history | “One plan” theme | Isolated tip-of-day feeling |
| No cognitive overload | Tier B load codes | No increase vs EP-008.1B clutter baseline | Dual CTA / decision paralysis |
| K8 hold | Explainability perception | No opacity / overclaim regression | Coach re-narration / Twin theatre |

---

## 3. Tier A — Structural / automated (delivery EP)

### 3.1 Contract tests

| Test ID | Assertion |
|---|---|
| CF-A01 | Schema-complete Home exposes commitment confirm (`data-commitment="confirm"`) or combined Start Session commitment helper |
| CF-A02 | Refusal fixture → no commitment / defer controls |
| CF-A03 | Defer POST with catalogue code persists deferred state + student-safe label |
| CF-A04 | Forbidden shame/streak strings absent from defer/reflection templates |
| CF-A05 | Single primary Start Session CTA (DR-050) |
| CF-A06 | Reflection snapshot binds what_you_did / what_changed / why / next from authored or humble frames — no Twin/LLM invention tokens |
| CF-A07 | History narrative includes completed + deferred entries when present; cap respected |
| CF-A08 | Continuity line present on commit, defer, and reflection paths |
| CF-A09 | Commit/defer does not mutate readiness/mastery tables (claim-boundary test) |
| CF-A10 | Observational events emit fail-open; RecommendationService scoring inputs unchanged |
| CF-A11 | Trust T1–T11 bindings still present (regression) |
| CF-A12 | Terminology guard: no pipeline/warrant/Twin leakage in commitment chrome |

### 3.2 Commands (expected on delivery)

```bash
ruff check app/application/student_experience app/presentation/student tests/presentation/student tests/application/student_experience
pytest tests/presentation/student/ tests/application/student_experience/ -q
```

### 3.3 Tier A exit

All CF-A0* green + Implementation Plan DoD → **Structural Pass**.  
Structural Pass **does not** raise validated K2.

---

## 4. Behavioural observables (research)

| Metric | Floor for Strong-band *discussion* | Notes |
|---|---|---|
| Commitment rate | Directional baseline established on dogfood / Stage 0 | Not a marketing KPI |
| Completion rate among committed | Directional; prefer under-claim | Link via commitment id |
| Deferred rate | Non-zero healthy band acceptable | Zero may imply shame UX |
| Reflection viewed | Majority of completions in dogfood | |
| Revisit after defer | Optional | Continuity signal |

These are **E2/E3 instrumentation** until external cohort lifts them (P-003.5). They enable K2 Strong-band *scoring eligibility*; they do not alone clear G1.9.

---

## 5. Tier B — Perception (post-delivery)

### 5.1 Method

| Method | N guidance | Focus |
|---|---|---|
| Blind review commitment pack | Prefer SV personas sensitive to trust, agency, motivation (SV-008 / SV-010 / SV-014 class) | Choice, defer honesty, reflection clarity, load |
| Structured interviews / dogfood | ≥5 internal or Stage 1 overlap | “Did you choose tonight’s work?” “What changed after?” |
| Theme coding | — | Agency / shame / clutter / continuity / Twin theatre |

Use reviewer framework when running named SV reviewers.

### 5.2 Perception hypotheses

| ID | Hypothesis | Falsifier |
|---|---|---|
| H1 | Students experience conscious choice (“I chose to do it”) | Majority report passive click-through or coercion |
| H2 | Defer feels honest and safe | Students prefer lying / ignoring over defer; or report shame |
| H3 | Reflection clarifies what changed and what next | Students cannot restate change/next after completion |
| H4 | History reads as educational narrative | Students call it clutter / audit log / irrelevant |
| H5 | Cognitive load does not increase vs trust-only baseline | Dual-CTA / overwhelm themes dominate |
| H6 | K8 does not regress | Opacity / overclaim / Twin-learning themes appear |

### 5.3 Tier B exit

| Result | Board interpretation |
|---|---|
| H1–H3 supported; H4–H6 non-blocking | Eligible for prefer-lower K2 Strong-band discussion **if** behavioural floors present |
| Shame / load / Twin theatre dominate | Fix UX; do not claim K2 ≥ 75 |
| Trust regression | Rollback commitment chrome density; keep Trust Contract |

---

## 6. K2 / K7 / K8 scoring rules (claim discipline)

| Step | Rule |
|---|---|
| Baseline | K2 = **68**, K7 = **58**, K8 = **72**, KSI = **64** (EP-008.1B) |
| After Tier A only | **No** category change |
| After Tier B + behavioural observables | Product may propose K2 in **75–80** planning band if H1–H3 clear **and** commitment instrumentation live; apply prefer-lower |
| K2 ≥ 75 claim | Requires Tier B agency themes **plus** observational commitment evidence — not UI alone |
| K7 | Propose **+2 to +6** only if history/continuity themes support; prefer-lower |
| K8 | Target **hold ≥ 72**; any opacity/overclaim → no K2 inflation |
| Cognitive load | Soft gate — fail themes block K2 raise |
| Marketing | DR-036 freeze remains |

Weighted planning math: see [`EXPECTED_KSI_MOVEMENT.md`](EXPECTED_KSI_MOVEMENT.md).

---

## 7. Explainability & recommendation reviews

On **delivery** completion:

1. Complete `EXPLAINABILITY_REVIEW_CHECKLIST.md` (P-001.2) — expect Pass if reflection/history stay authored + humble.  
2. Complete `RECOMMENDATION_REVIEW_CHECKLIST.md` (P-001.3) — expect Pass for explainable acceptance / deferral; ranking unchanged.  

K2 claims require checklist Pass (or waiver) per GOVERNANCE §4.3.

---

## 8. Regression watch

| Risk | Watch |
|---|---|
| K8 regression | Twin-learning copy; Coach dual messaging |
| K2 trust regression | Commitment chrome crowding out why/evidence |
| K1 / DR-050 | Dual primary CTAs |
| K5 integrity | Shame deferrals / streaks |
| Privacy | Commitment reasons logged beyond preference claim |

---

## 9. Evidence package (paths to file on delivery / validation)

| Evidence | Path / ID |
|---|---|
| Contract test log | CI / local pytest |
| Dogfood checklist | UI_SPEC §13 signed |
| Behavioural metric snapshot | Research aggregate (internal) |
| Tier B notes | Successor validation folder |
| Explainability Review | Delivery EP folder |
| Recommendation Review | Delivery EP folder |
| K2 / K7 re-score | KSI board artefact — separate from estimate |

Evidence hierarchy mapping: Tier A = **E2**; persona Tier B = **E3**; external acceptance = **E4** (Stage 1 / EP-008.2 path).

---

## 10. Out of scope validation

- M1–M9 educational effectiveness / G1.9 (EP-007.3 / EP-008.2)  
- Ranking precision sample (IMP-11)  
- Personalisation ON (EP-009.x)  

---

**End of VALIDATION_PLAN**
