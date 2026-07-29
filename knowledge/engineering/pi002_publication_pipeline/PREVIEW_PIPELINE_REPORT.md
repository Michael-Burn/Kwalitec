# Preview Pipeline Report

**Programme:** PI-002  
**Stage:** Preview

---

## 1. What Preview does

`PreviewService` (`app/application/curriculum_studio/preview_service.py`):

| Method | Behaviour |
|---|---|
| `preview` | Build hierarchy from Management `preview_version` payload, else CIP/workspace structure |
| `build_for_review` | Call prepare (best effort), then `preview`; **raise** if `node_count <= 0` |
| `approve` / `reject` | Optional Management approve/reject + fact updates |

Route `/workspaces/<id>/preview` calls `build_for_review` and flashes success with topic count.

---

## 2. Hierarchy / package / nodes

### Management preview

Management `PreviewService.preview` requires:

- Version state ≥ `validated` (rejects `draft` / `uploaded`)
- Non-empty curriculum package

On success from `blueprint_assigned`, advances to `preview_ready`.

Payload shape uses `section_refs` / `assignment_sections` / `asset_labels` (not always `hierarchy`/`nodes`). Studio `_nodes_from_payload` maps both shapes.

### Studio fallback

If Management preview fails or returns empty nodes, Studio builds nodes from:

1. `StructurePreparationService.hierarchy_nodes` (CIP / Foundation titles)
2. Else workspace `section_ids` / `topic_ids`

CIP extraction therefore can populate Preview **even when** Management preview is thin or unavailable.

---

## 3. Readiness calculation

`PreviewSummary.create`:

```text
if readiness is None:
  if nodes and validation_passed → ready_for_review
  else → not_ready
```

`publication_ready` is `workspace.ready_to_publish` (full checklist) — stricter than preview review readiness.

---

## 4. Why Preview never reaches Ready / ready_for_review

| Hypothesis | Verdict | Evidence |
|---|---|---|
| No package exists | **Not primary** | Documents Ready; Management can hold assets; CIP topics exist |
| Package incomplete | Possible secondary | Management preview may be thin; Studio falls back to CIP nodes |
| State incorrect | **Yes** | `validation_passed=False` forces `PreviewReadiness.NOT_READY` even with nodes |
| Readiness incorrectly calculated | Partially | Calculation is intentional: requires validation. Success flash ignores that rule |

**Dominant answer:** Preview fails to become review-ready because **validation never passed**, not because topics are missing.

---

## 5. Success vs not_ready contradiction

`build_for_review` success criterion: `node_count > 0` only.

Route flashes:

> We've built the preview successfully — {count} curriculum topics ready to review.

Workspace card uses `friendly_preview_summary`:

> Preview needs attention · not_ready · N topics

FV-001B Re-run LB-R2 matches this exact split.

Reproduction after failed validation with structure present:

```text
preview nodes >= 1
readiness = not_ready
validation_passed = False
```

---

## 6. Topic count disagreements

Observed in re-run: Structure/Overview topic counts can differ from Preview node counts because:

- Structure panel reads CIP / intelligence projections
- Preview may use Management section_refs (coarser) or a subset of prepared hierarchy
- Stub ingestion topics (`topic-e-1`) are unrelated to CIP topics

This is a consistency defect, not the gate that blocks Ready.

---

## 7. Transition conditions

| Step | Expected | Actual when validation failed |
|---|---|---|
| Build preview with topics | Success | Often succeeds |
| Preview readiness → `ready_for_review` | After validation | Stays `not_ready` |
| Management → `preview_ready` | On Management preview from `blueprint_assigned` | May advance independently of Studio fact |
| Studio fact `preview_approved` | After Approve | Never set |

Note: Management can show version status `preview_ready` while Studio checklist still lacks `validation_passed` / `preview_approved` — another cross-layer inconsistency.

---

## 8. Downstream consumers

- Approve requires meaningful preview content **and** `validation_passed`
- Founder UI preview summary card
- Publication checklist does **not** have a separate “preview built” fact — only `preview_approved`
