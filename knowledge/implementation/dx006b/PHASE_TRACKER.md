# DX-006B Phase Tracker

**Programme:** DX-006B — Founder & Student Surface Migration  
**Status:** Phase 1 Founder Home **IN REVIEW** (implementation complete; awaiting independent certification)  
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
| Phase 1 Founder Home | DX-004A | IN REVIEW | 97/100 | ≥9/10 provisional | PASS | PASS | PASS | Home suite PASS |
| Phase 2 Founder Subjects | DX-004B | NOT STARTED | — | — | — | — | — | — |
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
| Notes | Tokens remapped; L1–L3 + foundation API + macros/CSS shipped. Conditions: link `design_system.css` in Phase 1; import only from `foundation`; legacy rejected still on package root |

**Exit:** Every visual token has a canonical runtime source; catalogue components usable; Guardian G-1…G-12 enforceable on new UI. **Met** with conditions above.

---

## Phase 1 — Founder Home

### Meta

| Field | Value |
|---|---|
| Status | IN REVIEW |
| Authority | `knowledge/design/dx004a_founder_home/` |
| Surface migrated | Founder Home (`overview.html` → DX-004A body) |
| Started | 2026-07-29 |
| Certified | — (pending independent review) |
| Notes | Report: `DX006B_PHASE1_FOUNDER_HOME_COMPLETION_REPORT.md` |

### Completion report fields (fill on certify)

| Field | Value |
|---|---|
| Surface migrated | Founder Home (`/console/`) |
| Legacy removed | KPI grids, Platform Summary, Quick Actions, Operational detail, pulse essay, unused `index.html` |
| Components reused | Current Work, Publication Queue, Recent Publications, Primary Action Strip, Empty Operational |
| Guardian status | PASS |
| Accessibility | PASS |
| Performance | PASS |
| Architectural Fidelity | 97 /100 |
| Premium score | All dimensions ≥9 (provisional) |
| Regression summary | Founder Home suite PASS; ops reachable via Settings |
| Known issues | Footer pulse copy residual; Studio hubs nested not deleted |

### Certification checklist

- [x] Replace Home template  
- [x] Remove KPI cards  
- [x] Remove duplicate navigation  
- [x] Implement Current Work  
- [x] Implement Publication Queue  
- [x] Implement Recent Publications  
- [x] Implement one Primary  
- [x] Implement shared components  
- [ ] Founder validation PASS (independent)  
- [x] Guardian PASS  
- [x] Accessibility PASS  
- [x] Performance PASS  
- [x] Regression PASS  
- [ ] Premium PASS (provisional — confirm independently)  
- [x] Architectural Fidelity ≥95%  

---

## Phase 2 — Founder Subjects

### Meta

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx004b_subjects/` |
| Depends on | Phase 1 CERTIFIED |

### Completion report fields

| Field | Value |
|---|---|
| Surface migrated | |
| Legacy removed | |
| Components reused | |
| Guardian status | |
| Accessibility | |
| Performance | |
| Architectural Fidelity | /100 |
| Premium score | |
| Regression summary | |
| Known issues | |

### Certification checklist

- [ ] Catalogue  
- [ ] Search  
- [ ] Filters  
- [ ] Create Subject  
- [ ] Object permanence  
- [ ] Open → Workspace flow  
- [ ] Legacy hubs removed  
- [ ] Duplicate catalogue pages removed  
- [ ] All review gates PASS  
- [ ] Architectural Fidelity ≥95%  

---

## Phase 3 — Founder Workspace

### Meta

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx004c_workspace/` |
| Depends on | Phase 2 CERTIFIED |

### Completion report fields

| Field | Value |
|---|---|
| Surface migrated | |
| Legacy removed | |
| Components reused | |
| Guardian status | |
| Accessibility | |
| Performance | |
| Architectural Fidelity | /100 |
| Premium score | |
| Regression summary | |
| Known issues | |

### Certification checklist

- [ ] Upload stage  
- [ ] Validate stage  
- [ ] Review stage (in-workspace)  
- [ ] Approve stage  
- [ ] Publish stage  
- [ ] Single workspace  
- [ ] No separate Review page  
- [ ] No separate Publish page  
- [ ] Persistent Context  
- [ ] Blocking Findings  
- [ ] Primary Strip  
- [ ] All review gates PASS  
- [ ] Architectural Fidelity ≥95%  

---

## Phase 4 — Student Home

### Meta

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx005a_student_home/` |
| Depends on | Phase 3 CERTIFIED |

### Completion report fields

| Field | Value |
|---|---|
| Surface migrated | |
| Legacy removed | |
| Components reused | |
| Guardian status | |
| Accessibility | |
| Performance | |
| Architectural Fidelity | /100 |
| Premium score | |
| Regression summary | |
| Known issues | |

### Certification checklist

- [ ] Mission  
- [ ] Learning Queue  
- [ ] Recent Progress  
- [ ] Continuation  
- [ ] Legacy Home removed  
- [ ] Readiness cards removed  
- [ ] Study Sensei Home removed  
- [ ] Journey panels removed  
- [ ] Student + Guardian + a11y + perf + regression + Premium PASS  
- [ ] Architectural Fidelity ≥95%  

---

## Phase 5 — Choose Exam

### Meta

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx005b_choose_exam/` |
| Depends on | Phase 4 CERTIFIED |

### Completion report fields

| Field | Value |
|---|---|
| Surface migrated | |
| Legacy removed | |
| Components reused | |
| Guardian status | |
| Accessibility | |
| Performance | |
| Architectural Fidelity | /100 |
| Premium score | |
| Regression summary | |
| Known issues | |

### Certification checklist

- [ ] Ready  
- [ ] Coming Soon  
- [ ] Begin Learning  
- [ ] Search  
- [ ] Discovery  
- [ ] Legacy wizard theatre removed  
- [ ] Planning chrome removed  
- [ ] Marketing removed  
- [ ] All review gates PASS  
- [ ] Architectural Fidelity ≥95%  

---

## Phase 6 — Study Session

### Meta

| Field | Value |
|---|---|
| Status | NOT STARTED |
| Authority | `knowledge/design/dx005c_study_session/` |
| Depends on | Phase 5 CERTIFIED |

### Completion report fields

| Field | Value |
|---|---|
| Surface migrated | |
| Legacy removed | |
| Components reused | |
| Guardian status | |
| Accessibility | |
| Performance | |
| Architectural Fidelity | /100 |
| Premium score | |
| Regression summary | |
| Known issues | |

### Certification checklist

- [ ] Persistent Context  
- [ ] Practice  
- [ ] Feedback  
- [ ] Reflection  
- [ ] Continuity  
- [ ] Coach walls removed  
- [ ] Stats removed  
- [ ] Gamification removed  
- [ ] Dashboard chrome removed  
- [ ] All review gates PASS  
- [ ] Architectural Fidelity ≥95%  

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
