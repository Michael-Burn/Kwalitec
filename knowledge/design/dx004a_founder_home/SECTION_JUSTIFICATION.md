# Section Justification

**Programme:** DX-004A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Rule:** Every retained section must justify its existence against the primary question.

---

## Primary question

> What should I work on next?

Test for every section:

1. Does it help **Decision**?  
2. Does it enable **Action**?  
3. Does it provide **Feedback** (or orientation that prevents wrong action)?  

If none — remove.

---

## Retained sections

### Page title — Home

| Criterion | Answer |
|---|---|
| Decision | Establishes surface identity (recognition beat) |
| Action | No — correctly; title is not a CTA |
| Feedback | No |
| Why keep | DX-001 / DX-003 reading flow requires one page heading; without it the shell alone is ambiguous |
| Why not expand | No subtitle, pulse, greeting, or version eyebrow |

---

### L0 — Current Work

| Criterion | Answer |
|---|---|
| Decision | **Yes** — names the object and stage of the next work |
| Action | **Yes** — hosts the single Primary |
| Feedback | Indirect — stage label confirms pipeline position |
| Why keep | Without L0 the page cannot answer the one question in three seconds |
| What would fail without it | Founder must scan queues or nav to invent a next step |
| Authorities | DX-001 Dashboard Philosophy; DX-002 Home type; DX-003 Decision Architecture |

---

### L0 — Primary button (exactly one)

| Criterion | Answer |
|---|---|
| Decision | Resolves the decision |
| Action | **The** Action |
| Feedback | Leads to Workspace Feedback |
| Why keep | Non-negotiable DX-001 button rule + DX-004A Primary Action mandate |
| Alternatives rejected | Multiple Quick Actions; Primary + peer Primaries |

---

### L1 — Publication Queue

| Criterion | Answer |
|---|---|
| Decision | Supports Decision when L0 is empty or Founder chooses among attention items **after** seeing Primary |
| Action | Row open = secondary path (not Primary); does not compete visually |
| Feedback | Status labels are actionable Progress/Attention statuses (DX-003) |
| Why keep | Founders often have >1 in-flight subject; queue is the only honest attention list without KPI cards |
| Why not KPI cards | Metrics without rows fail Action-over-Analytics |
| Bound | Attention-only rows; no history; compact list |
| Authorities | DX-002 Queue affordance nested in Home; DX-003 status system |

---

### L2 — Recent Publications

| Criterion | Answer |
|---|---|
| Decision | Weak — orientation only (“what just shipped”) |
| Action | Quiet open only |
| Feedback | Confirms recent Publish outcomes without flashes stacking |
| Why keep | Prevents “did I already publish X?” cognitive reload; max 5; omit if empty |
| Why not larger | History belongs in Subjects / Studio; Home is not an archive |
| Risk if overbuilt | Becomes vanity feed — then **remove** |
| Authorities | DX-001 L2 secondary; DX-004A explicit L2 |

---

### L3 — Shell navigation

| Criterion | Answer |
|---|---|
| Decision | Escape hatch when next work is not publication (Support, Settings) |
| Action | Destinations elsewhere — not page Primaries |
| Feedback | N/A |
| Why keep | Console shell requires one primary nav (DX-002); Home is not a browser |
| Why not on-page Quick Actions | Duplicates nav (FP-03 / Nav audit); fails One Primary |

---

## Rejected section classes (summary)

| Proposed / legacy section | Decision / Action / Feedback? | Verdict |
|---|---|---|
| Welcome / greeting | No | Remove |
| Operational pulse essay | No | Remove |
| Version / build / timezone eyebrow | No (L3 leak) | Remove |
| Attention Required KPI grid | Fake Decision | Remove → list in L1 if publication-related only |
| Platform Summary KPIs | No | Remove |
| Quick Actions multi-CTA | Multi-Action | Remove |
| Operational detail cards (Support / Vision / Attention mashup) | Wrong jobs | Remove from Home |
| Charts / pulse widgets / health % | Report | Remove |
| Insights / motivational copy | No | Remove |
| Feature promotion / hero | No | Remove |
| Platform alerts list as L0 peer | Ops Report | Relocate to Operations / Attention |

Full register: `CONTENT_REMOVAL_REGISTER.md`.

---

## Decision flow (natural path)

```
Arrive at Home
    ↓
Recognise Current Work (L0)
    ↓
Click Resume Publication (one Primary)
    ↓
Continue publishing in Workspace
```

L1 and L2 are available if the Founder deliberately scans — they must not interrupt the default path.

---

## Workspace principle check

| Section | Decision | Action | Feedback |
|---|---|---|---|
| Home title | Recognition | — | — |
| Current Work | ✓ | ✓ (hosts Primary) | Stage as context |
| Primary | — | ✓ | Leads to Feedback off-page |
| Publication Queue | ✓ (alt) | Quiet | Status |
| Recent Publications | Orientation | Quiet | Outcome memory |
| Shell nav | Escape | Navigate | — |

All retained. No filler sections.
