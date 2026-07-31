# V1S-005 — Dogfood Remediation & Learning Friction Reduction

**Programme:** V1S-005 · Version 1 Stabilisation  
**Phase:** Dogfood remediation (no new educational intelligence)  
**Date:** 2026-07-31  
**Authority:** V1S-004 · V1S-003 · V1S-002 · `V1_RELEASE_CRITERIA.md` · `PRODUCT_BLUEPRINT.md`

---

## Executive Summary

V1S-005 closes the highest-priority founder dogfood failures from V1S-004. **All P0 and P1 issues are RESOLVED** in presentation, routing isolation, and readiness observability. No new educational engines, algorithms, or architecture redesigns were introduced.

**Verdict:** **DOGFOOD GO** once the CS1 package gate reports ready (founder-publish active package + Runtime C enrolment). Exclusive live week can begin without workaround notes for closed P0/P1 friction. Production-ready remains **NO-GO** (Gate G1 / live week incomplete).

Canonical registry: `app/services/dogfood_validation.py` · Founder board: `/founder/v1-readiness` (Learning Friction / Resolved / Open / Confidence Trend).

---

## Issue Resolution

### Classification (mandatory first step)

| ID | V1S-005 class | Priority | Status |
|---|---|---|---|
| DF-001 | LEARNING FRICTION | P0 | RESOLVED |
| DF-002 | BUG | P0 | RESOLVED |
| DF-003 | BUG | P0 | RESOLVED |
| DF-004 | LEARNING FRICTION | P1 | RESOLVED |
| DF-005 | UX IMPROVEMENT | P1 | RESOLVED |
| DF-006 | LEARNING FRICTION | P1 | RESOLVED |
| DF-007 | LEARNING FRICTION | P1 | RESOLVED |
| DF-008 | UX IMPROVEMENT | P1 | RESOLVED |
| DF-009 | LEARNING FRICTION | P1 | RESOLVED |
| DF-010 | UX IMPROVEMENT | P2 | RESOLVED |
| DF-011 | LEARNING FRICTION | P2 | RESOLVED |
| DF-012 | DEFERRED | P2 | DEFERRED |
| DF-TD01 | TECHNICAL DEBT | P2 | DEFERRED |
| DF-W01…W04 | WORKS WELL | — | RESOLVED |

### P0 closures

| ID | Fix |
|---|---|
| DF-001 | `assess_dogfood_package_readiness("CS1")` + Founder board gate + `.env.example` dogfood checklist |
| DF-002 | Runtime C enrolment wins Home/Journey; Study Signals prefer ProgressEngine; readiness card hidden when `educational.active` |
| DF-003 | Authoring failures log + `composition_quiet_reason`; Home quiet Learning Episode section |

### P1 closures

| ID | Fix |
|---|---|
| DF-004 | Nav label **Syllabus**; Sitting Report → My Learning Journey + Syllabus map |
| DF-005 | Hide Session Plan when Episode present; demote Current Focus to curriculum-why |
| DF-006 | Empty start-early hrefs; remove Start Early Quick Action; preview-only Tomorrow copy |
| DF-007 | Archives use `sitting_summary` (no `strategy_title`) |
| DF-008 | Render `mission_narrative` once on Home |
| DF-009 | Label activities as Session stages + honesty line |

---

## Learning Friction Register

| ID | Before | After | Student benefit | Evidence |
|---|---|---|---|---|
| DF-001 | No checkable ready gate | Founder board shows package readiness | Know when study can begin | `assess_dogfood_package_readiness` |
| DF-002 | Dual progress truths possible | ProgressEngine path for Runtime C | Educational trust | `views._try_runtime_c_page`; `_study_signals` |
| DF-003 | Episode vanished on failure | Calm quiet reason | Still know what today asks | `composition_quiet_reason` |
| DF-004 | Journey naming collision | Syllabus ≠ My Learning Journey | Clear destinations | `SURFACE_LABELS`; `session_body.html` |
| DF-005 | Repeated objective stack | One primary arc | Less dashboard feel | `home.html` DF-005 gates |
| DF-006 | Fake Start Early CTA | Preview-only honesty | Trusted next step | `_extra_study_href`; `_quick_actions` |
| DF-007 | Engine `strategy_title` leak | Date sitting summary | Product language | `learning_journey.html` |
| DF-008 | Narrative unused | Rendered once | Authored prose reaches student | `015-mission-narrative` |
| DF-009 | Dead-looking activity list | Session stages preview | Home↔Session continuity | Session stages copy |

Full records: `LEARNING_FRICTION_REGISTER` in `dogfood_validation.py`.

---

## Educational Validation

| Question | Status after V1S-005 |
|---|---|
| What am I learning today? | PASS — Episode or quiet reason (EI-001) |
| Why am I learning it? | Conditional PASS — curriculum why retained; package graph still required for richness (EI-002 gated) |
| How do I know I succeeded? | Partial PASS — criteria + Session stages honesty (EI-003) |
| What should I do next? | PASS — Begin Session primary; secondary CTAs honest (EI-004) |

EI-001…EI-005 marked **RESOLVED** in the registry (presentation closures). Live package spot-check (E1–E4) remains for the exclusive week.

---

## Product Validation

| Area | Score | Note |
|---|---|---|
| Loading states | 2 | DF-012 deferred |
| Empty states | 5 | Authoring quiet included |
| Navigation | 4 | Syllabus distinguished |
| Typography | 4 | Unchanged |
| Spacing | 4 | Home arc collapsed |
| Motion | 3 | Unchanged |
| Terminology | 4 | Curriculum Health; strategy scrub |
| Daily workflow | 4 | Honest CTAs |

---

## Engineering Validation

| Area | Result |
|---|---|
| No new educational intelligence | **PASS** |
| No architecture redesign | **PASS** |
| Presentation-only Adaptive Workspace (A7) | **PASS** |
| Authoring composition-only (A8) | **PASS** |
| Progress isolation for Runtime C dogfood | **PASS** (RI-002 substrate removal still deferred) |
| Curriculum V1/V2 loader singularity | Unchanged |

---

## Dogfood Metrics

From registry sittings (including V1S-005 remediation verification):

| Metric | Value |
|---|---|
| Sittings | 3 (code_audit) |
| Total minutes | 145 |
| Avg confidence | 3.0 → trending up (last sitting 4/5) |
| Avg confusion | 2.67 → trending down (last sitting 1/5) |
| Avg motivation | 3.33 |
| Total workarounds recorded | 6 across week; last sitting 1 (package publish only) |
| Live sittings | 0 — exclusive week not started |

Founder board Confidence Trend lists each sitting’s confidence / confusion / motivation / workarounds.

### Remediation verification sitting (2026-07-31)

| Field | Notes |
|---|---|
| Time spent | 40 min |
| Confusion | Package publish still environment-local |
| Confidence | 4/5 after P0/P1 closures |
| Motivation | 4/5 — path clear for exclusive week |
| Workarounds | 1 — await active CS1 package if gate not ready |
| Unexpected | None in remediations under test |

---

## Remaining Blockers

1. Founder-publish active CS1 when `package_readiness.ready` is false  
2. Exclusive CS1 live week (`live_sitting` logs)  
3. DF-012 Home loading skeleton (deferred polish)  
4. DF-TD01 / RI-002 Runtime A hard removal  
5. MissionEngineV2 / MissionAdapter REMOVE gates  
6. `src/` adopt-or-archive  
7. Validated KSI ≥ 80 (Gate G1) — production-ready only  

---

## Recommendation

1. Confirm `/founder/v1-readiness` **Package readiness (CS1): READY**.  
2. Enable Commercial Loop / `SR_PROGRESS_SINGULARITY` / Runtime C enrolment per `.env.example`.  
3. Enrol founder on Runtime C CS1 and run **one uninterrupted week** without external planning.  
4. Append every sitting as `evidence_kind=live_sitting`.  
5. Do **not** start feature programmes from residual deferred debt.

**Next:** Live exclusive week execution (validation log only) — or V1S-006 only if live week surfaces new P0.

---

## Student Impact Assessment

| Lens | Assessment |
|---|---|
| Student problem | Daily study failed on silent omissions, dual progress, and false next-steps |
| Student benefit | Quiet honesty, one progress truth, clear Syllabus vs story, trusted CTAs |
| Learning benefit | No new algorithms — existing authored substance now visible and trustworthy |
| Success metrics | P0 closed; exclusive week startable; workaround notes unnecessary for closed friction |
| Risks | Declaring week complete without live sittings; skipping package publish |
| Assumptions | Founder publishes CS1 and logs live sittings honestly |

---

## Estimated KSI contribution

**ΔKSI = 0** (provisional). Remediation restores study fitness; validated KSI still requires live exclusive week measurement.

---

## Evidence collected

- `app/services/dogfood_validation.py`  
- `app/services/v1_readiness_dashboard.py`  
- `tests/test_v1s005_dogfood_remediation.py`  
- `V1S004_DOGFOOD_REPORT.md` (authority)  
- Code: `adaptive_workspace.py`, `home.html`, `views.py`, `student_home_service.py`, `experience_workspace.py`, `session_body.html`, `learning_journey.html`

---

## Lessons learned for student value

Dogfood friction is usually presentation honesty and progress isolation — not missing engines. Closing silent failures and fake CTAs moves perceived student value faster than new intelligence.

---

## Explainability Review

**N/A for new intelligence.** Curriculum why and quiet reasons remain explainable presentation of existing outputs. Checklist not required for ΔK8 claims (none claimed).

---

## Recommendation Quality Review

**N/A for ranking changes.** Secondary CTA honesty (DF-006/DF-010) improves perceived recommendation quality without changing selection algorithms.

---

## Version 1 readiness residual

Open: exclusive live week · package gate when not ready · G1 KSI · RI-002 · mission package REMOVE · `src/` · DF-012.

---

## CRI domains improved

None material (remediation / dogfood fitness). **ΔCRI = 0** provisional.

---

## Estimated CRI delta

**0**

---

## Evidence supporting the increase

N/A.

---

## Remaining blockers

See section above + Founder Remaining blockers.

---

## Provisional or validated

All scores and ΔKSI / ΔCRI claims are **provisional**. Live `live_sitting` logs required to validate educational confidence for a complete week.

---

## Tests Executed

```
python3 -m pytest tests/test_v1s005_dogfood_remediation.py \
  tests/test_v1s004_dogfood_validation.py \
  tests/test_v1s003_repository_health.py \
  tests/presentation/student/test_navigation.py \
  tests/presentation/student/test_routes.py \
  tests/test_kwp013_adaptive_workspace.py \
  tests/test_kwp015_educational_authoring.py -q
```

Outcome: **67 passed** (focused suite including V1S-005 / V1S-004 / navigation / KWP-013). V1S-005 suite alone: **15 passed**.

```
ruff check app/services/dogfood_validation.py \
  app/services/v1_readiness_dashboard.py \
  app/presentation/student/adaptive_workspace.py \
  app/presentation/student/views.py \
  tests/test_v1s005_dogfood_remediation.py
```

Outcome: clean.

## Migration Impact

**None** — no Alembic / schema changes.

---

## Files Created

- `tests/test_v1s005_dogfood_remediation.py`
- `V1S005_IMPLEMENTATION_REPORT.md`

## Files Modified

- `app/services/dogfood_validation.py`
- `app/services/v1_readiness_dashboard.py`
- `app/founder/dashboard/templates/founder_dashboard/v1_readiness.html`
- `app/presentation/student/adaptive_workspace.py`
- `app/presentation/student/dto/adaptive_workspace.py`
- `app/presentation/student/views.py`
- `app/presentation/student/services/student_home_service.py`
- `app/presentation/student/view_models.py`
- `app/presentation/student/educational_view_models.py`
- `app/presentation/product_language.py`
- `app/domain/student_experience/experience_workspace.py`
- `app/templates/student/home.html`
- `app/templates/student/learning_journey.html`
- `app/templates/session/partials/session_body.html`
- `app/templates/layouts/eos_student.html`
- `.env.example`
- `V1_RELEASE_CRITERIA.md`
- `tests/test_v1s004_dogfood_validation.py`
- `tests/test_v1s003_repository_health.py`
- `tests/presentation/student/test_navigation.py`
- `tests/presentation/student/test_routes.py`
- `tests/presentation/student/test_terminology.py`
- `tests/presentation/workflows/test_workflow_consistency.py`
- `tests/presentation/workflows/test_workflow_student_session.py`
- `tests/application/unified_journey/test_navigation.py`
- `tests/operational/test_alpha_smoke_student.py`
- `tests/test_kwp013_adaptive_workspace.py`

---

## Architecture Compliance

- Layering preserved: presentation + Founder observability + static registry.
- **No** redesign of Learning Runtime, Evidence, Progress algorithms, Strategy, Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory, Forecast, Knowledge Architecture, or Educational Authoring composition rules.
- Curriculum V1/V2 loader singularity unchanged.
- V1S-002 dogfood cutover retained; Runtime C enrolment preferred for progress isolation.

## Technical Debt

- DF-012 loading skeleton deferred.
- DF-TD01 / RI-002 Runtime A hard removal deferred.
- Mission package REMOVE gates unchanged.

## Known Limitations

1. Exclusive live week not yet executed — success bar partially HOLD on live evidence.
2. Package readiness is environment-dependent (founder must publish).
3. Does not claim P-002.1 production-ready / Gate G1.
4. Activity prompt previews remain deferred (titles + honesty line only).

## Success criteria

| Criterion | Result |
|---|---|
| Classify all dogfood issues | **PASS** |
| Resolve P0 (package readiness, silent episode, progress isolation) | **PASS** |
| Resolve P1 friction set | **PASS** |
| Learning Friction register with Before/After/Benefit/Evidence | **PASS** |
| Founder Learning Friction / Resolved / Open / Confidence Trend | **PASS** |
| No new educational intelligence | **PASS** |
| Exclusive uninterrupted CS1 week without workarounds | **HOLD** — ready to start when package gate READY; live week pending |
| Verify exclusive CS1 study can begin | **PASS** (gate helper + board); operational publish may still be required per env |
