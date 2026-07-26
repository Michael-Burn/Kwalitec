# EP-008.1 — Engineering Design

**Programme:** EP-008.1 — Recommendation Trust  
**Date:** 2026-07-26  
**Status:** Design authority for successor implementation  
**Starting board:** Validated KSI **62** (K2 = **55**)  
**Primary lever:** K2 Recommendation usefulness  
**Secondary:** K8 Explainability (deepen Strong floor)

---

## 1. Problem statement

Runtime A already produces schema-complete recommendations (EP-003.1) and the canonical Home path already renders core MES Level-1 why + next and Level-2 evidence/confidence/review (EP-006.2). Validated perception cleared Coach opacity on schema-complete nights (EP-006.3), yet **K2 remains Partial at 55**.

Students still cannot treat the primary tip as a trustworthy professional priority because trust-critical speech is incomplete on the daily path:

| Student need (success criterion) | Runtime A field | Home today |
|---|---|---|
| Why this recommendation exists | `why_recommended` | Visible (L1) |
| Why it matters **now** | category / reason / readiness context | Weak / generic |
| What to do next | `suggested_next_action` | Visible (L1) |
| Expected improvement | `expected_benefit` | Mostly L2 only |
| How completion affects future tips | `review_point` + loop honesty | Buried in L2; outcome copy thin |
| Plan vs tip relationship (Q9) | `plan_coherence_label` | **Not on Home DTO/UI** |
| Alternatives / refusal (Q10) | `alternatives[]`, `honest_refusal` | **Not on Home/Coach** |

**Root cause:** RC-05 / REM-06 / IMP-01 — trust surfaces and inspectability, **not** ranking quality.

---

## 2. Design thesis

> Finish recommendation **trust presentation** on the sole-runtime daily path by projecting fields Runtime A already authors — plan coherence, alternatives, honest refusal, expected benefit at L1, readiness relationship, and completion-loop honesty — without changing educational reasoning.

Trust precedes acceptance. Acceptance instrumentation is **EP-008.3**. This programme makes tips *worth accepting*.

---

## 3. Non-negotiable constraints

| Constraint | Source |
|---|---|
| Do not change recommendation ranking or Decision Framework ladder | EP-003.1, REM-06, IMP-01 |
| Do not redesign `RecommendationService` educational core | User programme brief; Architecture Art. IV |
| Runtime A remains sole educational authority | DR-002; bridge docstrings |
| Presentation must not re-decide or re-rank | `recommendation_mapper.py`, `ExplanationService` |
| No LLM-authored educational truth | P-001.2 P9 |
| No second educational brain / Twin-as-authority | Architecture; Twin flags OFF |
| Advice must not silently fight Today’s Mission | P-001.2 P10; P-001.3 Q9 |
| Accept/dismiss HTTP + analytics PRD → EP-008.3 | IMP-02 sequencing |

---

## 4. System context (read-only authority map)

```
RecommendationService (+ recommendation_quality)
        │  schema-complete rows: why, evidence, confidence,
        │  benefit, next, review, plan_coherence*, honest_refusal*,
        │  alternatives (recs 2–5)
        ▼
RecommendationAdapter / recommendation_mapper  (pass-through)
        ▼
EducationalStateService → HomeService → ExplanationService
        ▼
HomeSnapshot / ExplanationSnapshot / (new) TrustSnapshot fields
        ▼
view_models.home_vm() → student/home.html + explanation_card
```

**Services reviewed; not modified by this design:**

| Service | Role in trust | EP-008.1 action |
|---|---|---|
| `RecommendationService` | Authoritative tip + MES | **Read-only** — no ranking/schema rewrite |
| `ReadinessService` | Readiness MES / drivers | **Read-only** — Home already attaches `readiness_explanation` (EP-006.4); trust UI *links* tip ↔ readiness |
| `PlanningService` | Mission / plan MES | **Read-only** — coherence label narrates relationship |
| Mission generation | Today’s Mission | **Read-only** — primary CTA remains Start Session (DR-050) |
| Unified journey / MES | Journey hero | Presentation may bind trust fields if journey is primary shell |
| Analytics | Decision journal exists server-side | **No new student accept UI** here |

---

## 5. Trust contract (student-visible)

### 5.1 Mandatory trust elements (daily path)

Every schema-complete primary recommendation on Student Home MUST present:

| ID | Element | Source field(s) | Level | Rule |
|---|---|---|---|---|
| **T1** | Recommendation title | `title` / mission-aligned label | L1 | One primary tip (DR-050) |
| **T2** | Why it exists | `why_recommended` | L1 | Already required (P-001.2); keep ≤40-word L1 budget for primary block |
| **T3** | Why it matters **now** | Timeliness line from authored `reason` / category context **or** readiness relationship sentence | L1 | Presentation composition only — no new engine score |
| **T4** | Expected improvement | `expected_benefit` | **L1** (promote from L2) | Short; full text may remain in disclosure if long |
| **T5** | Next action | `suggested_next_action` | L1 | One clear verb; CTA = Start Session when enabled |
| **T6** | Supporting evidence | `supporting_evidence` (≤4) | L2 | Existing `explanation_card` disclosure |
| **T7** | Confidence | `confidence_level` + `confidence_basis` | L2 | Speakable labels only |
| **T8** | Review / future loop | `review_point` | L2 + post-session echo | Answers “how completion affects future tips” |
| **T9** | Plan / mission relationship | `plan_coherence`, `plan_coherence_label` | L1 badge or one line | Q9 — label divergence; never hide conflict |
| **T10** | Alternatives | Bridge `alternatives[]` (≤2 on Home) | L2 section | Titles + one-line why; no re-ranking |
| **T11** | Honest refusal | `honest_refusal=True` path | L1 variant | Dedicated cold-start / thin-evidence UX |

### 5.2 Honest refusal variant

When `honest_refusal` is true:

- Hero title and copy must not invent a confident tip.  
- Show authored why + next toward evidence-building (usually Today’s Mission).  
- Confidence = “Cannot yet be estimated” (or equivalent authored label).  
- Hide fake alternatives; optional “What we need first” from evidence/next.  
- Do not show plan-coherence theatre that implies a ranked tip exists.

### 5.3 Readiness relationship

When `readiness_explanation` is present on Home:

- Keep readiness panel separate (EP-006.4).  
- Trust card may include **one** cross-link sentence if `expected_readiness_improvement` or readiness `expected_benefit` is available — presentation of existing numbers/labels only.  
- Never claim Exam Ready or guarantee score lifts.

### 5.4 Completion feedback (presentation-only)

Without EP-008.3 accept/dismiss:

| Moment | Trust behaviour |
|---|---|
| Before session | T5 next + Start Session CTA |
| Session / mission overview | Echo tip why + expected benefit (pass-through) |
| Session outcome / return Home | Surface authored `review_point` (or honest fallback: “Tonight’s practice updates what we suggest next”) — **no fabricated personalisation claims** |

`RecommendationService.record_decision` remains available for EP-008.3; this design does **not** add student HTTP accept/dismiss.

---

## 6. Data model changes (presentation layer)

### 6.1 Extend DTOs (additive, frozen dataclasses)

**`ExplanationSnapshot`** — add optional trust fields (defaults preserve back-compat):

| Field | Type | Notes |
|---|---|---|
| `plan_coherence` | `str` | Raw code if needed for tests |
| `plan_coherence_label` | `str` | Student-safe label |
| `honest_refusal` | `bool` | Default `False` |
| `timeliness_line` | `str` | Presentation-composed “why now” from authored inputs |
| `completion_loop_line` | `str` | Usually = `review_point`; may be short L1 echo |

**`HomeSnapshot`** — add:

| Field | Type | Notes |
|---|---|---|
| `recommendation_alternatives` | `tuple[RecommendationAlternativeSnapshot, ...]` | Max 2 on Home |
| `trust_state` | `str` | e.g. `complete` / `refusal` / `incomplete` |

**New `RecommendationAlternativeSnapshot`:**

| Field | Type |
|---|---|
| `title` | `str` |
| `why_recommended` | `str` |
| `expected_benefit` | `str` |
| `suggested_next_action` | `str` |

### 6.2 Mapping rules

| Rule | Detail |
|---|---|
| Source | `EducationalStateSnapshot.recommendation` / bridge projection — already carries MES pass-through + `alternatives` |
| Composition | `timeliness_line` may concatenate authored fragments; **must not invent evidence** |
| Empty | If field missing, omit UI block — never synthesise confidence or coherence |
| Alternatives | Cap at 2 on Home; full list may remain on Revision |
| Terminology | Existing educational terminology guard continues to strip internal enums |

### 6.3 Explicit non-changes

- No Alembic migrations.  
- No changes to `recommendation_quality.apply_quality_contract` ranking.  
- No new Twin / Adaptive authority.  
- No new analytics events for accept/dismiss (EP-008.3).

---

## 7. Presentation architecture

| Layer | Responsibility |
|---|---|
| Bridge mapper | Already passes MES keys — verify alternatives + coherence remain intact (contract test) |
| HomeService / ExplanationService | Map new DTO fields; prefer authored over synthesis |
| `view_models.home_vm()` | Expose trust VM: coherence badge, alternatives, refusal flag, L1 benefit, timeliness |
| Templates | Bind trust blocks; progressive disclosure for T6–T8, T10 |
| Coach panel | Structured trust summary (why / now / next / benefit) instead of single opaque paragraph when schema-complete |
| Mission | Show coherence line when advisory label differs from mission topic |
| Revision | Attach `explanation_card` (or compact trust row) per alternative |
| Unified journey | If journey hero is the sole-runtime shell, bind the same trust VM fields |

---

## 8. Traceability to K2

Every trust element maps to K2 (and supporting K8):

| Trust ID | K2 dimension (P-001.3) | KSI link |
|---|---|---|
| T2 Why exists | Explainability alignment / evidence-based | K2 + K8 |
| T3 Why now | Timeliness | K2 |
| T4 Expected benefit | Educational value / actionability | K2 |
| T5 Next | Actionability | K2 |
| T6–T7 Evidence + confidence | Evidence-based + honesty | K2 + K8 |
| T8 Completion loop | Trustworthy follow-through narrative | K2 |
| T9 Coherence | Q9 Plan coherence | K2 |
| T10 Alternatives | Decision quality / agency | K2 |
| T11 Refusal | Q10 Honest refusal | K2 + K8 |

**Out of scope for K2 claim in this programme:** acceptance rate, completion rate, effectiveness (need EP-008.3 + Stage 1).

---

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Over-claiming effectiveness in copy | Prefer authored MES; ban Exam Ready / guaranteed lifts |
| Cluttering L1 beyond 40-word budget | Promote benefit to short L1 line; keep evidence/alternatives in L2 |
| Dual messaging (Home vs Coach) | Same DTO; Coach composes from same fields |
| Implementing accept UI early | Explicit EP-008.3 boundary |
| Temptation to “fix” ranking | Conditional IMP-11 only after trust + sample defects |

---

## 10. Success definition (design)

Design is successful when a successor can implement presentation-only changes such that a serious exam candidate on Home can answer all five success questions using **authored Runtime A fields**, with T9–T11 no longer missing.

Validated K2 movement requires the Validation Plan (Tier B + prefer-lower) — not this document alone.

---

## References

- `../p004_1_ksi_gap_analysis/HIGH_LEVERAGE_IMPROVEMENTS.md` (IMP-01)  
- `../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md`  
- `../p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md`  
- `../ep006_2_mes_delivery_implementation/MES_DELIVERY_IMPLEMENTATION.md`  
- `app/services/recommendation_service.py`  
- `app/infrastructure/adapters/educational_runtime_bridge/recommendation_mapper.py`  
- `app/application/student_experience/dto/explanation_snapshot.py`  
- `app/templates/student/home.html`  

---

**End of ENGINEERING_DESIGN**
