# RR-002.3 — Runtime Ownership

**Programme:** RR-002 — Governance Convergence  
**Work Package:** RR-002.3 — Repository & Runtime Convergence  
**Date:** 2026-07-28  
**Governance authority:** DG-001.1 · DG-001.2 · DG-001.3 · DG-001.4 · RP-002 · RR-002  
**Binding companions:** `docs/architecture/PHASE_1_CANONICAL_DECLARATION.md`, `app/presentation/consolidation.py`

---

## Purpose

State which runtime is authoritative for student education presentation, which components are certified for Alpha / sole-runtime certification, which remain legacy Contained, and which may be removed only in a future cleanup. Educational behaviour is unchanged by this document.

---

## 1. Authoritative runtime

| Attribute | Declaration |
|---|---|
| **Authoritative student presentation runtime** | Education Operating System (EOS) under **`KWALITEC_V2_SOLE_RUNTIME=1`** |
| **Canonical home endpoint** | `student.home` (`CANONICAL_HOME_ENDPOINT` in `app/presentation/consolidation.py`) |
| **Canonical session path** | `/session/<id>/*` (`presentation/session`) |
| **Certification path** | Sole-runtime Alpha (RP-002 / RR-001 / RR-002 assumption) |
| **Legacy dual-run** | Contained soak / rollback only — **not** the certification path |

### Capability ownership (Phase 1 binding)

| Capability | Authoritative (Certified) | Legacy alternative |
|---|---|---|
| Dashboard / Home | `/student/` — D-B | `/dashboard/` — READY FOR MIGRATION |
| Journey | `/student/journey` — J-B | Embedded V1 — READY FOR MIGRATION |
| Coach / Guidance | Home coach panel — C-B | V1 tips / dashboard narrative — READY FOR MIGRATION |
| Analytics | `/student/history` — A-B | `/analytics/` — READY FOR MIGRATION |
| Session | `/session/<id>/*` — S-B | `/missions/.../session*` — READY FOR MIGRATION |
| Reflection | `/session/<id>/reflection` — R-B | V1 review shims — redirects |
| Mission presentation | Home Mission + Session CTA — M-B presentation | Legacy mission hub templates |

Educational **engines and calculators** remain protected until retirement evidence gates pass. Ownership of presentation ≠ license to delete domain services.

---

## 2. Chrome ownership (DEP-003)

| Flag posture | Layout | Navigation owner |
|---|---|---|
| `SOLE_RUNTIME` true | `layouts/eos_student.html` (via `layouts/base.html` router) | `student/components/navigation.html` |
| `SOLE_RUNTIME` false | `layouts/legacy_workspace.html` | `partials/sidebar.html` + `partials/topnav.html` |

Shared workflow pages (`study_plan`, `settings`, Help, onboarding) extend `layouts/base.html` and inherit the active chrome. Controllers and engines are unchanged by the router.

---

## 3. Certified components

Engineers **should** extend these for new student-facing educational presentation:

### Routes / modules

- `app/presentation/student/`
- `app/presentation/session/`
- `app/presentation/consolidation.py` (redirect / home resolution only)
- `app/presentation/product_language.py` (lexicon constants)
- `app/presentation/student/educational_view_models.py`

### Templates

- `app/templates/layouts/eos_student.html`
- `app/templates/student/**` (except latent macros noted below)
- `app/templates/session/**`
- Shared partials used from certified pages (`partials/welcome_modal.html`, `educational_explainability.html`, etc.)

### Governance / product language

- `knowledge/governance/CANONICAL_EDUCATIONAL_LEXICON.md`
- `knowledge/governance/EDUCATIONAL_AUTHORITY_MODEL.md`
- DG-001.1–DG-001.4

---

## 4. Legacy (Contained) components

Engineers **must not** use these as the default path for new educational features:

| Area | Paths |
|---|---|
| Blueprints | `app/dashboard/`, `app/mission/` (LXP shells), `app/analytics/` |
| Layouts | `layouts/legacy_workspace.html` |
| Nav | `partials/sidebar.html`, `partials/topnav.html` |
| Pages | `templates/dashboard/`, `templates/mission/`, `templates/analytics/` |

Under sole runtime these routes **redirect**; templates remain for dual-run soak and regression. Chrome on Contained surfaces was lexicon-aligned in RR-002.2 so misconfiguration cannot reintroduce RP002-NCR-005–007 copy defects.

---

## 5. Latent / flag-gated components

| Component | Status | Rule |
|---|---|---|
| `student/components/recommendation_card.html` | Latent | Guidance chrome certified; do not reintroduce as Mission-competing hero on Home |
| `student/components/educational_experience.html` | Flag-gated Runtime C | OFF in Alpha; do not enable without Board/flag programme |
| Parallel `src/` stack | Quarantined residual | Not Flask sole-runtime `/student` |

---

## 6. Safe future removal (cleanup backlog)

May be removed **only** under an explicit retirement work package with parity evidence:

1. Legacy dashboard / mission LXP / analytics blueprints + templates  
2. Legacy workspace layout + sidebar/topnav  
3. Dual-run-only JS (`study_session.js`) after Session Experience coverage  
4. Latent recommendation card macro if unused after Home Guidance panel owns the slot  
5. Parallel `src/` Education OS residual  

**Do not remove** without a dedicated programme: recommendation algorithms, Mission Intelligence composition, Reflection Architecture, Decision Journal, Timeline, History epistemology, database schema, feature-flag infrastructure, protected evidence/readiness calculators.

---

## 7. Authority model (presentation speech)

| Authority | Speaks as | Does not speak as |
|---|---|---|
| **System** | Facts, state updates, observed outcomes | Mentor conclusions |
| **Study Sensei** | Educational conclusions, guidance, support | Product brand |
| **Kwalitec (product)** | Brand, product chrome, Product Check-in | Educational observer / mentor |

Source: DG-001.2 / `EDUCATIONAL_AUTHORITY_MODEL.md`. RR-002.1 / RR-002.2 closed assigned chrome violations; this ownership doc does not alter speech rules.

---

## 8. Accepted residuals (unchanged)

Repository convergence does **not** close RP-002 Accepted Residuals AR-001–007 (flags, notifications, parallel reflection stacks, sole-runtime ops, Journal mirror, cohort validation, study-tip hygiene). Those remain Board-visible and out of RR-002.3 scope.

---

**End of RR002_3_RUNTIME_OWNERSHIP**
