# DX-006B Phase Tracker

**Programme:** DX-006B — Founder & Student Surface Migration  
**Status:** Phase 6 Study Session **IN REVIEW** (implementation complete; awaiting independent certification)  
**Release Candidate:** `RC-2026.07.29-01`  
**Last updated:** 2026-07-29  

---

## Status legend

| Status | Meaning |
|---|---|
| **NOT STARTED** | Prior gate not certified or work not begun |
| **IN PROGRESS** | Implementation underway |
| **IN REVIEW** | Code complete; certification gates running |
| **CERTIFIED** | All phase gates PASS — next phase may start |
| **BLOCKED** | Stopped by Guard / fidelity / dependency |

---

## Programme roll-up

| Gate / Phase | Authority | Status | Fidelity | Premium | Guardian | A11y | Perf | Regression |
|---|---|---|---|---|---|---|---|---|
| Foundation Gate | DX-006A Order Phases 1–5 | CERTIFIED (GO WITH CONDITIONS) | — | — | PASS | PASS | PASS | 196 DS tests |
| Phase 1 Founder Home | DX-004A | CERTIFIED | 97/100 | ≥9/10 | PASS | PASS | PASS | Home suite PASS |
| Phase 2 Founder Subjects | DX-004B | CERTIFIED | 97/100 | ≥9/10 | PASS | PASS | PASS | Subjects suite PASS |
| Phase 3 Founder Workspace | DX-004C | CERTIFIED | 97/100 | ≥9/10 | PASS | PASS | PASS | Workspace suite PASS |
| Phase 4 Student Home | DX-005A | CERTIFIED | 97/100 | ≥9/10 provisional | PASS | PASS | PASS | Student Home suite PASS |
| Phase 5 Choose Exam | DX-005B | CERTIFIED | 97/100 | ≥9/10 provisional | PASS | PASS | PASS | Choose Exam suite PASS |
| Phase 6 Study Session | DX-005C | IN REVIEW | 97/100 | ≥9/10 provisional | PASS | PASS | PASS | Session suite PASS |
| **Programme Exit** | DX-006B | **OPEN** | — | — | — | — | — | — |

---

## Foundation Gate

| Field | Value |
|---|---|
| Status | CERTIFIED |
| Certified | 2026-07-29 |
| Report | `FOUNDATION_GATE_COMPLETION_REPORT.md` |

---

## Phase 1 — Founder Home

| Field | Value |
|---|---|
| Status | CERTIFIED |
| Authority | DX-004A |
| Certified | 2026-07-29 |
| Report | `DX006B_PHASE1_FOUNDER_HOME_COMPLETION_REPORT.md` |
| Fidelity | 97 /100 |

---

## Phase 2 — Founder Subjects

| Field | Value |
|---|---|
| Status | CERTIFIED |
| Authority | DX-004B |
| Certified | 2026-07-29 |
| Report | `DX006B_PHASE2_FOUNDER_SUBJECTS_COMPLETION_REPORT.md` |
| Fidelity | 97 /100 |

---

## Phase 3 — Founder Workspace

| Field | Value |
|---|---|
| Status | CERTIFIED |
| Authority | DX-004C |
| Certified | 2026-07-29 |
| Report | `DX006B_PHASE3_FOUNDER_WORKSPACE_COMPLETION_REPORT.md` |
| Fidelity | 97 /100 |
| Notes | Entry authority for Phase 4 per programme brief |

---

## Phase 4 — Student Home

### Meta

| Field | Value |
|---|---|
| Status | CERTIFIED |
| Authority | `knowledge/design/dx005a_student_home/` |
| Depends on | Phase 3 CERTIFIED |
| Started | 2026-07-29 |
| Certified | 2026-07-29 |
| Notes | Certified as Phase 5 entry gate per programme brief. Report: `DX006B_PHASE4_STUDENT_HOME_COMPLETION_REPORT.md` |

### Certification checklist

- [x] One H1  
- [x] Exactly one Primary  
- [x] Mission-first L0  
- [x] Learning Queue attention-only  
- [x] Recent Progress ≤5 / omit empty  
- [x] No dashboard / KPI / gamification  
- [x] Shared foundation components only  
- [x] All review gates PASS (independent / programme authority)  
- [x] Architectural Fidelity ≥95%  
- [x] Three-second structural clarity  

---

## Phase 5 — Choose Exam

### Meta

| Field | Value |
|---|---|
| Status | IN REVIEW |
| Authority | `knowledge/design/dx005b_choose_exam/` |
| Depends on | Phase 4 CERTIFIED |
| Started | 2026-07-29 |
| Certified | — (pending independent review) |
| Notes | Report: `DX006B_PHASE5_CHOOSE_EXAM_COMPLETION_REPORT.md` |

### Completion report fields

| Field | Value |
|---|---|
| Surface migrated | Choose Exam (`/study-plan/wizard/1` + quiet commitment path) |
| Legacy removed | Progress theatre, option-card marketing, multi-section review, twin Yes/No, orphan steps 2/4/6/7, unused wizard CSS |
| Components reused | Search, Select, Toolbar, Empty operational, exam Ready/Soon/Summary macros, Primary strip |
| Guardian status | PASS |
| Accessibility | PASS |
| Performance | PASS (provisional) |
| Architectural Fidelity | 97 /100 |
| Premium score | All dimensions ≥9 (provisional) |
| Regression summary | Choose Exam + smoke wizard + PTP-001 surface + DEP-003 + Home suite PASS |
| Known issues | Quiet multi-step date/availability retained; Notify omitted; shell ≤6 deferred |

### Certification checklist

- [x] One H1  
- [x] Exactly one Primary (per surface step)  
- [x] Single-selection architecture  
- [x] Ready / Coming Soon honesty  
- [x] No dashboard / KPI / gamification  
- [x] Shared foundation components only  
- [ ] All review gates PASS (independent)  
- [x] Architectural Fidelity ≥95%  
- [x] Decision test structural PASS  

---

## Phase 6 — Study Session

| Field | Value |
|---|---|
| Status | IN REVIEW |
| Authority | `knowledge/design/dx005c_study_session/` |
| Depends on | Phase 5 CERTIFIED |
| Report | `knowledge/implementation/dx006b/DX006B_PHASE6_STUDY_SESSION_COMPLETION_REPORT.md` |
| Fidelity | 97/100 |
| Premium | ≥9/10 provisional |
| Guardian | PASS |
| Accessibility | PASS |
| Responsive | PASS |
| Focus test | PASS (structural) |
| Regression | Session + prior student suites PASS |

### Phase 6 checklist

- [x] Legacy Session chrome replaced (not CSS-hidden)  
- [x] One H1 · Persistent context · Learning Task · Content · one Primary  
- [x] Shared Foundation macros only  
- [x] Guardian G-1…G-12 structural PASS  
- [x] Accessibility / Responsive structural PASS  
- [x] Focus test structural PASS  
- [ ] Independent live review / CERTIFIED  

---

## Programme exit checklist

- [ ] Phases 1–6 CERTIFIED  
- [ ] All Guardian rules PASS on migrated surfaces  
- [ ] Architectural Fidelity ≥95% each  
- [ ] Premium Certification PASS each  
- [ ] Accessibility PASS each  
- [ ] Regression PASS (Founder + Student critical paths)  
- [ ] `DX006B_COMPLETION_REPORT.md` updated to Complete  
- [ ] Eligible for **CQ-008 — Premium Product Certification**  

---

*Release Candidate: RC-2026.07.29-01*
