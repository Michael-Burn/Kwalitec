# EA-008 — Educational Campaign Architecture

**Programme:** Educational Excellence Programme EA-008 — Educational Campaign Architecture  
**Status:** Binding — Campaign as primary educational publication unit  
**Effective:** 2026-08-01  
**Authority:** EA-001 PASS · EA-002 PASS · EA-003 PASS · EA-004 PASS · EA-005 PASS · EA-006 PASS · EA-007 FAIL · EV-001  
**Nature:** Educational architecture law — not curriculum content, not application code  
**Parents:** `EA001_EDUCATIONAL_FOUNDATION.md` · Mission / Session Philosophy · EA-002–EA-004 artefact law · EA-007 continuity findings  

---

## 1. Governing thesis

> **Students do not experience isolated Missions. Students experience continuous study journeys.**

Therefore the **Educational Campaign**—not the individual Mission, Session, or Educational Package—is the primary educational publication unit for Kwalitec.

EA-005 and EA-006 proved a single premium day can be authored and published.  
EA-007 proved that an orphan premium day inside a template sea **destroys semester trust**.  
EA-008 encodes the corrective architecture: publish journeys, not spikes.

### What this document is

| Is | Is not |
|----|--------|
| Architecture for how consecutive Missions become one coherent Campaign | CS1 content authoring |
| Coordination law for Mission → Session → Reading → Checks → Reflection → Tomorrow → Revision | Runtime A/C, SCI, Twin, or recommendation redesign |
| Publication-unit definition that prevents isolated Golden Days | Application code change |
| Continuity model measurable by the Academic Board | A claim that any existing Campaign already PASSes |

---

## 2. Definition

### 2.1 Educational Campaign

An **Educational Campaign** is a named, versioned, Board-certified sequence of contiguous Educational Packages that together deliver one coherent study journey for a stated educational objective within a subject package version.

```text
Campaign
  └── Contiguous Educational Packages (ordered)
        └── Mission bundle each day:
              Mission → Study Session → CMP Reading Guidance
              → Knowledge Checks → Reflection → Tomorrow Bridge
        └── Revision placements (spaced inside the Campaign)
        └── Confidence / pacing / dependency plan (Campaign-level)
```

### 2.2 Hierarchy of educational units

| Unit | Question it answers | Student trust horizon |
|------|---------------------|------------------------|
| **Episode / Knowledge Check** | Can I retrieve this skill now? | Minutes |
| **Study Session** | Was today’s sitting pedagogically complete? | One sitting |
| **Mission / Educational Package** | Was today’s day tutor-grade? | One day |
| **Educational Campaign** | Can I live here for weeks and still trust the product? | Journey |

**Publication primacy rule:** Student-reachable commercial pathways for Learning Mode may expose Educational Packages only when those packages belong to a **certified Campaign** (or certified Campaign Arc — see §8 and `EA008_CAMPAIGN_PUBLICATION_POLICY.md`).

---

## 3. Campaign purpose

### 3.1 Purpose statement (required field)

Every Campaign records a **Campaign Purpose**: one paragraph explaining why this journey exists as a unit — not a list of topic titles.

**Template (authoring, not student-facing copy):**

> This Campaign exists so the candidate can [cognitive journey] across [scope], arriving at [completion competence] with [revision / confidence outcome], under one consistent Study Sensei.

### 3.2 Purpose tests

| ID | Test | Fail if |
|----|------|---------|
| CP-01 | Purpose is educational (skill / understanding journey) | Purpose is “cover topics 2.1–2.6” only |
| CP-02 | Purpose is distinct from any single Mission Purpose | Copy-paste of one day’s purpose |
| CP-03 | Purpose implies continuity across days | Reads as a bag of unrelated sittings |
| CP-04 | Purpose respects Guidance Over Content | Implies Kwalitec replaces CMP as content authority |

---

## 4. Campaign educational objective

### 4.1 Objective statement (required)

A **Campaign Educational Objective** is an assessable journey outcome the Board can verify at Campaign completion — stronger than “visited every leaf node.”

**Properties:**

1. Uses an assessable verb (explain, justify, select, compute, diagnose, …).  
2. Names the concept family the Campaign develops.  
3. States what the student can do **across** the arc that no single day alone guarantees.  
4. Does not claim Topic Complete / Estimated Mastery for the whole subject unless evidence supports it.  
5. Distinguishes first-pass progress from revision fluency when both appear in the Campaign.

### 4.2 Objective vs Mission Learning Objective

| Layer | Scope |
|-------|-------|
| Mission Learning Objective | One deliberate day’s cognitive move |
| Campaign Educational Objective | The competence that emerges only because days are sequenced, bridged, paced, and revised together |

---

## 5. Campaign scope

### 5.1 Scope dimensions (all required in the Campaign dossier)

| Dimension | What to specify |
|-----------|-----------------|
| **Subject + package version** | e.g. CS1 · IFoA 2026 alignment |
| **Syllabus span** | Inclusive ordered topic codes (contiguous on the official spine, or justified multi-day allocations on heavy topics) |
| **Mode mix** | Learning days vs Revision days vs honest rest / exam-focus placements |
| **CMP edition pin** | Same edition discipline as EA-002/EA-005 packages |
| **Day count** | Planned Campaign days (Learning + Revision) |
| **Out of scope** | Topics, chapters, coding marathons, later LOs deferred |
| **Minimum arc length** | Contiguous package count (see §5.3) |

### 5.2 Scope honesty rules

1. Scope must map to lawful syllabus nodes only (U1; no contaminants).  
2. Multi-day treatment of a heavy topic is allowed when authored as distinct packages (different Tutor Intent / LO focus each day) — not as repeated template shells.  
3. Skipping a syllabus leaf inside a claimed contiguous span requires Board HOLD with educational rationale (not engineering convenience).  
4. “Full subject Campaign” and “Chapter Campaign” and “Pilot Arc” are different scope classes — label them explicitly.

### 5.3 Scope classes

| Class | Typical span | Use |
|-------|--------------|-----|
| **Pilot Arc** | ≥ 3 contiguous Learning packages + ≥ 1 Revision placement | Minimum publishable Campaign unit for commercial pathways |
| **Chapter Campaign** | One syllabus chapter (or equivalent coherent concept family) | Primary mid-scale unit |
| **First-pass Spine Campaign** | Full first-pass leaf sequence for a subject | Semester trust unit (EA-007 audit target) |
| **Revision Campaign** | Spaced return across prior Learning Campaigns | Memory-system unit |

**Floor:** No Campaign smaller than a Pilot Arc may receive Campaign Certification for student-reachable publication (see Publication Policy).

---

## 6. Campaign entry criteria

A student (or Board review persona) may **enter** a Campaign only when:

| ID | Criterion |
|----|-----------|
| CE-01 | Campaign dossier is complete (§12) |
| CE-02 | First-day package is certified (EA-003/EA-004/EA-001 gates) |
| CE-03 | Prerequisites for Day 1 are stated; cold-start is lawful or prior Campaign completion is declared |
| CE-04 | Contaminant-free entry node |
| CE-05 | CMP edition pin known |
| CE-06 | Mode for Day 1 honest (Learning vs Revision) |
| CE-07 | Campaign Certification PASS (or Board-approved Pilot Arc certification) before commercial exposure |

**Authoring entry (Board):** Campaign authoring may begin when the syllabus span is lawful and EA-001–EA-004 law is in force. Authoring ≠ student exposure.

---

## 7. Campaign completion criteria

### 7.1 Educational completion (student journey)

Campaign Completion is **not** “every Mission marked done.” It requires:

| ID | Criterion |
|----|-----------|
| CC-01 | Every Learning package in the Campaign inventory reached Session completion under certified substance |
| CC-02 | Every required Knowledge Check family in the Campaign plan was attempted under closed-book rules as authored |
| CC-03 | Every Reflection Goal produced a topic-specific residual (no stamp-only reflections across the arc) |
| CC-04 | All Tomorrow Bridges inside the Campaign were reciprocal with the next day’s prior_bridge (or honest Campaign-terminal bridge) |
| CC-05 | Required Revision placements inside the Campaign were completed (or honestly deferred with Board HOLD) |
| CC-06 | Campaign Educational Objective is assessable as met or partially met with truthful language (no mastery theatre) |
| CC-07 | Confidence language at exit matches evidence (no scoreboard theatre; EV-001 residual classes denied) |

### 7.2 Board completion readiness (publication sense)

A Campaign is **completion-ready for certification** when every package in inventory is certified, continuity metrics meet Gate CG thresholds (`EA008_CAMPAIGN_CERTIFICATION.md`), and revision strategy is present — not when a single Golden day exists.

---

## 8. Campaign continuity

### 8.1 Continuity definition (binding)

Continuity is **not** syllabus `display_order`. Continuity is the authored, measurable persistence of:

1. **Narrative** — yesterday → today → tomorrow feels tutor-authored  
2. **Pedagogical** — Session standard holds day after day  
3. **Voice** — one Study Sensei across the Campaign  
4. **Cognitive** — load and dependency track the syllabus honestly  
5. **Memory** — revision spacing protects earlier work inside the Campaign  
6. **Trust** — quality does not spike once then vanish  

Structural sequencing without these layers is **artificial continuity** (EA-007).

### 8.2 Continuity layers (scoring model)

| Layer ID | Layer | Evidence artefacts |
|----------|-------|--------------------|
| CL-01 | Syllabus order continuity | Lawful ordered topic map; no silent gaps |
| CL-02 | Mission narrative continuity | Unique Mission Purpose / why-now / prior_bridge per day |
| CL-03 | Session pedagogical continuity | Certified Session packs; no shell-only days |
| CL-04 | Tutor voice continuity | Tutor Intent unique; Style/Voice Guide consistency across packages |
| CL-05 | Reading Guidance continuity | CMP open/stop/out-of-scope every Learning day |
| CL-06 | Tomorrow / bridge continuity | Reciprocal bridges at every internal day boundary |
| CL-07 | Revision / memory continuity | Spaced Revision placements with topic-faithful return |
| CL-08 | Confidence / truth continuity | Progress and confidence language aligned with sitting evidence |

**Continuity Index (CI):** mean of CL-01…CL-08 scores on a 0–10 Board scale (`EA008_CAMPAIGN_CERTIFICATION.md`).

### 8.3 Reciprocal bridge rule

At every internal boundary Day *n* → Day *n+1*:

| From Day *n* | From Day *n+1* | Required |
|--------------|----------------|----------|
| `tomorrow_bridge` / Tomorrow Preview | `prior_bridge` | Same skill hinge named; no boilerplate-only pair |
| Skill preview | Prerequisite acknowledgement | Compatible; no orphan leap |

Terminal day may bridge to a successor Campaign or honest “Campaign pause / revision week” — not a fake next topic.

### 8.4 Anti-orphan rule

A certified Educational Package that lacks certified predecessor and successor packages **inside a Campaign that claims those neighbours** is an **orphan excellence hazard** (EA-007 LTB family). Campaign architecture forbids treating orphan excellence as Campaign continuity.

---

## 9. Campaign revision strategy

### 9.1 Requirement

Every Campaign must include an explicit **Revision Strategy**:

| Element | Required content |
|---------|------------------|
| Placement map | Which Campaign days are Revision mode (or interleaved micro-returns) |
| Return targets | Which earlier topics / skills are retrieved |
| Spacing rationale | Why those intervals protect memory for this syllabus weight |
| Session shape | Revision Session packs (Gate RV / EA-001) or honest HOLD with student-visible treatment |
| Confidence link | How revision evidence updates confidence without theatre |

### 9.2 Minimum for Pilot Arc

At least **one** Board-visible Revision placement that returns to a skill taught earlier in the same Campaign (or a declared prerequisite Campaign). First-pass-only spines without memory return **cannot** certify as Chapter or First-pass Spine Campaigns.

### 9.3 Forbidden revision theatre

- Empty Revision surfaces labelled as programme  
- Generic “review yesterday” with no assessable return  
- Claiming spaced repetition without named return targets  

---

## 10. Campaign certification (summary)

Full process: `EA008_CAMPAIGN_CERTIFICATION.md`.

**Gate CG — Campaign** sits above Gate MG/SS/LE/TP/RV. All member packages must individually PASS; Campaign PASS additionally requires Continuity Index, concept progression, revision timing, tutor consistency, trust, and completion readiness thresholds.

> Package PASS ≠ Campaign PASS.

---

## 11. Campaign publication (summary)

Full policy: `EA008_CAMPAIGN_PUBLICATION_POLICY.md`.

**Publication primacy:** Educational Packages may only be publication-approved for commercial student pathways when they are members of a certified Campaign (or certified Pilot Arc under that policy).

**Isolated Golden Day publication is prohibited** as a commercial primary-study release. EA-006’s single-node APPROVED publication is grandfathered as a **pre-Campaign pilot** and must be absorbed into a certified arc before scale claims.

---

## 12. Campaign dossier (required artefact)

Every Campaign maintains a dossier with:

| Section | Contents |
|---------|----------|
| Identity | `campaign_id`, subject, package version, scope class, version |
| Purpose | Campaign Purpose |
| Objective | Campaign Educational Objective |
| Scope map | Ordered days, topic codes, modes, out-of-scope |
| Package inventory | Educational Package IDs in order + certification refs |
| Continuity plan | Bridge map; voice plan; pacing plan |
| Dependency graph | Concept hinges between days |
| Revision strategy | Placements + return targets + spacing |
| Confidence plan | Honest progress language rules for the arc |
| Entry / completion criteria | CE / CC IDs applied |
| Certification record | Gate CG evidence |
| Publication record | Approval / HOLD / rejection |

---

## 13. Campaign components — coordination law

How a Campaign coordinates lower artefacts without redesigning Runtime or SCI:

### 13.1 Mission sequence

| Rule | Detail |
|------|--------|
| Ordered inventory | Campaign defines the only lawful Learning Mode sequence for its span |
| Unique briefs | No two Missions may share identical why-now / tutor_intent / reflection goal frames |
| Hinge authorship | Each Mission states the concept hinge from prior day |
| Mode honesty | Learning vs Revision labelled in the Campaign map |

### 13.2 Study Sessions

| Rule | Detail |
|------|--------|
| Joint with Mission | Every Campaign day ships a certified Mission bundle |
| Pedagogical floor | EA-004 Session Blueprint held on every Learning day |
| Load budget | Interruption / cognitive load planned at Campaign level for heavy chapters |
| No shell days | Session stages without substance are Campaign FAIL |

### 13.3 CMP Reading Guidance

| Rule | Detail |
|------|--------|
| Every Learning day | open / stop / out-of-scope present (EA-004 Reading Guidance Architecture) |
| Campaign progression | Reading scopes advance through CMP loci without dumping whole chapters daily |
| Guidance Over Content | Campaign never becomes a CMP prose reprint |

### 13.4 Knowledge Checks

| Rule | Detail |
|------|--------|
| Topic-faithful | Checks retrieve the day’s concept, not generic seeds |
| Campaign progression | Later checks may lightly depend on earlier Campaign skills when authored |
| Closed-book honesty | Success criteria remain assessable |

### 13.5 Reflection

| Rule | Detail |
|------|--------|
| Topic-specific residuals | Stamp reflections across consecutive days → Campaign reject |
| Memory feed | Reflection residuals must be usable by Revision Strategy (even if wiring is future engineering) |
| No generic harvest | “Note one idea” banned as Campaign-default |

### 13.6 Tomorrow Bridges

| Rule | Detail |
|------|--------|
| Reciprocal pairs | §8.3 |
| Skill-named | Gate TP quality every internal boundary |
| Campaign terminal | Honest handoff to next Campaign / revision week |

### 13.7 Revision

| Rule | Detail |
|------|--------|
| Inside Campaign | Not deferred to “someday after the spine” |
| Visible | Student can see return days in the Campaign map |
| Assessable | Revision Sessions carry Gate RV substance |

### 13.8 Confidence development

| Rule | Detail |
|------|--------|
| Evidence-linked | Confidence language tracks checks / sittings, not decorative meters |
| Arc narrative | Early fragile → mid competence → exit honesty planned |
| Anti-theatre | EV-001 confidence/progress failure classes denied at Campaign certification |

### 13.9 Educational pacing

| Rule | Detail |
|------|--------|
| Weight-aware | Exam-weight chapters get deliberate multi-day or denser packs |
| Fatigue control | Long template stretches forbidden; unique Tutor Intent per day |
| Honest hours | Campaign Scope states that first-pass day count is not “CS1 done” |

### 13.10 Concept dependencies

| Rule | Detail |
|------|--------|
| Dependency graph | Explicit hinges (e.g. joint → expectation → MGF) |
| Taught, not only ordered | Bridges and Reading Guidance exercise the hinge |
| Unsafe leaps | Cold-start into prerequisite-heavy nodes blocked by CE-03 |

---

## 14. Relationship to prior programmes

| Programme | Relationship |
|-----------|--------------|
| EA-001 | Principles and gates remain superior for artefact truth |
| EA-002 | Authoring / certification / publication workflows nest Campaign as a new publication unit |
| EA-003 / EA-004 | Mission and Session certification remain mandatory for each day |
| EA-005 / EA-006 | Golden Package and live publication remain valid **package** PASSes; insufficient for Campaign PASS |
| EA-007 | Continuity FAIL is the problem statement EA-008 answers architecturally |
| EV-001 | Trust-break classes remain regression law for Campaign certification |

EA-008 does **not** amend the text of EA-001–EA-007. It adds Campaign-layer law above them.

---

## 15. Explicit non-goals

- Authoring CS1 (or any subject) Campaign content in this programme  
- Modifying application code, templates, or educational package JSON  
- Redesigning Runtime A, Runtime C, SCI, recommendations, or the Student Digital Twin  
- Claiming any live Campaign already PASSes Gate CG  
- Lowering EA-001–EA-004 gates to force continuity PASS  

---

## 16. Closing rule

> **The unit students trust, complete, and recommend is the Campaign.**  
> Missions are days inside that journey. Packages without a Campaign are unfinished publication.

Signed notionally: Academic Board · EA-008 · Educational Campaign Architecture · 2026-08-01
