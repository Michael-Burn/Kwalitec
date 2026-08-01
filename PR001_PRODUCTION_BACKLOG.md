# PR-001 — Production Backlog

**Programme:** Production Readiness Programme PR-001 — Educational Production Pipeline Execution  
**Phase:** Educational Production Operations  
**Status:** Binding — production sequencing only  
**Effective:** 2026-08-01  
**Authority:** EA-001…EA-008 COMPLETE · EP-001 PASS · EO-001 PASS  
**Nature:** Prioritised Volume production backlog — **no educational content authored**; no new governance; no Runtime/application changes  

---

## 1. Purpose

Sequence future Educational Volumes by **educational value** so the house produces journeys students need next — not calendar coverage theatre.

This backlog:

- Names **CS1-002**, **CS1-003**, **CS1-004**  
- States educational purpose and membership **intent**  
- Assigns priority and dependencies  
- Does **not** author packages, Missions, Sessions, or Campaign JSON  

Commission briefs (EO-001 Stage 0) remain required before Authoring begins on each Volume.

---

## 2. Series context

| Sequence | volume_id | Working title (provisional) | Status |
|--------:|-----------|----------------------------|--------|
| 1 | **CS1-001** | Campaign Alpha — From Purpose to Exploratory Judgement | `publication_ready` (registered) |
| 2 | **CS1-002** | Opening spine continuation — PCA + distributions entry | `commission_queued` |
| 3 | **CS1-003** | Mid-spine absorption — GLM orphan remediation | `backlog` |
| 4 | **CS1-004** | Next contiguous first-pass arc | `backlog` |

Reference bar for all: **CS1-001** / Campaign Alpha (`ep001-1.0.0`).

---

## 3. Prioritisation law (educational value)

Priority scores educational student need, not engineering convenience alone.

| Rank criterion | Why it matters |
|----------------|----------------|
| **P1 Continuity after an open handoff** | Alpha terminals to 2.1 / deferred 1.2.3 — silence recreates orphan edges |
| **P2 Trust remediation (orphan excellence)** | EA-006 4.2 live orphan + EA-007 FAIL demand mid-spine absorption |
| **P3 Contiguous spine progress** | First-pass spine claims remain forbidden until arcs join under Gate CG |
| **P4 Activation of certified inventory** | CS1-001 value unrealised until Approver + joint release (ops, not authoring) |

**Explicit non-priority:** Rewriting EA/EO; Runtime redesign; marketing “full CS1” Volumes without Gate CG.

---

## 4. Priority queue

### Priority 0 — Release path for CS1-001 (ops, not authoring)

| Item | Educational value | Work type | Blocks |
|------|-------------------|-----------|--------|
| Publication Approver signature | Makes certified journey approvable | Human approval | CS1-001 → `approved` |
| Joint activation engineering | Makes approved journey student-reachable without FP-01 | Engineering successor | CS1-001 → `released` |

Do not start CS1-002 Authoring as a substitute for releasing CS1-001. Parallel ops is allowed; content labour should not outrun Approver discipline.

---

### Priority 1 — CS1-002 (next Educational Volume)

| Field | Value |
|-------|-------|
| `volume_id` | **CS1-002** |
| Provisional title | Complete the opening chapter-family and open the distributional spine |
| Proposed scope class | `pilot_arc` (or `chapter` if membership warrants — decide at commission) |
| Educational transformation | From *Alpha chain complete* → *PCA placed honestly* → *lawful entry to distributions (2.1)* under one Sensei |
| Membership intent (not authored) | Learning day(s) for **1.2.3 PCA**; Learning day(s) opening **Chapter 2 / 2.1**; **Revision** returning to named prior targets (Alpha hinge + new days) |
| Why this priority | Alpha explicitly deferred PCA and handed off to 2.1. Students who finish CS1-001 meet a syllabus cliff unless the house publishes the next contiguous journey. Highest educational value for opening-spine trust. |
| Depends on | CS1-001 Gate CG remains PASS; Alpha claims honesty preserved; commission under EO Stage 0 |
| Must not claim | Full first-pass spine; absorption of 4.2; exam readiness |
| Production programme | Successor EP-class production under EO lifecycle (not PR-001) |
| Authoring status | **Not authored** |

**Exit of backlog item:** Commission brief signed → enters EO Authoring.

---

### Priority 2 — CS1-003

| Field | Value |
|-------|-------|
| `volume_id` | **CS1-003** |
| Provisional title | Mid-spine absorption — from regression setup through GLM structure with honest neighbours |
| Proposed scope class | `pilot_arc` |
| Educational transformation | From *orphan premium at 4.2* → *contiguous 4.1 → 4.2 → 5.1 journey* with Revision |
| Membership intent (not authored) | Contiguous Learning packages covering **4.1 → 4.2 → 5.1** (exact day split at commission); absorb EA-006 grandfather package into Gate CG PASS Campaign; **Revision** placement |
| Why this priority | Second-highest educational value for **trust**: EA-007 FAIL and EA-006 orphan excellence are the house’s standing anti-pattern. Opening arcs alone do not clear mid-spine collapse. |
| Depends on | Alpha floor retained; 4.2 grandfather rules (EA-008 Policy); preferably CS1-002 in production or released so opening spine is not abandoned mid-flight |
| Must not claim | Spine PASS solely from mid-arc; Isolated Golden Day republication of 4.2 alone |
| Production programme | Successor EP-class production under EO lifecycle |
| Authoring status | **Not authored** |

**Note on sequencing vs CS1-002:** Educational value ranks CS1-002 first (handoff continuity at the door). CS1-003 may be **commissioned in parallel** once Subject Lead / Founder capacity allows, because orphan remediation is independent syllabus geography — but **must not** steal Approver attention from CS1-001 release honesty.

---

### Priority 3 — CS1-004

| Field | Value |
|-------|-------|
| `volume_id` | **CS1-004** |
| Provisional title | Next contiguous first-pass arc (post–Chapter 2 opening / pre- or post-absorption as series plan dictates) |
| Proposed scope class | `pilot_arc` (advance toward eventual `first_pass_spine` only when EA-007-method re-audit can PASS) |
| Educational transformation | Extend certified contiguous coverage along the official first-pass order — exact chapter-family chosen at commission from remaining highest-value gap after CS1-002/003 |
| Membership intent (not authored) | ≥ 3 contiguous Learning packages + Revision; reciprocal bridges to prior Volume terminals; contaminant-free |
| Why this priority | Sustains publishing cadence toward spine continuity. Educational value is **cumulative coverage under Gate CG**, not rushing a Spine Volume label. |
| Depends on | CS1-002 and preferably CS1-003 membership known; series roadmap from Founder; Alpha floor |
| Must not claim | First-pass spine PASS until EA-007-method re-audit PASS on joined arcs |
| Production programme | Successor EP-class production under EO lifecycle |
| Authoring status | **Not authored** |

**Commission rule:** Founder selects the concrete span at Stage 0 using syllabus gap analysis after CS1-002/003 inventory is known. PR-001 does not pre-author the day list.

---

## 5. Backlog board (summary)

| Priority | volume_id | Educational value thesis | Status | Do not |
|--------:|-----------|--------------------------|--------|--------|
| 0 | CS1-001 release path | Realise certified opening journey | Ops open | Skip Approver; partial-day activation |
| 1 | **CS1-002** | Close Alpha handoff (PCA + 2.1 entry) | Queued | Author in PR-001 |
| 2 | **CS1-003** | Absorb 4.2 orphan into contiguous arc | Backlog | Republish 4.2 alone |
| 3 | **CS1-004** | Next contiguous Gate CG arc | Backlog | Label as Spine prematurely |

---

## 6. Cross-cutting successor work (not Volumes)

| Work | Why | Owner class |
|------|-----|-------------|
| EA-007-method spine re-audit | Required before `first_pass_spine` Volume claims | Academic Auditor / EVF |
| EV-001 residual remediation on non-Alpha live paths | Live trust outside catalogue Alpha | Product / education ops |
| Subject Lead staffing | Series cadence without Founder bottleneck | Founder |
| CI / dossier linter (optional tooling) | Reduce manual drift | Engineering (non-educational law) |

These do not replace CS1-002…CS1-004 Volume production.

---

## 7. Production cadence recommendation

```text
Now     Formalise CS1-001 (done in PR-001) → Approver worksheet → schedule activation engineering
Next    Commission CS1-002 (Stage 0) when Approver path is owned
Then    Author / review / audit / founder / approve CS1-002 under EO lifecycle
Also    Commission CS1-003 when capacity allows (orphan remediation)
Later   Commission CS1-004 from remaining highest-value contiguous gap
After   contiguous arcs exist → EA-007-method spine re-audit → only then consider Spine Volume
```

---

## 8. Closing rules

1. Backlog prepares sequencing — it does not author content.  
2. Educational value outranks calendar completeness.  
3. Every Volume must meet or exceed CS1-001 / Alpha floor.  
4. No new governance frameworks are created by this backlog.  
5. Spine claims remain forbidden until re-audit PASS.

**The house’s next products are Volumes — produced under frozen law, in educational-value order.**

Signed notionally: Editorial Office · PR-001 · Production Backlog · 2026-08-01
