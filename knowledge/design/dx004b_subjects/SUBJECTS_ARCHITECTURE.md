# Subjects Architecture

**Programme:** DX-004B  
**Status:** Binding for Subjects redesign  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001, DX-002, DX-003, DX-004A, Brand Guidelines  
**Implementation:** Architecture only (UI in later execution)

---

## 1. Surface identity

| Attribute | Value |
|---|---|
| **Surface name** | Subjects |
| **Shell** | Console |
| **Type (DX-002)** | Catalogue — browse / find / create / open |
| **Page title** | Subjects |
| **Nav label** | Subjects |
| **One question** | Which subject do I want to work on? |
| **One sentence (DX-003)** | Find or create a subject. |
| **Design target** | Catalogue First |
| **Primary action** | Create Subject |

Legacy labels forbidden on this surface: Subjects Hub, Curriculum Hub, Dashboard, Catalogue Dashboard, Studio Subjects Overview.

Student-facing **Subject Catalogue** (Choose Exam / Ready offerings) is a **different surface**. This architecture binds the **Founder / operator Subjects** catalogue only.

---

## 2. Product philosophy

Subjects is the **system of record** for every curriculum object.

| It is | It is not |
|---|---|
| Where every curriculum originates and is discoverable | A second Home |
| A recognition-optimised catalogue | An analytics page |
| Search-first at scale | A tutorial / onboarding wall |
| One Primary: Create Subject | A multi-CTA launchpad |
| The only catalogue | One of five Studio hubs |

**Object permanence:** A Subject always appears as the same object — identity, naming, and status vocabulary — across Catalogue, Workspace, Publication, Review, and History. Never redesign the same object differently on each surface.

---

## 3. Decision → Action → Feedback

Per DX-003:

```
Decision:  Which subject do I want to work on?
    ↓
Action:    Open (row)  or  Create Subject (Primary)
    ↓
Feedback:  Workspace loads (execution)  or  create form / new workspace
```

| Beat | Subjects manifestation |
|---|---|
| **Decision** | L0 catalogue rows + L1 search/filter recognition |
| **Action** | Row Open / Create Subject (exactly one page Primary) |
| **Feedback** | Immediate workspace entry — no intermediate landing page |

Filters and sort change **what is visible**; they are not independent decisions that compete with Open / Create.

---

## 4. Information hierarchy (L0–L3)

| Layer | Name | Purpose | Visual weight |
|---|---|---|---|
| **L0** | Subject Catalogue | Professional table/list; every row = one subject | Dominant content |
| **L1** | Search & Filters | Find by name; constrain by status/activity | Tooling chrome above list |
| **L2** | Quick Metadata | Stage, updated, publication status — quiet columns | Supporting within rows |
| **L3** | Navigation | Shell sidebar only; no in-page duplicate nav | Chrome (not page content) |

```
┌─────────────────────────────────────────────────────────────┐
│ [Shell: Console · Home · Subjects · Studio · …]   ← L3     │
├─────────────────────────────────────────────────────────────┤
│ Subjects                              [ Create Subject ]    │
│                                                             │
│ [ Search subjects…          ]  Status ▾  Sort ▾   ← L1     │
│                                                             │
│ SUBJECT          STAGE        UPDATED      STATUS   ← L0/L2│
│ ─────────────    ────────     ────────     ──────           │
│ CS1 Financial    Validation   2h ago       In progress      │
│ CS1 Valuation    Published    Yesterday    Ready            │
│ …                                                           │
└─────────────────────────────────────────────────────────────┘
```

Page chrome: title **Subjects** + one Primary **Create Subject**. Catalogue body is the decision surface.

---

## 5. L0 — Subject Catalogue

### Purpose

Answer the one question via recognition: scan or search until the desired subject is found, then open it.

### Form

Professional **table or dense list**. Not cards. Not KPI tiles. Not activity feeds.

### Density rules

| Rule | Value |
|---|---|
| One row = one Subject | Mandatory |
| Default sort | Most recently active |
| Visible rows (first viewport) | ~8–12 depending on viewport |
| Scale target | Hundreds of subjects without layout redesign |
| Pagination / virtualisation | Allowed when list exceeds comfortable scroll; never redesign into dashboards |

### Row answers (only)

1. **What is this?** — Subject name (and quiet code if needed)  
2. **Where is it?** — Current stage / publication status  
3. **Can I continue?** — Affordance: Open (row click or Open action)

If more information is required → open the workspace. Do not expand the catalogue into a summary page.

---

## 6. L1 — Search & Filters

### Philosophy

**Search is primary. Browsing is secondary.**

The catalogue must remain usable when the Founder cannot remember exact location or stage — recognition via query, not recall of hub paths.

### Allowed controls

| Control | Role |
|---|---|
| Search field | Primary find mechanism (name, code, aliases) |
| Status filters | Status · Recently updated · Ready to publish · In progress · Archived |
| Sort | Most recently active (default) · Alphabetical · Recently published · Recently created |

### Forbidden

- Decorative filter chips without decision value  
- “Quick views” that recreate Review / Publishing / Versions / Quality as competing catalogues  
- Faceted analytics (counts as KPI theatre)  
- Saved-search marketing chrome  

Full rules: `SEARCH_FILTER_SPEC.md`.

---

## 7. L2 — Quick Metadata

Quiet columns or secondary text inside each row. Never dominate.

| Field | Purpose |
|---|---|
| Current stage | Where the workspace is in the pipeline |
| Last updated | Recency for recognition / default sort |
| Publication status | Draft / In progress / Ready to publish / Published / Archived |
| Owner | Only if multi-operator Alpha needs attribution |

Never: progress rings, percent complete, platform stats, tutorial tooltips as default chrome.

---

## 8. L3 — Navigation

**No** local tab bar for Review / Publishing / Versions / Quality.  
**No** Quick Actions cluster.  
**No** “Open Curriculum Studio” Primary competing with Create Subject.

Shell primary nav (DX-002 / DX-004A):

```
Home
Subjects
Curriculum Studio
Students
Support
Settings
```

Former peer hubs become **filter presets** on this catalogue (or Studio workspace list filters) — not separate catalogue pages. See `NAVIGATION_BOUNDARIES.md`.

---

## 9. Primary action

| Rule | Value |
|---|---|
| Count | Exactly **one** Primary on Subjects |
| Label | **Create Subject** |
| Placement | Page header, adjacent to title (right-aligned on desktop) |
| Secondary | Row Open / More (…) — never Primary weight |

Empty state Primary is the same label: **Create Subject** (see `EMPTY_STATE_SPEC.md`).

---

## 10. Row actions

| Action | Weight | Behaviour |
|---|---|---|
| **Open** | Default row action (click row or explicit Open) | Enter operational workspace immediately |
| **More (…)** | Secondary menu | Archive, rename, duplicate, view history — rare ops; never a second Primary |

Maximum: Open + More. No action overload (no Publish / Validate / Approve buttons on catalogue rows).

---

## 11. Workspace transition

Opening a Subject **immediately** enters its operational workspace.

| Allowed | Forbidden |
|---|---|
| One click → Workspace | Intermediate subject landing / summary page |
| Direct deep-link to workspace | Duplicate “subject overview” between catalogue and workspace |
| Create → create flow → workspace | Create → marketing interstitial |

Workspace redesign is **DX-004C**. DX-004B only binds the transition contract: catalogue Open = workspace entry.

---

## 12. Empty states

Exactly:

```
Reason
    ↓
Create Subject
```

Nothing else. Patterns: `EMPTY_STATE_SPEC.md`. Aligns DX-003 empty-state law.

---

## 13. Typography & spacing (DX-001)

| Role | Size |
|---|---|
| Page title Subjects | 24px |
| Search / filter labels | 14px |
| Subject name (row) | 16px semibold |
| Metadata columns | 14px |
| Captions (relative dates) | 12px |

Spacing: header → tools `space-4`; tools → table `space-4`; section gaps not required beyond single composition. Row padding `space-2`/`space-3`. No Display (32px). No card walls.

Colour: semantic status only; Brand gold not UI chrome. Inter only. Prefer text labels over decorative icons; Lucide only if an icon is required for More / search affordance.

---

## 14. Cards & KPIs

| Pattern | Policy |
|---|---|
| KPI cards | **Forbidden** |
| Analytics / charts | **Forbidden** |
| Progress rings | **Forbidden** |
| Cards as default row container | **Forbidden** — table/list |
| Activity feed | **Forbidden** |
| Tutorial / feature promo | **Forbidden** |

---

## 15. Reading flow

```
Enter Subjects
  → Recognise “Subjects”
  → Find Primary (Create) or Search
  → Recognise desired subject in L0
  → Open → Workspace
```

Search may short-circuit browse. Filters refine; they do not introduce a second Primary.

---

## 16. Relationship to other surfaces

| Need | Go to |
|---|---|
| Continue what I was doing | **Home** |
| Browse / find / create subjects | **Subjects** (this surface) |
| Execute pipeline stages | **Workspace** |
| Verify readiness | **Review** (workspace stage or filtered view — not a second catalogue) |
| Release | **Publish** (workspace stage) |
| Open Studio tooling without subject pick | **Curriculum Studio** (workspace list — not competing subject catalogue) |

Home may link “View all in Subjects.” Subjects must not become Home’s publication queue.

---

## 17. Scalability

| Scale | Behaviour |
|---|---|
| 0 subjects | Empty state (Reason → Create Subject) |
| 1–20 | Full list; search optional |
| 20–100 | Search primary; filters useful |
| 100–500+ | Search + virtualised/paginated table; same layout |

No redesign at scale thresholds. Performance targets: cached search visible **<200ms**; open workspace **one click**; time-to-action **<5s** for a known subject name.

---

## 18. Accessibility

- Search field keyboard-focusable on entry (or immediately after title/Primary in tab order)  
- Rows keyboard-navigable (arrow / tab per platform pattern); Enter opens  
- Filters and sort operable without pointer  
- Responsive: stack metadata under name on narrow viewports; keep one Primary  
- No regression from Alpha keyboard / focus behaviour  

---

## 19. Success test

A peer opens Subjects and within three seconds says either:

> “I should **Create Subject**.”

or, with a known name:

> “I search / see **[Subject]** and **Open**.”

If they say “which hub do I use?” or “there’s a lot going on,” the design fails.
