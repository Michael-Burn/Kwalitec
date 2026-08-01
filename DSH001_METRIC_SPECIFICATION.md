# DSH-001 — Dependable Study Horizon Metric Specification

**Programme:** Strategic Educational Metrics — DSH-001  
**Metric:** Dependable Study Horizon (DSH)  
**Status:** Binding — primary educational success metric  
**Effective:** 2026-08-01  
**Authority:** EA-001…EA-008 (Frozen) · EP-001 PASS · EO-001 PASS · PR-001 PASS · DX-001 PASS · CE-001 PASS  
**Nature:** Measurement law only — **no** educational redesign; **no** Runtime/application/SCI/Twin changes; **no** new publishing gates; consumes CE-001 coverage credit and EO-001 Volume status  

---

## 1. Purpose

Establish **Dependable Study Horizon (DSH)** as Kwalitec’s primary educational success metric.

DSH answers one question only:

> How long can a diligent student **genuinely depend** on Kwalitec before encountering an uncertified, unpublished, discontinuous, or missing educational experience?

DSH is the educational equivalent of **uptime**: a simple, honest reliability indicator — not a quality redesign, not a coverage mirage, and not a marketing claim of exam readiness.

---

## 2. Definition

### 2.1 Dependable Study Horizon (DSH)

**DSH** is the length of the **longest contiguous opening first-pass journey**, measured in **certified study days**, that a student may lawfully depend on from the subject’s first Learning day, where every day on that path is:

1. Mission-certified,  
2. Session-certified,  
3. Campaign-certified (Gate CG PASS),  
4. **Publication-approved** (Volume status ≥ `approved` per EO-001 / CE-001), and  
5. Contiguously bridged to the prior day (named handoff; no skip; no orphan island).

The horizon **ends** at the first LO / study day that fails any of the above — the **Continuity Front**.

### 2.2 One-line law

> DSH is contiguous Published study days from day one — not authored files, not Gate CG alone, not Awaiting Approval, not chapter percentage.

### 2.3 What DSH is not

| Not | Why |
|-----|-----|
| LO Coverage Rate | CE-001 coverage counts inventory; DSH counts **dependable length** |
| Continuity Index / Gate CG score | Quality of an authored arc ≠ student-reachable horizon |
| DX Delivery Quality Index | Delivery quality validates how days feel; DSH counts how far dependence lasts |
| Exam readiness / pass probability | Vision north star remains separate; DSH measures reliability of the companion path |
| Marketing “weeks of content” | Drafts and Approver-pending inventory are invisible to DSH |
| Runtime / Twin / recommendation health | Orthogonal systems |

---

## 3. Units of measurement

| Unit | Symbol | Role |
|------|--------|------|
| **Study day** | day | **Primary** — one certified Learning or Revision sitting in journey order |
| **Study hours** | h | **Secondary** — sum of package `estimated_study_time_minutes` midpoints ÷ 60 |
| **Horizon tip** | LO code | First Missing / uncertified LO after the contiguous Published opening arc (Continuity Front) |

**Student-facing default:** study days.  
**Founder / commercial default:** study days + hours + Continuity Front LO.

Revision days **count** toward DSH (they are dependable sittings). They do **not** create new LO coverage under CE-001; they protect memory inside the horizon.

---

## 4. Eligibility rules (what may count)

A study day enters the DSH numerator **only if all** hold:

| # | Rule | Authority |
|---|------|-----------|
| E1 | Mission Gate MG PASS | EA-003 / EA-001 |
| E2 | Session gates PASS (SS / LE / TP / RV as applicable) | EA-004 / EA-001 |
| E3 | Owning Campaign Gate CG PASS | EA-008 |
| E4 | Owning Educational Volume status ≥ **`approved`** (Publication Approver signed) | EO-001 · CE-001 |
| E5 | Day is on the **opening contiguous first-pass path** from the subject’s first Learning day | CE-001 Continuity Front |
| E6 | Prior-day bridge integrity holds (named successor; reciprocal prior_bridge where required) | EA-008 · DX continuity law |
| E7 | Day is not an orphan / grandfather package without Campaign membership | EA-007 / EA-008 FP-01 |

### 4.1 Explicit exclusions (do not count)

| Excluded | Rationale |
|----------|-----------|
| Drafts | Not certified |
| Under Authoring / Under Review | Not certified |
| **Awaiting Approval** (`publication_ready`, Approver unsigned) | CE-001: not Published |
| Certified but not Approver-queued | Not Published |
| Placeholder / stub / template days | Not genuine educational experiences |
| Uncertified packages | Fail E1–E3 |
| Orphan excellence (e.g. EA-006 `4.2` without Campaign) | Fail E3 / E7 — `Missing*` |
| Mid-spine islands disconnected from opening path | Fail E5 — may form a **Trust Band**, not Opening DSH |
| `released` without `approved` | Forbidden; never credits DSH |
| Activation-only pathways without Volume Approval | Forbidden |

**Hard honesty:** `publication_ready` inventory may be reported as **Certified Inventory Horizon (CIH)** for Founder planning. CIH is **not** DSH.

---

## 5. Calculation method

### 5.1 Opening DSH (primary metric)

```text
1. Order all study days on the subject’s opening first-pass path
   (syllabus / Campaign order from the first Learning day).

2. Walk forward from day 1.

3. While each day satisfies E1–E7, accumulate:
     DSH_days  += 1
     DSH_hours += midpoint(estimated_study_time_minutes) / 60

4. Stop at the first day that fails any eligibility rule.
   That LO / day is the Continuity Front (Horizon Tip).

5. Publish:
     DSH = DSH_days study days
     (DSH_hours h; Horizon Tip = <LO code>)
```

### 5.2 Formula (compact)

\[
\mathrm{DSH}_{\text{days}} = \max \{ n : \text{days } 1..n \text{ are contiguous and each satisfies E1–E7} \}
\]

If day 1 is not eligible, \(\mathrm{DSH}_{\text{days}} = 0\).

### 5.3 Certified Inventory Horizon (CIH) — Founder secondary only

Identical walk using E1–E3, E5–E7, and Volume status ≥ `publication_ready` **instead of** E4.

| Metric | Counts Awaiting Approval? | Student-facing? | Commercial claim? |
|--------|---------------------------|-----------------|-------------------|
| **DSH** | **No** | Yes (when > 0 and released) | Yes (with release honesty) |
| **CIH** | Yes | **No** | **No** — planning only |

### 5.4 Trust Band (non-primary)

A contiguous Certified/Published arc that is **not** connected to the opening path (e.g. future mid-spine absorption) may be recorded as a Trust Band length for remediation monitoring. It does **not** increase Opening DSH until the Continuity Front advances into that geography without a gap.

### 5.5 Relationship to CE-001 coverage

| Metric | Grain | Optimises |
|--------|-------|-----------|
| LO Coverage Rate | Published LOs / 72 | Inventory completeness |
| **DSH** | Contiguous Published study days from day 1 | **Dependable length** |

Production that maximises DSH naturally prefers Approver seals + contiguous successor Volumes at the Continuity Front — aligning with CE-001 Production Priority.

---

## 6. Update frequency

| Trigger | Action |
|---------|--------|
| Volume transitions to `approved` | Recalculate DSH immediately |
| Volume transitions to `released` | Recalculate DSH; enable student-facing communication |
| Volume revoked, HOLD, or Gate CG revoked | Recalculate immediately; DSH may shrink |
| Successor Volume certified + approved with unbroken handoff | DSH extends by that Volume’s eligible days |
| Continuity Front LO changes (new Missing tip) | Update Horizon Tip; DSH unchanged unless eligibility lost |
| Errata that remove or break a day | Recalculate |
| Syllabus package version change | Impact inventory; recalculate under new LO universe |
| Scheduled Board refresh | **At least weekly** while any Volume is Awaiting Approval; otherwise on every status change |

**No silent carry-forward:** DSH figures older than the last Volume status event are stale.

---

## 7. Publication policy

### 7.1 Internal (Editorial / Founder)

| Artefact | Required content |
|----------|------------------|
| Baseline dossier | Current DSH, CIH (labelled), Horizon Tip, evidence paths |
| Coverage Map companion | DSH published alongside CE-001 Published LO counts |
| Volume dossier | Declared DSH contribution (days added if approved contiguous) |

### 7.2 External / commercial

| Allowed when | Forbidden |
|--------------|-----------|
| DSH > 0 **and** Volumes on the path are `released` (student-reachable) | Citing CIH as “Dependable Study Horizon” |
| Honest wording: “N certified study days of dependable guidance” | “Exam-ready companion” from DSH alone |
| Naming Horizon Tip when disclosing limits | Claiming full CS1 from Pilot Arc DSH |
| Comparing DSH growth after each released Volume | Equating chapter % with DSH |

**Commercial law:** Market DSH only as reliability of the certified path that students can actually walk. Never sell Awaiting Approval as uptime.

### 7.3 Claim registry classes

| Claim class | Requires |
|-------------|----------|
| Internal DSH measurement | Approved days (E4); release not required for Board honesty |
| Student-facing DSH | Approved **and** released path |
| Commercial DSH | Student-facing DSH + scope honesty (Pilot Arc ≠ Spine) |

---

## 8. Student communication

### 8.1 Plain-language definition

> **Dependable Study Horizon** is how many study days in a row you can trust Kwalitec to guide you before the certified journey runs out.

### 8.2 Allowed student copy (examples)

| Condition | Copy |
|-----------|------|
| DSH = 0 (not released / not approved) | Do not show a numeric horizon. Prefer: “We’re preparing the next certified study days.” |
| DSH = n, released | “You can depend on Kwalitec for the next **n** study days of certified guidance.” |
| Approaching tip | “After these days, the next certified day is still being prepared — we won’t invent a placeholder.” |

### 8.3 Forbidden student copy

- Presenting CIH as live dependence  
- “Full CS1 coverage” from opening Pilot Arc DSH  
- Implying the horizon includes drafts or orphans  
- Hiding the cliff at the Continuity Front once the student is near it  

Tone: tutor honesty — the same truthfulness Gate CG and DX require inside days.

---

## 9. Founder dashboard representation

Minimum Founder board fields:

| Field | Display |
|-------|---------|
| **DSH (primary)** | Large number: `N study days` (+ secondary `H h`) |
| **Horizon Tip** | LO code + short title (e.g. `2.1.3`) |
| **Status light** | Green if DSH growing QoQ; Amber if flat with Approver pending; Red if DSH = 0 while CIH > 0 |
| **CIH (secondary)** | Smaller, labelled “Certified inventory — not live DSH” |
| **Last Volume affecting DSH** | `volume_id` + status |
| **Next action that extends DSH** | Approver seal **or** contiguous successor Volume at Horizon Tip |
| **Coverage Rate** | CE-001 Published LO % (companion, not substitute) |
| **As-of timestamp** | Measurement date |

Dashboard law: **optimise the large DSH number**. Every production priority should ask: “Does this extend Opening DSH without breaking contiguity?”

---

## 10. Commercial reporting

| Report use | Rule |
|------------|------|
| Board / investor reliability | Lead with DSH study days; footnote Horizon Tip |
| Cohort readiness narratives | Pair DSH with release status; never imply CIH |
| Competitive positioning | “Dependable certified days” — not “topics authored” |
| Risk disclosure | State residual: activation, Approver staffing, Continuity Front, Trust Band |

**Uptime analogy for commercial decks:**

```text
Infrastructure uptime  →  % time the system is available
Educational DSH        →  contiguous days the tutor path is dependably certified
```

Both punish silent gaps. Both reward honest seals over theatre.

---

## 11. Future Volume effect on DSH

Every newly **certified and Publication-approved** Educational Volume **automatically extends Opening DSH** if and only if:

1. Its first Learning day is the named Continuity Front handoff (or contiguous continuation) from the current Horizon Tip,  
2. Bridge integrity holds at the Volume boundary,  
3. Membership satisfies E1–E7 for each included day,  
4. No syllabus skip creates a Missing LO inside the path.

| Volume outcome | DSH effect |
|----------------|------------|
| Contiguous successor Approved | **DSH +=** eligible study days in that Volume |
| Contiguous successor only `publication_ready` | **CIH +=** days; **DSH unchanged** |
| Mid-spine Trust Remediation Approved but Front still open | Trust Band grows; **Opening DSH unchanged** |
| Gap / skip Volume | Does not extend Opening DSH |
| Orphan package publish | **DSH unchanged** (fails E7) |
| Gate CG or Approval revoked | **DSH may shrink** to last contiguous eligible prefix |

**Production corollary:** The Editorial Office maximises DSH by (1) Approving sealed inventory, then (2) authoring the Volume that closes the Horizon Tip — never by filling distant chapters.

---

## 12. Governance boundaries

| May | May not |
|-----|---------|
| Measure and publish DSH / CIH | Amend EA educational architecture |
| Steer production toward DSH growth | Soften Gate CG / Approver rules to inflate DSH |
| Use CE-001 / EO-001 statuses as inputs | Count Awaiting Approval as DSH |
| Define student/Founder/commercial speech | Change Runtime, application code, or SCI |

---

## 13. Closing

DSH makes educational reliability countable. Students deserve a horizon they can understand. Founders deserve a dial that production cannot game with drafts. Commercial reporting deserves an uptime metaphor that refuses Approver theatre.

**DSH is how long Kwalitec is truly there.**

Signed notionally: Chief Academic Officer · DSH-001 Metric Specification · 2026-08-01
