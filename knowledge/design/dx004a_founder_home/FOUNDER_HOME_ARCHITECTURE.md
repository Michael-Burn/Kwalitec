# Founder Home Architecture

**Programme:** DX-004A  
**Status:** Binding for Founder Home redesign  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001, DX-002, DX-003, Brand Guidelines  
**Implementation:** Architecture only (UI in later DX-004 execution)

---

## 1. Surface identity

| Attribute | Value |
|---|---|
| **Surface name** | Founder Home |
| **Shell** | Console |
| **Type (DX-002)** | Home — daily decision surface |
| **Page title** | Home |
| **Nav label** | Home |
| **One question** | What should I work on next? |
| **One sentence (DX-003)** | Continue curriculum publication. |
| **Design target** | Operational Elegance |

**Terminology note:** DX-003 listed this surface as **Overview**. DX-004A renames the decision surface to **Home** under the Console shell so the label matches its job (continue work) and sheds analytics connotations of “Overview / Dashboard.” Update `TERMINOLOGY_DICTIONARY.md` when DX-004 implements.

Legacy labels forbidden on this surface: Dashboard, Console Home, Overview (as page title), Command Centre Home.

---

## 2. Product philosophy

Founder Home is an **operational workspace**, not a dashboard.

| It is | It is not |
|---|---|
| Where the Founder continues publishing | An analytics page |
| Calm, precise, deliberate | A reporting wall |
| One decision → one action | A multi-CTA launchpad |
| Publication-first | Platform health theatre |

The Founder arrives here to **continue publishing curricula**. Browsing belongs in Subjects. Reporting belongs in Reports (Settings → Operations). Configuration belongs in Settings.

---

## 3. Decision → Action → Feedback

Per DX-003:

```
Decision:  Which publication work needs me next?
    ↓
Action:    Exactly one Primary (Resume / Continue / Review / Publish…)
    ↓
Feedback:  Workspace loads, or stage status updates, or flash
```

| Beat | Founder Home manifestation |
|---|---|
| **Decision** | L0 Current Work object (subject + stage) |
| **Action** | One Primary button in L0 |
| **Feedback** | Navigation to Workspace, or empty-state Next Action |

No second independent decision may appear before Feedback. Queue rows (L1) and recent items (L2) are **context after** Primary is found — they do not introduce competing Primaries.

---

## 4. Information hierarchy (L0–L3)

Maps DX-001 progressive disclosure + DX-004A screen structure.

| Layer | Name | Purpose | Visual weight |
|---|---|---|---|
| **L0** | Current Work | Single most important publication item + one Primary | Dominant |
| **L1** | Publication Queue | Work requiring attention only (no history) | Secondary list |
| **L2** | Recent Publications | Quiet orientation; max 5 | Supporting / muted |
| **L3** | Navigation | Shell sidebar only; no in-page nav duplicates | Chrome (not page content) |

```
┌─────────────────────────────────────────────────────────────┐
│ [Shell: Console · Home · Subjects · Studio · …]   ← L3     │
├─────────────────────────────────────────────────────────────┤
│ Home                                              ← title   │
│                                                             │
│ CURRENT WORK                                      ← L0      │
│   Subject · Stage                                           │
│   [ Primary ]                                               │
│                                                             │
│ PUBLICATION QUEUE                                 ← L1      │
│   row · row · row                                           │
│                                                             │
│ RECENT PUBLICATIONS                               ← L2      │
│   quiet · compact · ≤5                                      │
└─────────────────────────────────────────────────────────────┘
```

Everything must fit in the **first viewport** so “what next” needs no scroll (DX-004A content rule; DX-001 hierarchy).

---

## 5. L0 — Current Work

### Purpose

Answer the one question immediately.

### Content (only)

| Element | Type | Notes |
|---|---|---|
| Section label | Section title 18px | “Current Work” |
| Subject name | Body 16px semibold | Decision object |
| Current stage | Supporting 14px | Progress status only |
| Optional one-line blocker | Supporting 14px | Only if it changes the Primary label |
| **Primary button** | One | Resume Publication / Continue / Review Subject / Publish |

### Primary label rules (DX-003 terminology)

| Situation | Primary label |
|---|---|
| Workspace mid-pipeline | **Resume Publication** or **Continue** |
| Awaiting validation / approval / publish | Stage verb: **Validate** / **Approve** / **Publish** — or **Review Subject** if open-only |
| No in-progress work; queue has items | Primary targets top L1 row (same button, label from that row) |
| No work at all | Empty state Primary: **Create Subject** (Subjects) |

Never more than one Primary. Never a Primary cluster.

### Selection algorithm (deterministic)

1. Most recently active incomplete workspace (last opened / last stage advance).  
2. Else highest-priority queue item (see L1 ordering).  
3. Else empty state.

---

## 6. L1 — Publication Queue

### Purpose

Show only work that **requires attention** — not inventory, not history.

### Allowed row kinds

| Status (operator) | Meaning |
|---|---|
| Awaiting Validation | Validate next |
| Awaiting Approval | Approve next |
| Ready to Publish | Publish next |
| Incomplete (docs / structure) | Resume next |

### Forbidden in L1

- Published history  
- Idle drafts with no pending gate (optional: omit or demote below fold — prefer omit)  
- Support / findings / platform health  
- KPI counts as cards  

### Row content

| Field | Type |
|---|---|
| Subject name | Body |
| Status / stage | Supporting |
| Quiet text link or row click | Opens workspace — **not** a second Primary |

### Ordering

1. Ready to Publish  
2. Awaiting Approval  
3. Awaiting Validation  
4. Incomplete  

Stable secondary key: most recently updated.

### Density

Compact list / table. No cards. Max visible ~5–7; if more, quiet “View all in Subjects” text link (not Primary).

---

## 7. L2 — Recent Publications

### Purpose

Quiet orientation: what recently became Ready.

### Rules

- Maximum **5** entries  
- Compact: subject name + Published date (Caption 12px)  
- Row click → Subjects / subject detail — **Ghost / text** affordance only  
- No Primary, no KPI, no celebration copy  

If none: omit the section entirely (do not show empty theatre).

---

## 8. L3 — Navigation

### On-page rule

**No** Quick Actions. **No** secondary dashboard links. **No** duplicate CTAs that already exist in the sidebar.

Shell primary nav (DX-002 target, ≤6):

```
Home
Subjects
Curriculum Studio
Students
Support
Settings
```

Reports, Attention, Operations, Intelligence, Findings, Search → under Settings (or Support for Findings) — not on Founder Home.

---

## 9. Empty states (DX-003)

### No current work & empty queue

```
Reason: No publication work in progress.
Next Action: Create Subject
```

### Queue empty but L2 has recent

L0 may state quietly that nothing needs attention; Primary may be omitted **only** if justified read-only — prefer Primary **Open Subjects** as the single next useful action.

### L1 empty

Omit L1 section or one line: “No items awaiting action.” No tips.

---

## 10. Typography & spacing (DX-001)

| Role | Size |
|---|---|
| Page title Home | 24px |
| Section titles | 18px |
| Body | 16px |
| Support | 14px |
| Captions (dates) | 12px |

Spacing: section gaps `space-6` (48); L0 internal `space-4`/`space-5`; list rows `space-2`/`space-3`. No Display (32px) on this surface.

Colour: semantic status only; Brand gold not UI chrome. Inter only. Lucide only if icons used (prefer text labels).

---

## 11. Cards & KPIs

| Pattern | Policy |
|---|---|
| KPI cards | **Forbidden** |
| Attention metric grids | **Forbidden** |
| Platform Summary | **Forbidden** |
| Cards as default container | **Forbidden** — lists/table for L1/L2 |
| L0 as card | Optional single grouping unit only if it improves scan; prefer open layout with whitespace |

---

## 12. Reading flow (DX-003)

```
Enter Home
  → Recognise “Home”
  → Find Current Work + Primary
  → Confirm subject + stage
  → Act (Resume)
  → Leave to Workspace
```

Queue and Recent are scanned **after** Primary location is known — never before.

---

## 13. Relationship to other surfaces

| Need | Go to |
|---|---|
| Continue publishing | **Home** → Workspace |
| Browse / create subjects | **Subjects** |
| Open any workspace | **Curriculum Studio** |
| Support inbox | **Support** |
| Platform health / research | **Settings → Operations / Research** |
| Student interventions | **Support** / Attention (nested) — not Home hero |

Alpha ops signal that blocks publication may appear as a **single Supporting line** under L0 only when it changes whether Publish is safe — otherwise omit.

---

## 14. Success test

A peer opens Founder Home and within three seconds says:

> “I should **Resume Publication** on [Subject].”

If they say “there’s a lot going on,” the design fails.
