# Reading Flow

**Programme:** DX-003  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`

---

## Canonical sequence

```
Eye enters
    ↓
Recognises page
    ↓
Finds primary action
    ↓
Confirms context
    ↓
Acts
    ↓
Leaves
```

If the eye must loop **backwards** (re-read helpers to understand the button; climb from KPIs to find the task), the screen fails.

---

## Beat definitions

| Beat | What the user needs | Allowed UI |
|---|---|---|
| **Eye enters** | Stable shell; no competing heroes | Quiet chrome; one page heading |
| **Recognises page** | Where am I? | Page title = screen job (one sentence) |
| **Finds primary action** | What do I do? | Exactly one Primary in the first viewport |
| **Confirms context** | Is this the right object / stage? | One line of L1 context (subject, mission, stage) |
| **Acts** | Commit | Click / select / submit |
| **Leaves** | Feedback or next Decision | Flash, navigation, or stage advance |

Context confirmation happens **after** Primary is found — never as a tutorial wall before the action appears.

---

## Pass / fail tests

| Test | Pass | Fail |
|---|---|---|
| F-shape / top-down | Title → Primary → context | KPIs → essay → buried Primary |
| Backwards loop | None | Helper under every control explaining what the label already says |
| Competing Primary | One | Multiple equal-weight buttons in L0 |
| Recognition | Title matches one sentence | Title + eyebrow + greeting restating same idea |
| Exit | Clear leave path | Stay to read ontology |

---

## Target flows (primary screens)

### Student Home

```
Enter shell
  → Recognise "Home" / Mission title
  → Find Start / Continue
  → Confirm duration + one-line why (optional L1)
  → Act
  → Leave to Session
```

**Fails today:** Greeting → Sensei eyebrow → title → status → purpose → educational panel → alternatives → readiness cards → Primary buried among secondary CTAs.

### Curriculum Workspace

```
Enter workspace
  → Recognise subject + stage
  → Find stage Primary (Upload / Validate / Approve / Publish…)
  → Confirm blockers if any (findings list)
  → Act
  → Leave via Feedback (stage advance)
```

**Fails today:** Workflow card → KPI triad → upload essay → pipeline → 9 tabs → Actions grid — Primary ambiguous; eye loops.

### Console Overview

```
Enter Overview
  → Recognise “what needs attention”
  → Find top item Primary
  → Confirm short list context
  → Act
  → Leave to Workspace / queue
```

**Fails today:** Version eyebrow → pulse essay → KPI grids → Quick Actions → detail cards.

### Choose Exam

```
Enter wizard
  → Recognise “Select a published curriculum”
  → Find subject selection
  → Confirm Ready vs Coming Soon
  → Next
  → Leave to step 2
```

**Mostly passes** — protect this pattern.

### Session activity

```
Enter activity
  → Recognise question
  → Find Submit / Continue
  → Confirm progress quietly
  → Act
  → Next item or reflection
```

**Mostly passes** — keep lean.

### History (target)

```
Enter History
  → Recognise practice archive
  → Find session to open
  → Confirm date/duration in row
  → Act
  → Leave to detail
```

**Fails today:** Epistemology essay → KPI cards → dual Journal/Timeline CTAs before archive.

---

## Forbidden reading patterns

| Pattern | Why it fails |
|---|---|
| Tutorial before control | Forces backwards loop after finding the button |
| Status essay as permanent L0 | Recognition of page becomes “read monitoring” |
| Duplicate headings | Recognition costs double |
| Primary below fold with L0 filler above | Action delayed |
| Equal-weight nav + in-page CTAs | Eye re-enters nav mid-task |

---

## Design rule for DX-004+

Compose first viewport so the sequence is **linear and downward**. Do not use CSS “cleverness” to paper over backwards reading — fix content order and density first (this programme), then layout (later programmes).
