# Approval Pipeline Report

**Programme:** PI-002  
**Stage:** Approval

---

## 1. Approval entry points

| Path | Service method | Used by Founder UI? |
|---|---|---|
| Primary | `PublicationService.approve` | Yes — `POST .../approve` |
| Alternate | `PreviewService.approve` | Available; not the workspace Approve button |

Workspace Approve uses **PublicationService.approve**.

---

## 2. Prerequisites (PublicationService.approve)

```text
1. Management port available
2. workspace.version_id present
3. workspace.facts.validation_passed is True
4. mgmt.preview_version(version_id) succeeds
   (advances Management BLUEPRINT_ASSIGNED → PREVIEW_READY when applicable)
5. mgmt.approve(version_id, ...)
6. Studio facts: preview_approved=True, blueprint_assigned=True
```

On success: checklist gains `preview_approved`; Management state → `approved`.

---

## 3. Why approval never succeeds (Founder path)

Earliest blocker encountered:

```text
PublicationError("Approval requires successful validation")
```

Because `validation_passed` remains False after Validation investigation failure.

FV-001B Re-run `C4_approve` never shows approval success; checklist stays without preview approval.

---

## 4. Why Approve shows Publish refusal copy

`recover_flash` for `PublicationError`:

| Message contains | Flash |
|---|---|
| `not ready` / `blocking` | `FLASH_WARNING["publish"]` |
| `version` | Version-missing publish copy |
| else | **`FLASH_WARNING["publish"]`** (default) |

`"Approval requires successful validation"` matches the **else** branch → generic **publish** warning:

> We couldn't publish this curriculum. Publication without approval and a version would expose incomplete material to students…

This is LB-R3. The action was Approve; the copy talks about Publish. Approval is not entangled in the service — the **flash mapper** collapses distinct PublicationError causes into publish language.

Incomplete-workspace Approve (no version) hits the `version` branch — also publish-flavoured copy (seen in `C7_incomplete_approve`).

---

## 5. Preview dependency

Approve intentionally calls `mgmt.preview_version` before `mgmt.approve` so Management reaches `PREVIEW_READY` (FV-001B-R1 wiring).

That call is never reached when validation_passed is false.

---

## 6. Persistence

| Artefact | Persistence |
|---|---|
| `preview_approved` fact | StudioRegistry (in-memory) |
| Management approval decision | CurriculumCatalogue (in-memory) |
| Foundation founder_review | SQLAlchemy (only later, on publish bridge) |

No durable Studio fact store. Within one process session, facts persist on the singleton service; they are not DB-backed.

---

## 7. State transitions on success (expected)

| Layer | Before | After |
|---|---|---|
| Management | `preview_ready` | `approved` |
| Studio fact | `preview_approved=False` | `True` |
| Checklist | missing preview item | satisfied |
| Workflow stage | may remain wherever Founder navigated | not auto-advanced by approve |

---

## 8. Evidence

- `_evidence/complete.json` → `C4_approve` flashes (publish copy, duplicated)
- Reproduction: `PublicationError Approval requires successful validation` → publish flash text
- Code: `publication_service.py` approve; `operator_guidance.py` recover_flash
