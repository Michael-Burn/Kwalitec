# FV-001A — Curriculum Studio Workflow State Machine

**Status:** Canonical specification  
**Programme:** Founder Validation · FV-001A  
**Authority:** Future Curriculum Studio development must follow this document.  
**Companion:** `FV001A_CURRICULUM_STUDIO_WORKFLOW_REPORT.md` (delivery report)

---

## 1. Purpose

Define the Founder publication workflow so the authoring experience is linear,
transparent, and free of dead ends. The educational engine is out of scope —
this specification governs **workflow communication, facts, transitions,
navigation, and readiness gates** only.

---

## 2. Founder mental model (product states)

These are the states the Founder must understand. The UI stage strip exposes
**Upload → Preview → Approve → Publish**. Processing is a visible **in-progress
pipeline** during the Upload→Preview transition, not a dead-end screen.

| State | Entry condition | Exit condition |
|-------|-----------------|----------------|
| **Upload** | Workspace opened / subject created; Founder may upload CMP + syllabus | Both required documents are uploaded **and** processing has started |
| **Processing** | Document upload succeeded; extraction / validation / hierarchy work running | `preview_built = true` (hierarchy available for review) |
| **Preview** | `preview_built = true`; Founder can inspect subject / sections / topics | Founder explicitly **Approves** structure → `preview_approved = true` |
| **Approval** | `preview_approved = true`; structure is accepted for release | Publish enabled (version + remaining publish gates complete) |
| **Published** | Publication complete via Management + Foundation Ready bridge | **Terminal** |

### Non-negotiable product rules

1. The Founder always sees generated curriculum **before** approving it.
2. `preview_built` and `preview_approved` are **different facts**.
3. Advancing into Approve must **not** require `preview_approved` (that caused the Preview stall).
4. Validation is an **automatic** readiness step inside Processing — not a Founder-facing strip stage.
5. The UI reflects true workflow state; it must not mask incorrect gates with copy-only workarounds.

---

## 3. Domain stages (implementation vocabulary)

Domain `WorkflowStage` remains the persisted stage token on the workspace
workflow aggregate. Founder labels are a projection.

| Domain stage | Founder strip | Role |
|--------------|---------------|------|
| `subject` | Upload | Product identity confirmed |
| `content_sources` | Upload | Document upload / replace |
| `validation` | Upload *(Processing)* | Automated structural readiness |
| `preview` | Preview | Inspect hierarchy; approve structure from here |
| `approval` | Approve | Release approval recorded; prepare publish |
| `publication` | Publish | Assign version if needed; publish |

Canonical order:

```
subject → content_sources → validation → preview → approval → publication
```

Lawful events: `ADVANCE`, `RETREAT`, `RESET`, `JUMP_TO_*` (application gates
apply on forward jumps).

---

## 4. Publication facts

Facts are boolean inputs. Checklist items are **computed** from facts and are
never manually toggled.

| Fact | Set by | Meaning |
|------|--------|---------|
| `cmp_uploaded` | Document upload / refresh | Official CMP present |
| `official_syllabus_uploaded` | Document upload / refresh | Official syllabus present |
| `validation_passed` | Validation service (auto or explicit) | Structure passed readiness checks |
| `blueprint_assigned` | Validation / structure prep | Blueprint / structure bound |
| **`preview_built`** | `PreviewService.build_for_review` success | Hierarchy exists and is reviewable |
| **`preview_approved`** | Approve action (`PreviewService.approve` / `PublicationService.approve`) | Founder accepted structure |
| `version_assigned` | Version assign | Immutable version label bound |
| `rollback_snapshot_created` | Publish safety path | Rollback snapshot exists |

Derived: `ready_to_publish` when all publication prerequisites (including
`preview_approved`, `version_assigned`, rollback) are satisfied.

### Critical distinction

| Fact | Answers |
|------|---------|
| `preview_built` | “Can the Founder **review** the structure?” |
| `preview_approved` | “Has the Founder **accepted** the structure?” |

---

## 5. Advance readiness gates

Gates apply when **entering** the target domain stage via forward transition.

| Target stage | Required facts | Rationale |
|--------------|----------------|-----------|
| `content_sources` | _(none)_ | Open upload surface |
| `validation` | `cmp_uploaded`, `official_syllabus_uploaded` | Both sources required |
| `preview` | `validation_passed` | Do not review unvalidated structure |
| **`approval`** | **`preview_built`** | Structure must be visible; approval has **not** happened yet |
| `publication` | `preview_approved`, `version_assigned` | Publish only after Founder approval + version |

### Root cause of the Preview stall (pre-FV-001A)

```
POST /preview  →  build_for_review()   # sets nothing on preview_approved
Continue to Approve → ADVANCE → approval
Gate for approval required preview_approved   # DEADLOCK
preview_approved only set on Approve stage UI  # unreachable
```

**Corrected gate:** entering `approval` requires `preview_built`, not
`preview_approved`. Approving sets `preview_approved` and enables Publish.

---

## 6. Events that advance each Founder state

| From → To | Triggering event | Fact / stage effect |
|-----------|------------------|---------------------|
| Upload → Processing | Successful PDF upload (CMP and/or syllabus) | Upload facts; CIP pipeline starts; UI shows stage pipeline |
| Processing → Preview | Pipeline + auto-validation succeed; preview hierarchy built | `validation_passed`; **`preview_built=true`**; domain stage → `preview` |
| Preview → Approval | Founder clicks **Approve** | **`preview_approved=true`**; domain stage → `approval` (then typically auto-advance toward Publish when safe) |
| Approval → Publish enabled | Approve recorded + version assigned | Enter / remain on `publication` with publish CTA enabled |
| Publish → Published | Successful `publish` | Workspace `PUBLISHED`; Foundation Ready package; terminal |

Retreat and reset remain lawful domain events for recovery; Founder UI should
prefer explicit recovery CTAs over silent jumps.

---

## 7. Persistence

| Concern | Store | Durable? |
|---------|-------|----------|
| Documents / processing stage | `studio_foundation_documents` (+ storage) | Yes |
| Subjects / versions | Foundation tables | Yes |
| **Workflow stage + publication facts + structure projection** | `studio_workspace_projections` (write-through from Studio registry) | **Yes (FV-001A)** |
| Activity feed | Registry (+ optional audit) | Best-effort |
| Publication authority | Curriculum Management port | Yes (external authority) |

Rules:

1. `put_workspace` write-through persists stage, facts, and structure.
2. `get_workspace` hydrates from DB on cache miss (survives process restart).
3. Documents alone are insufficient — without projection persistence the
   Founder appears stuck on a “missing workspace” after restart.

---

## 8. Client / server synchronisation

| Surface | Mechanism |
|---------|-----------|
| Document upload | Multipart POST → JSON `{document, status}` |
| Processing progress | Poll `documents_status`; render stage pipeline |
| Workspace stage / CTAs | Full page reload after form POST (advance / validate / preview / approve / publish) |
| Preview hierarchy | Server-rendered on Preview stage from `PreviewService` |
| Auto-transition | Server applies advance after successful build/approve when gates pass; response redirects to workspace at new stage |

No hidden client-only stage. Browser never invents `preview_approved`.

---

## 9. Processing pipeline stages (Founder-facing)

Shown after upload while `preview_built` is false:

1. Uploading  
2. Extracting document  
3. Analysing curriculum  
4. Building hierarchy  
5. Generating preview  
6. Ready for review  

Prefer stage-based progress when percentages are unavailable. Never leave a
static page with no progress signal during Processing.

---

## 10. Readiness / blocking UX contract

Every blocking message must include:

1. **What happened**
2. **Why it happened**
3. **How to fix it**
4. **Primary action** (e.g. Go to Preview / Upload documents)

Gate blocks expose a checklist of remaining tasks (satisfied vs missing), not
generic “readiness gates are incomplete” copy alone.

---

## 11. Automation (safe transitions)

Where gates are already satisfied, the server **auto-transitions**:

| After | Auto behaviour |
|-------|----------------|
| Preview built (`preview_built`) | Remain on / move to Preview; open hierarchy review (no extra confirm) |
| Structure approved (`preview_approved`) | Enable Publish path; advance to `publication` when version gates allow |
| Both documents ready + extraction complete | Auto-validate when safe; do not require a separate “Validate” strip click for the happy path |

Do not auto-publish. Publish remains an explicit Founder action.

---

## 12. UI stage strip

```
Upload ──●──── Preview ────○──── Approve ────○──── Publish ────○
```

- Current stage highlighted  
- Completed stages remain visible  
- Processing progress appears **within** Upload→Preview, not as a contradictory strip label  

---

## 13. Regression invariants

1. Building preview never sets `preview_approved`.
2. Approving never occurs without a reviewable hierarchy (`preview_built`).
3. `ADVANCE` to `approval` succeeds when `preview_built` and fails when not.
4. Workflow state survives process restart via durable projection.
5. No Founder-facing dead end after successful preview build.
6. Educational algorithms / curriculum extraction math are unchanged.

---

## 14. Change control

Changes to gates, facts, or Founder strip mapping require an update to **this
document** in the same change set as code. The delivery report may summarise;
it does not supersede this specification.
