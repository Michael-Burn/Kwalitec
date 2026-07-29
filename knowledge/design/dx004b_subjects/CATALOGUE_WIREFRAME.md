# Catalogue Wireframe

**Programme:** DX-004B  
**Status:** Binding layout authority (ASCII)  
**Release Candidate:** `RC-2026.07.29-01`  
**Companion:** `SUBJECTS_ARCHITECTURE.md`

---

## Desktop — populated catalogue

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ◎ Console                                                                │
│   Home                                                                   │
│   Subjects  ← active                                                     │
│   Curriculum Studio                                                      │
│   Students                                                               │
│   Support                                                                │
│   Settings                                                               │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Subjects                                          [ Create Subject ]    │
│                                                                          │
│  ┌─────────────────────────────────────┐  Status ▾    Sort ▾             │
│  │ 🔍 Search subjects…                 │                                 │
│  └─────────────────────────────────────┘                                 │
│                                                                          │
│  Subject                 Stage            Updated        Status          │
│  ─────────────────────────────────────────────────────────────────────   │
│  CS1 Financial Reporting Validation       2 hours ago    In progress  ⋯  │
│  CS1 Valuation           Published        Yesterday      Ready        ⋯  │
│  CS2 Advanced Financial  Documents        3 days ago     In progress  ⋯  │
│  …                                                                       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Interaction notes

| Region | Behaviour |
|---|---|
| Row click / Enter | Open → Workspace |
| Trailing ⋯ | More menu (Archive, …) |
| Create Subject | Only Primary button |
| Search | Filters L0 live; <200ms cached target |
| Status / Sort | Quiet selects; no chip explosion |

---

## Desktop — empty state

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Shell nav — Subjects active]                                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Subjects                                          [ Create Subject ]    │
│                                                                          │
│                                                                          │
│              No subjects yet.                                            │
│                                                                          │
│              [ Create Subject ]                                          │
│                                                                          │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

Exactly **Reason** + **Create Subject**. No tips, illustrations essays, or secondary CTAs.  
(Header Primary may remain; empty-state Primary is the same action — one visual Primary in the empty region is preferred; do not show two competing filled Primaries. Prefer header Primary only **or** empty-region Primary — pick one filled Primary. Spec: keep header Primary; empty region uses the same control as the sole focus when list is empty, or duplicate label once in empty region and demote header to text if needed. **Canonical:** empty region holds the filled Primary; header Primary may hide when empty to avoid twin Primaries.)

**Canonical empty:** page title only in header; filled Primary in empty region.

---

## Desktop — search with no matches

```
│  Subjects                                          [ Create Subject ]    │
│                                                                          │
│  ┌─────────────────────────────────────┐  Status ▾    Sort ▾             │
│  │ Search subjects…  "actuarial"    ✕  │                                 │
│  └─────────────────────────────────────┘                                 │
│                                                                          │
│              No matches.                                                 │
│                                                                          │
│              Clear query                                                 │
```

Per DX-003: Reason + Next Action (Clear query). Create Subject remains available as page Primary but is not the empty-result Next Action unless the Founder intends to create.

---

## Narrow / mobile

```
┌────────────────────────────┐
│ Subjects                   │
│ [ Create Subject ]         │
│                            │
│ [ Search subjects…      ]  │
│ Status ▾   Sort ▾          │
│                            │
│ CS1 Financial Reporting    │
│ Validation · 2h · In prog  │
│                         ⋯  │
│────────────────────────────│
│ CS1 Valuation              │
│ Published · Yest · Ready   │
│                         ⋯  │
└────────────────────────────┘
```

Metadata stacks under the name. One Primary retained. No card grid.

---

## Forbidden compositions (do not ship)

```
✗  KPI strip above table
✗  “How Subjects works” tutorial column
✗  Side-by-side Create + Open Workspace cards
✗  Local tabs: Subjects | Review | Publishing | Versions | Quality
✗  Recent activity feed beside catalogue
✗  Progress rings in Status column
```

---

## Focus order (keyboard)

1. Skip to content (if present)  
2. Page title region  
3. Create Subject (when shown as Primary)  
4. Search  
5. Status filter  
6. Sort  
7. First row → subsequent rows → More on focused row  

Search should be reachable within a few tabs; optional autofocus on search when list is non-empty and no modal is open.
