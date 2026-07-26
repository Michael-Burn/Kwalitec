# EP-007.2 — Student Surface Pack (post–EP-007.1)

**Programme:** EP-007.2 — Canonical Journey Perception Validation (Tier B)  
**Date:** 2026-07-26  
**Purpose:** Student-visible journey experience judged by Tier B reviewers after canonical consolidation.  
**Constraint:** Evidence-only — no runtime / UI / educational reasoning changes in this programme.  
**Authority:** REVIEW_PROTOCOL — when package and live student experience diverge, judge the **live student-facing experience**.

---

## 1. What changed for students (EP-007.1)

Under production sole runtime (`KWALITEC_V2_SOLE_RUNTIME=ON`):

| Element | Student-visible behaviour |
|---|---|
| Single Home | Login and root land on Student Home (`/student/`); `/dashboard/` and `/missions/` redirect there |
| One start path | Primary CTA on Home: Start / Resume Study Session → `/session/*` |
| One duration fact | Preferred session minutes shown on Home and Session Overview (shared resolver) |
| Continuity | Complete returns to Student Home; resume stays on Education OS session surfaces |
| MES / readiness | Unchanged from EP-006.2 / EP-006.4 — still visible on schema-complete Home |

Educational “what to study” still comes from Runtime A (Recommendation / Planning / Readiness). This pack measures **journey coherence**, not ranking quality.

---

## 2. Capture artefacts used by Tier B

| File | Content |
|---|---|
| [`_capture/home_canonical.txt`](_capture/home_canonical.txt) | Canonical Home speech + journey annotations (30-minute mission) |
| [`_capture/session_overview.txt`](_capture/session_overview.txt) | Session Overview duration matching Home |
| [`_capture/duration_consistency.txt`](_capture/duration_consistency.txt) | Resolver proof: preferred 30 equals legacy path (no 90) |
| [`_capture/navigation_map.txt`](_capture/navigation_map.txt) | Sole-runtime entry / redirect map |
| [`_capture/continuity_path.txt`](_capture/continuity_path.txt) | Today’s study loop |
| [`_capture/cold_start_residual.txt`](_capture/cold_start_residual.txt) | Honest incomplete-schema residual |
| EP-007.1 regression suite | `tests/presentation/test_canonical_journey.py` |

Representative duration speech (schema-complete night):

> Today’s Mission — *Review CM1-A: Cash flow models* — **30 minutes**  
> Next — *Start a 30-minute cash flow practice session.*  
> Session Overview — **30 minutes** estimated  
> Pre-change contrast — Home 30 vs Learning Workspace Session **90** for the same day.

Representative navigation speech:

> Login → Student Home only. Bookmarks to Dashboard / Missions bounce back to Student Home. No second “home” to reconcile.

---

## 3. Known limitations reviewers must treat as current product

1. Dual-home still exists when sole runtime is **OFF** (soak / Internal Alpha) — not the W-PROD claim.  
2. Cold-start / incomplete MES nights remain weaker on explainability (separate from dual-home).  
3. Thin activity content on a sparse session can still feel empty — continuity ≠ content depth.  
4. Personalisation / feedback flags remain OFF.  
5. `V1_REVIEW_PACKAGE` may lag live sole-runtime chrome — reviewers use this pack + live behaviour.  
6. Guided Unified Journey chrome may be OFF; single home does not require it.

---

## 4. Tier B cohort

Post-change re-reviews archived under [`tier_b_reviews/`](tier_b_reviews/) (baseline corpora **not** overwritten):

SV-001, SV-002, SV-004, SV-009, SV-010, SV-015, SV-016, SV-018, SV-020 (N=9; meets methodology interview floor ≥8).

Focus: workflow / adoption / cognitive load / decision support / recoverability — dual-home and duration themes are in-scope for all.

---

**End of STUDENT_SURFACE_PACK**
