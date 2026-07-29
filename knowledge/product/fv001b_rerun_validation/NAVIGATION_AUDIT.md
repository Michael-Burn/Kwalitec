# FV-001B Re-run — Navigation Audit

---

## Global navigation

| Item | Clarity | Notes |
|---|---|---|
| CURRICULUM AUTHORITY sidebar | High | Founder recognises curriculum ops home |
| Subjects | High | Direct catalogue |
| Curriculum Studio | High | Primary authoring hub |
| Review Queue / Publishing / Versions / Quality | Medium | Present; not required if workspace Actions work |
| Console Home | Medium | Ops pulse; curriculum CTA not hero |

---

## Intended journey vs NEXT STEP

| Moment | Visible NEXT STEP | Actual state | Gap |
|---|---|---|---|
| Fresh workspace | Confirm subject / advance to Content Sources | Empty uploads | OK |
| Both docs Ready (CS1U) | Often still “Confirm…” or “Run validation after both… uploaded” | Docs Ready, topics extracted | **Stale** |
| After Validate failure | “Run validation after both official documents are uploaded…” | Docs already uploaded & Ready | **Misleading** |
| After Preview success flash | Same validation NEXT STEP | Preview claimed success; status `not_ready` | **Contradictory** |
| After Approve click | Unchanged | Publish refusal flash | **No approval progress** |

---

## Action control placement

- Advance / Validate / Preview / Approve / Publish sit in an **Actions** block far below Content Sources and review tabs.
- Controls are `input[type=submit]` with values as labels — visible, but easy to miss without scrolling.
- Workflow strip implies a linear stage; stage marker lags (stuck on Subject/Validation while topics already exist).

---

## Next-action clarity score

| Phase | Score (0–10) | Why |
|---|---|---|
| Login → Console | 7 | Sidebar obvious |
| Subjects / Studio | 8 | Create/Open clear |
| Upload | 7 | Slots clear; auto-upload surprising but OK |
| After upload Ready | 3 | NEXT STEP + Validate failure without findings |
| After preview flash | 2 | Success vs not_ready |
| Approve / Publish | 1 | Wrong flash attribution; no success path |
| Catalogue Ready check | 2 | Never Ready |

---

## Navigation defects

1. **Stale NEXT STEP** after documents Ready.  
2. **Validate failure without findings UI** — dead end.  
3. **Approve labelled action produces Publish messaging.**  
4. **No single “you are blocked because X; click Y” pattern** once extraction completes.
