# EP-008.3 — Implementation Plan

**Programme:** EP-008.3 — Recommendation Commitment & Follow-through  
**Date:** 2026-07-26  
**Status:** Delivery plan for successor implementation milestone  
**Constraint:** Commitment / presentation / preference-journal / observational metrics only — **no** Runtime A ranking or educational-reasoning changes  
**Estimated effort:** Medium–Large (1 focused delivery programme after this design)  
**Upstream:** EP-008.1 Trust Contract permanent; EP-008.1B K2 **68**  

---

## 1. Goal

Ship the Commitment Contract ([`ENGINEERING_DESIGN.md`](ENGINEERING_DESIGN.md) §5–§6) on the sole-runtime Student Home / Mission / session-outcome / History path so students can consciously commit, honestly defer, see completion reflection, and read a lightweight recommendation narrative — enabling observational follow-through metrics and Strong-band K2 validation eligibility.

---

## 2. Phases

### Phase 0 — Contract lock (this programme)

| # | Task | Done when |
|---|---|---|
| 0.1 | Publish engineering design + UI + validation + KSI + SIA | Artefacts in this folder |
| 0.2 | Confirm non-goals (no ranking, no LLM, no streaks, no Runtime A edits) | Explicit in README / this plan |
| 0.3 | Confirm Decision Journal / learning-feedback call boundaries | Design §4 / §7 |
| 0.4 | Privacy / PRD checklist for observational metrics (IMP-02) | Linked in Validation Plan |

**Exit:** Design Complete (this programme).

---

### Phase 1 — Commitment domain & persistence (successor)

| # | Task | Primary paths | Notes |
|---|---|---|---|
| 1.1 | Add commitment DTOs | `app/application/student_experience/dto/` | Frozen dataclasses per Design §7 |
| 1.2 | Add `RecommendationCommitmentService` | `app/application/student_experience/` | State transitions; no ranking |
| 1.3 | Persist commitments (Option A preferred) | `app/models/` + Alembic | Preference/intent claim only |
| 1.4 | Wire `record_decision` on commit/complete | Call existing API | **Do not** edit ranking methods |
| 1.5 | Defer catalogue + labels | domain helper | Fixed codes; no shame copy |
| 1.6 | Compose reflection snapshot from authored MES + session facts | presentation helper | No LLM; no Twin invention |
| 1.7 | Unit tests for state machine + claim boundary | `tests/application/student_experience/` | Accept ≠ mastery |

**DoD:** Commit / defer / complete / reflect transitions work in unit tests; refusal nights skip commit CTA; no writes to readiness/mastery.

---

### Phase 2 — HTTP + Home / Mission binding (successor)

| # | Task | Primary paths | Notes |
|---|---|---|---|
| 2.1 | CSRF-safe POST routes (commit, defer, reflection ack) | student / dashboard blueprint | `@login_required`; ownership scoped |
| 2.2 | Extend HomeSnapshot / VM with commitment | `home_snapshot.py`, `view_models.py` | |
| 2.3 | Home UI — commit + defer per [`UI_SPECIFICATION.md`](UI_SPECIFICATION.md) | `home.html` | Preserve DR-050 |
| 2.4 | Mission / unified journey committed chrome | mission / journey templates | Continuity line |
| 2.5 | Coach remains trust speech only | No second commitment CTA | Avoid dual primary |
| 2.6 | Honest refusal: hide commit; keep restorative Start Session | trust_state=refusal | |

**DoD:** Dogfood checklist UI § dogfood Pass; single primary educational CTA.

---

### Phase 3 — Completion reflection + history (successor)

| # | Task | Primary paths | Notes |
|---|---|---|---|
| 3.1 | Session outcome / Home reflection block | outcome templates / home reflection branch | Design §6.4 |
| 3.2 | Extend HistorySnapshot with narrative entries | `history_snapshot.py`, `history_service.py` | Cap ≤10 |
| 3.3 | History template narrative section | history / journey history UI | Educational, not audit |
| 3.4 | Plan continuity copy helper | shared presentation | Same strings everywhere |

**DoD:** Completed session shows reflection elements; History shows completed + deferred narrative.

---

### Phase 4 — Observational metrics + contract tests (successor)

| # | Task | Primary paths |
|---|---|---|
| 4.1 | Emit research events (commit / defer / complete-link / reflection_viewed) | learning_feedback fail-open or analytics registry under approved PRD |
| 4.2 | Operator-safe aggregate helpers (optional) | founder / analytics research — **no** student streaks |
| 4.3 | Contract tests CF-A0* | `tests/presentation/student/`, application tests |
| 4.4 | Regression: Trust T1–T11 still bound; DR-050; terminology guard | existing + new |
| 4.5 | Ruff + pytest green on touched packages | CI |

**DoD:** All CF-A0* green; metrics never imported into RecommendationService scoring.

---

### Phase 5 — Validation handoff

| # | Task | Owner |
|---|---|---|
| 5.1 | Run [`VALIDATION_PLAN.md`](VALIDATION_PLAN.md) Tier A | Eng |
| 5.2 | Collect observational KPI baselines (dogfood / Stage 0) | Product |
| 5.3 | Tier B commitment / follow-through perception pack | Product |
| 5.4 | Prefer-lower K2 re-score only after Tier B + KPI floors | Product measurement |
| 5.5 | File Explainability + Recommendation Reviews on delivery | Eng / Product |

**Exit:** Implementation Complete + validation package filed (may be EP-008.3A / EP-008.3B if Board prefers).

---

## 3. Recommended file touch list (successor)

### Expected create

- `app/application/student_experience/recommendation_commitment.py` (or equivalent)  
- `app/application/student_experience/dto/recommendation_commitment_snapshot.py`  
- `app/application/student_experience/dto/commitment_reflection_snapshot.py`  
- `app/application/student_experience/dto/recommendation_narrative_entry_snapshot.py`  
- Optional: `app/models/recommendation_commitment.py`  
- Alembic revision (if Option A)  
- Tests under `tests/application/student_experience/` and `tests/presentation/student/`  

### Expected modify

- `app/application/student_experience/dto/home_snapshot.py`  
- `app/application/student_experience/dto/history_snapshot.py`  
- `app/application/student_experience/home_service.py`  
- `app/application/student_experience/history_service.py`  
- `app/application/student_experience/_snapshots.py`  
- `app/presentation/student/view_models.py`  
- `app/templates/student/home.html` (+ components as needed)  
- History / session outcome / mission templates  
- Blueprint routes for commit/defer/ack (dashboard or student)  
- Learning-feedback emitter hooks (fail-open) if used  

### Call only — do not modify educational cores

- `app/services/recommendation_service.py` — **call** `record_decision` / read tip fields; **do not** change ranking, Decision Framework, or quality ladder  
- `app/services/planning_service.py`  
- `app/services/readiness_service.py`  
- `app/services/recommendation_quality.py`  

### Verify only

- `app/application/student_experience/recommendation_trust.py` — Trust Contract remains intact  
- Bridge recommendation mapper — pass-through unchanged  

---

## 4. Work sequencing (suggested PR slices)

1. **PR-A:** Model + service + unit tests (no UI)  
2. **PR-B:** Home commit/defer HTTP + templates + DR-050 tests  
3. **PR-C:** Reflection + History narrative  
4. **PR-D:** Observational metrics + contract suite + dogfood fixes  

Keep PRs out of Twin / personalisation flag flips / ranking experiments.

---

## 5. Definition of done (implementation)

- [ ] Commitment CTA “I’m doing this next.” on schema-complete Home (not on refusal)  
- [ ] Deferred commitment with catalogue reasons; no punishment copy  
- [ ] Session completion surfaces reflection elements (authored + humble frames)  
- [ ] Recommendation history narrative (completed + deferred) on History  
- [ ] Plan continuity line present on commit, defer, and reflection  
- [ ] Observational metrics emitted (research-only); not fed to ranking  
- [ ] Trust Contract T1–T11 unchanged / still bound  
- [ ] Single primary educational CTA (DR-050)  
- [ ] Accept/commit ≠ mastery (tests + EIP-002 claim boundary)  
- [ ] Explainability + Recommendation Review checklists Pass for delivery EP  
- [ ] No Runtime A / RecommendationService ranking / Planning / Readiness reasoning changes  
- [ ] Student Impact Assessment exit sections updated on delivery  

---

## 6. Explicit non-goals

| Non-goal | Owner instead |
|---|---|
| Ranking / Decision Framework changes | Conditional IMP-11 only |
| LLM coach / chat | Never-build / constitutional STOP |
| Learning Twin as authority | Architecture |
| Streaks / gamification / shame nudges | Rejected |
| Effectiveness marketing / DR-036 lift | EP-008.2 / Stage 1 + approved evidence |
| Cold-start sparse-state programme | EP-008.4 (if commissioned) |
| Personalisation flags ON | EP-009.x |
| Replacing Trust Contract | EP-008.1 permanent |

---

## 7. STOP checks

Stop implementation and escalate if asked to:

1. Change ranking to raise commitment rates  
2. Add LLM-authored reflection or “what we learned about you”  
3. Introduce streaks, points, or shame deferrals  
4. Treat commit/defer as mastery or readiness evidence  
5. Soft-amend Educational or Architecture Constitutions  
6. Claim K2 ≥ 75 or effectiveness from Tier A alone  

---

**End of IMPLEMENTATION_PLAN**
