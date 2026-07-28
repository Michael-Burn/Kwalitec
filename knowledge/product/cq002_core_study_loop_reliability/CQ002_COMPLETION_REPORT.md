# CQ-002 Completion Report — Core Study Loop Reliability

**Programme:** CQ-002 — Commercial Quality Programme  
**Date:** 2026-07-28  
**Status:** Complete  
**Commit:** `94e989e` (`feat(cq-002): streamline founder core study loop`)  

---

### Summary

CQ-002 audited the founder daily study loop and implemented the highest-value Version 1 polish fixes for **CR1 Core Study Loop**: one-click start into Activity (auto-begin after Home start), a single primary “Next” on Home, empty-Home forward paths, honest session progress chrome (no phantom Complete step), unified Start Session verb, Finish resume when a real session exists, Profile examination fallback from the active Study Plan, and a sole-runtime student revision-acknowledgement POST. Application behaviour was refined without Version 2 capabilities or architecture expansion. Provisional CRI moves from **43% → 45%**; no `cri-*` tag (validation required).

---

### Files Created

- `knowledge/product/cq002_core_study_loop_reliability/README.md`
- `knowledge/product/cq002_core_study_loop_reliability/CRI_INTAKE.md`
- `knowledge/product/cq002_core_study_loop_reliability/CORE_STUDY_LOOP_AUDIT.md`
- `knowledge/product/cq002_core_study_loop_reliability/IMPROVEMENT_PLAN.md`
- `knowledge/product/cq002_core_study_loop_reliability/CQ002_COMPLETION_REPORT.md`
- `tests/presentation/student/test_cq002_core_study_loop.py`

---

### Files Modified

- `app/presentation/student/routes.py` — auto-begin after start; student revision ack route
- `app/templates/student/home.html` — empty forward paths; Finish resume; student ack form
- `app/presentation/student/view_models.py` — single primary Next (suppress competing readiness Next)
- `app/presentation/session/navigation.py` — hide Complete from chrome; 4-step page meta
- `app/presentation/session/forms.py` — Start Session CTA verb
- `app/presentation/session/routes.py` — docstring verb
- `app/presentation/session/view_models.py` — Start Session default label
- `app/presentation/product_language.py` — preferred CTA list
- `app/application/session_experience/dto/overview_snapshot.py` — Start Session default
- `app/domain/session_experience/learning_session.py` — Start Session default
- `app/application/student_experience/profile_service.py` — exam label fallback from plan
- Related presentation/workflow tests updated for CTA verb and chrome behaviour
- `knowledge/product/cq001_commercial_readiness/COMMERCIAL_READINESS_BOARD.md`
- `.cursor/rules/99-CURRENT_MILESTONE.md`
- `knowledge/operations/oa001/PROGRAMME_DASHBOARD.md`

---

### Tests Executed

```bash
python3 -m pytest tests/presentation/student/test_cq002_core_study_loop.py \
  tests/presentation/session/test_matrix.py \
  tests/presentation/session/test_factory.py \
  tests/presentation/session/test_product_language.py \
  tests/presentation/session/test_routes.py \
  tests/presentation/student/test_readiness_experience_delivery.py \
  tests/presentation/student/test_rr001_1_critical_remediation.py \
  tests/presentation/workflows/test_workflow_student_session.py \
  tests/presentation/workflows/test_workflow_consistency.py \
  tests/presentation/workflows/test_workflow_session_resume.py \
  tests/presentation/session/test_regression.py \
  tests/presentation/session/test_view_models.py -q
```

**Outcome:** CQ-002 contracts **4 passed**; focused suite **313 passed** (1 pre-existing unrelated failure in `test_completion_readiness_label` — readiness copy, not CQ-002).

```bash
python3 -m ruff check <CQ-002 touched app modules + new test>
```

**Outcome:** All checks passed.

---

### Migration Impact

None.

---

### Architecture Compliance

Layering preserved (templates / presentation / application / domain). No blueprint math changes; no Twin ranking or curriculum engine changes. Curriculum V1/V2 load/traversal untouched. Sole-runtime canonical path strengthened; legacy dashboard revision ack retained for dual-run.

---

### Technical Debt

- Home hero can still stack many conditional blocks (audit F08) — deferred.
- Dual session paradigms under dual-run remain (F09) — architecture backlog.
- Auto-begin fails open to Overview; rare begin failures still cost an extra click.
- Education OS dashboard mapper still defaults to a separate “Begin Session” label (out of sole-runtime student path).

---

### Known Limitations

- CRI increase is **provisional** (internal evidence + tests; not founder dogfood-validated).
- CR1 remains Emerging (not Strong); residual “what now?” risk under scarce time and hero density.
- Duration / reflection-note blockers were already closed before CQ-002 and were not reworked.
- No `cri-45` tag — threshold met only provisionally.

---

### CRI domains improved

| Domain | Before | After | Notes |
|---|---:|---:|---|
| CR1 Core Study Loop | 50 | **56** | Start friction, dual Next, empty path, chrome honesty |
| CR2 Daily Habit Fit | 42 | **44** | Lower restart / start friction (natural) |
| CR5 Experience Cohesion | 42 | **45** | Single Next; Profile↔Plan exam; CTA verb; student ack |

---

### Estimated CRI delta

| Field | Value |
|---|---|
| Prior composite | 42.84 → **43%** |
| New weighted sum | 42.84 + 1.08 + 0.28 + 0.30 = **44.50** → **45%** (half up) |
| **Estimated ΔCRI** | **+2 provisional points** |
| Validation | **Provisional** |

---

### Evidence supporting the increase

- `CORE_STUDY_LOOP_AUDIT.md` / `IMPROVEMENT_PLAN.md` — friction → action map
- Code paths: Home start auto-begin; readiness Next suppression; empty Home links; session chrome; Profile exam fallback
- `tests/presentation/student/test_cq002_core_study_loop.py` + updated readiness / session / workflow tests

---

### Remaining blockers

| ID | Blocker | Caps |
|---|---|---|
| B-CR1-01 | Residual Emerging CR1 (hero density; scarce-time continuity) | CR1 Strong |
| B-CR2-01 | Habit continuity / restart not yet Strong | CR2 |
| B-CR8-01 / B-CR8-02 | Validated KSI / effectiveness evidence | CR8 |
| B-CR7-01 | G7 HOLD | CR7 claims |
| B-CR9-01 | Commercial freezes | CR9 |

---

### Provisional or validated

**Provisional.** Do **not** create `cri-45` until a founder dogfood CRI window validates the board.

---

### Student Impact Assessment

N/A as EP/P programme template — CQ is commercial-quality. Student-visible benefit: fewer dead ends and duplicate next-steps on the daily study path; Profile no longer contradicts an active plan’s exam name.

### Estimated KSI contribution

ΔKSI = 0 (not claimed). Mechanism may support K1/K5 perception later; no KSI validation window in CQ-002.

### Evidence collected

Paths above; RP-001 / PX-003 priors cited in the audit.

### Lessons learned for student value

Commercial loop trust fails on small honesty and click taxes more than missing features. Closing an extra Begin click and dual “Next” moved CRI without new capability.

### Explainability Review

N/A — no recommendation ranking / MES content change beyond suppressing duplicate Next display.

### Recommendation Quality Review

N/A — no ranking/selection change; presentation cohesion only.

### Version 1 readiness residual

N/A for V1 production-ready declaration. CRI provisional 45% does not clear P-002.1 gates.

---

**End of CQ-002 Completion Report**
