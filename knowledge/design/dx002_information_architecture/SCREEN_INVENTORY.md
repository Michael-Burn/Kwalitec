# Screen Inventory

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**Method:** Routes + templates as of 2026-07-29 (SOLE_RUNTIME canonical for students).  
**Scope:** Primary product surfaces. Engineering JSON diagnostics under `/founder/*` APIs excluded as non-product screens.

---

## Legend

| Column | Meaning |
|---|---|
| Type (current) | How the UI behaves today |
| Type (target) | Taxonomy from `PRODUCT_ARCHITECTURE.md` |
| Premium | Estimated DX-001 checklist readiness today (1–10) |
| Priority | P0–P3 from `DESIGN_PRIORITY_MATRIX.md` |

---

## A. Public / Auth

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| A1 | Login | `/auth/login` | `auth/login.html` | Auth+Landing → Auth | How do I enter? | 5 | P1 |
| A2 | Logout | `POST /auth/logout` | — | Action | — | — | — |

---

## B. Student — Alpha & Help

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| B1 | Onboarding | `/alpha/onboarding` | `alpha/onboarding.html` | Orientation | What must I know before I start? | 6 | P2 |
| B2 | Help & Support | `/alpha/help` | `alpha/help.html` | Help essay → Help | How do I get unblocked? | 4 | P1 |
| B3–B6 | Feedback forms | `/alpha/feedback/*` | `alpha/feedback_*.html` | Forms | Submit this feedback? | 7 | P2 |
| B7 | Product Check-in | `/research/checkin` | `research/checkin.html` | Form | Share product feedback? | 7 | P2 |
| B8 | Check-in thank you | `/research/thank-you` | `research/thank_you.html` | Confirmation | Done — what next? | 6 | P2 |

---

## C. Student — Planning

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| C1 | Choose Exam | `/study-plan/wizard/1` | `wizard_step_1.html` | Catalogue/Wizard | What can I begin studying? | 7 | P1 |
| C2 | Exam date | `/study-plan/wizard/2` | `wizard_step_3.html` | Wizard | When is my exam? | 8 | P2 |
| C3 | Availability | `/study-plan/wizard/3` | `wizard_step_5.html` | Wizard | How much time can I study? | 8 | P2 |
| C4 | Begin Learning | `/study-plan/review` | `review.html` | Wizard review | Confirm and start? | 5 | P1 |
| C5 | Study Plan view | `/study-plan/<id>` | `view.html` | Settings/detail | What is my plan configuration? | 6 | P2 |
| C6 | Study Plan list | `/study-plan/plans/all` | `list.html` | Catalogue | Which plan is active? | 7 | P2 |
| C7 | Study Plan edit | `/study-plan/<id>/edit` | `edit.html` | Settings | How do I change my plan? | 7 | P2 |
| C8 | Calibration | `/calibration/after-plan/<id>` | `calibration/alpha.html` | Wizard | What prior coverage should guide me? | 6 | P2 |

*Orphan templates on disk (not routed): `wizard_step_2/4/6/7.html` — remove in cleanup.*

---

## D. Student — Daily experience

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| D1 | Home | `/student/` | `student/home.html` | Home (dense) | What should I study next? | 5 | P0 |
| D2 | Journey | `/student/journey` | `student/journey.html` | Progress map | Where am I in the syllabus? | 6 | P1 |
| D3 | Revision | `/student/revision` | `student/revision.html` | Workspace | What should I revise to support today? | 6 | P1 |
| D4 | History | `/student/history` | `student/history.html` | Report+Archive | What have I practiced? | 3 | P1 |
| D5 | Decision Journal | `/student/decision-journal` | `student/decision_journal.html` | Archive | What guidance shaped my path? | 5 | P1 |
| D6 | Educational Timeline | `/student/educational-timeline` | `student/educational_timeline.html` | Archive | How does my story read over time? | 5 | P1 |
| D7 | Profile (Settings) | `/student/profile` | `student/profile.html` | Settings | How do I configure my account? | 5 | P2 |

---

## E. Student — Session & assessment

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| E1 | Session overview | `/session/<id>/overview` | `session/overview.html` | Workspace | Ready to begin? | 7 | P2 |
| E2 | Session activity | `/session/<id>/activity` | `session/activity.html` | Workspace | Next practice step? | 8 | P3 |
| E3 | Session reflection | `/session/<id>/reflection` | `session/reflection.html` | Workspace | What do I notice? | 7 | P2 |
| E4 | Session summary | `/session/<id>/summary` | `session/summary.html` | Workspace | What happened? | 7 | P2 |
| E5 | Session complete | `/session/<id>/complete` | `session/complete.html` | Workspace | Where next? | 8 | P3 |
| E6–E9 | Learning Check | `/assessment/*` | `student/assessment/*` | Workspace | Complete this check? | 7 | P2 |
| E10–E14 | Quick Check | `/adaptive-assessment/...` | `adaptive_assessment/*` | Embedded workspace | Complete this check? | 7 | P2 |

*Legacy `/missions/*` redirects under SOLE_RUNTIME — inventory as deprecated, not redesign targets.*

---

## F. Student — Settings (product)

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| F1 | Settings sections | `/settings/*` | `settings/index.html` | Settings | How do I configure X? | 6 | P2 |

*General settings redirects to Profile under SOLE_RUNTIME.*

---

## G. Console — Overview & queues

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| G1 | Console Home | `/console/` | `founder_dashboard/overview.html` | Dashboard mashup → Home | What should I publish or fix next? | 3 | P0 |
| G2 | Search | `/console/search` | `founder_dashboard/search.html` | Catalogue | Where is this object? | 7 | P2 |
| G3 | Attention | `/console/attention` | `founder_dashboard/attention.html` | Queue | What needs intervention? | 6 | P1 |
| G4 | Support | `/console/feedback` | `founder_dashboard/feedback.html` | Queue | Which feedback needs review? | 6 | P1 |
| G5 | Review submission | `/console/feedback/review/<id>` | `founder_dashboard/review.html` | Workspace | How do I disposition this? | 7 | P2 |
| G6 | Findings | `/console/findings` | `founder_dashboard/findings.html` | Queue/Archive | Which findings are open? | 6 | P2 |
| G7 | Finding detail | `/console/findings/<id>` | `finding_detail.html` | Workspace | Update this finding? | 7 | P2 |
| G8 | Students | `/console/participants` | `participants.html` | Catalogue | Who is participating? | 6 | P2 |

---

## H. Console — Curriculum Authority

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| H1 | Curriculum Studio | `/console/studio/` | `dashboard.html` | Catalogue | Which workspace needs work? | 4 | P0 |
| H2 | Subjects hub | `/console/studio/subjects` | `hub.html` | Catalogue | Which subject do I open/create? | 4 | P0 |
| H3 | Review Queue hub | `/console/studio/review-queue` | `hub.html` | Duplicate catalogue | *(fold)* | 3 | P0 |
| H4 | Publishing hub | `/console/studio/publishing` | `hub.html` | Duplicate catalogue | *(fold)* | 3 | P0 |
| H5 | Versions hub | `/console/studio/versions` | `hub.html` | Duplicate catalogue | *(fold)* | 3 | P0 |
| H6 | Quality hub | `/console/studio/quality` | `hub.html` | Duplicate catalogue | *(fold)* | 3 | P0 |
| H7 | Workspace | `/console/studio/workspaces/<id>` | `workspace.html` | Overloaded workspace | What is the next publication task? | 2 | P0 |

---

## I. Console — Secondary reports (demote)

| ID | Screen | Route | Template | Type now → target | One question (target) | Premium | P |
|---|---|---|---|---|---|---|---|
| I1 | Operational Health | `/console/operational-health` | `operational_health.html` | Report | Is the platform healthy? | 5 | P2 |
| I2 | Runtime Health | `/console/runtime-health` | `runtime_health.html` | Report | Is educational runtime healthy? | 4 | P2 |
| I3 | Founder Intelligence | `/console/intelligence` | `founder_intelligence.html` | Report | What learning signals matter? | 4 | P2 |
| I4 | Evidence Gates | `/console/evidence-gates` | `evidence_gates.html` | Report | Are cutover gates met? | 4 | P2 |
| I5 | Research / Analytics | `/console/research` | `research.html` | Report | What do check-ins show? | 5 | P2 |
| I6 | Internal Alpha | `/console/internal-alpha` | `internal_alpha.html` | Report | How is Alpha programme health? | 4 | P2 |
| I7 | Platform Intelligence | `/console/alpha-observability` | `alpha_observability.html` | Report | What telemetry events matter? | 4 | P2 |
| I8 | System Operations | `/console/operations` | `operations.html` | Report | What is FOS operational state? | 4 | P2 |
| I9 | Releases | `/console/releases` | `releases.html` | Archive | Findings by release? | 6 | P2 |
| I10 | Vision Journal | `/console/vision*` | `vision_*.html` | Archive/editor | Capture product vision? | 6 | P3 |
| I11 | Console Settings | `/console/settings` | `settings.html` | Settings | Console configuration? | 7 | P2 |

---

## J. Shared / system

| ID | Screen | Template | Notes | P |
|---|---|---|---|---|
| J1 | Confirm modal | `partials/confirm_modal.html` | Focused; keep | P3 |
| J2 | Welcome modal | `partials/welcome_modal.html` | Forbidden welcome pattern | P1 |
| J3 | Errors 403/404/500 | `errors/*` | Minimal | P3 |
| J4 | Subject support gate | `partials/subject_support_gate.html` | Blocking context | P2 |
| J5 | Legacy Dashboard | `dashboard/index.html` | Redirected; do not redesign | — |
| J6 | Legacy Analytics | `analytics/index.html` | Redirected; do not redesign | — |
| J7 | Legacy Mission | `mission/*` | Redirected; do not redesign | — |

---

## K. Layouts (not screens, but shells)

| Layout | Path | Role |
|---|---|---|
| `layouts/eos_student.html` | Student primary shell | Keep; calm nav |
| `layouts/console_base.html` | Console primary shell | Collapse nav |
| `layouts/auth_base.html` | Auth | Keep |
| `layouts/legacy_workspace.html` | Dual-run only | Hide from product IA |
| `study_plan/wizard_base.html` | Wizard chrome | Keep step indicator lean |
| `session/base.html` | Session chrome | Keep minimal |

---

## Counts

| Category | Screens audited |
|---|---|
| Primary product screens (A–I, active) | **~55** |
| Deprecated / redirect-only | 3 families |
| Shared chrome / modals | 7 |
| **Total reviewed for IA** | **~65 surfaces** |

Every active primary screen has a target question in `PRODUCT_ARCHITECTURE.md` §4 and a full audit row in `INFORMATION_HIERARCHY_AUDIT.md`.
