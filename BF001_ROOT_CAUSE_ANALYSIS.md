# BF-001 — Root Cause Analysis

**Programme:** Blocker Fix Programme BF-001  
**Phase:** Founder Validation Readiness  
**Authority:** RF-001 · PX-004 PASS  
**Date:** 2026-07-31

---

## Summary

Six Category A workflow blockers trapped Founders during live RF verification. Each had a concrete root cause in presentation or wiring — not educational logic. Domain services for retreat/reset already existed; HTTP/UI surfaces and a handful of defects prevented intended behaviour.

---

## Blocker 1 — Expand All / Collapse All

| | |
|---|---|
| **Symptom** | Buttons do nothing |
| **Root cause** | `buildForest()` in `curriculum_preview_tree.js` assigned `var byId = Object` / `var children = Object` (the constructor) instead of plain `{}` maps. Parent/child indexing corrupted the forest; expand/collapse handlers ran against a broken tree. |
| **Secondary** | Keyboard handlers were click-only |
| **Fix** | Initialise plain objects; bind Enter/Space on expand/collapse and row toggles |

---

## Blocker 2 — Workflow back navigation

| | |
|---|---|
| **Symptom** | Founder cannot return to a previous step |
| **Root cause** | `WorkflowService.retreat()` and domain `RETREAT` transitions existed and were unit-tested, but **no HTTP route, WTForm, or workspace control** exposed them. Stage strip was display-only. |
| **Fix** | `POST .../retreat` + Back button when `can_retreat` |

---

## Blocker 3 — Version assignment

| | |
|---|---|
| **Symptom** | Generic flash: “We couldn't assign this version…” |
| **Root causes** | 1. UI/placeholder/`FLASH_WARNING` told Founders to use **semver `1.0.0`**, while Management `VersionPolicy` requires **`YYYY.N` (e.g. 2026.1)**. 2. Form accepted any non-empty string. 3. Management `PolicyViolation` was not mapped to actionable Studio copy. 4. `assign_version` did not restore Management subject after process restart (unlike `get_workspace` reconciliation). |
| **Fix** | Form + flash + guidance aligned to `YYYY.N`; map Management errors; reconcile/ensure subject before `create_version`; surface field-level validation errors |

---

## Blocker 4 — Restart workflow

| | |
|---|---|
| **Symptom** | Cannot restart curriculum creation |
| **Root cause** | `WorkflowService.reset()` → `SUBJECT` (Founder Upload) existed with no route/UI |
| **Fix** | `POST .../reset` + “Restart workflow”; resets stage only (no duplicate records; documents retained) |

---

## Blocker 5 — Subject lifecycle

| | |
|---|---|
| **Symptom** | Cannot remove obsolete subjects |
| **Root cause** | Catalogue filtered “Archived” but had **no mutate path**. `WorkspaceStatus.ARCHIVED` / `ABANDONED` and registry `delete_workspace` existed unused. |
| **Fix** | Delete draft (unpublished); Archive published (protects student history); clear messaging when delete is blocked |

---

## Blocker 6 — Duplicate subject rows

| | |
|---|---|
| **Symptom** | Duplicate information below the table |
| **Root cause** | Responsive dual markup (table + mobile `<ul class="ds-catalogue__list ds-list">`). `.ds-catalogue__list { display: none }` lost to later `.ds-list { display: flex }` (equal specificity) — **both visible on desktop**. |
| **Fix** | Compound selector `.ds-catalogue__list.ds-list { display: none }` (desktop); flex only in mobile media query |

---

## Out of scope (confirmed untouched)

Runtime · SCI · recommendation engine · curriculum processing algorithms · educational twin logic.
