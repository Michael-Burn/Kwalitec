# RC-2026.07.29-06 — Student Home State Synchronisation

**Programme:** CQ-008 Remediation  
**Status:** IMPLEMENTATION complete — awaiting independent review  
**Date:** 2026-07-29  
**Commit:** not created (per mission)

---

## Executive Summary

Student Home was projecting an empty “No exam selected…” state after a successful study-plan + mission creation because Experience Home read Twin/`examination_label` only and never bound the active Study Plan (the same CQ-002 gap Profile already fixed). The smallest safe correction aligns Home with that canonical Study Plan identity, propagates mission session topic when Adaptive recommendation is blank, and keeps empty-state logic from treating demo mission stubs as real study context.

**Verdict: GO WITH CONDITIONS**

Functional synchronisation is verified (unit + Flask HTTP walk under V2 Experience flags). Playwright Chromium could not capture `student_home_after_plan.png` in this agent environment (headless_shell SIGSEGV). HTML DOM capture and structured evidence are present for review; local Playwright re-run is the residual condition.

---

## Problem Description

RC-2026.07.29-05 Browser Acceptance confirmed:

- Study Plan creation succeeds
- Wizard / calibration complete
- Mission and Study Session launch
- Returning to `/student/` still showed empty-state copy: “No exam selected yet. Choose an exam to begin studying.”

That broke the learner mental model: onboarding completed, yet Home denied the existence of an exam/plan.

---

## Root Cause

**Classification:** □ Wrong source of truth · □ View / projection logic · □ Incomplete sync (not missing SQL persistence)

| Layer | Finding |
|---|---|
| Persistence | Study Plan + Mission rows were written correctly (`/missions/` worked). |
| Experience Twin | Auto-provisioned / empty `examination_label` after plan creation — not updated from SQL. |
| `HomeService` | Read Twin/readiness only; **no** `StudyPlanService.get_user_active_plan` fallback (Profile already had this). |
| Recommendation title | Built from Adaptive dict only; ignored mission `session.topic_title`. |
| `StudentHomeService` | Empty when `_select_mission` returned `None` **and** `_has_study_plan_signal` was false — both true when Twin label + recommendation title were blank. |

Not: cached HTTP responses, redirect timing, ORM relationship failure, or template-only bug.

---

## Source of Truth

Canonical learner study identity for Student Home:

1. **Examination name** — `StudyPlanService.get_user_active_plan(user_id).exam_name`  
   Shared helper: `app.application.student_experience.examination_identity.exam_label_from_active_plan`  
   (same authority as Profile CQ-002 / PX-003 B2).

2. **Today’s mission / session** — Runtime A `MissionService` via Experience Mission read bridge (`EducationalStateService.todays_session`).

3. **L0 narrative title** — Adaptive recommendation when present; otherwise mission session `topic_title`.

Student Home must reflect (1)+(2)+(3). It must not invent a parallel learner-state store.

---

## Behaviour Before

| Learner state | Home |
|---|---|
| No plan | Empty — “No exam selected…” |
| Plan + mission created; Twin label blank | **Empty — “No exam selected…”** (incorrect) |
| `/missions/` | Mission / session available (correct) |

---

## Behaviour After

| Learner state | Home |
|---|---|
| Genuinely no plan / no topic | Empty — “No exam selected…” |
| Active plan, mission not CTA-ready | Quiet — session-ready copy (not empty-exam) |
| Active plan + startable mission (V2 bridges) | **Mission panel** with exam name + **Start Session** / Continue |

Verified HTTP evidence (`evidence.json`):

- `before_empty_state: true`
- `after_mission_panel: true`, `after_primary: true`, `after_has_exam_name: true`
- `after_empty: false`
- Refresh + logout/login still non-empty with mission panel

HTML capture shows:

- Subject: `IFoA CM1`
- Primary: `Start Session`
- No “No exam selected” copy

---

## Files Modified

### Created

- `app/application/student_experience/examination_identity.py`
- `tests/application/student_experience/test_home_exam_identity.py`
- `knowledge/engineering/rc20260729_06_student_home_state_sync/_evidence/browser_acceptance/rc20260729_06_playwright_run.py`
- `knowledge/engineering/rc20260729_06_student_home_state_sync/_evidence/browser_acceptance/rc20260729_06_http_verify.py`
- `knowledge/engineering/rc20260729_06_student_home_state_sync/_evidence/browser_acceptance/student_home_after_plan.html`
- `knowledge/engineering/rc20260729_06_student_home_state_sync/_evidence/browser_acceptance/evidence.json`
- `knowledge/engineering/rc20260729_06_student_home_state_sync/RC20260729_06_STUDENT_HOME_STATE_SYNC_REPORT.md` (this file)

### Modified

- `app/application/student_experience/home_service.py` — plan exam fallback + session topic → recommendation title
- `app/application/student_experience/profile_service.py` — use shared `exam_label_from_active_plan`
- `app/presentation/student/view_models.py` — Home `examination_label` authoritative fallback (Profile parity)
- `app/presentation/student/services/student_home_service.py` — subject/objective use `start_session.topic_title`; quiet signal includes real topic (not bare demo mission ids)
- `tests/test_dx006b_student_home.py` — mission / demo-stub / quiet regressions

### Intentionally untouched

Study engine, mission generation math, curriculum engine, auth, shell, navigation, schema/migrations, API contracts.

---

## Tests Executed

```text
.venv/bin/python -m pytest \
  tests/test_dx006b_student_home.py \
  tests/application/student_experience/test_home_exam_identity.py \
  -v
→ 13 passed

.venv/bin/ruff check \
  app/application/student_experience/examination_identity.py \
  app/application/student_experience/home_service.py \
  app/application/student_experience/profile_service.py \
  app/presentation/student/services/student_home_service.py \
  app/presentation/student/view_models.py \
  tests/test_dx006b_student_home.py \
  tests/application/student_experience/test_home_exam_identity.py
→ All checks passed

KWALITEC_V2_STUDENT_EXPERIENCE=1 KWALITEC_V2_DURABLE_STORE=1 \
KWALITEC_V2_INJECT_ENGINES=1 KWALITEC_V2_FOUNDER_INTELLIGENCE=1 \
KWALITEC_EI_INTERNAL_ALPHA=1 \
PYTHONPATH=. .venv/bin/python \
  knowledge/engineering/rc20260729_06_student_home_state_sync/_evidence/browser_acceptance/rc20260729_06_http_verify.py
→ pass: true
```

Broader `tests/presentation/student/` still reports pre-existing DX-005A / welcome-modal / craft-hook failures unrelated to this sync (e.g. missing welcome modal, CSS token expectations). Not introduced by RC-06.

---

## Browser Evidence

| Artefact | Status |
|---|---|
| `student_home_after_plan.html` | **Captured** — mission panel + Start Session + IFoA CM1 |
| `evidence.json` | **Pass** — empty → mission → refresh → relogin |
| `student_home_after_plan.png` | **Not captured** — Playwright `chrome-headless-shell` SIGSEGV on launch in agent environment |
| `rc20260729_06_playwright_run.py` | Ready for local re-run against `:5055` |

**Condition:** Independent reviewer should run the Playwright script locally and attach `student_home_after_plan.png`.

---

## Known Risks

1. **Twin still not written on plan create** — Home reads Study Plan as fail-open fallback; Twin can remain empty until a later sync programme.
2. **Demo Experience mission stubs** — bare `mission-{id}` / `sess-{id}` without topic no longer suppress empty-state (by design).
3. **Mission bridge required for L0 Start CTA** — without V2 Mission read bridge, Home correctly shows quiet (plan known) rather than empty-exam; Start Session needs bridge/runtime posture used in CQ-008 acceptance.
4. **Playwright PNG gap** in this agent run only.

---

## Recommendation

### GO WITH CONDITIONS

**GO** on functional state synchronisation:

- Empty state only for genuine new learners
- Active plan/mission learners see study context (exam + mission / Start Session)
- Refresh and re-login preserve state
- No schema / engine / shell regressions in scope

**Conditions before unconditional CQ-008 close:**

1. Local Playwright capture of `student_home_after_plan.png` using `_evidence/browser_acceptance/rc20260729_06_playwright_run.py` (or equivalent) against the V2-flagged app.
2. Independent review of the projection-only change set (no commit yet, per mission).

---

## Architecture Compliance

- Presentation / Experience projection only — no study/mission engine changes
- Curriculum V1/V2 traversal untouched
- Shared Study Plan identity helper avoids duplicate learner state
- Layering preserved: HomeService → Educational State / StudyPlanService; StudentHomeService remains presentation assembly
