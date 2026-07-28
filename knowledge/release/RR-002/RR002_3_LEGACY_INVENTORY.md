# RR-002.3 — Legacy Educational Presentation Inventory

**Programme:** RR-002 — Governance Convergence  
**Work Package:** RR-002.3 — Repository & Runtime Convergence  
**Date:** 2026-07-28  
**Governance authority:** DG-001.1 · DG-001.2 · DG-001.3 · DG-001.4 · RP-002 · RR-002  
**Status:** Authoritative inventory for repository convergence (no behavioural change)

---

## Purpose

Definitive inventory of educational presentation surfaces, shared components, and terminology mappings that coexist in the repository after RR-002.1 (navigation) and RR-002.2 (chrome lexicon). This document does **not** retire code; it classifies assets so engineers do not accidentally extend legacy paths.

**Authoritative runtime ownership:** see `RR002_3_RUNTIME_OWNERSHIP.md`.  
**Convergence narrative:** see `RR002_3_RUNTIME_CONVERGENCE_REPORT.md`.

---

## Classification legend

| Class | Meaning |
|---|---|
| **Certified** | Part of the sole-runtime Education OS certification path (`KWALITEC_V2_SOLE_RUNTIME=1`) |
| **Shared** | Used by both sole-runtime and dual-run; chrome may fork via `layouts/base.html` |
| **Legacy (Contained)** | Runtime A / V1 shell retained for dual-run soak; redirects under sole runtime; chrome remediated where assigned (RR-002.2) |
| **Latent** | Present in repo; not on the default sole-runtime Home path; reuse risk if included |
| **Flag-gated** | Present but OFF under Alpha / production posture |
| **Safe future cleanup** | Candidate for removal only after an explicit retirement work package (not this WP) |

---

## 1. Sole-runtime educational surfaces (Certified)

### Blueprints / routes

| Surface | Blueprint | URL | Ownership notes |
|---|---|---|---|
| Home | `presentation/student` | `/student/` | Canonical home — `student.home` |
| Journey | `presentation/student` | `/student/journey` | Canonical journey |
| Revision | `presentation/student` | `/student/revision` | Canonical revision focus |
| History (student label: Analytics) | `presentation/student` | `/student/history` | Canonical analytics projection |
| Profile | `presentation/student` | `/student/profile` | Exam / preference settings entry |
| Decision Journal | `presentation/student` | `/student/decision-journal` | Memory surface (RR-001.3C) |
| Educational Timeline | `presentation/student` | `/student/timeline` | Memory surface |
| Learning Check | `presentation/student` | `/student/assessment/*` | Assessment delivery |
| Session Experience | `presentation/session` | `/session/<id>/*` | Overview → activity → reflection → summary |

### Layout / chrome

| Path | Class | Notes |
|---|---|---|
| `app/templates/layouts/eos_student.html` | Certified | EOS shell; owns top nav via `student/components/navigation.html` |
| `app/templates/student/components/navigation.html` | Certified | Primary learner nav under sole runtime |
| `app/templates/student/base.html` | Certified | Student feature base |
| `app/templates/session/base.html` | Certified | Session feature base |

### Certified page templates

```
app/templates/student/home.html
app/templates/student/journey.html
app/templates/student/revision.html
app/templates/student/history.html
app/templates/student/profile.html
app/templates/student/decision_journal.html
app/templates/student/educational_timeline.html
app/templates/student/assessment/*.html
app/templates/session/overview.html
app/templates/session/activity.html
app/templates/session/reflection.html
app/templates/session/summary.html
app/templates/session/complete.html
```

### Certified session components

```
app/templates/session/components/navigation.html
app/templates/session/components/activity_card.html
app/templates/session/components/question_card.html
app/templates/session/components/timer_card.html
app/templates/session/components/progress_bar.html
app/templates/session/components/completion_card.html
app/templates/session/components/reflection_card.html
app/templates/session/components/explanation_card.html
```

### Certified student projection components (wired on EOS surfaces)

| Path | Class | Notes |
|---|---|---|
| `student/components/readiness_card.html` | Certified | Readiness projection |
| `student/components/journey_card.html` | Certified | Journey summary |
| `student/components/progress_card.html` | Certified | Progress snapshot |
| `student/components/history_card.html` | Certified | History context |
| `student/components/countdown_card.html` | Certified | Exam countdown |
| `student/components/explanation_card.html` | Certified / Latent on Home | MES Level-2; used on Revision; **not** wired as Home hero |

### Consolidation helpers (developer-facing)

| Path | Role |
|---|---|
| `app/presentation/consolidation.py` | Sole-runtime redirects; `CANONICAL_HOME_ENDPOINT = "student.home"` |
| `app/application/config/v2_flags.py` | `SOLE_RUNTIME` and related V2 flags |
| `app/presentation/product_language.py` | Approved / rejected educational terms |

---

## 2. Deprecated / legacy runtime surfaces (Legacy Contained)

Redirect under sole runtime; remain registered for dual-run soak. **Do not extend for new educational features.**

### Blueprints

| Blueprint | Module | Sole-runtime redirect | Disposition |
|---|---|---|---|
| `dashboard` | `app/dashboard/routes.py` | → `student.home` | READY FOR MIGRATION |
| `mission` | `app/mission/routes.py` | → `student.home` (session entry) | READY FOR MIGRATION |
| `analytics` | `app/analytics/routes.py` | → `student.history` | READY FOR MIGRATION |

### Legacy layouts / chrome

| Path | Class | Safe future cleanup? |
|---|---|---|
| `app/templates/layouts/legacy_workspace.html` | Legacy | Yes — after dual-run retirement |
| `app/templates/partials/sidebar.html` | Legacy | Yes — after dual-run retirement |
| `app/templates/partials/topnav.html` | Legacy | Yes — after dual-run retirement |

### Legacy page templates

| Path | Class | RR-002 chrome status | Safe future cleanup? |
|---|---|---|---|
| `app/templates/dashboard/index.html` | Legacy | Guidance chrome (RR-002.2 NCR-007) | Yes — after dual-run retirement |
| `app/templates/analytics/index.html` | Legacy | Contained | Yes — after chart-parity gate |
| `app/templates/mission/index.html` | Legacy | Contained | Yes — after session parity gate |
| `app/templates/mission/session.html` | Legacy | Contained | Yes — after Session Experience owns all entry |
| `app/templates/mission/session_recorded.html` | Legacy | System / Study Sensei (RR-002.2 NCR-006) | Yes — after LXP feedback parity |
| `app/templates/mission/session_practice_outcome.html` | Legacy | Contained | Yes — after practice-outcome parity |

### Legacy static (dual-run soak)

| Path | Class | Notes |
|---|---|---|
| `app/static/js/study_session.js` | Legacy | Dual-run session interactions |

---

## 3. Shared presentation components

Used across certified and legacy stacks. Prefer extending **certified** call sites; treat dual-chrome forks carefully.

| Path | Class | Notes |
|---|---|---|
| `app/templates/layouts/base.html` | Shared (DEP-003 router) | Selects `eos_student` vs `legacy_workspace` via `SOLE_RUNTIME` |
| `app/templates/partials/educational_explainability.html` | Shared | EIP-003 claim block |
| `app/templates/partials/empty_state.html` | Shared | EOS + legacy empty states |
| `app/templates/partials/welcome_modal.html` | Shared | Study Sensei handoff (RR-001.3A) |
| `app/templates/partials/flash_messages.html` | Shared | Flash chrome |
| `app/templates/partials/brand_meta.html` | Shared | Brand meta |
| `app/templates/partials/app_footer.html` | Shared | Footer |
| `app/templates/partials/contextual_help.html` | Shared | Help tips |
| `app/templates/study_plan/*.html` | Shared | Workflow; eyebrow may fork by `SOLE_RUNTIME` |
| `app/templates/settings/index.html` | Shared | Account settings; Product Check-in label (RR-002.1) |
| `app/templates/alpha/onboarding.html` | Shared | Onboarding count honesty (RR-002.1) |
| `app/templates/alpha/help.html` | Shared | Orientation / memory canon (RR-001.3B/C) |

### Latent reusable macros (reuse risk)

| Path | Class | Notes |
|---|---|---|
| `app/templates/student/components/recommendation_card.html` | Latent | Guidance eyebrow (RR-002.2); **not** sole-runtime Home include — do not reintroduce as Mission hero |
| `app/templates/student/components/educational_experience.html` | Flag-gated | Runtime C (`data-educational-experience="runtime-c"`); PX-001; OFF in Alpha |

---

## 4. Legacy educational terminology mappings

Source law: `knowledge/governance/CANONICAL_EDUCATIONAL_LEXICON.md`, `TERM_DEPRECATION_REGISTER.md`, DG-001.1 / DG-001.2. Presentation remediations: RR-001.3A–3D, RR-002.1, RR-002.2.

| Deprecated / rejected (student chrome) | Canonical | Register / finding | Status |
|---|---|---|---|
| tip / Mission tip / “Why this tip?” | Mission / Guidance / Recommendation (role-correct) | DEP-01 | Closed on certified + Contained chrome |
| Today's Recommendation *(as daily-focus hero)* | Today's Mission; **Guidance** eyebrow for recommendation slot | DEP-03 · RP002-NCR-005/007 | Closed RR-002.2 |
| Today's Session *(as Mission synonym)* | Today's Mission (focus); Session (practice unit) | DEP-02 | Closed RR-001.3A on certified surfaces |
| Kwalitec as educational observer / mentor | **System** (facts) + **Study Sensei** (conclusions); KW = product | DG-001.2 · CP-10 · RP002-NCR-006 | Closed RR-002.2 on session feedback |
| Share Feedback (nav label) | **Product Check-in** | CI-03 · RP002-NCR-001 | Closed RR-002.1 |
| “What we updated” (unnamed authority) | **What the system updated** | D05 · RP002-NCR-002 | Closed RR-002.1 |
| Dashboard / Analytics *(as learner product names under sole runtime)* | Home / History (Analytics label on History) | DEP-05/06 | Redirects; templates remain Contained |
| the system / the algorithm *(as mentor narrator)* | Study Sensei | DEP-04 | Runtime C Contained OFF |

### Domain translation (not student chrome headers)

Internal `TERMINOLOGY_MAP` in `app/domain/student_experience/recommendation_explanation.py` still maps:

| Domain key | Student-safety string | RR-002.3 note |
|---|---|---|
| `Adaptive Decision Engine` | `Today's Recommendation` | Domain translation synonym — **not** remediating chrome; do not promote as Mission hero |
| `Mission Engine` | `Today's Session` | Domain translation — prefer Mission / Session role split in new chrome |

These mappings are **not** certified presentation chrome. Future lexicon pass requires Board / DG-001 authority — out of RR-002.3 scope.

---

## 5. Safe future cleanup candidates

Eligible for a **future retirement** work package only (engines/calculators protected until evidence gates pass):

1. Legacy blueprints `dashboard`, `mission` (LXP session UX), `analytics` after sole-runtime-only ops + parity gates.
2. Templates under `app/templates/dashboard/`, `mission/`, `analytics/`.
3. `layouts/legacy_workspace.html` + `partials/sidebar.html` + `partials/topnav.html` when dual-run is retired.
4. Latent `recommendation_card.html` if Home never re-adopts the macro (or fold into certified Guidance panel only).
5. Parallel `src/` Education OS stack (quarantined residual — RR-001.3E) after Board retirement.
6. Dual-run-only static (`study_session.js`) after Session Experience owns interactions.

**Not cleanup candidates without separate programme:** Mission Intelligence algorithms, Reflection Architecture, Decision Journal, Timeline/History epistemology, schema, feature-flag framework, protected readiness/session evidence calculators.

---

## 6. Inventory anchors (tests)

| Suite | Guards |
|---|---|
| `tests/presentation/student/test_rr001_3a_educational_identity.py` … `3d` | Educational identity / orientation / memory / consistency |
| `tests/presentation/student/test_rr002_1_navigation_educational_consistency.py` | Navigation lexicon |
| `tests/presentation/student/test_rr002_2_educational_chrome.py` | Contained chrome (Guidance / System / Sensei) |
| `tests/presentation/workflows/test_workflow_dual_run.py` | Dual-run workflow soak |

---

**End of RR002_3_LEGACY_INVENTORY**
