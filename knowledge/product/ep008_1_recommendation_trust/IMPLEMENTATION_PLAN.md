# EP-008.1 — Implementation Plan

**Programme:** EP-008.1 — Recommendation Trust  
**Date:** 2026-07-26  
**Status:** Delivery plan for successor implementation milestone  
**Constraint:** Presentation / DTO / view-model / template only — no ranking changes  
**Estimated effort:** Medium (1 focused delivery programme after this design)

---

## 1. Goal

Ship the Trust Contract ([`ENGINEERING_DESIGN.md`](ENGINEERING_DESIGN.md) §5) on the sole-runtime Student Home / Coach path (and Mission / Revision parity), so K2 inspectability gaps T9–T11 and L1 benefit / timeliness / completion-loop speech are closed.

---

## 2. Phases

### Phase 0 — Contract lock (this programme)

| # | Task | Done when |
|---|---|---|
| 0.1 | Publish engineering design + UI spec + validation plan | Artefacts in this folder |
| 0.2 | Confirm non-goals with Product (no accept UI; no ranking) | Explicit in README / this plan |
| 0.3 | Baseline field inventory vs bridge projection | Design §1 / §6 |

**Exit:** Design Complete (this programme).

---

### Phase 1 — DTO & mapping (successor)

| # | Task | Primary paths | Notes |
|---|---|---|---|
| 1.1 | Add `RecommendationAlternativeSnapshot` | `app/application/student_experience/dto/` | Frozen dataclass |
| 1.2 | Extend `ExplanationSnapshot` with trust fields | `explanation_snapshot.py` | Defaults preserve callers |
| 1.3 | Extend `HomeSnapshot` (`alternatives`, `trust_state`) | `home_snapshot.py` | |
| 1.4 | Map from educational state / explanation service | `explanation_service.py`, `_snapshots.py`, `home_service.py` | Prefer authored MES |
| 1.5 | Compose `timeliness_line` from authored fragments only | domain or presentation helper | No new evidence invention |
| 1.6 | Contract unit tests for mapping | `tests/application/student_experience/` | Refusal + coherence + alts |

**DoD:** Schema-complete fixture yields complete trust DTO; refusal fixture yields `trust_state=refusal` without fake alternatives.

---

### Phase 2 — View models & templates (successor)

| # | Task | Primary paths | Notes |
|---|---|---|---|
| 2.1 | Extend `HomePageViewModel` / explanation VM | `app/presentation/student/view_models.py` | Coherence, alts, refusal, L1 benefit |
| 2.2 | Restructure Coach insight composition | `_compose_coach_insight` | Structured why/now/next/benefit from same fields |
| 2.3 | Home hero + trust blocks | `app/templates/student/home.html` | Per [`UI_SPECIFICATION.md`](UI_SPECIFICATION.md) |
| 2.4 | Extend `explanation_card` or add `recommendation_trust_card` | `app/templates/student/components/` | Coherence + alternatives + refusal |
| 2.5 | Mission coherence line | `app/templates/mission/index.html` | When label diverges |
| 2.6 | Revision alternatives explanations | `app/templates/student/revision.html` | Compact explanation per option |
| 2.7 | Session outcome / return-home review echo | session outcome templates / journey outcome | Pass-through `review_point` |
| 2.8 | Unified journey hero bind (if primary shell) | `app/application/unified_journey/` + templates | Same trust VM |

**DoD:** Manual dogfood checklist in UI spec §8 Pass; no CSS theatre that hides missing fields.

---

### Phase 3 — Contract & regression tests (successor)

| # | Task | Primary paths |
|---|---|---|
| 3.1 | Extend MES delivery contract tests | `tests/presentation/student/test_mes_delivery_contract.py` (or successor) |
| 3.2 | Add trust-specific binding tests (coherence, refusal, alts, L1 benefit) | new test module under `tests/presentation/student/` |
| 3.3 | Regression: DR-050 single primary CTA | assert one Start Session CTA |
| 3.4 | Regression: terminology guard still strips internals | existing guard tests |
| 3.5 | Ruff + pytest green on touched packages | CI |

**DoD:** All Phase 3 tests green; no changes under `app/services/recommendation_service.py` / `recommendation_quality.py` unless defect hotfix approved separately.

---

### Phase 4 — Perception validation handoff

| # | Task | Owner |
|---|---|---|
| 4.1 | Run [`VALIDATION_PLAN.md`](VALIDATION_PLAN.md) Tier A (automated) | Eng |
| 4.2 | Schedule Tier B blind / interview pack (trust themes) | Product |
| 4.3 | Prefer-lower K2 re-score only after Tier B | Product measurement |
| 4.4 | Open EP-008.3 for acceptance instrumentation | Product Board |

**Exit:** Implementation Complete + validation package filed (may be a separate EP id if Board prefers).

---

## 3. Recommended file touch list (successor)

### Expected modify

- `app/application/student_experience/dto/explanation_snapshot.py`  
- `app/application/student_experience/dto/home_snapshot.py`  
- `app/application/student_experience/dto/__init__.py`  
- `app/application/student_experience/explanation_service.py`  
- `app/application/student_experience/_snapshots.py`  
- `app/application/student_experience/home_service.py`  
- `app/domain/student_experience/recommendation_explanation.py` (if domain model mirrors DTO)  
- `app/presentation/student/view_models.py`  
- `app/templates/student/home.html`  
- `app/templates/student/components/explanation_card.html` (or new component)  
- `app/templates/student/revision.html`  
- `app/templates/mission/index.html`  
- Session / journey outcome templates as needed  
- Tests under `tests/application/student_experience/` and `tests/presentation/student/`

### Verify only (no behaviour change unless pass-through bug)

- `app/infrastructure/adapters/educational_runtime_bridge/recommendation_mapper.py`  
- `app/infrastructure/adapters/educational_runtime_bridge/recommendation_adapter.py`  

### Do not modify (unless separate defect programme)

- `app/services/recommendation_service.py` ranking / Decision Framework  
- `app/services/recommendation_quality.py` ladder logic  
- `app/services/readiness_service.py` weights  
- `app/services/planning_service.py` optimisation  
- Analytics accept/dismiss routes (EP-008.3)

---

## 4. Work sequencing (suggested PR slices)

1. **PR-A:** DTO + mapping + unit tests (no template change)  
2. **PR-B:** Home/Coach UI + contract tests  
3. **PR-C:** Mission + Revision + outcome echo  
4. **PR-D:** Dogfood fixes + documentation note in programme folder  

Keep PRs presentation-scoped; avoid bundling with personalisation flag work (EP-009.x).

---

## 5. Definition of done (implementation)

- [ ] T1–T11 trust elements bound per Engineering Design on sole-runtime Home for schema-complete tips  
- [ ] Honest refusal variant ships without fake confidence  
- [ ] Alternatives ≤2 on Home; no re-ranking  
- [ ] Expected benefit visible at L1 when authored  
- [ ] Review point / completion-loop echo visible without inventing personalisation  
- [ ] Plan coherence label visible when authored  
- [ ] Coach uses same authored fields (no opaque re-narration)  
- [ ] Contract tests cover coherence, refusal, alternatives, L1 benefit  
- [ ] Explainability + Recommendation Review checklists Pass for the delivery EP  
- [ ] No ranking / LLM / accept-UI scope creep  
- [ ] Student Impact Assessment exit sections updated on delivery completion  

---

## 6. Explicit non-goals

| Non-goal | Owner instead |
|---|---|
| Accept / defer / dismiss HTTP + KPI | EP-008.3 / IMP-02 |
| Stage 1 external cohort | EP-008.2 |
| Cold-start sparse-state programme beyond refusal UX | EP-008.4 |
| Personalisation factor provenance ON by default | EP-009.x |
| New recommendation algorithm / precision sample | Conditional IMP-11 |
| Dual-home Dashboard as primary | Closed on W-PROD (parity optional only) |

---

## 7. STOP checks

Stop implementation and escalate if asked to:

1. Change ranking to “make trust scores look better”  
2. Add LLM-authored why/evidence/confidence  
3. Market effectiveness lifts without Stage 1 evidence  
4. Flip personalisation flags as part of trust UI  
5. Soft-amend Educational or Architecture Constitutions  

---

**End of IMPLEMENTATION_PLAN**
