# Dashboard Philosophy

**Programme:** DX-001  
**Status:** Binding  

---

## Definition

A dashboard in Kwalitec is a **decision surface**, not a reporting wall.

Its job is to answer the screen’s one question and move the user into action.

It is not a place to admire database statistics.

---

## Canonical questions

| Surface | One question |
|---|---|
| **Founder Console** | What should I work on next? |
| **Student Home / Dashboard** | What should I study next? |
| **Subject / Curriculum Workspace** | What is the next publication task? |

Any widget that does not serve that question is a candidate for removal.

---

## Action over analytics

| Put first | Put later or nowhere |
|---|---|
| Next mission / next publish step | Historical totals |
| Blocking errors / approval queue | Subjects created |
| Clear Primary CTA | Topics imported |
| Decision-critical status | Vanity KPI grids |

**Default KPI policy: no KPI cards.** See `COMPONENT_GUIDELINES.md`.

---

## Layout model

Recommended primary viewport:

```
┌─────────────────────────────────────────────┐
│ Page Heading                                │
│                                             │
│ [ Primary next action / decision object ]   │
│                                             │
│ Critical status (only if it changes action) │
│                                             │
│ Supporting list or table (tasks / items)    │
│                                             │
│ Secondary links (quiet)                     │
└─────────────────────────────────────────────┘
```

Not:

```
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ KPI  │ │ KPI  │ │ KPI  │ │ KPI  │
└──────┘ └──────┘ └──────┘ └──────┘
┌──────────── cards everywhere ───────────────┐
```

---

## Founder Console

- Lead with **work to do** (blockers, approvals, unfinished publication steps).  
- Avoid admin-heavy inventory views as the home hero.  
- Deep lists belong on dedicated catalogue pages — linked quietly.  
- One Primary: the highest-leverage next task.

---

## Student Home

- Lead with **what to study next** (mission / session entry).  
- Supporting readiness or coach explanation: concise, not paraphrased six times.  
- Do not compete with a second “dashboard” personality or duplicate duration facts.  
- Analytics and history are secondary routes — not equal heroes.

---

## Subject / Curriculum Workspace

- Lead with **next publication task** in the pipeline.  
- Show stage-critical blockers, not document counts as vanity.  
- Prefer tables and stage lists over card mosaics.  
- Operator guidance: labels and status — not tutorial essays.

---

## Density

Professionals prefer a calm primary column with an efficient table over a colourful card board.

Whitespace between sections is success. Filling gaps with charts is failure.

---

## Navigation calm

- No duplicated CTAs across sidebar, header, and hero.  
- No competing “homes.”  
- No dashboard overload: if everything is pinned, nothing is priority.

---

## Success test

A peer can open the dashboard and, within three seconds, say:

> “I should do **X** next.”

If they instead say “there’s a lot going on,” the dashboard fails DX-001.
