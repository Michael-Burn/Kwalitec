# DX-006B Execution Plan

**Programme:** DX-006B — Founder & Student Surface Migration (Architecture Fidelity)  
**Status:** Approved — execution framework binding  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Predecessor:** DX-006A (Complete)  

---

## 1. Purpose

Implement every Founder and Student operating-system surface using the frozen design architecture:

| Authority | Role |
|---|---|
| **DX-001** | Design language |
| **DX-002** | Information architecture / surface types |
| **DX-003** | Decision → Action → Feedback / copy |
| **DX-004A/B/C** | Founder OS (Home, Subjects, Workspace) |
| **DX-005A/B/C** | Student OS (Home, Choose Exam, Study Session) |
| **DX-006A** | Design System (tokens, L0–L3 catalogue, Guardian G-1…G-12) |

This programme does **not** redesign. It **faithfully implements**.

---

## 2. Engineering Law

```text
Architecture is the authority.
Code conforms to architecture.
Architecture does not conform to code.
```

On conflict:

1. Surface structure → DX-004 / DX-005 win.  
2. Shared UI foundation → DX-006A wins (tokens, components, Guardian).  
3. Visual values → DX-001 (as encoded in DX-006A tokens).  
4. Copy / decision density → DX-003.  
5. Surface type / one-question rule → DX-002.  
6. Live code never overrides architecture documents.

---

## 3. Migration Philosophy

| Rule | Meaning |
|---|---|
| **Replace** | New body is the canonical implementation |
| **Never layer** | Do not wrap legacy chrome with new skins |
| **Never CSS-hide** | Do not `display:none` legacy KPI / Quick Action blocks |
| **Never preserve legacy chrome** | Delete Platform Summary, Sensei walls, hub peers, etc. |

Every migrated surface becomes the **sole** product path for that job.

---

## 4. Preconditions (before Phase 1 code)

DX-006A foundation Phases 1–5 (tokens → primitives → layout → operational → Guardian) must be treated as binding acceptance criteria. Where code remap is still pending:

1. Complete DX-006A `IMPLEMENTATION_ORDER.md` Phases 1–5 **before or as the opening tranche** of DX-006B Phase 1.  
2. Do **not** invent page-local primitives during surface migration.  
3. Do **not** start Founder Subjects until Founder Home is certified.

Track foundation readiness in `PHASE_TRACKER.md` under **Foundation Gate**.

---

## 5. Mandatory phase order

```text
Foundation Gate (DX-006A code Phases 1–5)
        ↓
Phase 1 — Founder Home          (DX-004A)
        ↓
Phase 2 — Founder Subjects      (DX-004B)
        ↓
Phase 3 — Founder Workspace     (DX-004C)
        ↓
Phase 4 — Student Home          (DX-005A)
        ↓
Phase 5 — Choose Exam           (DX-005B)
        ↓
Phase 6 — Study Session         (DX-005C)
        ↓
Programme Exit → CQ-008 eligible
```

**No later phase may begin until the previous phase is certified.**  
Certification = all phase gates PASS (see §7).

---

## 6. Phase briefs

### Phase 1 — Founder Home

| Field | Value |
|---|---|
| **Authority** | `knowledge/design/dx004a_founder_home/` |
| **Question** | What should I work on next? |
| **Implement** | Current Work (L0), Publication Queue (L1), Recent Publications (L2), one Primary, shared L3 components |
| **Remove** | KPI cards, Platform Summary, Quick Actions, duplicate in-page navigation, operational detail essays |
| **Primary template** | Founder Console Home (legacy Overview / `overview.html` or successor) |
| **Shared components** | Current Work, Publication Queue, Primary Action Strip, Empty State |

### Phase 2 — Founder Subjects

| Field | Value |
|---|---|
| **Authority** | `knowledge/design/dx004b_subjects/` |
| **Question** | Which subject am I managing? |
| **Implement** | Catalogue, search, filters, Create Subject, object permanence, Open → Workspace |
| **Remove** | Legacy hubs (Review / Publishing / Versions / Quality peers), duplicate catalogue pages, tutorial essays, dual Primary cards |
| **Shared components** | Search Bar, List/Table, Publication Status, Empty State, Badge |

### Phase 3 — Founder Workspace

| Field | Value |
|---|---|
| **Authority** | `knowledge/design/dx004c_workspace/` |
| **Question** | What is the next publishing action for this subject? |
| **Implement** | Upload → Validate → Review → Approve → Publish as **stages** in one workspace; Persistent Context; Blocking Findings; Primary Strip |
| **Remove** | Separate Review page, separate Publish page, readiness KPI card rows, multi-Primary clusters |
| **Shared components** | Persistent Context Header, Stage Indicator, Primary Action Strip, Blocking Findings |

### Phase 4 — Student Home

| Field | Value |
|---|---|
| **Authority** | `knowledge/design/dx005a_student_home/` |
| **Question** | What should I study next? |
| **Implement** | Mission (L0), Learning Queue (L1), Recent Progress (L2), continuation / one-click resume |
| **Remove** | Legacy Home chrome, readiness cards, Study Sensei Home, Journey panels, Quick Actions, gamification |
| **Primary template** | `app/templates/student/home.html` |
| **Shared components** | Mission Card, Learning Queue, Recent Progress, Primary Action Strip, Empty State |

### Phase 5 — Choose Exam

| Field | Value |
|---|---|
| **Authority** | `knowledge/design/dx005b_choose_exam/` |
| **Question** | What can I begin studying? |
| **Implement** | Ready, Coming Soon, Begin Learning, search, discovery list |
| **Remove** | Legacy wizard theatre, planning chrome, marketing essays, multi-CTA commitment |
| **Primary template** | `app/templates/study_plan/wizard_step_1.html` (or successor discovery route) |
| **Shared components** | Search Results, List, Publication Status / readiness honesty, Empty State |

### Phase 6 — Study Session

| Field | Value |
|---|---|
| **Authority** | `knowledge/design/dx005c_study_session/` |
| **Question** | What do I practice now? |
| **Implement** | Persistent Context, Practice, Feedback, Reflection (post-complete), Continuity |
| **Remove** | Coach walls, stats strips, gamification, dashboard chrome, multi-Primary clusters |
| **Primary templates** | Session activity / overview under `app/templates/session/` |
| **Shared components** | Session Context, Feedback Block, Blocking Findings, Primary Action Strip, Disclosure |

---

## 7. Required review after every phase

No phase proceeds until **all** of the following PASS:

| Gate | Artefact / method |
|---|---|
| Founder validation | Operator walkthrough against DX-004 authority (Phases 1–3) |
| Student validation | Learner walkthrough against DX-005 authority (Phases 4–6; N/A for Founder-only phases) |
| Guardian validation | G-1…G-12 + surface extras (`GUARDIAN_RULES.md`, `UI_GUARDIAN.md`) |
| Accessibility audit | DX-006A `ACCESSIBILITY_STANDARD.md` |
| Performance audit | First paint / no unnecessary DOM / lazy L2–L3 disclosure |
| Regression tests | Relevant pytest + critical path smoke |
| Premium certification | Per-surface scorecard via `PREMIUM_CERTIFICATION_TEMPLATE.md` (all dims ≥9) |
| Architectural Fidelity | ≥95% via `ARCHITECTURAL_FIDELITY_CHECKLIST.md` |
| Implementation report | Phase completion block in `PHASE_TRACKER.md` + notes in programme report |

---

## 8. Architectural Fidelity Score

Every migrated page must score using weights:

| Category | Weight |
|---|---:|
| Matches DX Architecture | 30 |
| Shared Components | 20 |
| Token Compliance | 15 |
| Guardian Compliance | 15 |
| Accessibility | 10 |
| Performance | 10 |
| **Total** | **100** |

**Minimum to certify a phase: 95%.**

Scoring procedure: `ARCHITECTURAL_FIDELITY_CHECKLIST.md`.

---

## 9. Forbidden during DX-006B

- No new dashboards  
- No new KPI cards  
- No extra Primaries  
- No page redesign (architecture already frozen)  
- No new IA / navigation trees  
- No component duplication  
- No token duplication  
- No hard-coded colours  
- No architecture changes to DX-001…006A corpora  

Violations are **stop-ship**. See `IMPLEMENTATION_GUARD.md`.

---

## 10. Deliverables (this programme)

| Artefact | Path |
|---|---|
| Execution Plan | `DX006B_EXECUTION_PLAN.md` (this file) |
| Phase Tracker | `PHASE_TRACKER.md` |
| Fidelity Checklist | `ARCHITECTURAL_FIDELITY_CHECKLIST.md` |
| Implementation Guard | `IMPLEMENTATION_GUARD.md` |
| Migration Sequence | `MIGRATION_SEQUENCE.md` |
| Premium Template | `PREMIUM_CERTIFICATION_TEMPLATE.md` |
| Completion Report | `DX006B_COMPLETION_REPORT.md` |

Per-phase completion blocks live in `PHASE_TRACKER.md` until programme exit updates the completion report.

---

## 11. Exit criteria (programme)

DX-006B is complete **only** when:

- [ ] Founder Home migrated and certified  
- [ ] Founder Subjects migrated and certified  
- [ ] Founder Workspace migrated and certified  
- [ ] Student Home migrated and certified  
- [ ] Choose Exam migrated and certified  
- [ ] Study Session migrated and certified  
- [ ] All Guardian rules PASS on migrated surfaces  
- [ ] Architectural Fidelity ≥95% on every migrated surface  
- [ ] Premium Certification PASS on every migrated surface  
- [ ] Accessibility PASS on every migrated surface  
- [ ] Regression PASS for Founder + Student critical paths  

**Only then** may the project proceed to **CQ-008 — Premium Product Certification**.

---

## 12. Non-goals

- Curriculum engine / V1–V2 traversal changes  
- Alembic schema redesign  
- New educational algorithms or LLM paths  
- Assessment surface redesign (separate from Session)  
- Founder Operations / Research dashboard redesign  
- Brand guideline rewrite  

---

*Release Candidate: RC-2026.07.29-01*
