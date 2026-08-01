# DSH-001 — Measurement Guide

**Programme:** Strategic Educational Metrics — DSH-001  
**Purpose:** Operational procedure to measure, refresh, and publish Dependable Study Horizon  
**Status:** Binding — Editorial measurement runbook  
**Effective:** 2026-08-01  
**Parents:** `DSH001_METRIC_SPECIFICATION.md` · `CE001_CATALOGUE_COVERAGE.md` · `EO001_EDUCATIONAL_VOLUME_STANDARD.md`  
**Nature:** Process guide only — no application automation required in DSH-001  

---

## 1. Who measures

| Role | Responsibility |
|------|----------------|
| **Editorial Director / Founder** (Subject Lead unstaffed) | Owns published DSH figure; signs baseline refreshes |
| Publication Approver | Triggers recalculation by signing / refusing Volumes |
| Quality Gate Owner | Confirms Gate CG still PASS for member Campaigns |
| Production backlog owner | Declares which successor Volume would next extend DSH |

Automation may later lint DSH; until then measurement is **Board / manual** with cited evidence paths.

---

## 2. Inputs checklist

Gather before each measurement:

| # | Input | Source |
|---|-------|--------|
| 1 | Official LO universe | `app/curriculum/data/ifoa/cs1/2026.json` (or subject pin) |
| 2 | Volume register + status | `PR001_VOLUME_REGISTER.md` · successor Volume dossiers |
| 3 | Campaign Gate CG outcomes | Certification reports (e.g. `EP001_CAMPAIGN_CERTIFICATION.md`) |
| 4 | Publication Approver records | Volume Approval history (EO-001 §7) |
| 5 | Ordered package inventory | Campaign `packages/` + Volume membership tables |
| 6 | Duration budgets | Package `estimated_study_time_minutes` |
| 7 | Continuity / bridge evidence | DX findings or Gate CG bridge integrity |
| 8 | Orphan / Missing* flags | CE-001 Coverage Map · EA-006 register |
| 9 | Prior baseline | `DSH001_CURRENT_BASELINE.md` (or successor baseline file) |

---

## 3. Step-by-step calculation

### Step A — Build the opening day list

1. Start at the subject’s first Learning package in series order (CS1: CS1-001 CA-D1).  
2. Append days in Campaign / Volume journey order, including Revision days.  
3. Stop listing when membership ends; note the named successor LO as the **candidate Horizon Tip**.

### Step B — Score each day (eligibility)

For each day, mark PASS/FAIL:

| Code | Test | Fail → |
|------|------|--------|
| E1–E3 | Mission + Session + Campaign certified | Exclude day; stop walk if on opening path |
| E4 | Volume ≥ `approved` | Exclude from **DSH**; may still count in CIH if ≥ `publication_ready` |
| E5 | On opening contiguous path | Exclude from Opening DSH (Trust Band only) |
| E6 | Bridge from prior day intact | Stop walk at prior day |
| E7 | Not orphan / not Missing* | Exclude |

### Step C — Walk for DSH

```text
n = 0
hours = 0
for day in opening_list:
    if day fails any of E1–E7:
        Horizon_Tip = day.lo_or_named_handoff
        break
    n += 1
    hours += midpoint(day.estimated_study_time_minutes) / 60
DSH_days = n
DSH_hours = round(hours, 1)
```

If the first day fails, DSH = 0 and Horizon Tip = first Learning LO (or “unpublished opening”).

### Step D — Walk for CIH (Founder secondary)

Repeat Step C with E4 replaced by: Volume status ≥ `publication_ready`.  
Label clearly: **CIH ≠ DSH**.

### Step E — Record Volume contributions

For each Volume on the path:

| Field | Record |
|-------|--------|
| `volume_id` | e.g. CS1-001 |
| Study days in membership | count |
| Status | EO status |
| DSH contribution now | days counted under E4 |
| Potential if Approved | days that would count |

### Step F — Publish

Update:

1. Baseline dossier (or dated addendum)  
2. Founder dashboard fields (spec §9)  
3. Change log row (date, DSH, CIH, event)  
4. Optional: note on CE-001 Coverage Map companion line  

---

## 4. Worked example — CS1 @ 2026-08-01

See full tables in `DSH001_CURRENT_BASELINE.md`.

| Result | Value |
|--------|------:|
| Days passing E1–E3, E5–E7 | 8 |
| Days passing E4 | 0 |
| **DSH** | **0** |
| **CIH** | **8** |
| CIH Horizon Tip | 2.1.3 |
| DSH Horizon Tip | Opening unpublished (1.1.1) |

---

## 5. How future Volumes change the figure

| Event | Measurement action |
|-------|--------------------|
| CS1-001 → `approved` | Recalculate: DSH becomes 4 if day 1–4 pass; Tip moves to CB-D1 / 1.2.3 until CS1-002 approved |
| CS1-002 → `approved` (after CS1-001) | DSH → 8; Tip → **2.1.3** |
| Both → `released` | Student-facing / commercial DSH speech unlocked at 8 |
| CS1-004 commissioned, certified, approved at 2.1.3… | DSH += new eligible days; Tip advances |
| CS1-003 approved while Tip still 2.1.3 | Record Trust Band; **Opening DSH unchanged** |
| Approver refusal / Gate CG revoke | Shrink DSH to last contiguous eligible prefix |
| Errata removing a middle day | Re-walk; may collapse DSH to prefix before break |

### Automatic extension rule (checklist)

A new Volume extends Opening DSH when **all** are true:

- [ ] Gate CG PASS on member Campaign(s)  
- [ ] Publication Approver signed (`approved`)  
- [ ] First Learning day matches current Continuity Front handoff  
- [ ] Bridges PASS at Volume boundary  
- [ ] No Missing LO inside the Volume’s claimed path  
- [ ] No orphan-only membership  

If any box fails, **do not** add days to Opening DSH.

---

## 6. Update cadence

| Cadence | When |
|---------|------|
| **Event-driven** | Every Volume status change affecting the opening path |
| **Weekly Board** | While any opening Volume is Awaiting Approval |
| **Post-DX / post-Gate CG** | After continuity validation of a new arc |
| **Syllabus pin change** | Before claiming DSH under a new curriculum version |

Stale rule: if a Volume status event occurred after the baseline `as-of` date, the published DSH is invalid until refreshed.

---

## 7. Quality controls (anti-gaming)

| Anti-pattern | Detection |
|--------------|-----------|
| Counting Awaiting Approval as DSH | E4 checklist; compare to CE-001 Published count |
| Counting orphan 4.2 | Missing* on Coverage Map |
| Skipping to Chapter 3 to “add days” | E5 / Continuity Front mismatch |
| Inflating hours without days | Primary unit remains study days |
| Claiming student DSH without `released` | Spec §7.3 claim classes |
| Treating CIH growth as success theatre | Dashboard: CIH secondary, amber/red while DSH = 0 |

**Reproducibility:** Two editors with the same Volume statuses and inventories must obtain the same DSH (±0 days). Hours may differ by ≤0.1 h on midpoint rounding only.

---

## 8. Communication templates

### Founder dashboard blurb

```text
DSH: {n} study days ({h} h) · Tip: {lo_code}
CIH: {m} study days (not live) · As-of: {date}
Next extension: {approve volume_id | author volume_id at tip}
```

### Student (released path only)

```text
You can depend on Kwalitec for the next {n} certified study days.
We stop where the certified journey stops — no placeholders.
```

### Commercial footnote

```text
Dependable Study Horizon counts contiguous Publication-Approved study days
from the opening path. Certified-but-unapproved inventory is excluded.
```

---

## 9. Handoff to production

After each measurement, answer:

1. What single action most increases Opening DSH this week?  
2. Does the CE-001 priority queue still point at that action?  
3. Is any Trust Band work being mistaken for Opening DSH growth?

If (2) is no, escalate — production is not optimising the primary educational success metric.

---

## 10. Closing

Measure DSH like uptime: same inputs, same number, no credit for systems that are “almost” sealed. Refresh on every seal. Extend only when continuity is unbroken.

Signed notionally: Chief Academic Officer · DSH-001 Measurement Guide · 2026-08-01
