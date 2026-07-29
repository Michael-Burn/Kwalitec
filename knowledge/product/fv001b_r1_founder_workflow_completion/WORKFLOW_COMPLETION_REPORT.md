# FV-001B-R1 — Workflow Completion Report

**Programme:** FV-001B-R1  
**Date:** 2026-07-28

---

## Intended Founder path (now wired)

```text
Create Subject
    ↓
Open Workspace
    ↓
Upload Official CMP  (kind=cmp bound to labelled slot)
Upload Official Syllabus  (kind=syllabus bound to labelled slot)
    ↓
Document processing / extraction completes
    ↓
Validate  → structure sync + default blueprints + Management gate
    ↓
Build Preview  → meaningful topics required (else warning, no success flash)
    ↓
Approve  → Management PREVIEW_READY then approval; preview_approved fact
    ↓
Publish  → rollback snapshot + Management publish + Foundation Ready package
    ↓
Subjects catalogue shows Ready · Current Version · Published Date
Students discover Ready subject via Subject Catalogue (dev bridge default)
```

---

## Gate wiring (before → after)

| Checklist / gate | Before R1 | After R1 |
|---|---|---|
| `cmp_uploaded` / `official_syllabus_uploaded` | Upload | Upload (unchanged) |
| `validation_passed` | Validate (often failed: missing blueprints) | Validate after auto blueprint assign |
| `blueprint_assigned` | No Founder UI | Satisfied during validate preparation |
| Preview content | 0 topics + success flash | Topics from CIP/Management; empty fails |
| `preview_approved` | Approve sets fact; Management often not PREVIEW_READY | Approve calls preview gate first |
| `version_assigned` | Upload / Assign Version | Unchanged |
| `rollback_snapshot_created` | No UI | Auto-created on publish intent |
| Student Ready | Management only | Foundation package + catalogue |

---

## Contradiction removals

1. **Preview** — success flash only after `build_for_review` with `node_count > 0`; summary never says “Preview ready · not_ready · 0 nodes”.
2. **Validation NEXT STEP** — no longer claims “Validation looks ready” while validation is incomplete.
3. **Publish refuse** — incomplete path still refused; complete path can succeed.

---

## Explicit non-goals

- No Educational Intelligence redesign
- No Runtime Integration / LP-001 / VP-001 / Curriculum Authority model redesign
- No weakening of publication safety policies
