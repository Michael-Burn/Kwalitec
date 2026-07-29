# FV-001B — Navigation Audit

**Date:** 2026-07-28  
**Question:** Is the next action obvious at each Founder Studio step?

---

## Overall

**Partial.** Sidebar IA for Curriculum Authority is coherent. In-workspace and “open existing subject” paths still create stalls and false confidence.

---

## Navigation map (observed)

```
Sign in
  → Console Home (Overview)
       ├─ Subjects
       ├─ Curriculum Studio
       ├─ Review Queue
       ├─ Publishing
       ├─ Versions
       ├─ Quality
       ├─ Students / Settings / Support
       └─ Workspace /console/studio/workspaces/ws-{code}
```

Landing after founder login: **Console Home**, not Subjects or Studio.

---

## Step-by-step next-action clarity

| Step | Expected next action | What the UI suggests | Clarity |
|---|---|---|---|
| After login | Start curriculum prep | Ops pulse + Platform Health 0% | **Poor** |
| From Home to Subjects | Click Subjects | Sidebar label clear | **Good** |
| Empty Subjects | Create Subject | Form + NEXT STEP text | **Good** |
| After Create Subject | Open Workspace | Success flash; NEXT STEP still “create then open”; must type code again | **Fair** |
| Open existing subject | Resume workspace | Open Workspace form **creates** and errors if exists; must click list row | **Poor** |
| In workspace (no docs) | Upload CMP + Syllabus | NEXT STEP + blocking findings | **Good** |
| After upload | Validate / review structure | Advance / Validate / Preview all visible; contradictory status copy | **Poor** |
| Review Queue nav | Correct extraction | Hub with workspace link only — no structure UI | **Poor** |
| Publishing nav | Publish Ready | Hub blurb good; action only inside workspace | **Fair** |
| After failed publish | Fix blockers | Flashes name version/approval; preview still 0 nodes | **Fair** (message) / **Fail** (recovery) |
| Return to catalogue | Confirm Ready | Stage crumb only; Published 0 | **Poor** |

---

## Redundant / competing paths

1. **Subjects vs Curriculum Studio** — both host Create Subject + Open Workspace; easy to wonder which is canonical.
2. **Four hubs** (Review Queue, Publishing, Versions, Quality) — nearly identical shells; compete with workspace stages.
3. **Workflow strip vs Workflow stages vs action buttons** — three parallel progress metaphors (strip on hubs, stage rail in workspace, Validate/Preview/Approve/Publish buttons).

---

## Dead ends / traps

| Trap | Evidence |
|---|---|
| Open Workspace with existing code | Flash: *couldn't open a new workspace because one already exists… Open the existing workspace from the dashboard* |
| Clicking Approve/Publish early | Correct refusal — good — but NEXT STEP may still say validation looks ready |
| Expecting Review Queue to show topics | Empty of extractables; must return to workspace tabs |

---

## What to fix for navigation confidence

1. Post-login Founder home: primary CTA **Subjects** or **Continue curriculum setup**.
2. Open Workspace → if exists, **navigate to it** (do not error).
3. Catalogue row: one **Open** button + Ready/Draft badge.
4. Either deepen hubs or fold them into Studio stages.
5. Single source of truth for “what is blocking Ready” pinned at top of workspace.

---

## Navigation score

**4 / 10** for end-to-end Founder Studio publication path.
