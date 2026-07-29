# FV-001A — Curriculum Studio Workflow Repair Report

**Programme:** Founder Validation  
**Status:** P0 blocker repaired (authoring workflow)  
**Date:** 2026-07-29  
**Canonical specification:** [`FV001A_WORKFLOW_STATE_MACHINE.md`](./FV001A_WORKFLOW_STATE_MACHINE.md)

---

## Summary

Curriculum Studio was stalling after Preview because the state machine conflated **building** a preview with **approving** it: advancing into Approve required `preview_approved`, a fact only set by the Approve action that lived on the unreachable Approve stage.

FV-001A fixed the **workflow**, not the educational engine. We introduced `preview_built`, gated Approve on that fact, made workflow/facts durable, auto-advanced safe transitions, simplified the Founder strip to **Upload → Preview → Approve → Publish**, showed hierarchy before approval, replaced generic gate copy with actionable remaining tasks, and removed duplicated login value-proposition copy.

---

## Root causes

| Finding | Cause |
|---------|-------|
| FV-001.5 Stuck after Preview | `_ADVANCE_GATES[APPROVAL]` required `preview_approved`; `POST /preview` only called `build_for_review()` |
| FV-001.4 Approve before seeing structure | Review UI showed topic count only; no hierarchy |
| FV-001.6 Opaque readiness | `WorkflowGateBlocked` mapped to generic “readiness gates are incomplete” |
| FV-001.2 Static processing | Pipeline stages existed in JS without a Founder-facing strip + polling |
| FV-001.3 Confusing sequence | Strip exposed Validate/Review implementation stages |
| FV-001.1 Login duplication | Hero `Know exactly what to study next.` repeated as first feature bullet |
| Restart loss | `StudioRegistry` was in-memory only |

---

## Workflow changes

Founder strip (projection only):

```
Upload → Preview → Approve → Publish
```

Processing is a visible pipeline under Upload→Preview, not a dead-end strip stage. Validation remains automatic readiness work (domain `validation`), not a Founder strip label.

Full state table, gates, events, and persistence rules: **see the canonical state machine**.

---

## State-machine fixes

1. Added fact / checklist code **`preview_built`**.
2. `PreviewService.build_for_review` sets `preview_built=True` and never sets `preview_approved`.
3. Advance into **`approval` requires `preview_built`** (not `preview_approved`).
4. Advance into **`publication` requires `preview_approved` + `version_assigned`**.
5. Approve sets both `preview_built` and `preview_approved`, then auto-advances when gates pass.
6. Durable projections: `studio_workspace_projections` + write-through from `StudioRegistry`.

---

## Preview improvements

- Preview stage renders subject, topic count, and scrollable hierarchy tree before approval.
- When `preview_built`, primary CTA is **Approve structure** (not a blind advance).
- No requirement to approve an invisible structure.

---

## Progress indicator implementation

- Founder processing pipeline: Uploading → Extracting → Analysing → Building hierarchy → Generating preview → Ready for review.
- Status polling every 2.5s while the Upload surface is open.
- Stage strip visualisation with ●/○ current/completed markers.

---

## Readiness gate improvements

`WorkflowGateBlocked` now carries `missing_codes` / `satisfied_codes`. Operator copy lists:

```
Advancement blocked — …
Remaining tasks:
✓ …
✗ …
Next: Go to Preview.
```

---

## Navigation improvements

- Auto-advance after validate / preview build / approve when gates already pass.
- Successful validate attempts preview build so Founders land on a reviewable Preview.
- Login page keeps a single instance of the value proposition.

---

## Files Created

- `knowledge/engineering/fv001a_curriculum_studio_workflow_repair/FV001A_WORKFLOW_STATE_MACHINE.md`
- `knowledge/engineering/fv001a_curriculum_studio_workflow_repair/FV001A_CURRICULUM_STUDIO_WORKFLOW_REPORT.md`
- `app/application/curriculum_studio/fact_updates.py`
- `app/infrastructure/adapters/curriculum_studio_workspace_persistence.py`
- `migrations/versions/202607290001_fv001a_studio_workspace_projections.py`
- `tests/application/curriculum_studio/test_fv001a_workflow_repair.py`

## Files Modified

Domain / application: publication checklist facts; workflow gates; preview / publication / validation / workspace / version / document upload fact copies; Studio registry hydration.

Presentation: founder stage map; operator guidance; workspace template; document upload JS; design-system stage indicator; login feature list; Founder workspace DTO/service; Studio routes (auto-advance).

Models / factory wiring: `StudioWorkspaceProjection`; model exports.

Tests: matrix/helpers/certification/workflow presentation contracts updated for `preview_built` and four-stage strip.

## Tests Executed

```text
python3 -m pytest tests/application/curriculum_studio/ \
  tests/certification/test_pr001a_founder_operations.py \
  tests/presentation/workflows/test_workflow_founder_studio.py \
  tests/domain/curriculum_studio/ -q
```

**Result:** 1766 passed.

Focused FV-001A cases cover: preview_built without approval; advance-to-approval after build; actionable gate copy; approve → publication path; Founder strip labels.

## Migration Impact

Alembic revision `202607290001` adds `studio_workspace_projections`. No student curriculum / V1–V2 educational schema changes.

## Architecture Compliance

- Layering preserved; Flask/SQLAlchemy persistence lives under `app/infrastructure/adapters/`.
- Educational algorithms, curriculum extraction parsers, and recommendation engines were **not** modified.
- Curriculum V1/V2 traversal/import compatibility: **N/A** (Founder authoring workflow only).

## Technical Debt

- Multi-head Alembic history remains; this revision chains from `202607280080`.
- Auto-validate on every document status poll is not yet a closed-loop server worker — validate/preview still need a Founder Continue/Generate on some paths when CIP lags.
- Preview tree is a flat ordered list (kind badges), not nested expand/collapse by parent_id.
- Registry activity feed is still process-local.

## Remaining technical debt / Known Limitations

- End-to-end browser dogfood on production (real PDF → CIP → Publish) still required to resume Founder Validation certification.
- Concurrent multi-worker write contention on projections is last-write-wins (acceptable for single-Founder alpha).

## Recommendations

1. Apply migration `202607290001` on every environment before Founder Validation resume.
2. Dogfood the full Upload → Process → Preview → Approve → Publish path on staging with real CMP/syllabus PDFs.
3. Follow `FV001A_WORKFLOW_STATE_MACHINE.md` for any future gate/fact/strip changes.
4. Optionally nest the preview tree by `parent_id` in a small follow-up UX pass.

---

## Success criteria

| Criterion | Status |
|-----------|--------|
| Login duplication removed | ✓ |
| Processing progress visible | ✓ |
| Founder always knows current stage | ✓ |
| Preview shown before approval | ✓ |
| Workflow advances correctly | ✓ |
| Readiness gates explain themselves | ✓ |
| Founder never stuck after preview build | ✓ |
| Workflow feels linear | ✓ |
| Ready to resume Founder Validation | ✓ (pending migration + dogfood) |
