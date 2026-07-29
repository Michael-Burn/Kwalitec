# Implementation Plan

**Programme:** DX-004C  
**Status:** Plan for subsequent UI execution (not executed in DX-004C)  
**Release Candidate:** `RC-2026.07.29-01`  
**Depends on:** This corpus + DX-001 / DX-002 / DX-003 / DX-004A / DX-004B  

---

## Scope boundary

| DX-004C (this programme) | Later execution |
|---|---|
| Architecture, stage model, wireframe, findings/transitions/errors, scorecard | Template + CSS + view-model |
| Documentation only | Route/nav hub collapse coordination |
| No application code | `workspace.html` + Studio chrome redesign |

DX-004C does **not** ship UI. The following is the ordered plan for the implementation milestone that consumes these artefacts.

---

## Phase 0 — Preconditions

1. Treat `WORKSPACE_ARCHITECTURE.md` + `STAGE_MODEL.md` + `WORKSPACE_WIREFRAME.md` as binding.  
2. Confirm Subjects Open and Home Resume land on workspace at persisted stage (DX-004B / DX-004A contracts).  
3. Map Founder stages ↔ domain `WorkflowStage` in presentation labels (no engine rewrite required for first UI slice).  
4. Do not resurrect Review/Publishing hubs during this work.  
5. Coordinate with DX-004D for Approve/Publish confirm copy refinement — may ship after basic stage chrome.

---

## Phase 1 — Structure & content (before token polish)

1. Replace workspace body with: Persistent context → L0 → L1 → L2 → L3.  
2. Delete Validation / Preview / Checklist metric card row.  
3. Collapse multi-Primary clusters to one Primary per stage (`PRIMARY_ACTION_BY_STAGE` + blocking override).  
4. Present blocking findings at L0; warnings demoted.  
5. Stage strip uses Founder labels: Upload · Validate · Review · Approve · Publish.  
6. Omit empty L2; collapse L3 by default.

**Exit:** One question answerable without scroll; one Primary; no KPI readiness cards.

---

## Phase 2 — View-model

1. Workspace DTO:  
   - Persistent: code, name, version, current_stage (Founder label)  
   - L0: primary_label, primary_action, blocking_count, blocking_findings[]  
   - L1: stage-specific payload (documents / validation / preview / approval / publish)  
   - L2: supporting summaries (optional)  
   - L3: workspace_id, timestamps, diagnostics  
2. Primary selection algorithm per `STAGE_MODEL.md`.  
3. Stop feeding workspace with dashboard-style aggregate cards.  
4. Ensure publish success redirects to Home and recent-publications list includes the item.

**Exit:** Workspace renders without legacy three-up readiness cards.

---

## Phase 3 — Continuity & errors

1. Persist/restore stage on Open/Resume/refresh.  
2. Inline error surfaces for upload/process/validate/publish failures.  
3. Focus management after failed submit → recovery Primary.  
4. Disable unlawful future-stage strip activation.

**Exit:** Continuity + error recovery specs satisfied in live UI.

---

## Phase 4 — Navigation cleanup

1. Remove/redirect Review Queue and Publishing hub destinations (if still present) to Subjects filters or workspace stages.  
2. Quiet Exit / Back to Subjects only — not a second Primary.  
3. Align breadcrumbs: Home · Subjects · {Subject name} (prefer over Studio dashboard as parent when Subjects is catalogue of record).

**Exit:** No peer hub reachable mid-execution.

---

## Phase 5 — Visual system compliance

1. DX-001 type scale and spacing.  
2. Semantic status colour; no gold chrome.  
3. Sticky persistent context on desktop if it does not hide Primary.  
4. Keyboard order per wireframe.  
5. Re-run `PREMIUM_SCORECARD.md`; all ≥9.

**Exit:** Scorecard PASS on live UI.

---

## Phase 6 — Guardian & copy

1. Update UI Guardian: Workspace L0–L3, one Primary, no KPI cards, Review/Publish as stages only.  
2. Align `TERMINOLOGY_DICTIONARY.md`: Workspace one-sentence; Review/Publish as stages.  
3. DX-004D may refine Approve/Publish decision copy without changing stage model.

---

## Sequencing with sibling programmes

| Programme | Relationship |
|---|---|
| DX-004A Home UI | Resume must open workspace stage — contract already designed |
| DX-004B Subjects UI | Open must enter workspace immediately |
| **DX-004C UI** | This plan |
| DX-004D | Review & Publish flow refinement inside stages |

Prefer: stable Open/Resume contracts before or tightly coupled with Workspace chrome.

---

## Non-goals (implementation)

- Curriculum engine / V1–V2 traversal changes  
- Student catalogue changes  
- New LLM/AI in publication path  
- Rebuilding domain `WorkflowStage` enum names (label map is enough initially)

---

## Risk notes

| Risk | Mitigation |
|---|---|
| Preview UI still large | Contain under Review L1; do not spawn peer nav |
| Operators habitually use hubs | Redirect + Guardian; Subjects filters |
| Publish confirm UX ambiguous | Defer polish to DX-004D; keep single Primary |
