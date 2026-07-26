# EP-008.1 — Validation Plan

**Programme:** EP-008.1 — Recommendation Trust  
**Date:** 2026-07-26  
**Status:** Validation contract for design + successor delivery  
**Primary claim target:** K2 Recommendation usefulness (inspectability / trust)  
**Secondary:** K8 residual deepen  
**Rule:** Prefer-lower; estimated ΔKSI ≠ validated progress (DR-026)

---

## 1. What this plan proves

| Claim | In scope? |
|---|---|
| Trust fields authored by Runtime A reach Home/Coach/Mission/Revision UI | **Yes** |
| Students can answer the five success questions on schema-complete nights | **Yes** (Tier B) |
| Honest refusal is perceivable and non-deceptive | **Yes** |
| Ranking / precision improved | **No** |
| Acceptance / completion rates moved | **No** — EP-008.3 + Stage 1 |
| Validated KSI board amended | **Only after** Tier B + re-score programme |

---

## 2. Success criteria → observables

| Student success criterion | Observable | Pass signal | Fail signal |
|---|---|---|---|
| Why this recommendation exists | L1 `why_recommended` bound | Visible without opening disclosure | Missing / internal jargon |
| Why it matters now | L1 `timeliness` bound | Student can restate urgency in own words (Tier B) | Generic / absent |
| What to do next | L1 next + CTA | One clear action | Competing CTAs / vague next |
| Expected improvement | L1 benefit | Student names expected learning benefit | Benefit only buried or marketing |
| How completion affects future tips | Review / outcome echo | Student understands tip can change after practice | “Magic coach” / no loop |
| Coherence (Q9) | Coherence label | Divergence labelled as advice | Silent conflict with mission |
| Alternatives / refusal (Q10) | Alts or refusal UX | Agency or honest empty | Fake tip with false confidence |

---

## 3. Tier A — Structural / automated (delivery EP)

### 3.1 Contract tests

| Test ID | Assertion |
|---|---|
| TR-A01 | Schema-complete fixture → Home HTML contains `data-mes-field` for why, next, expected_benefit (L1), plan_coherence, review (L2) |
| TR-A02 | Alternatives ≤2 rendered with titles when projection supplies them |
| TR-A03 | `honest_refusal` fixture → no alternatives block; confidence cannot-yet / authored refusal title |
| TR-A04 | Coach insight strings ⊆ authored Home fields (no novel sentences beyond composition glue) |
| TR-A05 | Single Start Session primary CTA (DR-050) |
| TR-A06 | Terminology guard: no Twin/pipeline/warrant tokens in rendered trust blocks |
| TR-A07 | Mapper/DTO round-trip: `plan_coherence_label`, `honest_refusal`, alternatives preserved |
| TR-A08 | Incomplete MES → omit blocks; no invented confidence |

### 3.2 Commands (expected on delivery)

```bash
ruff check app/application/student_experience app/presentation/student tests/presentation/student tests/application/student_experience
pytest tests/presentation/student/ tests/application/student_experience/ -q
```

(Exact paths may match successor test modules.)

### 3.3 Tier A exit

All TR-A0* green + Implementation Plan DoD checklist complete → **Structural Pass**.  
Structural Pass **does not** raise validated K2.

---

## 4. Tier B — Perception (post-delivery)

### 4.1 Method

| Method | N guidance | Focus |
|---|---|---|
| Blind review trust pack | Prefer existing SV personas sensitive to Coach/recommendation trust (e.g. SV-014 class) | Five success questions; coherence; refusal |
| Short structured interviews / dogfood | ≥5 internal or Stage 1 overlap if available | “Would you follow this tip tonight? Why/why not?” |
| Theme coding | — | Trust gained / still opaque / overclaim / clutter |

Use reviewer framework when running named SV reviewers (`knowledge/product/ep004_private_beta/reviewer_framework/`).

### 4.2 Perception hypotheses

| ID | Hypothesis | Falsifier |
|---|---|---|
| H1 | Schema-complete Home clears “I don’t know why I should follow this” | ≥50% still cannot state why/evidence |
| H2 | Why-now + benefit raise stated willingness to start session | No change vs pre-trust baseline anecdotes |
| H3 | Refusal state increases honesty trust vs fake tip | Students prefer fabricated confident tip |
| H4 | Alternatives increase agency without decision paralysis | Students report overwhelm / ignore primary CTA |

### 4.3 Tier B exit

| Result | Board interpretation |
|---|---|
| Themes support H1–H3; H4 non-blocking | Eligible for prefer-lower K2 lift discussion |
| Opacity / overclaim themes dominate | Fix copy/bindings; do not claim K2 |
| Clutter dominates | Tighten L1; move benefit or alts deeper |

---

## 5. K2 scoring rules (claim discipline)

| Step | Rule |
|---|---|
| Baseline | K2 = **55** (validated W-PROD / DR-051 lineage) |
| After Tier A only | **No** category change |
| After Tier B | Product measurement may propose K2 in **67–73** planning band if themes clear; apply prefer-lower |
| Strong-band (≥75) | Requires acceptance KPI (EP-008.3) and/or Stage 1 uptake — **not** claimable from UI alone |
| Marketing | DR-036 freeze remains until effectiveness evidence |

Weighted planning math: see [`EXPECTED_KSI_MOVEMENT.md`](EXPECTED_KSI_MOVEMENT.md).

---

## 6. Explainability & recommendation reviews

On **delivery** completion (not this design-only programme):

1. Complete `EXPLAINABILITY_REVIEW_CHECKLIST.md` (P-001.2) — expect Pass if T1–T11 bound without LLM invention.  
2. Complete `RECOMMENDATION_REVIEW_CHECKLIST.md` (P-001.3) — expect Pass for presentation/inspectability; Q9/Q10 surfaced; ranking unchanged.  

Design-time reviews in this folder document checklist posture against the contract.

---

## 7. Regression watch

| Risk | Watch |
|---|---|
| K8 regression | Cold-start opacity returns; Coach re-narration |
| K1 regression | Dual CTA / mission fight |
| Honesty incident | Overclaim benefit / Exam Ready |
| Performance | Irrelevant — presentation only |

---

## 8. Evidence package (paths to file on delivery)

| Evidence | Path / ID |
|---|---|
| Contract test log | CI / local pytest output |
| Dogfood checklist | UI_SPEC §12 signed |
| Tier B notes | `knowledge/product/…` successor validation folder |
| Explainability Review | Delivery EP folder |
| Recommendation Review | Delivery EP folder |
| K2 re-score (if any) | KSI board artefact — separate from estimate |

---

## 9. Out of scope validation

- M1–M9 educational effectiveness (EP-008.2 / EP-007.3)  
- Acceptance rate dashboards (EP-008.3)  
- Recommendation precision sample (IMP-11 conditional)  

---

**End of VALIDATION_PLAN**
