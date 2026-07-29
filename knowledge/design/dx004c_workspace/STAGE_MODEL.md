# Stage Model

**Programme:** DX-004C  
**Status:** Binding for Founder-facing workspace stages  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-002 Workspace type, DX-003 Decision Architecture, domain `WorkflowStage`

---

## 1. Purpose

Define the **Founder-facing stage model** so the Workspace is stage-based, not page-based. Each stage is a focused mode with exactly one Primary.

---

## 2. Canonical Founder stages

```
Upload
  ↓
Validate
  ↓
Review
  ↓
Approve
  ↓
Publish
```

| Stage | One question (stage-local) | Completed when |
|---|---|---|
| **Upload** | Are required sources present and processable? | CMP + syllabus (as required) uploaded and processing gates clear |
| **Validate** | Does structure pass readiness checks? | Validation passed; no blocking findings |
| **Review** | Is the student-visible curriculum acceptable? | Founder has confirmed structure/preview is acceptable |
| **Approve** | May this curriculum be approved for release? | Explicit Founder approval recorded |
| **Publish** | Can this release? | Publication succeeds; students may see Ready |

These five are the **only** stage destinations in workspace chrome.

---

## 3. Mapping to domain `WorkflowStage`

Domain enum (authoritative for persistence / transitions today):

| Domain `WorkflowStage` | Founder stage (DX-004C) | Notes |
|---|---|---|
| `subject` | *(pre-workspace / Create)* | Subject creation lands into Upload; not a competing workspace stage strip item |
| `content_sources` | **Upload** | Documents / CMP / syllabus |
| `validation` | **Validate** | Readiness checks + findings |
| `preview` | **Review** | Student-visible structure acceptance |
| `approval` | **Approve** | Founder approval gate |
| `publication` | **Publish** | Release |

**Design rule:** UI stage strip shows the five Founder labels. Domain tokens remain in APIs/persistence until an implementation milestone remaps labels — do not invent parallel stage machines.

If structure preparation is required between Upload and Validate in the engine, it is **sub-work of Upload or Validate**, not a sixth peer stage in the strip.

---

## 4. Primary action by stage

Exactly one Primary. Label reflects the **next** concrete act.

| Stage | Default Primary | When blocked | Forbidden as Primary peers |
|---|---|---|---|
| Upload | **Upload documents** or **Continue processing** | Fix upload / retry processing | Validate, Approve, Publish |
| Validate | **Run validation** or **Continue validation** | **Resolve findings** | Approve, Publish |
| Review | **Confirm structure** / **Continue review** | Return to Validate if blocking | Publish |
| Approve | **Approve** | Resolve blockers / return upstream | Publish (until approved) |
| Publish | **Publish** | Resolve publication blockers | Duplicate “Go to publish hub” |

Secondary actions (add another file, view L2 history, expand finding detail) use quiet / secondary styling.

### Primary selection algorithm

```
if blocking_findings_at_current_stage:
    Primary = Resolve findings (or first recovery action)
else if stage_work_incomplete:
    Primary = stage default (Upload / Validate / Confirm / Approve / Publish)
else:
    Primary = Advance to next stage (or Publish when on Publish and ready)
```

Never show Advance and Approve and Publish as equal Primaries.

---

## 5. Stage header content

| Field | Required | Example |
|---|---|---|
| Current stage name | Yes | Validate |
| Completed summary | Yes (quiet) | Upload complete |
| Next summary | Yes (quiet) | Then: Review |
| Progress essay | No | — |
| Percentage wheel | No | — |

Completed / next may be a single quiet line: `Upload ✓ · Validate (current) · Review →`

---

## 6. Stage content (L1) — what belongs where

### Upload

- Document upload controls for required sources  
- Processing status for in-flight jobs (brief, not novels)  
- Inline errors for failed uploads  

**Not:** validation finding lists, publish checklist theatre.

### Validate

- Run / re-run validation  
- Blocking findings (also mirrored at L0)  
- Quiet warnings under L1/L2  

**Not:** full student preview as the main pane (that is Review).

### Review

- Student-visible curriculum structure / preview sufficient to accept or reject  
- Confirm / request changes  

**Not:** a separate Review Queue of other subjects.

### Approve

- Clear statement of what approval means  
- Approve Primary  
- Link back to Review/Validate only as recovery, not as peer destinations  

### Publish

- Release confirmation of this Subject + version  
- Publish Primary  
- On success → Home + Recent Publications  

**Not:** a catalogue of all publishable subjects.

---

## 7. Review is a stage

| Form | Allowed |
|---|---|
| Review as workspace stage | **Yes** |
| Review as filter on Subjects | Yes (discovery preset) |
| Review as peer catalogue / hub page | **No** |

### Publish is a stage

| Form | Allowed |
|---|---|
| Publish as final workspace stage | **Yes** |
| Ready to publish filter on Subjects | Yes |
| Publishing hub as second catalogue | **No** |

---

## 8. Lawful transitions (Founder model)

Happy path: forward only when stage exit criteria met.

| From | To | Trigger |
|---|---|---|
| Upload | Validate | Sources ready |
| Validate | Review | Validation passed |
| Review | Approve | Structure accepted |
| Approve | Publish | Approved |
| Publish | *(exit)* | Published → Home |

Retreat is allowed when the Founder must fix upstream work (e.g. blocking finding requires re-upload). Retreat must:

- Keep the same workspace  
- Update persistent context stage  
- Set Primary to the recovery action  
- Not dump the Founder onto a hub page  

Domain `ADVANCE` / `RETREAT` / jump events remain the engine; UI must not expose illegal jumps as Primaries (e.g. Publish while Validate blocked).

---

## 9. Continuity

`current_stage` on the workspace is the continuity key.

| Entry | Landing stage |
|---|---|
| Subjects → Open | Persisted `current_stage` |
| Home → Resume / Continue | Persisted `current_stage` |
| Create Subject | **Upload** |
| After successful Publish | Leave workspace → Home |

---

## 10. Stages merged / pages eliminated

| Legacy pattern | DX-004C treatment |
|---|---|
| Review Queue hub | Eliminated as destination; Review stage + Subjects filter |
| Publishing hub | Eliminated; Publish stage + Ready to publish filter |
| Preview as separate “app panel” competing with workflow | Absorbed into **Review** stage content |
| Content Sources as isolated dashboard | Absorbed into **Upload** |
| Validation / Preview / Checklist metric cards | Eliminated; stage L0/L1 owns readiness |
| Multi-step wizard routes as separate products | Single workspace, stage modes |

---

## 11. Success test

A Founder who has never seen Studio should, on opening a workspace:

1. Name the current stage.  
2. Click the only Primary.  
3. Never ask which of five hubs to open next.
