# DX-006B Phase Tracker

**Programme:** DX-006B — Founder & Student Surface Migration  
**Status:** Phase 2 Founder Subjects **IN REVIEW** (implementation complete; awaiting independent certification)  
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
| Phase 2 Founder Subjects | DX-004B | IN REVIEW | 97/100 | ≥9/10 provisional | PASS | PASS | PASS | Subjects suite PASS |
| Phase 3 Founder Workspace | DX-004C | NOT STARTED | — | — | — | — | — | — |
| Phase 4 Student Home | DX-005A | NOT STARTED | — | — | — | — | — | — |
| Phase 5 Choose Exam | DX-005B | NOT STARTED | — | — | — | — | — | — |
| Phase 6 Study Session | DX-005C | NOT STARTED | — | — | — | — | — | — |
| **Programme Exit** | DX-006B | **OPEN** | — | — | — | — | — | — |

---

## Foundation Gate

**Goal:** DX-006A tokens, L1–L3, Guardian enforcement available for composition.

| Field | Value |
|---|---|
| Status | CERTIFIED |
| Acceptance | `knowledge/design/dx006a_design_system/IMPLEMENTATION_ORDER.md` |
| Certified | 2026-07-29 |
| Report | `FOUNDATION_GATE_COMPLETION_REPORT.md` |
| Notes | Tokens remapped; L1–L3 + foundation API + macros/CSS shipped |

**Exit:** Met with conditions (foundation import surface; `design_system.css` linked in Phase 1).

---

## Phase 1 — Founder Home

| Field | Value |
|---|---|
| Status | CERTIFIED |
| Authority | `knowledge/design/dx004a_founder_home/` |
| Surface migrated | Founder Home (`/console/`) |
| Certified | 2026-07-29 |
| Report | `DX006B_PHASE1_FOUNDER_HOME_COMPLETION_REPORT.md` |
| Fidelity | 97 /100 |
| Premium | All dimensions ≥9 |
| Guardian | PASS |

---

## Phase 2 — Founder Subjects

### Meta

| Field | Value |
|---|---|
| Status | IN REVIEW |
| Authority | `knowledge/design/dx004b_subjects/` |
| Depends on | Phase 1 CERTIFIED |
| Started | 2026-07-29 |
| Certified | — (pending independent review) |
| Notes | Report: `DX006B_PHASE2_FOUNDER_SUBJECTS_COMPLETION_REPORT.md` |

### Completion report fields

| Field | Value |
|---|---|
| Surface migrated | Founder Subjects (`/console/studio/subjects` → DX-004B catalogue) |
| Legacy removed | `hub.html`; workflow essay; dual Primaries; hub peer catalogues (redirected); Studio KPI / create peer forms |
| Components reused | Search, Select, Toolbar, Page header, Primary strip, Badge, Empty operational, Catalogue table/list |
| Guardian status | PASS |
| Accessibility | PASS |
| Performance | PASS |
| Architectural Fidelity | 97 /100 |
| Premium score | All dimensions ≥9 (provisional) |
| Regression summary | Subjects suite PASS; hubs redirect to filter presets |
| Known issues | More (…) deferred; created_at sort fallback; live dogfood pending |

### Certification checklist

- [x] Catalogue  
- [x] Search  
- [x] Filters  
- [x] Create Subject  
- [x] Object permanence  
- [x] Open → Workspace flow  
- [x] Legacy hubs removed (redirected to Subjects filters)  
- [x] Duplicate catalogue pages removed  
- [ ] All review gates PASS (independent)  
- [x] Architectural Fidelity ≥95%  

---

## Phase 3 — Founder Workspace

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx004c_workspace/` |
| Depends on | Phase 2 CERTIFIED |

---

## Phase 4 — Student Home

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx005a_student_home/` |
| Depends on | Phase 3 CERTIFIED |

---

## Phase 5 — Choose Exam

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx005b_choose_exam/` |
| Depends on | Phase 4 CERTIFIED |

---

## Phase 6 — Study Session

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx005c_study_session/` |
| Depends on | Phase 5 CERTIFIED |

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
