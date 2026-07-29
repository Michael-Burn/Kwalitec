# Search & Filter Specification

**Programme:** DX-005B  
**Status:** Binding for Choose Exam L1  
**Release Candidate:** `RC-2026.07.29-01`  
**Companion:** `DISCOVERY_ARCHITECTURE.md`

---

## 1. Philosophy

| Principle | Implication |
|---|---|
| **Simple** | Few controls; each changes the decision set |
| **Recognition over recall** | Student finds a known exam by name |
| **Ready-first** | Filters must not bury Ready under Soon |
| **No decorative filters** | No chips for vanity, tutorials, or marketing facets |
| **Reduce uncertainty** | Filters help commit — they do not maximise browsing theatre |

Unlike Founder Subjects (search-first at hundreds), student Alpha lists are often small. Search is still present and becomes habit as the catalogue grows — browsing Ready remains valid.

---

## 2. Search

### Behaviour

| Rule | Value |
|---|---|
| Field label / placeholder | Search exams… |
| Matches | Subject / exam title, known codes, aliases |
| Update | Live filter of L0 / Soon bands (debounce as needed) |
| Performance | Target **<200ms** visible results (client or cached) |
| Clear | Explicit clear when query non-empty |
| Empty query | Show browse set (respecting filters + sort) |
| No matches | Reason: No matches. Next Action: Clear query |

### Keyboard

- Focusable early in tab order  
- Esc clears query when search focused (platform norm)  

### Forbidden

- Natural-language “AI search” theatre  
- Search that navigates away from Choose Exam  
- Result cards that redesign the offering object  

---

## 3. Filters

Per DX-005B brief — keep simple:

| Control | Options | Decision value |
|---|---|---|
| **Exam family** | All · family groupings (e.g. CS1, CM2 — product-defined) | Narrow by known family |
| **Status** | All · Ready · Coming Soon | Honesty of selectability |
| **Sort** | Recently updated (default within Ready) · Alphabetical | Scan habit |

### Filter rules

| Do | Do not |
|---|---|
| Combine with search (AND) | Stack decorative chip walls |
| Keep Ready above Soon when Status = All | Interleave Soon into Ready radios |
| Show empty Reason when zero rows | Show vanity counts as KPI cards |
| Persist in URL optional | Persist as a competing “mode” app |

Filter option counts (e.g. “Ready (2)”) optional and quiet — never KPI tiles.

### Exam family

Families are student-meaningful groupings of related exams — not operator pipeline stages. If family metadata is thin at Alpha, ship **All** only and add families when data exists — do not invent empty family chrome.

---

## 4. Sorting

| Sort option | Order | Scope |
|---|---|---|
| **Recently updated** | `updated_at` / published freshness desc | **Default** within Ready |
| **Alphabetical** | Title asc | Known-name scan |

Recommended (when applicable) may boost within Ready **before** recency — not as a separate labelled “Relevance” sort without a query.

### Forbidden sort exposure

- Technical ids  
- Internal pipeline ordinals  
- “Relevance” with empty query  
- Database insertion order as a labelled option  

---

## 5. Control layout

```
[ Search exams… ____________________ ]   Family ▾   Status ▾   Sort ▾
```

- Search takes dominant width  
- Family / Status / Sort are secondary selects  
- No third row of decorative facets  

---

## 6. Scalability

| n offerings | Expectation |
|---|---|
| 0 Ready | Empty Reason → Return later |
| <10 | Browse Ready; search present |
| 10–50 | Search + family become useful |
| 50+ | Search habit; same L0–L3; Soon collapse allowed |

Layout does not change into a dashboard at thresholds.

---

## 7. Success test

Student types a partial exam name and sees the Ready row quickly. Status **Ready** hides Soon. Status **Coming Soon** never enables Begin Learning. Alphabetical scan works without technical sort labels.
