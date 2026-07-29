# Search & Filter Specification

**Programme:** DX-004B  
**Status:** Binding for Subjects L1  
**Release Candidate:** `RC-2026.07.29-01`  
**Companion:** `SUBJECTS_ARCHITECTURE.md`

---

## 1. Philosophy

| Principle | Implication |
|---|---|
| **Search is primary** | Name/code find is the default path at scale |
| **Browsing is secondary** | Full list exists; not the only strategy |
| **Recognition over recall** | Founder need not remember which hub held the subject |
| **Minimal controls** | Only filters that change the decision set |
| **No decorative filters** | No chips for vanity or tutorial |

---

## 2. Search

### Behaviour

| Rule | Value |
|---|---|
| Field label / placeholder | Search subjects… |
| Matches | Subject name, code, known aliases |
| Update | Live filter of L0 (debounce as needed) |
| Performance | Cached / client index target **<200ms** visible results |
| Clear | Explicit clear control when query non-empty |
| Empty query | Show browse set (respecting filters + sort) |
| No matches | Reason: No matches. Next Action: Clear query |

### Keyboard

- Focusable early in tab order  
- Optional autofocus when catalogue non-empty  
- Esc clears query (when search focused) or blurs per platform norm  

### Forbidden

- Natural-language “AI search” theatre as default  
- Search that navigates away from Subjects  
- Result cards that redesign the Subject object  

---

## 3. Filters

Suggested set (DX-004B brief) — implement as one Status control and/or discrete useful presets:

| Filter | Meaning | Decision value |
|---|---|---|
| **Status** (all) | No status constraint | Default browse |
| **Recently updated** | Updated within a short window (e.g. 7 days) | Find active work by recency |
| **Ready to publish** | Publication gate cleared | Find releasable subjects |
| **In progress** | Active non-archived, not solely Published idle | Find continuable work |
| **Archived** | Archived only | Recover / audit |

Implementation may use:

- A single **Status** select whose options include the above, **or**  
- Status select + “Recently updated” as a time facet  

Do **not** expose five peer hub pages as filters-with-page-chrome.

### Filter rules

| Do | Do not |
|---|---|
| Combine with search (AND) | Stack filter chips that recreate dashboards |
| Persist filter in URL optional | Persist as a competing “mode” that feels like another app |
| Show empty Reason when zero rows | Show KPI counts on each filter option as vanity |

Filter option counts (e.g. “In progress (12)”) are optional and must stay quiet — not KPI cards.

---

## 4. Sorting

| Sort option | Order | When to use |
|---|---|---|
| **Most recently active** | `updated_at` desc | **Default** |
| **Alphabetical** | Name asc | Known name scan |
| **Recently published** | `published_at` desc (nulls last) | Find fresh releases |
| **Recently created** | `created_at` desc | Find new subjects |

### Forbidden sort exposure

- Technical ids  
- Internal pipeline ordinals as “Stage order” unless product-named  
- “Relevance” without search query  
- Database insertion order as a labelled option  

Never expose technical ordering in the UI.

---

## 5. Former hub absorption

DX-002 / DX-004A require collapsing Review / Publishing / Versions / Quality hubs.

| Legacy hub intent | Subjects treatment |
|---|---|
| Review Queue | Filter: awaiting validation / approval (stage or status) — or Studio workspace list filter; **not** a second Subjects page |
| Publishing | Filter: **Ready to publish** |
| Versions | More → History / version list on subject — **not** catalogue of versions-as-subjects |
| Quality | Findings live in Workspace / Support — **not** Subjects filter theatre |

Subjects remains one catalogue. Presets may deep-link `?status=ready_to_publish` from Home “View all” — still one page.

---

## 6. Control layout

```
[ Search subjects… ____________________ ]   Status ▾   Sort ▾
```

- Search takes dominant width  
- Status and Sort are secondary selects  
- No third row of decorative facets  

---

## 7. Scalability

| n subjects | Expectation |
|---|---|
| <20 | Browse works; search still present |
| 20–100 | Search becomes default habit |
| 100+ | Search + virtualisation; same controls |

Layout does not change at thresholds.

---

## 8. Success test

Founder types a partial subject name and sees the row in under **200ms** (cached). Applies **Ready to publish** and sees only releasable subjects. Never asks which Studio hub to open.
