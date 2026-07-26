# Architecture Summary — Version 1 (Board Level)

**Programme:** P-003.1 — Version 1 Release Dossier  
**Date:** 2026-07-26  
**Audience:** Product Board  
**Constraint:** No source code. Board language only.

Authoritative technical baseline: `knowledge/architecture/ep002_9_programme_exit_certification/AUTHORITATIVE_ARCHITECTURE_BASELINE.md`.

---

## 1. Runtime A in one paragraph

**Runtime A** is the Education OS that students use: authentication, Student Home, today’s mission/session, practice, reflection, readiness, and tomorrow’s next action. It is curriculum-first and deterministic: the same educational inputs produce the same planning, readiness, and recommendation outputs. Under **production defaults**, Twin and cutover feature flags are **OFF**, so legacy Runtime A services remain the student-visible educational authority. Twin-gated paths exist for soak and dual-run but are not the Version 1 production-default student truth.

---

## 2. Recommendation authority

| Item | Board statement |
|---|---|
| **Owner** | RecommendationService (Runtime A) |
| **Role** | Decide and explain *what the student should do next* within educational law |
| **Quality law** | P-001.3 Recommendation Quality Standard; EP-003.1 quality contract |
| **Explainability** | P-001.2 schema (why, evidence, confidence, next action) |
| **Must not** | Invent readiness scores or daily plans; market effectiveness without approved evidence |

Personalisation (EP-004.2) may influence ordering within decision bands when its flag is ON; production default is **OFF**.

---

## 3. Planning authority

| Item | Board statement |
|---|---|
| **Owner** | PlanningService (Runtime A) |
| **Role** | Author today’s mission / daily plan and persist mission facts |
| **Quality law** | Planning Service Quality Contract (EP-003.3) |
| **Must not** | Compete with a second planner; present conflicting “today” durations on the same day |

Personalisation (EP-004.3) may adjust pacing/duration presentation when ON; production default **OFF**. Educational topic priority remains PlanningService authority.

---

## 4. Readiness authority

| Item | Board statement |
|---|---|
| **Owner** | ReadinessService (Runtime A) |
| **Role** | Estimate preparedness from evidence; state unknowns honestly |
| **Quality law** | Readiness Service Quality Contract (EP-003.2); Home delivery EP-006.4 |
| **Must not** | Exam Ready marketing without gates; soothing composites that hide missing evidence |

Validated perception: K3 **65** (EP-006.5) — improved unpackability; not yet a Version 1 excellence claim.

---

## 5. Presentation

| Item | Board statement |
|---|---|
| **Role** | Deliver authored explanations (MES) and journey chrome to students |
| **Surfaces** | Student Home, Coach/Insights, Mission, Analytics (as applicable) |
| **EP-006 finding** | Service-authored MES was previously lost before templates — delivery fixed without changing educational maths |
| **Must not** | Invent evaluation, planning, or a third educational narrator |

---

## 6. Student Experience

Canonical journey (EP-007.1):

Login → (plan wizard if needed) → **Student Home** → Start/Resume Session → Overview → Activity → Reflection → Summary → Complete → Home.

Sole-runtime consolidation removed dual-home and conflicting duration clocks on the W-PROD claim window. Session experience remains presentation/orchestration around Runtime A facts.

---

## 7. Boundaries (non-negotiable)

1. **One Education OS runtime** in production defaults — no second educational brain.  
2. **Curriculum Engine** owns syllabus structure; do not duplicate ordering in presentation or cutover.  
3. **Runtime A writes** own educational facts; Twin/Insight do not write educational state.  
4. **Fail-open:** cutover flag OFF restores legacy student-visible payloads.  
5. **Production hard gate:** HTTP cutovers ineligible when environment is production/prod.  
6. **Curriculum V1 and V2** remain loadable and traversable.

---

## 8. Educational ownership (governance vs runtime)

| Concern | Owner |
|---|---|
| Why the product exists / Never-Build | Vision 2030 |
| Educational meaning / mastery / evidence law | Educational Constitution (EGI) |
| Whether quality is good enough to release to students | EVF Educational Release Gate |
| Educational usefulness score | Product Success Framework (KSI) |
| Version 1 production-ready declaration | Version 1 Release Framework (P-002.1) |
| What to study / plan / readiness maths | Runtime A services (above) |

Architecture enables honesty; it does not by itself prove educational effectiveness. Effectiveness evidence remains **NO-GO / PENDING EVIDENCE** (EP-007.3).

---

## 9. Feature-flag posture (Version 1 defaults)

| Capability family | Production default | Board implication |
|---|---|---|
| Digital Twin / Authority / Cutover | OFF | Legacy Runtime A is student truth |
| Learning feedback / Profile / Personalisation | OFF | Do not market as live student capability |
| Analytics Journey emit | Deferred / gated | Do not claim live Journey KPIs as production-active without checklist |

A published Version 1 flag matrix is required for Gate **G12** before declaration. **Evidence currently unavailable** for a completed G12 declaration board.

---

## 10. Rollback model (board view)

| Intent | Action |
|---|---|
| Surface rollback | Turn cutover flag OFF + restart → legacy payload for that surface |
| Capability rollback | Turn capability flag OFF → feature absent; claim language must exclude it |
| Emergency | Kill-switch / flag OFF for high-risk educational flags (must be documented for G12) |

Detail in authoritative architecture baseline §7.
