# FV-001B — Founder Experience Completion Report

**Programme:** Founder Validation  
**Status:** Certification & Deployment  
**Date:** 2026-07-29  
**Release commit message:** `feat(founder-experience): complete founder validation experience`

Canonical workflow law remains:  
[`../fv001a_curriculum_studio_workflow_repair/FV001A_WORKFLOW_STATE_MACHINE.md`](../fv001a_curriculum_studio_workflow_repair/FV001A_WORKFLOW_STATE_MACHINE.md)  
*(unchanged — FV-001B did not alter stage gates, facts, or strip mapping from FV-001A).*

---

## Summary

FV-001B certifies the completed Founder Experience: explicit **Experience Selection** after login for dual-access operators (versioned device localStorage: Always Ask / Remember Founder / Remember Student), persistent **Switch Experience** without logout, nested **curriculum preview** with expand/collapse and virtualised rows, plus FV-001A workflow repairs (`preview_built`, durable projections, actionable gates).

No educational engine, extraction algorithm, or recommendation changes. Navigation and presentation only, plus durable Studio workflow projection persistence from FV-001A.

---

## Features completed

| Feature | Status |
|---------|--------|
| Experience Selection (`/auth/experience`) | Certified |
| Device preference (versioned localStorage object) | Certified |
| Switch Experience (Console + Student) | Certified |
| Nested preview tree (`parent_id`) | Certified |
| Expand / Collapse / Expand All / Collapse All | Certified |
| Virtualised large-tree rendering | Certified |
| FV-001A workflow continuity (`preview_built` / gates / auto-advance) | Certified |
| Durable workspace projections (migration `202607290001`) | Certified |
| Login value-prop de-duplication | Certified |

Product naming note: mission text says “Workspace Selection”; shipping surface is **Experience Selection** (Founder Console ↔ Student Experience). Curriculum Studio *workspaces* remain a separate domain object.

---

## Repository audit

Reviewed modified / new paths for FV-001A+B:

- No temporary debugging or `debugger` statements in release paths  
- No TODO/FIXME/HACK markers in FV release delta  
- No duplicate Experience Selection routes  
- Persistence adapter lives under `app/infrastructure/` (application layer independence preserved)  
- Auth base gained `extra_scripts` block only — no dead templates  
- Login feature bullet “Always know what to study next” removed (headline retains value proposition)

Unrelated untracked RC-2026.07.29-09 evidence directories were **not** bundled into this release commit unless already tracked.

---

## Regression summary

Suites executed (local):

```text
tests/presentation/test_ux001_founder_routing.py
tests/presentation/test_fv001b_founder_experience.py
tests/presentation/test_canonical_journey.py
tests/application/curriculum_studio/ (+ FV-001A)
tests/domain/curriculum_studio/
tests/presentation/workflows/test_workflow_founder_studio.py
tests/certification/test_pr001a_founder_operations.py
tests/test_smoke.py
tests/test_theme_system.py
tests/presentation/student/test_routes.py
tests/test_dx006b_founder_workspace.py
tests/test_px001_brand_identity.py
tests/test_auth.py
```

**Result:** targeted certification mesh green after aligning DX-006B / UX-001 contracts to four-stage strip + Experience Selection (**0 failures** on the release suite above).

Static analysis: `ruff check` clean on FV Python paths. JS ship files syntax-reviewed.

---

## Experience Selection

| Scenario | Behaviour |
|----------|-----------|
| Student-only | No selection page — existing student onboarding / home path |
| Dual-access (Founder / Admin / console.access) | Redirect to `/auth/experience` after login (unless safe `?next=`) |
| Remember Founder | Client redirects to `/console/` immediately |
| Remember Student | Client redirects to `/student/` immediately |
| Always Ask | Chooser UI shown |
| Switch Experience | `/auth/experience?switch=1` forces chooser without logout |

Preference schema (`localStorage` key `kwalitec.experiencePreference.v1`):

```json
{ "v": 1, "behaviour": "always_ask|remember_founder|remember_student", "updatedAt": "<ISO-8601>" }
```

No database fields. No preference migration.

---

## Nested Preview

- Hierarchy built from prepared structure `section_ref` when available; otherwise topics nest under first section for flat extraction payloads  
- Client tree: expand/collapse, Expand All (chunked), Collapse All, section/topic counts  
- Viewport virtualisation (`translateY` window) for large curricula  
- Noscript flat fallback retained  

---

## Workflow verification (FV-001A carry-forward)

| Check | Status |
|-------|--------|
| `preview_built` ≠ `preview_approved` | Pass |
| Advance to approval requires `preview_built` | Pass |
| Approval sets `preview_approved` | Pass |
| Actionable readiness gate copy | Pass |
| Durable `studio_workspace_projections` | Pass (requires Alembic on deploy) |
| Auto-advance when gates ready | Pass |

---

## Manual walkthrough

Local + production walkthrough checklist:

1. Login as Founder → Experience Selection  
2. Choose Founder Console (Always Ask)  
3. Subjects → create subject → Upload CMP/Syllabus → Processing strip  
4. Preview hierarchy expand/collapse → Approve → Publish  
5. Switch Experience → Student → Home / Journey / History / Revision / Settings  

Evidence folder: [`knowledge/evidence/releases/FV001B/`](../../evidence/releases/FV001B/)  
*(Production visual captures added post-deploy when Render is live.)*

---

## Visual evidence

| Asset | Path |
|-------|------|
| Evidence index | `knowledge/evidence/releases/FV001B/README.md` |
| Screenshots | Captured on production post-deploy |

---

## Performance notes

- Preview DOM renders only the visible row window (± overscan)  
- Expand All processes nodes in RAF chunks of 500  
- Preference read/write is synchronous localStorage (fail-soft)

---

## Known limitations

- Flat extraction without section linkage nests all topics under the first section (presentation approximation until richer CIP parent maps are present)  
- Remembered preference is per-browser, not per-account  
- Multi-worker last-write-wins on workspace projections (alpha-acceptable)  
- Alembic graph still has historical multi-heads elsewhere; this revision chains from `202607280080`

---

## Recommendations

1. Deploy migration `202607290001` and verify `/auth/experience` + Studio Preview in production  
2. Resume **FV-001** with a **brand-new curriculum upload** and complete Founder → Student pipeline — no further UX programmes until FV-001 finishes unless a new P0 appears  

---

## Final decision

See release certification footer after deploy verification.
