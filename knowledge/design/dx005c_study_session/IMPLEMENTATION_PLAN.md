# Implementation Plan

**Programme:** DX-005C  
**Status:** Plan for subsequent UI execution (not executed in DX-005C)  
**Release Candidate:** `RC-2026.07.29-01`  
**Depends on:** This corpus + DX-001 / DX-002 / DX-003 / DX-005A / DX-005B  

---

## Scope boundary

| DX-005C (this programme) | Later execution |
|---|---|
| Architecture, practice model, wireframe, feedback/reflection/continuity, scorecard | Templates + CSS + view-model |
| Documentation only | Session activity / overview route redesign |
| No application code | Restore coordinates + draft persistence hardening |

DX-005C does **not** ship UI. The following is the ordered plan for the implementation milestone that consumes these artefacts.

---

## Phase 0 — Preconditions

1. Treat `SESSION_ARCHITECTURE.md` + `PRACTICE_MODEL.md` + `SESSION_WIREFRAME.md` as binding.  
2. Confirm Home **Continue Session** / **Start Session** land on Session with continuity pointer (DX-005A).  
3. Prefer Home UI contracts clear before or tightly coupled with Session UI so resume/handoff stay coherent.  
4. Map existing session/activity templates to L0–L3 — do not CSS-hide legacy chrome.  
5. No curriculum engine / V1–V2 / publication pipeline changes in this UI milestone.  
6. Assessment remains a separate surface — do not absorb evaluation UI into Session.

---

## Phase 1 — Structure & content (before token polish)

Per DX-003: content and IA before chrome polish.

1. Replace Session body with: Persistent context → L0 → L1 → L2 → L3.  
2. Remove progress dashboards, stats strips, streak/badge/XP, welcome essays, decorative illustrations, multi-Primary clusters.  
3. Single Primary per activity (`PRIMARY_ACTION_BY_ACTIVITY` + blocking override).  
4. Collapse hints / reference / previous attempt / explainability to L2.  
5. Collapse technical metadata to L3.  
6. Move reflection UI to post-**Complete Session** only.

**Exit:** One question answerable without scroll-hunt; one Primary; no KPI theatre.

---

## Phase 2 — View-model

1. Session DTO:  
   - Persistent: subject, chapter, objective, activity, session progress  
   - L0: primary_label, primary_action, blocking_issue?  
   - L1: activity payload (section / question / exercise / feedback)  
   - L2: hint, reference, previous_attempt, explainability (lazy)  
   - L3: session_id, timestamps, diagnostics  
2. Feedback payload per `FEEDBACK_SPEC.md` (outcome + educational line).  
3. Continuity DTO per `SESSION_CONTINUITY_SPEC.md` (draft, scroll, timer, ui_phase).  
4. Stop feeding Session with Home-style coach / readiness aggregates on critical path.

**Exit:** Session renders practice-first without legacy dashboard chrome.

---

## Phase 3 — Continuity & performance

1. Persist/restore chapter, question, draft input, timer, feedback phase.  
2. Best-effort scroll restore; always restore activity anchor.  
3. First paint: context + Primary in <3s from Home Continue.  
4. Debounced draft save; server-authoritative timer.  
5. Focus management after submit → feedback → next Primary.

**Exit:** Continuity + performance targets satisfied in live UI.

---

## Phase 4 — Completion & reflection

1. Wire **Complete Session** → Reflection (or Home if disabled).  
2. Reflection: one Primary; Skip quiet; no gamification.  
3. Return Home; ensure Home Primary advances (no zombie Continue for completed session).  
4. Align copy with DX-003 Session reflection / Sensei reflection terms.

**Exit:** Complete → Reflect → Home flow verified.

---

## Phase 5 — Accessibility & Guardian

1. Keyboard order per wireframe; live region for feedback.  
2. Responsive compression of persistent context.  
3. Update UI Guardian for Session L0–L3, one Primary, feedback tone, no pre-practice reflection.  
4. Re-score live UI with `PREMIUM_SCORECARD.md`; any dimension ≤8 → redesign before ship.

**Exit:** A11y + Guardian + scorecard live PASS.

---

## Phase 6 — Coordination with DX-006

DX-006 — Shared Components & Design System Implementation should extract reusable pieces **after** Session structure is correct:

| Candidate shared component | Session use |
|---|---|
| Persistent context header | Student Session (+ patterns for Founder Workspace) |
| L0 decision strip (Primary + blocking) | Session / Assessment / Workspace |
| Feedback outcome block | Session (+ Assessment where educational) |
| Collapsed L2 / L3 disclosure | Cross-surface |
| Quiet Exit / Return Home | Session |

Do not invent a component library before IA is implemented once on Session.

---

## Non-goals for Session UI execution

- Redesigning Assessment, History, Choose Exam, or Home (separate plans)  
- Recommendation ranking changes  
- Curriculum JSON / engine changes  
- Founder Publication Workspace changes  

---

## Suggested verification checklist

- [ ] One Primary visible in each activity mode  
- [ ] Persistent context five fields present  
- [ ] Incorrect feedback matches Feedback Spec (no cheer)  
- [ ] Hint collapsed by default  
- [ ] Mid-session leave → Continue Session restores draft + position  
- [ ] Complete → Reflection → Home  
- [ ] No streaks/badges/stats dashboard  
- [ ] Premium scorecard re-run ≥9 all dimensions  
- [ ] Resume <3s to Primary (local measurement)
