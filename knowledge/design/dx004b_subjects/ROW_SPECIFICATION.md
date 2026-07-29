# Row Specification

**Programme:** DX-004B  
**Status:** Binding for catalogue rows  
**Release Candidate:** `RC-2026.07.29-01`  
**Companions:** `SUBJECTS_ARCHITECTURE.md`, `OBJECT_MODEL.md`, `CATALOGUE_WIREFRAME.md`

---

## 1. Purpose

Every row answers three questions and no more:

| # | Question | Field |
|---|---|---|
| 1 | What is this? | Subject name (+ quiet code) |
| 2 | Where is it? | Stage · publication status |
| 3 | Can I continue? | Open affordance |

If the Founder needs more → **Open** the workspace.

---

## 2. Anatomy

```
┌─────────────────────────────────────────────────────────────────────────┐
│ [Name]                    [Stage]    [Updated]    [Status]    [⋯]       │
│  optional code                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

| Zone | Content | Type | Weight |
|---|---|---|---|
| **Name** | Subject title | 16px semibold | Primary recognition |
| **Code** | Optional subject code | 12–14px muted | Secondary; omit if redundant |
| **Stage** | Current pipeline stage | 14px | Where |
| **Updated** | Relative or short date | 12–14px muted | Recency |
| **Status** | Publication status | 14px; semantic colour if needed | Continuity signal |
| **More** | ⋯ menu | Icon button | Secondary ops |

Owner column: optional; omit in single-operator Alpha.

---

## 3. Columns (desktop)

| Column | Sortable? | Default visible |
|---|---|---|
| Subject | Via Alphabetical sort control | Yes |
| Stage | No (filter instead) | Yes |
| Updated | Via default / activity sorts | Yes |
| Status | Via Status filter | Yes |
| Actions | — | More only; Open = row |

Do not add: progress %, document counts, finding counts, health scores, last publisher avatar walls.

---

## 4. Actions

| Action | Max | Notes |
|---|---|---|
| **Open** | Default | Entire row clickable; optional explicit “Open” text on hover/focus — not a second Primary |
| **More (…)** | One menu | Archive, Rename, Duplicate, View history — as Alpha needs; no Publish/Validate in menu as fake Primaries |

**Forbidden on rows:** Publish, Validate, Approve, Upload, Resume Publication as button clusters. Those belong in Workspace / Home.

---

## 5. States

| Row state | Presentation |
|---|---|
| Default | Quiet |
| Hover | Subtle background; cursor pointer |
| Focus | Visible focus ring; Enter opens |
| Active / selected | Optional for keyboard; not multi-select theatre |
| Archived (when filter shows) | Muted name; still Openable if policy allows |

---

## 6. Density

| Property | Target |
|---|---|
| Row height | Compact (approx. 40–48px desktop) |
| Separators | Hairline or spacing only — not card chrome |
| First viewport | ~8–12 rows |
| Cards | **Forbidden** |

---

## 7. Narrow viewport

Stack:

```
Name
Stage · Updated · Status
                                         ⋯
```

Preserve Open-on-activate. Do not convert to marketing cards.

---

## 8. Content rules

| Do | Do not |
|---|---|
| Use canonical Subject name | Truncate so subjects become unrecognisable without tooltip essays |
| Prefer stage vocabulary from pipeline | Invent cute status copy (“Almost there!”) |
| Use relative time for Updated | Show timezone pulse essays |
| Keep Status one word/phrase | Duplicate Stage and Status as long sentences |

---

## 9. Accessibility

- Row is a single interactive unit (link or button pattern) plus separate More button  
- More must not steal row Open without explicit activation  
- Name is the accessible name; status available to AT  
- Contrast meets DX-001 / Alpha baseline  

---

## 10. Success test

Cover metadata columns: Founder still recognises the subject by **name**. Uncover metadata: Founder knows **where it is** and that they can **continue** without leaving the catalogue for a summary page.
